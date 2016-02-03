import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


from pluq.base import Correlation
from pluq.inbase import load_pdf_dict, get_pdf, estimate_pdf
from pluq.dbtools import DBMySQL, PacsyCorrelation


def plot_smoothed(data, smooth, figure_name=None):
    """
    :param smooth:
    :return:
    """
    if smooth.dims == 1:

        y = smooth.pdf
        x = smooth.grid

        data = np.array(data).flatten()

        if smooth.bandwidth:
            n = np.abs(x[-1]-x[0])/smooth.bandwidth
        else:
            n = int(len(x)/3)

        levels = list(smooth.levels(data, 68, 95))

        plt.hold(True)
        plt.plot(x, y, linewidth=3)
        plt.hist(data, n, normed=True, alpha=0.5)

        plt.vlines(np.array(levels).flatten(), 0, np.max(y), color='r',
                   linestyles='dashed')
        plt.vlines(smooth.mode(), 0, np.max(y), color='purple', linewidth=3)
        plt.hold(False)
        plt.gca().invert_xaxis

    else:
        z = smooth.pdf
        x, y = smooth.grid

        if smooth.bandwidth:
            n = int(np.abs(np.max(x)-np.min(x))/smooth.bandwidth)
            m = int(np.abs(np.max(y)-np.min(y))/smooth.bandwidth)
        else:
            n, m = np.ceil(np.shape(x)/3)

        data = np.array(data)

        plt.figure()
        plt.hold(True)

        levels = list(smooth.get_levels(data, 5, 68, 85, 90))

        plt.contour(x, y, z, levels, linewidths=3, colors='k')
        plt.hist2d(data[:, 0], data[:, 1], bins=(n, m), alpha=0.7, norm=LogNorm())
        plt.scatter(smooth.mode()[0], smooth.mode()[1], s=[200, ], c=['purple', ])
        plt.hold(False)
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal')

    if figure_name:
        plt.title(figure_name[:-4])
        plt.savefig(figure_name)


if __name__ == "__main__":


    corr = Correlation('A', ('CA', 'CB'), 'H')

    pacsy = DBMySQL(db='pacsy2', password='pass')
    pacsy_corr = PacsyCorrelation(corr, pacsy)
    data = pacsy_corr.get_cs(piqc=True, model='all',  sigma_n=3, like_ss=True)
    smooth = estimate_pdf(data,
                          params={'bandwidth': np.linspace(0.4, 1.5, 15)})


    pdf_dict = load_pdf_dict('cc')
    other = get_pdf(corr, pdf_dict)

    plt.figure(1)

    x, y = smooth.grid
    z = smooth.pdf
    plt.contour(x, y, z, list(smooth.get_levels(data, 68, 98, 95)))

    plt.figure(2)

    x, y = other.grid
    z = other.pdf
    l = other.levels

    plt.contour(x, y, z, l)

    plt.show()