#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
====
PIQC
====

Purging by Intrinsic Quality Criteria
-------------------------------------
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
It takes an additional hour to analyze the chemical shift distributions of
several thousand proteins. Calculation times on on a 6-Core 3.5 GHz Xeon E5
Mac Pro.

References
----------

1. K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally Selective
   Multidimensional Chemical Shift Ranges in Proteins from a PACSY Database
   Purged Using Intrinsic Quality Criteria " J. Biomol. NMR 2016
   doi:10.1007/s10858-016-0013-5

2. Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational Database
   Management System for Protein Structure and Chemical Shift Analysis. J
   Biomol NMR 2012, 54 (2),169–179. doi: 10.1007/s10858-012-9660-3

Please kindly cite the two references if use of this code leads to publication.
"""

import time
import os
import sys
from collections import defaultdict
from pluq.inbase import estimate_pdf

import numpy as np
import pluq.fileio
from pluq.aminoacids import aa_list, aa_atoms
from pluq.base import Correlation, ProteinID
from pluq.dbtools import DBMySQL, PacsyCorrelation, PacsyProtein


def calc_cs_stats(pacsy_database, verbose=True):
    """
    Given a PACSY database connection, this function analyzes the chemical
    shifts for all the H, C, N atom of the 20 canonical amino acid residues in
    Helix, Sheet Coil and Turn secondary structures and groups the data into a
    Python dictionary.

    :param pacsy_database: pacsy database connection pluq.dbtools.DBMySQL
    :param verbose: print out progress to the screen
    :return: cs_stats dictionary, no_good list
    """

    params = {'bandwidth': np.linspace(0.05, 1.0, 10)}

    cs_stats = defaultdict(_dd)

    # Keep track of any correlation with no database data.
    no_good = []

    # Generate a list of the needed correlations
    correlation_list = _build_correlation_list()

    total = len(correlation_list)
    if verbose:
        sys.stdout.write('Calculating chemical shift statistics.')

    # Go through every correlation.
    for n, corr in enumerate(correlation_list):
        data = PacsyCorrelation(corr, pacsy_database)

        try:
            data = np.array(data).flaten()
            min_cs = np.min(data) - 0.2
            max_cs = np.max(data) + 0.2
            num = int(max_cs - min_cs) / 0.1
            if num == 0:
                num = int((max_cs - min_cs) / 0.01)
            x_grid = np.linspace(min_cs, max_cs, num)

            smooth = estimate_pdf(data, grid=x_grid, bandwidth='cv',
                                  params=params, cv=10)

        except ValueError:
            no_good.append(corr)
            continue

        cs_stats[corr]['mode'] = smooth.mode
        cs_stats[corr]['avg'] = np.mean(data)
        cs_stats[corr]['std'] = np.std(data)
        levels = smooth.levels(data, 95)
        cs_stats[corr]['min95'] = np.min(levels)
        cs_stats[corr]['max95'] = np.min(levels)

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


def calc_seq_cs(pacsy_db, cs_stats, key_ids, verbose=True):
    """
    Given a PACSY database connection, a list of key_ids, and a dictionary
    with chemicals shift statistics for the 20 canonical amino acid
    this function analyzes each protien and groups the statistics into a
    returned dictionary.
    :param key_ids: list of pacsy key_ids
    :param cs_stats: from calc_cs_stats
    :param pacsy_database: pacsy database connection pluq.dbtools.DBMySQL
    :param verbose: print out progress to the screen
    :return: cs_stats dictionary, no_good list
    """

    params = {'bandwidth': np.linspace(0.05, 1.0, 10)}

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
                deltas = _calc_cs_offset_array(cs, cs_stats)
            except ValueError:
                protein_no_data.append((key_id, element))
                continue

            try:

                # Set up a scoring grid.
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
                    # This data had  a very small distribution or none.
                    raise ValueError

                x_grid = np.linspace(mincs, maxcs, num)

                smooth = estimate_pdf(deltas,  grid=x_grid, bandwidth='cv',
                                      params=params, cv=10)
            except ValueError:
                protein_no_data.append((key_id, element))
                continue

            mode = smooth.mode()
            mean = np.mean(deltas)
            std = np.std(deltas)
            count = len(deltas)

            if element == 'C':
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

            # For the backbone atoms look at each ss independently.
            if atom in {'C', 'CA', 'CB', 'H', 'N'}:
                ss_list = ['H', 'E', 'C', 'T']
            else:
                ss_list = ['X']

            for ss in ss_list:
                # Get the Chemical Shifts from the PACSY database
                corr = Correlation(res, (atom, ), ss)
                correlation_list.append(corr)
    return correlation_list


def _calc_cs_offset_array(cs, cs_stats):
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
            mesg = 'One of the chemical shifts given was not a number.'
            print(mesg)
            continue

        deltas.append(delta)

    return np.array(deltas)[:, None]


def main(pacsy_db, key_ids=None, cs_stats_file=None,
         seq_cs_file='SEQ_CS_DB.txt', verbose=True):
    """
    Runs the PIQC analysis on a PACSY database, and outputs up to two tables in
    two separate csv files. The first table 'CS_STATS_DB.txt' has chemical
    shift statistics for all the atom types (with data is the database). The
    second table 'seq_offsets' has statistics on the chemical shift offset for
    proteins.
    """

    # Step 1: Get all the chemical shift statistics.

    if cs_stats_file:

        cs_stats, bad_correlations = calc_cs_stats(pacsy_db, verbose)

        if verbose:
            # The following correlation are not in the database:
            if bad_correlations:
                print('The following correlation are not in the database: ')
                for bad_correlation in bad_correlations:
                    print(bad_correlation)

        # Right out cs_Stats to a csv file:
        pluq.fileio.write_cs_stats(cs_stats, cs_stats_file)

    else:
        # read cs stats from fie
        cs_stats = pluq.fileio.read_cs_stats(cs_stats_file)

    # Step 2: For every protein compare chemical shifts to the expected mode.
    if not key_ids:
        key_ids = pacsy_db.query('SELECT KEY_ID from seq_db')
        key_ids = [int(x[0]) for x in key_ids]

    protein_stats, bad_protein = calc_seq_cs(
        pacsy_db, cs_stats, key_ids, verbose)

    pluq.fileio.write_seq_cs(protein_stats, seq_cs_file)

    if verbose:
        if cs_stats_file:
            print('Output {}'.format(cs_stats_file))
        print('Output {}'.format(seq_cs_file))


    return cs_stats, protein_stats


if __name__ == '__main__':


    pacsy = DBMySQL(db='pacsy2', password='pass')
    t1 = time.time()
    main(pacsy)
    t2 = time.time()
    print('This took {} min.'.format((t2-t1)/60))
