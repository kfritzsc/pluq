"""
Function for reading files related to the PACSY database.
"""
import os
import csv
from pkg_resources import resource_filename
from collections import defaultdict

import h5py
import fiona
from shapely.geometry import shape

from pluq.base import Correlation


pdffile_exptype = {'cc': 'cc_pdf_all.h5',
                   'cn': 'cn_pdf_all.h5',
                   'ch': 'ch_pdf_all.h5',
                   'c': 'c_pdf_all.h5',
                   'n': 'n_pdf_all.h5',
                   'h': 'h_pdf_all.h5'}


def read_pdf(exp_type='c'):
    """
    Loads pre-made 1D PDF into dictionary
    """
    # shape file path
    file_name = pdffile_exptype[exp_type]
    file_path_name = os.path.join('data', 'pdf', file_name)
    pdf_file = resource_filename(__name__, file_path_name)

    return h5py.File(pdf_file, 'r')


schema = {'geometry': 'Polygon',
          'properties': {'corr': 'str',
                         'levels': 'float', }}

shapefile_exptype = {'cc': os.path.join('cc_region_all', 'cc_region_all.shp'),
                     'cn': os.path.join('cn_region_all', 'cn_region_all.shp')}


def read_region(exp_name='cc', level=95):
    """
    Reads shape-files with 2D chemical shift regions into a dictionary.

    :param exp_name: experiment name str in shapefile_exptype
    :returns dict['Correlation'] = `shapely.Polygon' or `shapely.MultiPolygon'
    :rtype dict[Correlation] = shapely.Multipolygon
    """
    # shape file path
    file_name = shapefile_exptype[exp_name]
    file_path_name = os.path.join('data', 'regions', file_name)
    shape_file = resource_filename(__name__, file_path_name)

    # Get the Shape files, combine them and add them to a dictionary.
    regions = dict()
    with fiona.open(shape_file, 'r', 'ESRI Shapefile', schema) as shp:

        for s in shp:

            corr = s['properties']['corr']

            if s['properties']['levels'] != level:
                continue

            region = shape(s['geometry'])

            if corr in regions.keys():
                regions[str(corr)] = regions[corr].union(region)
            else:
                regions[str(corr)] = region

    return regions


def read_cs_stats(cs_stats_file=None):
    """
    Read CS_STATS_DB.txt into a dictionary.

    :param cs_stats_file: CS_STATS_DB.txt file path name or None to use
        pluq package resource.
    """

    if not cs_stats_file:
        file_path_name = os.path.join('data', 'piqc_db', 'CS_STATS_DB.txt')
        cs_stats_file = resource_filename(__name__, file_path_name)

    cs_stats = defaultdict(_dd)

    with open(cs_stats_file, 'r') as fid:
        reader = csv.reader(
            fid, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            corr = Correlation(row[0], (row[1], ), row[2])
            cs_stats[corr]['mode'] = row[3]
            cs_stats[corr]['avg'] = row[4]
            cs_stats[corr]['std'] = row[5]
            cs_stats[corr]['min95'] = row[6]
            cs_stats[corr]['max95'] = row[7]
    return cs_stats


def write_cs_stats(cs_stats, cs_stats_file):
    """
    Write CS_STATS_DB.txt from a dictionary.

    :param cs_stats_file: CS_STATS_DB.txt file path name
    """
    with open(cs_stats_file, 'w+') as fid:
        writer = csv.writer(
            fid, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        stat_columns = ['mode', 'avg', 'std', 'min95', 'max95']
        for corr in cs_stats:
            atom_type = [corr.aa, corr.atoms[0].strip(), corr.ss]
            stats = [round(cs_stats[corr][x], 2) for x in stat_columns]
            writer.writerow(atom_type + stats)


def read_seq_cs(seq_cs_file=None):
    """
    Read SEQ_CS_DB.txt into a dictionary.

    :param seq_cs_file: SEQ_CS_DB.txt file path name or None to use
        pluq package resource.
    """

    if not read_seq_cs:
        file_path_name = os.path.join('data', 'piqc_db', 'SEQ_CS_DB.txt')
        seq_cs_file = resource_filename(__name__, file_path_name)

    protein_stats = defaultdict(_dd)

    with open(seq_cs_file, 'r') as fid:
        reader = csv.reader(
            fid, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            key_id = row[0]
            element = row[1]
            if element == 'C':
                mode, mean, std, count = row[-5:-1]

                protein_stats[key_id]['mode'] = mode
                protein_stats[key_id]['mean'] = mean
                protein_stats[key_id]['std'] = std
                protein_stats[key_id]['count'] = count
    return protein_stats


def write_seq_cs(protein_stats, seq_cs_file):
    """
    Write SEQ_CS_DB.txt from a dictionary.

    :param seq_cs_file: SEQ_CS_DB.txt file path name
    """

    with open(seq_cs_file, 'w+') as fid:
        writer = csv.writer(fid, delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC)
        stat_columns = ['mode', 'avg', 'std', 'count', 'piqc']
        for seq in protein_stats:
            stats = [round(protein_stats[seq][x], 2) for x in stat_columns]
            writer.writerow([seq[0], seq[1]] + stats)


def _dd():
    """
    Magic with the collections module.
    """
    return defaultdict(_dd)
