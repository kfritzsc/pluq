"""
Functionality for smoothing 1D and 2D distributions so that properties can be
estimated. Also functions for loading and writing the various data files used
internally.
"""

# Import everything and the kitchen sink.
import os
import sys

import h5py
import numpy as np

from skimage import measure

from scipy.interpolate import interp1d, RectBivariateSpline

from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

import fiona
from shapely import speedups
from shapely.prepared import prep
from shapely.ops import transform
from shapely.geometry import MultiPolygon, Polygon, Point, mapping

from pluq.fileio import read_pdf
from pluq.base import Correlation, ProteinSeq, CSExperiment


# Use shapely speed-ups if they are available.
if speedups.available:
    speedups.enable()


# PDF class with methods for extracting parameters
class Continuous(object):
    """
    Smoothed data-sets. Methods for extracting properties from a probability
    density function.

    :param pdf: probability distribution function np.array()
    :param grid: np.array(x) or np.meshgrid(x, y)
    :param bandwidth: float, 'silverman', 'cv' or None
    :param levels:
    """

    def __init__(self, pdf, grid, bandwidth=None, levels=None):
        self.pdf = np.array(pdf)
        self.grid = np.array(grid)
        self.bandwidth = bandwidth
        self.dims = np.ndim(pdf)
        self.levels = levels

        if self.dims == 1:
            self.space = np.abs(self.grid[1]-self.grid[0])
        elif self.dims == 2:
            x_space = np.abs(self.grid[0, 0, 1]-self.grid[0, 0, 0])
            y_space = np.abs(self.grid[1][0][0]-self.grid[1][-1][0])
            self.space = np.array((x_space, y_space))
        else:
            raise ValueError('Only 1D or 2D data is acceded!')

    @property
    def limits(self):
        if self.dims == 1:
            return np.array([self.grid.min(), self.grid.max()])
        else:
            min_x = self.grid[0][0:1].min()
            max_x = self.grid[0][0:1].max()

            min_y = self.grid[1][:, 0].min()
            max_y = self.grid[1][:, 0].max()

            return np.array([[min_x, max_x], [min_y, max_y]])

    @property
    def grid_str(self):
        limits = list(self.limits.flatten())
        shape = list(self.pdf.shape)

        return np.array(limits + shape)

    @property
    def cdf(self):
        if self.dims == 1:
            return np.cumsum(self.pdf) * self.space

        else:
            raise NotImplementedError

    def score(self, data):
        if self.dims == 1:
            f = interp1d(self.grid, self.pdf)
            return f(data)* (1/self.space)

        else:
            f = RectBivariateSpline(self.grid[1][:, 0], self.grid[0][0:1],
                                    self.pdf)
            data = np.array(data)
            if data.ndim == 1:
                return f.ev(data[1], data[0]) * 1/np.prod(self.space)
            else:
                return f.ev(data[:, 1], data[:, 0]) * 1/np.prod(self.space)

    def get_levels(self, data=None, *percentiles, **kwargs):
        """
        Returns the levels (or limits) of the chemical shift range at a chosen
        confidence level. Done by randomly sampling the PDF.
        """

        if data is None:
            try:
                n = kwargs['n']
            except KeyError:
                n = 1000
            data = self.random_sample(n)
        else:
            n = len(data)

        if self.dims == 1:
            data = np.array(data).flatten()
            scores = self.score(data)

            data = data[scores.argsort()]
            for percentile in percentiles:
                alpha = (100-percentile)/100.0
                ind = int(n * alpha)
                yield data[ind:].min(), data[ind:].max()

        else:
            scores = self.score(data)

            for percentile in percentiles:
                alpha = 100-percentile
                yield np.percentile(scores, alpha)

    def mode(self):
        if self.dims == 1:
            index = np.argmax(self.pdf)
            position = self.grid[index]
        else:
            index = np.unravel_index(self.pdf.argmax(), self.pdf.shape)
            position = [self.grid[x][index] for x in [0, 1]]
        return position


# Functions for estimating PDF
def estimate_pdf(data, grid=None, bandwidth=None, params=None, **kwargs):
    """

    :param data:
    :param bandwidth:
    :param cv_params:
    :param kwargs:
    :return:
    """

    data = np.array(data)

    # What is the dimensionality of the data.
    dims = len(data[0])
    if dims >= 3:
        raise NotImplementedError('Only 1D and 2D data is supported.')

    try:
        int(bandwidth)
    except (TypeError, ValueError):
        bandwidth = estimate_bandwidth(data, bandwidth, params, **kwargs)

    # If needed score the PDF over a grid using limits and bandwidth_sample.
    if grid is None:
        try:
            limits = kwargs['limits']
        except KeyError:
            limits = zip(np.min(data, axis=0),  np.max(data, axis=0))
            if dims == 1:
                limits = limits[0]
        try:
            bandwidth_sample = kwargs['bandwidth_sample']
        except KeyError:
            bandwidth_sample = 3

        grid = make_grid(limits, bandwidth, bandwidth_sample)

    # Kernel Density Estimation
    kde = KernelDensity(bandwidth=bandwidth).fit(data)

    # Score grid to generate PDF
    if dims == 1:
        xgrid = grid
        score_grid = xgrid.reshape((-1, 1))
    else:
        xgrid, ygrid = grid
        score_grid = np.array(list(zip(np.ravel(xgrid), np.ravel(ygrid))))

    log_pdf = kde.score_samples(score_grid).reshape(np.shape(xgrid))

    # Return grid and PDF
    return Continuous(np.exp(log_pdf), grid, bandwidth)


def estimate_bandwidth(data, estimation_type='cv', params=None, **kwargs):
    """

    :param data:
    :param estimation_type:
    :param params:
    :param kwargs:
    :return:
    """

    if estimation_type == 'silverman':
        return silverman(data)
    else:
        return grid_search(data, params, **kwargs)


def grid_search(data, params=None, **kwargs):
    """

    :param data:
    :param params:
    :param cv:
    :param n_jobs:
    :return:
    """

    try:
        kwargs['cv']
    except KeyError:
        kwargs['cv'] = 3

    try:
        kwargs['n_jobs']
    except KeyError:
        kwargs['n_jobs'] = -1

    if not params:
        params = {'bandwidth': np.linspace(0.3, 1.5, 15)}

    search = GridSearchCV(KernelDensity(), params, **kwargs)
    search.fit(data)
    return search.best_estimator_.bandwidth


def silverman(data):
    """
    Normal distribution approximation i.e. Silverman's rule of thumb.

    (4*sigma^5/3*n)^(1/5)
    """
    return np.min((4*np.std(data)**5.0 / (3 * len(data)))**(1/5.0))


def make_grid(limits, bandwidth, bandwidth_sample=1):

        """Generate a Scoring grid."""
        dims = np.ndim(limits)
        if dims == 1:
            (x_min, x_max) = limits

            xn = int((x_max - x_min) / bandwidth)
            x = np.linspace(x_min, x_max, xn * bandwidth_sample)
            return x

        else:
            ((x_min, x_max), (y_min, y_max)) = limits

            xn = int((x_max - x_min) / bandwidth)
            yn = int((y_max - y_min) / bandwidth)
            x = np.linspace(x_min, x_max, xn * bandwidth_sample)
            y = np.linspace(y_min, y_max, yn * bandwidth_sample)
            return np.meshgrid(x, y)


def under_sample_data(data, sampled_fraction):
    sample_size = len(data)
    under_sample_size = np.ceil(sample_size * sampled_fraction)
    choice = np.random.choice(sample_size, under_sample_size)
    return data[choice]


standard_experiments = {'cc': CSExperiment(('C', 'C'), bonds=1),
                        'cn': CSExperiment(('C', 'N'), bonds=1),
                        'c': CSExperiment(('C', )),
                        'n': CSExperiment(('N', )),
                        'h': CSExperiment(('H', ))}


def make_pdf(exp, pacsy, file_name, seq=None, confidence_levels=[68, 80, 95],
             verbose=True):
    """
    """

    from pluq.dbtools import PacsyCorrelation

    h5f = h5py.File(file_name, 'w')
    h5f.attrs['experiment'] = str(exp)
    h5f.attrs['confidence_levels'] = np.array(confidence_levels)

    protein = ProteinSeq(seq)
    corrs = protein.relevant_correlations(
        exp, ignoresymmetry=True, offdiagonal=False)

    catch = []
    for n, corr in enumerate(corrs):

        pacsy_corr = PacsyCorrelation(corr, pacsy)
        try:
            data = pacsy_corr.get_cs(
                piqc=True, model='all',  sigma_n=3, like_ss=True)
        except ValueError:
            catch.append(corr)
            continue

        try:
            if exp.dims == 1:
                smooth = estimate_pdf(data, bandwidth='silverman')
            else:
                smooth = estimate_pdf(data, bandwidth='silverman')
                # smooth = estimate_pdf(
                #     data, bandwidth=None,
                #     params={'bandwidth': np.linspace(0.4, 1.5, 15)})
        except:
            catch.append(corrs)
            continue

        try:
            h5f['{}'.format(str(corr))] = smooth.pdf
            h5f['{},x'.format(str(corr))] = smooth.grid_str
            levels = list(smooth.get_levels(data, *confidence_levels))
            h5f['{},levs'.format(str(corr))] = levels
        except:
            catch.append(corrs)
            continue

        if verbose:
            sys.stdout.write('\r')
            sys.stdout.write('Finished {}, Progress: {} | {}'.format(
                corr, n+1, len(corrs)))
            sys.stdout.flush()

    if catch and verbose:
        print('There was no data available for: ')
        for bad_corr in catch:
            print(bad_corr)


def get_pdf(corr, pdf_dict):
    """
    Read a correlation from a h5py

    :param corr:
    :param pdf_dict:
    :return:
    :rtype: Continuous
    """

    if type(corr) is Correlation:
        corr = str(corr)

    pdf = np.array(pdf_dict[corr])
    x_params = np.array(pdf_dict[corr+',x'])
    levels = np.array(pdf_dict[corr+',levs'])

    if len(x_params) == 3:
        grid = np.linspace(x_params[0], x_params[1], int(x_params[-1]))
    else:
        x_grid = np.linspace(x_params[0], x_params[1], int(x_params[-1]))
        y_grid = np.linspace(x_params[2], x_params[3], int(x_params[-2]))
        grid = np.meshgrid(x_grid, y_grid)

    return Continuous(pdf, grid, levels=levels)


# Functions for making, saving, and manipulating regions.
def counterpart(region_shape):
    return transform(lambda x, y, z=None: (y, x), region_shape)


def make_region(exp_type, file_name, corrs, verbose=True):
    """
    Makes regions for correlations in given experiment type by reading hdf5
    file data and exporting a new shapefiles.

    :param exp_type: :param exp_name: experiment name str in pdffile_exptype
    :param corrs: [Correlation, ...]
    :param verbose: if True, prints list of failures
    """
    schema = {'geometry': 'Polygon',
              'properties': {'corr': 'str',
                             'levels': 'float', }}

    pdf_dict = read_pdf(exp_type)

    if os.path.isfile(file_name):
        file_operation = 'a'
    else:
        file_operation = 'w'

    stype = 'ESRI Shapefile'
    with fiona.open(file_name, file_operation, stype, schema) as shp:
        for corr in corrs:
            try:
                smooth = get_pdf(corr, pdf_dict)

                for n, percentile in enumerate([68, 80, 95]):
                    try:
                        regions = _region(smooth, smooth.levels[n])
                    except ValueError:
                        if verbose:
                            print(corr)
                        break

                    for region in regions:
                        # Add the Polygon to the shape_file.
                        shp.write({'geometry': mapping(region),
                                   'properties':
                                       {'corr': str(corr),
                                        'levels': percentile}})

            except KeyError:
                if verbose:
                    print(corr)


def _region(smooth, level):
    if smooth.pdf.ndim != 2:
        raise ValueError('Should be a 2D data set.')

    xgrid, ygrid = smooth.grid
    x = xgrid[0, :]
    y = ygrid[:, 0]

    fx = interp1d(range(len(x)), x)
    fy = interp1d(range(len(y)), y)

    c_vertex = measure.find_contours(np.transpose(smooth.pdf), level)

    polygon = []
    for patch in c_vertex:

        fi_patch = np.zeros((len(patch[:, 0]), 2))
        fi_patch[:, 0] = fx(patch[:, 0])
        fi_patch[:, 1] = fy(patch[:, 1])

        polygon.append((fi_patch, None))
        return MultiPolygon(polygon)


# Function rasterizing regions into binary masks
def make_mask(x, y, polygon, centers=True):
    """
    Turns a polygon to a mask matrix over a mesh grid.

    :param x: X mesh grid
    :param y: y mesh grid
    :param poly: shapely Polygon or MultiPolygon
    :return: binary matrix with np.shape(X)
    """
    # Initial optimization was done.
    # It would be nice if this function was faster.

    # The array points should define the centers of the bins
    if not centers:
        x = x + (x[0, 1]-x[0, 0])/2.0
        y = y + (y[1, 0]-y[0, 0])/2.0

    mask = np.zeros_like(x)
    mask = np.bool_(mask)
    #
    if isinstance(polygon, MultiPolygon):
        for poly in polygon:
            # It is faster to only search the points within the binding box.
            (xmin, ymin, xmax, ymax) = poly.bounds
            idx_min = np.searchsorted(x[0, :], xmin)
            idx_max = np.searchsorted(x[0, :], xmax)
            idy_min = np.searchsorted(y[:, 0], ymin)
            idy_max = np.searchsorted(y[:, 0], ymax)
            x = np.ravel(x[idy_min:idy_max, idx_min:idx_max])
            y = np.ravel(y[idy_min:idy_max, idx_min:idx_max])

            # It was 3x faster to use a prepared geometry and map.
            # Point cast took about 30% of the time for test cases.
            points = map(Point, zip(x, y))
            poly = prep(poly)
            hits = np.array(map(poly.contains, points))
            hits = hits.reshape(((idy_max-idy_min), (idx_max-idx_min)))
            mask[idy_min:idy_max, idx_min:idx_max] += hits

    elif isinstance(polygon, Polygon):
        poly = polygon
        (xmin, ymin, xmax, ymax) = poly.bounds
        idx_min = np.searchsorted(x[0, :], xmin)
        idx_max = np.searchsorted(x[0, :], xmax)
        idy_min = np.searchsorted(y[:, 0], ymin)
        idy_max = np.searchsorted(y[:, 0], ymax)
        x = np.ravel(x[idy_min:idy_max, idx_min:idx_max])
        y = np.ravel(y[idy_min:idy_max, idx_min:idx_max])

        points = map(Point, zip(x, y))
        poly = prep(poly)
        hits = np.array(map(poly.contains, points))
        hits = hits.reshape(((idy_max-idy_min), (idx_max-idx_min)))
        mask[idy_min:idy_max, idx_min:idx_max] += hits

    return mask


def integrate_region(x, y, data, poly, centers=True):
    """
    Integrate data in region defined by poly

    :param x: X mesh grid
    :param y: y mesh grid
    :param data : data to integrate
    :param poly: shapely Polygon or MultiPolygon
    :return: float
    """
    mask = make_mask(x, y, poly, centers=centers)
    #TODO: This need to be devided by the area.
    return np.sum(data * mask)
