#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
======
PLUQin
======

A program to help assign protein chemical shifts peaks. Especially helpful for
assigning chemical shift correlations in a 2D plane. The data used by this
program comes from the PIQC [1] analysis of the PACSY/BMRB [2] database.

All possible intra-residue chemical shift assignments within a given confidence
level are provided. The possible assignments are ranked by likelihood using
probability density functions determined with non-parametric methods. If
desired you can truncate the assignment at a certain likelihood. If you are
worried about miss-grouping peaks, keep the cut-off value negative, this
returns all possibilities for each resonance even if some options are missing
peaks and can not be assigned. The program also provides secondary structure
(H:C:E probability). The probabilities will be adjusted based on the sequence
if it is provided, by default the probabilities are adjusted to the average
amino-acid frequencies.

Experiments
------------

- 2D Carbon 1-bond: cc
- 2D Carbon-Nitrogen 1-bond (ie. mostly CA-N ): cn
- 1D Carbon: c
- 1D Nitrogen: n
- 1D Proton: h

If you know a little python it is pretty easy to add new experiments but you
will need the full version of the PACSY database with the PIQC tables. See
'utility/build_exp_pdf.py' for an example.

Warning
--------
No Database Chemical Shifts for: Trp-(CD2)-All, Trp-(CG)-All Glu-(HE2)-All,
Asp-(HD2)-All, Lys-(HZ1)-All, Pro-(H2)-All, Pro-(H3)-All, Tyr-(HH)-All,
Asp-(CB,CG)-Sheet, Asp-(CG,CB)-Sheet, His-(CG,CB)-Coil, Trp-(CZ2,CE2)-All,
Trp-(CD2,CE3)-All, Trp-(CB,CG)-Helix, Trp-(CB,CG)-Coil, Trp-(CG,CB)-Helix,
Trp-(CG,CB)-Coil, Trp-(CE3,CD2)-All, Trp-(CE2,CZ2)-All, Tyr-(CB,CG)-Coil
Tyr-(CG,CB)-Coil, Lys-(CE,NZ)-All, Pro-(CA,N)-Coil, Pro-(CD,N)-Helix
Pro-(CD,N)-Sheet, Thr-(CA,N)-Helix

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
import collections
from collections import namedtuple
from itertools import compress, product
import numpy as np
from pluq.base import Correlation
import pluq.base as base
import pluq.fileio as fileio
import pluq.inbase as inbase
from shapely.geometry import Point

__version__ = '0.2.1.0'

Assignment = namedtuple('Assignment', ['res', 'atoms', 'scores', 'ss_scores'],
                        verbose=False)
Assignment.__new__.__defaults__ = (None,) * len(Assignment._fields)


# TODO Assignment and AssignmentLine can and should be joined.
class AssignmentLine(object):
    """
    Little container class for holding assignment and assignment scores.

    :param aa: 1-letter code amino acid
    :param atoms: tuple of BMRB atom names
    :param scores: list of scores, 1 score for each atom in atoms
    :param ss_scores: list of tuple of scores, 1 tuple of length 3 for each
                      atom in atoms
    """
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
        """
        Returns the product of the scores.
        """
        return np.product(self.scores)

    @property
    def ss_prob(self):
        """
        Returns the product of non zero scores converted to probabilities.
        """
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
        """
        Return a formatted list of the assignment line.
        """

        line = [self.aa]
        line += self.atoms + list(self.scores) + [self.joint_score]
        line += list(self.ss_prob)

        return line

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ', '.join(self.list)


def get_resonance_choices(resonance, correlations, experiment_name, level=95):
    """
    Determine which chemical shift ranges at the given confidence level for an
    experiment contain the input resonance. If so adds the matching correlation
    to a dictionary and scores the resonance against the probability density
    functions. The correlation are sorted by there amino acid in the
    dictionary.

    :param resonance: float or list of float chemical shifts.
    :param correlations: list of pluq.base.Correlation
    :param experiment_name: one of the key from inbase.standard_experiments
    :param level: int, one of the defined levels normally in [68, 85, 95]
    :return dict[res] = list(Assignment, ...)
    """

    pdf_dict = inbase.read_pdf(experiment_name)
    levels = list(pdf_dict.attrs['confidence_levels'])

    try:
        ind = levels.index(level)
    except ValueError:
        mesg = 'You must chose a confidence level from {}'.format(levels)
        raise ValueError(mesg)

    # Find all the hits
    exp = inbase.standard_experiments[experiment_name]
    if exp.dims == 1:
        new_correlations = []
        for corr in correlations:
            try:
                cs_range = pdf_dict[str(corr)+',levs'][ind]
            except KeyError:
                continue

            if min(cs_range) <= resonance <= max(cs_range):
                new_correlations.append(corr)
        correlations = new_correlations

    else:
        region_dict = fileio.read_region(experiment_name, level)
        regions = [region_dict[str(x)] for x in correlations]

        # Find all the hits
        hits = map(Point(resonance).within, regions)
        correlations = list(compress(correlations, hits))

    # Score all the hits
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


def main(resonance_set, experiment_name='c', seq=None, level=95,
         frequency=True):
    """
    PLUQin: returns a table of possible intra-residue assignments
    and there likelihoods based on input chemical shifts and optionally the
    sequence. They are sorted first by the assignment joint probability and
    then by the sum of the individual probabilities.

    :param resonance_set: list or a list of lists of chemical shifts floats
    :param experiment_name: one of the keys from inbase.standard_experiments
    :param seq: protein sequence 1-letter amino-acid codes
    :type seq: iterable or None, defualt is the 20 standard amino-acids
    :param level: int, one of the defined levels normally in [68, 85, 95]
    :param frequency: If true accounts for the frequency of amino acids in
        the sequence. If no sequence it used the average amino acid
        frequencies.
    :returns: list of AssignmentLine.list
    """
    try:
        exp = inbase.standard_experiments[experiment_name]
    except KeyError:
        mesg = '{} is not a known experiment'.format(experiment_name)
        raise ValueError(mesg)

    # A little input validation.
    if isinstance(resonance_set[0], collections.Iterable):
        peak_dims = len(resonance_set[0])
    else:
        peak_dims = 1

    if exp.dims != peak_dims:
        mesg = 'The peak dims does not equal the dims of the experiment!'
        raise ValueError(mesg)

    # Build a list of possible assignments
    protein = base.ProteinSeq(seq)
    correlations = protein.relevant_correlations(
        exp, structure=False, ignoresymmetry=True, offdiagonal=False)

    # Assign and score each resonance in cs_set.
    n = len(resonance_set)
    assignment_sets = []
    for cs in resonance_set:
        resonance_choices = get_resonance_choices(
            cs, correlations, experiment_name, level)
        assignment_sets.append(resonance_choices)

    # Get a list of all possible residue assignments
    res_types = set([y for x in assignment_sets for y in x])

    # Combine the info into a table like structure
    assignment_lines = []
    for res in res_types:
        res_assignments = [x[res] for x in assignment_sets]

        # Regroup and fill in placeholder  nulls
        rows = []
        # TODO: should append None, but it break collections.product
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

    # Compare scores with one another to get probabilities
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

    # Sort the assignment by the joint and then sum of probabilities
    order_scores = [columns[-4],
                    list(np.sum(np.array(columns[n+1:n*2+1]), axis=0))]
    ind = np.lexsort((order_scores[1], order_scores[0]))[::-1]
    rows = [zip(*columns)[x] for x in ind]

    return rows


if __name__ == "__main__":
    import argparse

    # Set up command line options.
    parser = argparse.ArgumentParser(
        description="""PLUQin: returns a table of possible intra-residue
        assignments and there likelihoods based on input chemical shifts and
        optionally the sequence. They are sorted first by the assignment joint
        probability and then by the sum of the individual probabilities.""",

        epilog=""" Fritzsching, Hong, Schmidt-Rohr. J. Biomol. NMR 2016
        doi:10.1007/s10858-016-0013-5""")

    parser.add_argument(
        "-p", "--peak",
        action='append',
        type=float,
        nargs='+',
        help="""Chemical shifts, examples: -p 55 -p 18 (if exp_name is 1D)
                -p 55 18 (if exp_name is 2D.""")

    parser.add_argument(
        "-e", "--exp_name",
        default='c',
        choices=['c', 'h', 'n', 'cc', 'cn'],
        help="Experiments available: c, n, h, cc, cn")

    parser.add_argument(
        "-c", "--cut_off",
        action="store",
        type=float,
        default=-1,
        help="Cut off %% value, input a negative number for everything.")

    parser.add_argument(
        "-s", "--seq",
        action="store",
        type=str,
        default='',
        help="Protein sequence in 1-letter amino-acid code.")

    # Parse the options.
    parser_dict = vars(parser.parse_args())

    if parser_dict['peak'] is None:
        parser.error('Use pluqin.py -h to see options.')

    cs_set = parser_dict['peak']
    exp_name = parser_dict['exp_name']
    cut_off = parser_dict['cut_off']
    seq = parser_dict['seq']

    table = main(cs_set, exp_name, seq=seq)

    # Pretty Printing
    print('input: {}'.format(', '.join(map(str, cs_set))))
    print('experiment: {}'.format(exp_name))

    if table is None:
        print('No chemical shifts were found!')

    else:
        n = len(cs_set)
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
