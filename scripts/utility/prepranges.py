"""
Main functionality is to determine chemical shift ranges and add them to an ESRI Shape
file.

Important Note/ Warning:
Depending on the options this can take a very long time to run! For many bonds, and
all atom types it can take days (Mac Pro with 6-3.5 Ghz cores, 32 Gb RAM and a very
fast SSD.)
"""
# TODO: Set up an "argparse" interface for this script.
# TODO: Make option to use known bandwidths.
# TODO: Add function to update.
# TODO: Make a faster way to find a list of levels in inbase.Continuous.
# TODO: Add function to delete unwanted regions from shape_shape file.
# TODO: Consider adding bonding box(s).
# TODO: For prep_ranges function instead of no return, return a log of added shapes

import os

import fiona
from shapely.geometry import mapping

from pluq.base import ProteinSeq, CSExperiment
from pluq.dbtools import DBMySQL, PacsyCorrelation
from pluq.inbase import Continuous, counterpart


# Define the shape file structure.
# MultiPolygon with one attribute
schema = {'geometry': 'Polygon',
          'properties': {'res': 'str',
                         'atoms': 'str',
                         'ss': 'str',
                         'levels': 'float',
                         'bandwidth': 'float'}}


def prepranges(seq, db, exp, shape_file_path, structure=True, ignoresymmetry=False,
               diagonal=False):
    """
    Given a sequence, experiment, database and shape_file path this function will
    determine the chemical shift  ranges that are needed to assign the spectrum and
    output all of those ranges to a shape_file for latter use.

    If a current available shape_file is provided the ranges will be appended to the end,
    Otherwise a new shape_file will be made.

    The shape_file schema is defined as:

        {'geometry': 'Polygon',
         'properties': {'res': 'str',
                        'atoms': 'str',
                        'ss': 'str',
                        'levels': 'float',
                        'bandwidth': 'float'}}

    Correlations that are defined by multiple non-overlaying polygons are not
    `fiona.Mulipolygon` by separate `fiona.Polygon` with identical properties.

    :param seq: Unique sequence of a Protein or All of the aminoacids
    :param db: pacsy_ref datbase connection
    :type db: DBMySQL

    :param exp: Experiment type
    :type exp: CSExperiment

    :param shape_file_path: file path to shape_file
    :param structure: Bool, True to include secondary-structure types
    :param ignoresymmetry: Bool, False to ignore the symmetry of the experiment and only
     get "one half of the diagonal".

    :param diagonal: bool if True exclude diagonal "self correlations"
    """

    # Define Sequence
    res_types = ProteinSeq(seq)
    corrs = res_types.relevant_correlations(exp,
                                            structure=structure,
                                            ignoresymmetry=True,
                                            offdiagonal=diagonal)

    if os.path.isfile(shape_file_path):
        file_operation = 'a'
    else:
        file_operation = 'w'

    with fiona.open(shape_file_path, file_operation, 'ESRI Shapefile', schema) as shp:

        for corr in corrs:
            frame = PacsyCorrelation(corr, db)

            # Get Data
            cs = frame.get_cs()

            if len(cs[0]) <= 3:
                print('No Database Chemical Shifts: ', corr)
                continue

            tight_limits = frame.real_limits
            buffered_limits = ((tight_limits[0][0] - 2.5, tight_limits[0][1] + 2.5),
                               (tight_limits[1][0] - 2.5, tight_limits[1][1] + 2.5))
            continuous = Continuous(cs, limits=buffered_limits)

            # We can now find a few levels
            for percentile in [5, 68, 85, 95]:
                regions = continuous.region(percentile=percentile)

                for regions in regions:
                    # Add the Polygon to the shape_file.
                    shp.write({'geometry': mapping(regions),
                               'properties':
                                   {'res': corr.aa,
                                    'atoms': ', '.join(corr.atoms),
                                    'ss': corr.ss,
                                    'levels': percentile,
                                    'bandwidth': continuous.bandwidth}})
                    # Add the Polygon on the other side of the diagonal to the
                    # shape_file.
                    if not ignoresymmetry:
                        shp.write({'geometry': mapping(counterpart(regions)),
                                   'properties':
                                       {'res': corr.aa,
                                        'atoms': ', '.join(corr.counterpart().atoms),
                                        'ss': corr.ss,
                                        'levels': percentile,
                                        'bandwidth': continuous.bandwidth}})

            print('Added: ', corr)


if __name__ == "__main__":

    import pluq.aminoacids as aminoacids

    pacsy_ref = DBMySQL(db='pacsy_ref', password='pass')

    all_aa = aminoacids.aa_list
    all_aa = sorted(list(all_aa))

    CC_PDSD = CSExperiment(('C', 'C'), bonds=2, symmetric=True)

    dirname = os.path.dirname(__file__)
    shape_file = os.path.join(dirname, 'data/regions_2d', 'roi_2dcc_nostruct.shp')

    prepranges(all_aa, pacsy_ref,  CC_PDSD, shape_file, structure=False)
