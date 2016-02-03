#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PLUQin
======
A program to help assign protein chemical shifts peaks. Especially, helpful for
assigning chemical shift correlations in a 2D plane. The data used by this
program comes from the PIQC [1] analysis of the PACSY/BMRB [2] database.

All possible intra-residue chemical shift assignment within a given confidence
level are provided. The possible assignments are based on likelihood using
non-parametric methods. If desired you can truncate the assignment at a certain
likely hood. If you are worried about miss-grouping peaks, keep the cut off
value negative. provides secondary structure  (H:C:E probability). The
probabilities will be adjusted based on the sequence if it is provided, by
default it weight .

Current Available Experiments:
----------------------------
2D Carbon 1-bond: cc
2D Carbon-nitrogen 1-bond: cn
1D Carbon: c
1D Nitrogen: n
1D Proton: h

It is pretty easy to add new experiments but you will need the full version of
the PACSY database. See 'utility/build_exp_pdf.py' for example.

Warning:
-----------------------
No Database Chemical Shifts for: Trp-(CD2)-All, Trp-(CG)-All Glu-(HE2)-All,
Asp-(HD2)-All, Lys-(HZ1)-All, Pro-(H2)-All, Pro-(H3)-All, Tyr-(HH)-All,
Asp-(CB,CG)-Sheet, Asp-(CG,CB)-Sheet, His-(CG,CB)-Coil, Trp-(CZ2,CE2)-All,
Trp-(CD2,CE3)-All, Trp-(CB,CG)-Helix, Trp-(CB,CG)-Coil, Trp-(CG,CB)-Helix,
Trp-(CG,CB)-Coil, Trp-(CE3,CD2)-All, Trp-(CE2,CZ2)-All, Tyr-(CB,CG)-Coil
Tyr-(CG,CB)-Coil, Lys-(CE,NZ)-All, Pro-(CA,N)-Coil, Pro-(CD,N)-Helix
Pro-(CD,N)-Sheet, Thr-(CA,N)-Helix

References:
----------
[1] K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally Selective
Multidimensional Chemical Shift Ranges in Proteins from a PACSY Database
Purged Using Intrinsic Quality Criteria " J. Biomol. NMR 2016
doi:10.1007/s10858-016-0013-5

[2]	Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational Database
Management System for Protein Structure and Chemical Shift Analysis. J Biomol
NMR 2012, 54 (2),169–179.

Please kindly cite the two references if use of this code leads to publication.

Keith J. Fritzsching
"""

import collections
from collections import namedtuple
from itertools import compress, product
import numpy as np
from pluq.base import Correlation
import pluq.base as base
import pluq.inbase as inbase
from shapely.geometry import Point

Assignment = namedtuple('Assignment', ['res', 'atoms', 'scores', 'ss_scores'],
                        verbose=False)
Assignment.__new__.__defaults__ = (None,) * len(Assignment._fields)


class AssignmentLine(object):
    def __init__(self, aa, atoms, scores, ss_scores):
        self.aa = aa
        self.atoms = atoms

        self.n = len(atoms)

        if len(scores) != self.n:
            raise ValueError('len(atoms) should len(probs)')
        self.scores = np.array(scores)

        if len(ss_scores) != self.n:
            raise ValueError('len(atoms) should len(ss_scores)')
        self.ss_scores = np.array(ss_scores)

    @property
    def joint_score(self):
        return np.product(self.scores)

    @property
    def ss_prob(self):
        ss_scores = self.ss_scores
        ss_scores = ss_scores[~np.isnan(ss_scores).any(axis=1)]
        if ss_scores.any():
            ss_scores = np.product(ss_scores, axis=0)
            ss_scores /= ss_scores.sum()
            ss_scores = np.round(ss_scores*100, 1)
        else:
            ss_scores = [None] * 3

        return ss_scores

    @property
    def list(self):

        line = [self.aa]
        line += self.atoms + list(self.scores) + [self.joint_score]
        line += list(self.ss_prob)

        return line

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ', '.join(self.list)


def get_resonance_choices_1d(resonance, correlations, exp_name, level=95):
    """

    :param resonance:
    :param correlations:
    :param pdf_dict:
    :param level:
    :return:
    """
    pdf_dict = inbase.load_pdf_dict(exp_name)
    levels = list(pdf_dict.attrs['confidence_levels'])

    try:
        ind = levels.index(level)
    except ValueError:
        mesg = 'You must chose a confidence level from {}'.format(levels)
        raise ValueError(mesg)

    # Find all the hits
    assignments = collections.defaultdict(list)
    for corr in correlations:
        try:
            cs_range = pdf_dict[str(corr)+',levs'][ind]
        except KeyError:
            continue

        if min(cs_range) <= resonance <= max(cs_range):

            try:
                smooth = inbase.get_pdf(corr, pdf_dict)
                corr_score = float(smooth.score(resonance))
            except ValueError:
                    corr_score = 0
            except KeyError:
                    corr_score = 0

            ss_scores = []
            for ss in ['H', 'C', 'E']:
                try:
                    ss_corr = Correlation(corr.aa, corr.atoms, ss)
                    corr_ss_smooth = inbase.get_pdf(ss_corr, pdf_dict)
                    ss_scores.append(float(corr_ss_smooth.score(resonance)))
                except ValueError:
                    ss_scores.append(0)
                except KeyError:
                    ss_scores = None
                    break

            assign = Assignment(corr.aa, corr.atoms[0], corr_score, ss_scores)
            assignments[corr.aa].append(assign)

    return assignments


def get_resonance_choices_2d(resonance, correlations, exp_name, level=95):


    pdf_dict = inbase.load_pdf_dict(exp_name)
    levels = list(pdf_dict.attrs['confidence_levels'])

    try:
        ind = levels.index(level)
    except ValueError:
        mesg = 'You must chose a confidence level from {}'.format(levels)
        raise ValueError(mesg)


    region_dict = inbase.load_region(exp_name, level)
    regions = [region_dict[str(x)] for x in correlations]

    # Find all the hits
    hits = map(Point(resonance).within, regions)
    correlations = list(compress(correlations, hits))


    # Find all the hits
    assignments = collections.defaultdict(list)
    for corr in correlations:

        try:
            smooth = inbase.get_pdf(corr, pdf_dict)
            corr_score = float(smooth.score(resonance))
        except ValueError:
                corr_score = 0
        except KeyError:
                corr_score = 0

        ss_scores = []
        for ss in ['H', 'C', 'E']:
            try:
                ss_corr = Correlation(corr.aa, corr.atoms, ss)
                corr_ss_smooth = inbase.get_pdf(ss_corr, pdf_dict)
                ss_scores.append(float(corr_ss_smooth.score(resonance)))
            except ValueError:
                ss_scores.append(0)
            except KeyError:
                ss_scores = None
                break

        assign = Assignment(corr.aa, corr.atoms, corr_score, ss_scores)
        assignments[corr.aa].append(assign)

    return assignments


def main(cs_set, exp_name='c', seq=None, level=95, frequency=True):
    """
    Run Pluqin for cs_set

    :param cs_set:
    :param seq:
    :param level:
    :param shape_path:
    :param pdf_path:
    :return:
    """
    try:
        exp = inbase.standard_experiments[exp_name]
    except KeyError:
        raise ValueError('{} is not a known experiment'.format(exp_name))

    protein = base.ProteinSeq(seq)
    correlations = protein.relevant_correlations(
        exp, structure=False, ignoresymmetry=True, offdiagonal=False)

    n = len(cs_set)
    assignment_sets = []
    if exp.dims == 1:
        for cs in cs_set:
            resonance_choices = get_resonance_choices_1d(
                cs, correlations, exp_name, level)
            assignment_sets.append(resonance_choices)

    else:
        for cs in cs_set:
            resonance_choices = get_resonance_choices_2d(
                cs, correlations, exp_name, level)
            assignment_sets.append(resonance_choices)


    # Get a list of all possible residue assignments
    res_types = set([y for x in assignment_sets for y in x])

    # Combine the info into a table like structure
    assignment_lines = []
    for res in res_types:
        res_assignments = [x[res] for x in assignment_sets]

        # Regroup and fill in placeholder  nulls
        rows = []
        for assign in res_assignments:
            if not assign:
                rows.append('-')
            else:
                rows.append(assign)

        # Separate different atoms type assignments
        sub_assignments = list(product(*rows))
        for sub_assignment in sub_assignments:
            atoms = []
            scores = []
            ss_scores = []
            for atom_sub_assignment in sub_assignment:
                try:
                    atoms.append(atom_sub_assignment.atoms)
                except AttributeError:
                    atoms.append(None)

                try:
                    scores.append(atom_sub_assignment.scores)
                except AttributeError:
                    scores.append(0)

                try:
                    if atom_sub_assignment.ss_scores:
                        ss_scores.append(atom_sub_assignment.ss_scores)
                    else:
                        ss_scores.append(np.empty(3)*np.nan)
                except AttributeError:
                    ss_scores.append(np.empty(3)*np.nan)

            line = AssignmentLine(res, atoms, scores, ss_scores)
            assignment_lines.append(line)

    # Compare score with one another to get probabilities

    rows = [x.list for x in assignment_lines]
    columns = zip(*rows)

    if not columns:
        return None

    for k in xrange(n+1, n*2+1+1):
        scores = np.array(columns[k])

        # get the amino acid fractions
        if frequency:
            aa_scale = np.array([protein.aa_fractions[x] for x in columns[0]])
            aa_scale = aa_scale / aa_scale.sum()
            scores = scores * aa_scale

        summed = scores.sum()
        if not summed:
            scores = [0, ] * len(scores)
        else:
            scores = scores/summed
            scores = np.round(scores * 100, 1)
        columns[k] = scores

    rows = zip(*columns)
    rows = sorted(rows,
                  key=lambda x: tuple([x[-4]] + [y for y in x[n+1:n*2+1]]),
                  reverse=True)
    return rows

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--peak", action='append',
        type=float,
        nargs='+',
        help="""Chemical shifts, examples: -p 55 -p 18 (if exp_name is 1D)
                -p 55 18 (if exp_name is 2D.""")

    parser.add_argument("-e", "--exp_name",
        default='c',
        choices=['c', 'h', 'n', 'cc', 'cn'],
        help="Experiments available: c, n, h, cc, cn")

    parser.add_argument("-c", "--cut_off",
        action="store",
        type=float,
        default=-1,
        help="Cut off %% value, input a negative number for everything.")

    parser.add_argument("-s", "--seq",
        action="store",
        type=str,
        default='',
        help="Protein sequence in 1-letter amino-acid code.")

    parser_dict = vars(parser.parse_args())

    cs_set = parser_dict['peak']
    exp_name = parser_dict['exp_name']
    cut_off = parser_dict['cut_off']
    seq = parser_dict['seq']

    # A little input validation.
    exp = inbase.standard_experiments[exp_name]
    if isinstance(cs_set[0], collections.Iterable):

        peak_dims = len(cs_set[0])
    else:
        peak_dims = 1

    if exp.dims != peak_dims:
        raise ValueError(
            'The peak dims does not equal the dims of the experiment!')

    n = len(cs_set)
    table = main(cs_set, exp_name, seq=seq)
    # Pretty Printing
    print('input: {}'.format(', '.join(map(str, cs_set))))
    print('experiment: {}'.format(exp_name))

    if table is None:
        print('No chemical shifts were found!')
    else:
        header = ['AA'] + ['p{}'.format(x+1) for x in xrange(n)]*2
        header += ['Joint', 'H', 'C', 'E']
        table.insert(0, header)
        cols = [list(x) for x in zip(*table)]
        col_widths = [max(map(len, map(str, x))) for x in cols]
        fmt = '  '.join(['{{:<{}}}'.format(width) for width in col_widths])

        for line in table:

            if line[-4] <= cut_off:
                break
            line = [x if x else '-' for x in line]
            print(fmt.format(*line))
