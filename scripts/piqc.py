#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PIQC
====
Purging by Intrinsic Quality Criteria:
Used to identify mis-referenced and otherwise comprised protein chemical shift
data sets from the PACSY database.

This script runs the PIQC (Purging by Intrinsic Quality Criteria) analysis as
outlined in Fritzsching et. al. 2016 [1] on a pre-made PACSY database [2].
Does not overwrite the PACSY database but rather performs analysis and outputs
2 new tables.

Warning
-------
By default this code will try to use all available cores. To calculate the
chemical shift types for all atom in all the residues it takes about 2 hours.
It takes an additional ~ to analyse the chemical shift distributions of several
thousand proteins. Calculation times on on a 6-Core 3.5 GHz Xeon E5 Mac Pro.

References
----------
1. K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally Selective
   Multidimensional Chemical Shift Ranges in Proteins from a PACSY Database
   Purged Using Intrinsic Quality Criteria " J. Biomol. NMR 2016
   doi:10.1007/s10858-016-0013-5

2. Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational Database
   Management System for Protein Structure and Chemical Shift Analysis. J
   Biomol NMR 2012, 54 (2),169–179.
"""

import time
import os
import sys
import csv
from collections import defaultdict

from pluq.inbase import estimate_pdf

import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV

from pluq.aminoacids import aa_list, aa_atoms
from pluq.base import Correlation, ProteinID
from pluq.dbtools import DBMySQL, PacsyCorrelation, PacsyProtein


def read_seq_cs(seq_cs_file):
    """
    """
    protein_stats = defaultdict(_dd)

    with open(seq_cs_file, 'r') as fid:
        reader = csv.reader(fid, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC)
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


def read_cs_stats(cs_stats_file=None):

    if not cs_stats_file:
        cs_stats_file = '/Users/kjf/git/pluqin_env/pluq/pluq/data/piqc_db/CS_STATS_DB.txt'
    cs_stats = defaultdict(_dd)

    with open(cs_stats_file, 'r') as fid:
        reader = csv.reader(fid, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            corr = Correlation(row[0], (row[1], ), row[2])
            cs_stats[corr]['mode'] = row[3]
            cs_stats[corr]['avg'] = row[4]
            cs_stats[corr]['std'] = row[5]
            cs_stats[corr]['min95'] = row[6]
            cs_stats[corr]['max95'] = row[7]
    return cs_stats


def analyse_cs_data(data, params=None,  **kwargs):
    """ Analyse chemical shift data from a PacsyCorrelation with 1 atom.

    Finds the chemical shift modes for a chemical shift distribution. To
    accurately find the mode, performs gaussian kernel density estimation
    (KDE) for each distributions. The band-with of the KDE is optimized using
    a grid search and k-fold cross-validation.

    :param data: chemical shifts data for 1 atom as a PacsyCorrelation
    :type data: PacsyCorrelation
    :return: (mode, avg, sd min95, max95)
    :raises ValueError: if no chemical shift data or if KDE fails
    """
    # Make the evaluation grid.
    data = np.array(data).flaten()
    min_cs = np.min(data) - 0.2
    max_cs = np.max(data) + 0.2
    num = int(max_cs - min_cs) / 0.1
    if num == 0:
        num = int((max_cs - min_cs) / 0.01)
    x_grid = np.linspace(min_cs, max_cs, num)
    smooth = estimate_pdf(data, grid=x_grid, bandwidth='cv', cv=10)

    mode = smooth.mode()
    avg = np.mean(data)
    std = np.std(data)
    levels =list(smooth.levels(data, 95))
    min95 = levels[0]
    max95 = levels[1]
    return mode, avg, std, min95, max95


def fit_cs_offset_data(deltas, params=None,  **kwargs):
    # Parse input cross validation parameters or use defaults.
    if not params:
        # Default cross validation parameters are replace by the kwargs.
        params = {'bandwidth': np.linspace(0.05, 1.0, 10)}

    try:
        kwargs['cv']
    except KeyError:
        kwargs['cv'] = 10

    try:
        kwargs['n_jobs']
    except KeyError:
        kwargs['n_jobs'] = -1

    deltas = np.array(deltas)

    # Set up a scoring grid.
    # This is a little ugly.
    scale = 0.1
    mincs = np.min(deltas) - 0.2
    maxcs = np.max(deltas) + 0.2
    num = int(maxcs - mincs) / scale

    while num < 50:
        scale /= 10
        num = int(maxcs - mincs) / scale
        if scale <= 0.00001:
            break

    if num < 50:
        # This data has no has a very small distribution.
        raise ValueError

    x_grid = np.linspace(mincs, maxcs, num)

    return estimate_pdf(deltas, grid=x_grid, cv=3)


def analyse_protein_cs_fit(xgrid, pdf, deltas):
    """

    :param deltas:
    :param params:
    :param kwargs:
    :return:
    """

    mode_ind = np.argmax(pdf)

    # Extract all the statistics.
    mode = xgrid[mode_ind]
    mean = np.mean(deltas)
    std = np.std(deltas)
    count = len(deltas)
    return mode, mean, std, count


def calc_cs_offset_array(cs, cs_stats):
    """
    :param cs: tuple(atom type -- Correlation, chemical shift -- float)
    :param cs_stats: chemcial shift statistics dict from analyse_cs_data
    :return: list of of chemical shift offsets
    """
    deltas = []
    for corr, cs in cs:
        # Get the expected chemical shifts
        # If we don't have the expected chemical shifts just skip it.
        try:
            expected_cs = cs_stats[corr]['mode']
        except KeyError:
            continue
        # Also have to check for an empty dict
        if not expected_cs:
            continue

        # Compare the found chemical shift to the expected
        delta = cs - expected_cs

        # There must be a few improperly formatted float in the database?
        if np.isnan(delta):
            print 'One of the chemical shift given was not a number, skipped it.'
            continue

        deltas.append(delta)
    return deltas


def calc_cs_stats(pacsy_database, verbose=True):
    """
    Given a PACSY database, this function analysis the chemical shifts for all
    the H, C, N atom of the 20 canonical amino acid residues in Helix, Sheet
    Coil and Turn secondary structures and groups the data into a Python
    dictionary.

    :param pacsy_database:
    :param verbose: print out progress to the screen
    :type pacsy_database: DBMySQL
    :return: cs_stats, no_good
    """
    cs_stats = defaultdict(_dd)

    # Keep track of any correlation with no database data.
    no_good = []

    # Generate a list of the needed correlations
    correlation_list = _build_correlation_list()

    if verbose:
        total = len(correlation_list)
        sys.stdout.write('Calculating chemical shift statistics.')

    # Go throught every correlation.
    for n, corr in enumerate(correlation_list):
        data = PacsyCorrelation(corr, pacsy_database)

        try:
            stats = analyse_cs_data(data)
        except ValueError:
            no_good.append(corr)
            continue

        mode, avg, std, min95, max95 = stats
        cs_stats[corr]['mode'] = mode
        cs_stats[corr]['avg'] = avg
        cs_stats[corr]['std'] = std
        cs_stats[corr]['min95'] = min95
        cs_stats[corr]['max95'] = max95

        if verbose:
            progress = 'Finished {}, \
            Progress: {} | {}'.format(corr, n+1, total)
            sys.stdout.write('\r')
            sys.stdout.write(progress)
            sys.stdout.flush()

    if verbose:
        print(os.linesep)
        print('Done calculating chemical shift statistics!')
    return cs_stats, no_good


def calc_protein_offset_stats(key_ids, pacsy_db, cs_stats, verbose=True):
    seq_offsets = defaultdict(dict)
    protein_no_data = []

    if verbose:
        total = len(key_ids)
        sys.stdout.write('Calculating Protein Offsets.')

    # Get the chemical shift data for every protein in the database.
    for n, key_id in enumerate(key_ids):

        protein_id = ProteinID(key_id, "KEY_ID")
        pacsy_protein = PacsyProtein(protein_id, pacsy_db)

        cs_data = pacsy_protein.cs_data()

        # Sort the data by nucleus type and find the difference from ideal.
        for element in ['C', 'N', 'H']:
            cs = [x for x in cs_data if x[0].atoms[0] == element]

            if len(cs) < 15:
                # Protein is to small protein
                protein_no_data.append((key_id, element))
                continue
            try:
                offsets = calc_cs_offset_array(cs, cs_stats)
            except ValueError:
                protein_no_data.append((key_id, element))
                continue

            try:
                xgrid, pdf = fit_cs_offset_data(offsets)
                offset_stats = analyse_protein_cs_fit(xgrid, pdf, offsets)
                mode, mean, std, count = offset_stats
            except ValueError:
                protein_no_data.append((key_id, element))
                continue

            if element=='C':
                piqc_good = all([abs(mode) <= 1.0,  std <= 4.0])
            else:
                piqc_good = True

            seq_offsets[(key_id, element)]['mode'] = mode
            seq_offsets[(key_id, element)]['avg'] = mean
            seq_offsets[(key_id, element)]['std'] = std
            seq_offsets[(key_id, element)]['count'] = count
            seq_offsets[(key_id, element)]['piqc'] = piqc_good

            if verbose:
                progress = 'Finished Key ID {} - {},\
                Progress: {} | {}'.format(key_id, element, n+1, total)
                sys.stdout.write('\r')
                sys.stdout.write(progress)
                sys.stdout.flush()

    if verbose:
        print(os.linesep)
        print('Done calculating chemical shift offsets!')
    return seq_offsets, protein_no_data


def _dd():
    """
    Magic with the collections module.
    """
    return defaultdict(_dd)


def _build_correlation_list():
    """
    Little utility function to make a list of all the needed correlation.
    """

    correlation_list = []
    for res in aa_list:
        for atom in aa_atoms[res]:

            # Only perform the analysis for H, C, and N.
            if atom[0] not in {'H', 'C', 'N'}:
                continue

            # For the backbone atoms look at each secondary structure independently.
            if atom in {'C', 'CA', 'CB', 'H', 'N'}:
                ss_list = ['H', 'E', 'C', 'T']
            else:
                ss_list = ['X']

            for ss in ss_list:
                # Get the Chemical Shifts from the PACSY database
                corr = Correlation(res, (atom, ), ss)
                correlation_list.append(corr)
    return correlation_list


def main(pacsy_db, recalculate_cs_stats=False, cs_stats_file='CS_STATS_DB.txt',
         key_ids=None, seq_offsets_file='SEQ_CS_DB.txt', verbose=True):
    """
    Runs the PIQC analysis on a PACSY database, and outputs up to two tables in
    two separate csv files. The first table 'CS_STATS_DB.txt' has chemical shift
    statistics for all the atom types (with data is the database). The second
    table 'seq_offsets' has statistics on the chemical shift offset for
    proteins.

    :param pacsy_db:
    :param csv_file: bool if True writes csv table
    :param file_path: file path for output csv file, default:`CS_STATS_DB.txt`
    :param verbose:
    """

    # Step 1: Get all the chemical shift statistics.
    if recalculate_cs_stats:
        cs_stats, bad_correlations = calc_cs_stats(pacsy_db, verbose)

        if verbose:
            # The following correlation are not in the database:
            # Glu-(HE2)-All,  Asp-(HD2)-All, Lys-(HZ1)-All, Pro-(H2)-All,
            # Pro-(H3)-All, Tyr-(HH)-All
            if bad_correlations:
                print('The following correlation are not in the database: ')
                for bad_correlation in bad_correlations:
                    print(bad_correlation)

        # Right out cs_Stats to a csv file:
        with open(cs_stats_file, 'w+') as fid:
            writer = csv.writer(fid, delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)
            stat_columns = ['mode', 'avg', 'std', 'min95', 'max95']
            for corr in cs_stats:
                atom_type = [corr.aa, corr.atoms[0].strip(), corr.ss]
                stats = [round(cs_stats[corr][x], 2) for x in stat_columns]
                writer.writerow(atom_type + stats)

    else:
        # Don't recalculate the chemical shift statistics, read them from the
        # given csv file.
        cs_stats = read_cs_stats()

    # Step 2: For every protein compare each chemical shift to the expected mode.
    if not key_ids:
        key_ids = pacsy_db.query('SELECT KEY_ID from seq_db')
        key_ids = [int(x[0]) for x in key_ids]

    args = (key_ids,  pacsy_db, cs_stats, verbose)
    seq_offsets, bad_protein = calc_protein_offset_stats(*args)


    # Output seq offsets to a to a csv file:
    with open(seq_offsets_file, 'w+') as fid:
        writer = csv.writer(fid, delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC)
        stat_columns = ['mode', 'avg', 'std', 'count', 'piqc']
        for seq in seq_offsets:
            stats = [round(seq_offsets[seq][x], 2) for x in stat_columns]
            writer.writerow([seq[0], seq[1]] + stats)

    if verbose:
        if recalculate_cs_stats:
            print('Output {}'.format(cs_stats_file))
        print('Output {}'.format(seq_offsets_file))


    return cs_stats, seq_offsets


if __name__ == '__main__':


    pacsy = DBMySQL(db='pacsy2', password='pass')
    t1 = time.time()
    main(pacsy)
    t2 = time.time()
    print('This took {} min.'.format((t2-t1)/60))
