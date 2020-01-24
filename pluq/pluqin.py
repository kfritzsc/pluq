from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
from collections import namedtuple
from itertools import compress, product
import numpy as np
from pluq.base import Correlation
import pluq.base as base
import pluq.fileio as fileio
import pluq.inbase as inbase
from shapely.geometry import Point


Assignment = namedtuple('Assignment', ['res', 'atoms', 'scores', 'ss_scores'])
Assignment.__new__.__defaults__ = (None,) * len(Assignment._fields)


# TODO Assignment and AssignmentLine can and should be joined.
class AssignmentLine(object):
    """
    Little container class for holding assignment and assignment
    scores.

    :param aa: 1-letter code amino acid
    :param atoms: tuple of BMRB atom names
    :param scores: list of scores, 1 score for each atom in atoms
    :param ss_scores: list of tuple of scores, 1 tuple of length 3
        for each atom in atoms
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
        Returns the product of non zero scores converted to
        probabilities.
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


def get_resonance_choices(resonance, correlations, experiment_name,
                          level=95):
    """
    Determine which chemical shift ranges at the given confidence
    level for an experiment contain the input resonance. If so adds
    the matching correlation to a dictionary and scores the resonance
    against the probability density functions. The correlation are
    sorted by there amino acid in the dictionary.

    :param resonance: float or list of float chemical shifts.
    :param correlations: list of pluq.base.Correlation
    :param experiment_name: one of the key from
        inbase.standard_experiments
    :param level: int, one of the defined levels normally in
        [68, 85, 95]
    :return dict[res] = list(Assignment, ...)
    """

    pdf_dict = inbase.read_pdf(experiment_name)
    levels = list(pdf_dict.attrs['confidence_levels'])

    try:
        ind = levels.index(level)
    except ValueError:
        mesg = 'Chose a confidence level from {}'.format(levels)
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

        assign = Assignment(corr.aa, corr.atoms, corr_score,
                            ss_scores)
        assignments[corr.aa].append(assign)
    return assignments


def main(resonance_set, experiment_name='c', seq=None, level=95,
         frequency=True):
    """
    PLUQin: returns a table of possible intra-residue assignments
    and there likelihoods based on input chemical shifts and
    optionally the sequence. They are sorted first by the assignment
    joint probability and then by the sum of the individual
    probabilities.

    :param resonance_set: list or a list of lists of chemical shifts
        floats
    :param experiment_name: one of the keys from
        inbase.standard_experiments
    :param seq: protein sequence 1-letter amino-acid codes
    :type seq: iterable or None, defualt is the 20 standard
        amino-acids
    :param level: int, one of the defined levels normally in
        {68, 85, 95}
    :param frequency: If true accounts for the frequency of amino
        acids in the sequence. If no sequence it used the average
        amino acid frequencies.
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
        mesg = 'The peak dims in not equal to the experiment!'
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
        # TODO: should append None, but it breaks collections.product
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
    columns = list(zip(*rows))

    if not columns:
        return None

    for k in list(range(n+1, n*2+1+1)):
        scores = np.array(columns[k])

        # get the amino acid fractions
        if frequency:
            aa_scale = np.array([protein.aa_fractions[x] for x in
                                 columns[0]])
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
    rows = [list(zip(*columns))[x] for x in ind]

    return rows
