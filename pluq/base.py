"""
Common PLUQ classes
"""
from collections import Counter
from itertools import product, chain
from itertools import combinations as combi
from itertools import combinations_with_replacement as combi_r
import pluq.aminoacids as aminoacids


class Correlation(object):
    """
    Validates inputs and groups information together to define a
    complete assignable intra-residue correlation with
    secondary-structure information.

    :param aa: 1 letter str, 1 of the 20 canonical amino-acids
    :param atoms: valid bmrb atom names in an iterable, example
        ('CA', )
    :param ss: secondary-structure name from STRIDE or none
    """

    def __init__(self, aa, atoms, ss='X'):
        self.aa = aa
        assert isinstance(atoms, tuple)
        self.atoms = atoms
        self.ss = ss

    @property
    def aa(self):
        return self._aa

    @aa.setter
    def aa(self, aa):
        """Validate the amino-acid."""
        if aa not in aminoacids.aa_list:
            raise ValueError('{} is not a supported amino-acid'.format(aa))
        self._aa = aa

    def counterpart(self):
        """
        Generates the symmetric counterpart of the correlation. If
        not a 2d returns an error.

        :rtype Correlation
        :raises ValueError if not 2d
        """
        if len(self.atoms) != 2:
            raise ValueError('Only valid for 2d correlations')
        atoms = tuple(self.atoms[::-1])
        return Correlation(self.aa, atoms, self.ss)

    def __repr__(self):
        str_fmt = "'{}', " * len(self.atoms)

        if self.ss:
            ss = aminoacids.common_sndstr[self.ss]
        else:
            ss = 'X'

        return "Correlation('{}',({}),'{}')".format(
            self.aa,
            str_fmt.format(*self.atoms),
            ss)

    def __str__(self):
        return "{}-({})-{}".format(
            aminoacids.aa_3let[self.aa], ','.join(self.atoms),
            aminoacids.sndstr[self.ss])

    def __hash__(self):
        return hash((self.aa, self.atoms, self.ss))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __nq__(self, other):
        return not self.__eq__(other)


class ProteinID(object):
    """
    Validates inputs and groups `id` and `id type` together to define
    a protein in the PACSY database.

    :param id_value: int or str
    :param idtype: str in {'ID', 'KEY_ID', 'PDB_ID', 'BMRB_ID'}
    """
    def __init__(self, id_value, idtype):
        self.id = id_value
        self.idtype = idtype

    @property
    def idtype(self):
        return self._idtype

    @idtype.setter
    def idtype(self, idtype):
        """ Validate the id type."""
        if idtype not in {'ID', 'KEY_ID', 'PDB_ID', 'BMRB_ID'}:
            raise ValueError("{} not a valid idtype.".format(idtype))
        self._idtype = idtype

    def __str__(self):
        return "{}: {}".format(self.idtype, self.id)


class ProteinSeq(object):
    """
    Protein Sequence Class.

    :param sequence: iterable of 1-letter amino acid code str. If
        False, default to the 20 amino acids in alphabetical order.
    """
    def __init__(self, sequence):
        """
        :param sequence: Any iterable with one-letter amino-acid
            codes.
        """
        self.seq = sequence
        if not sequence:
            self.average = True
        else:
            self.average = False

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, sequence):
        if not sequence:
            self._seq = list(aminoacids.aa_list)
        else:
            for s in sequence:
                if s not in aminoacids.aa_list:
                    mesg = '{} is not an amino-acid'.format(s)
                    raise ValueError(mesg)
            self._seq = sequence

    @property
    def unique(self):
        return set(self.seq)

    @property
    def count(self):
        return Counter(self.seq)

    @property
    def aa_fractions(self):
        if self.average:
            return aminoacids.aa_fractions
        else:
            n = float(len(self.seq))
            aa_fractions = dict()
            for res in self.seq:
                aa_fractions[res] = self.count[res]/n
            return aa_fractions

    def relevant_correlations(self, cs_exp, structure=True,
            ignoresymmetry=False, offdiagonal=True):
        """
        Generates a list of unique correlation determined by the
        sequence and the required instance of CSExperiment.

        :param cs_exp: Instance of CSExperiment.
        :param structure: bool, if True common second-structures are
            included in correlations for C, CA, CB, N, HN and HA.
        :param ignoresymmetry: bool, if True gives all correlation
        :param offdiagonal: bool, if True keeps Correlation with
            between the same atom.
        :return: [correlation, ...]
        """
        assert isinstance(cs_exp, CSExperiment)

        correlations = []
        for res in self.unique:
            patoms = []
            for nucleus in cs_exp.nuclei:
                patoms.append(
                    [x for x in aminoacids.aa_atoms[res] if x[0] == nucleus])

            if cs_exp.symmetric and cs_exp.diagonal:
                groups = combi_r({x for x in chain(*patoms)}, cs_exp.dims)
            elif cs_exp.symmetric:
                groups = combi({x for x in chain(*patoms)}, cs_exp.dims)
            else:
                groups = product(*patoms)

            possible = []
            if cs_exp.dims == 1:
                possible.extend(groups)

            else:
                for group in groups:
                    if (aminoacids.bonds_between_atoms(
                            res, group[0], group[1]) <= cs_exp.bonds):
                        possible.append(group)

            for atoms in possible:

                if len(set(atoms)) < cs_exp.dims and not offdiagonal:
                        continue
                if structure:
                    if [atom for atom in atoms if atom in aminoacids.ss_atoms]:
                        ss_list = ['H', 'E', 'C', 'X']
                    else:
                        ss_list = ['X']
                else:
                    ss_list = [None]

                for ss in ss_list:
                    correlations.append(Correlation(res, atoms, ss))

                    if cs_exp.symmetric and not ignoresymmetry:
                        correlations.append(Correlation(res, atoms[::-1], ss))
        return correlations

    def __repr__(self):
        return "ProteinSeq('{}')".format(self.seq)

    def __str__(self):
        return "ProteinSeq: {}".format(self.seq)


class Experiment(object):
    """
    Base class for defining NMR experiment(s). nuclei, symmetric and
    diagonal are the only experimental attributes defined, any other
    attributes methods should be defined in derived classes.

    :param nuclei: tuple of str, example ('C', 'N') for a
        carbon-nitrogen exp.
    :param symmetric: bool, True if spectrum is symmetric
    :param diagonal: bool, True if the experiment have a diagonal
    """
    def __init__(self, nuclei, symmetric=False, diagonal=False):
        assert isinstance(nuclei, tuple)
        super(Experiment, self).__init__()
        self.nuclei = nuclei
        self.diagonal = diagonal

        if len(set(nuclei)) > 1 and symmetric:
            raise ValueError('If symmetric all nuclei must be the same.')
        self.symmetric = symmetric

    @property
    def nuclei(self):
        return self._nuclei

    @nuclei.setter
    def nuclei(self, nuclei):
        """Run nuclei type error checking."""
        for nuc in nuclei:
            if nuc not in {'C', 'H', 'N'}:
                raise ValueError('{} is not a supported nucleus.'.format(nuc))
        self._nuclei = nuclei

    @property
    def dims(self):
        return len(self.nuclei)

    def __repr__(self):
        return 'Experiment({})'.format(self.nuclei)

    def __str__(self):
        return self.__repr__()


class CSExperiment(Experiment):
    """
    Chemical shift experiment definition.

    :param bonds: int

    """
    def __init__(self, nuclei, bonds=None, *args, **kwargs):
        super(CSExperiment, self).__init__(nuclei, *args, **kwargs)
        self.bonds = bonds
        self.data = []

    def __repr__(self):
        return 'Experiment({}, bonds={})'.format(
            self.nuclei, self.bonds)

    def __str__(self):
        return self.__repr__()


# class Resonance(object):
#     """
#     Chemical shifts which can be  completely explained by one instances
#     of the correlation class and associated instance of CSExperiment class.
#     """
#     def __init__(self, shifts, intensity=None, integral=None, width=None,
#                  ambiguity=None):
#         self.shifts = shifts
#         self.intensity = intensity
#         self.integral = integral
#         self.width = width
#         self.ambiguity = ambiguity
#
#
#     def __repr__(self):
#         return "Resonance(self.shifts)"
#
#     def __str__(self):
#         return self.__repr__()
