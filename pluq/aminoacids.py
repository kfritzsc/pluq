"""
Lists, dictionaries and functions to determine the number of bonds between
two atoms in a amino-acid residue. Also dictionaries for secondary-structure
classifications and for converting between 1 and 3 letter amino-acids codes.

The amino acid graphs are hard coded and have been extensively tested.

BMRB notation is used throughout.
"""


# One letter amino-acid list.
aa_list = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P',
           'Q', 'R', 'S', 'T', 'V', 'W', 'Y'}

aa_fractions = {'A': .074, 'R': .042, 'N': .044, 'D': .059, 'C': .033,
                'E': .058, 'Q': .037, 'G': .074, 'H': .029, 'I': .038,
                'L': .076, 'K': .072, 'M': .018, 'F': .040, 'P': .050,
                'S': .081, 'T': .062, 'W': .013, 'Y': .033, 'V': .068}

ss_list = {'H', 'C', 'T', 'E', 'G', 'b', 'I', 'B', 'X', None}

ss_atoms = {'C', 'CA', 'CB', 'N', 'H', 'HA'}

# One letter to three letter amino-acid conversion dictionary.
aa_3let = dict()
aa_3let['A'] = 'Ala'
aa_3let['C'] = 'Cys'
aa_3let['D'] = 'Asp'
aa_3let['E'] = 'Glu'
aa_3let['F'] = 'Phe'
aa_3let['G'] = 'Gly'
aa_3let['H'] = 'His'
aa_3let['I'] = 'Ile'
aa_3let['K'] = 'Lys'
aa_3let['L'] = 'Leu'
aa_3let['M'] = 'Met'
aa_3let['N'] = 'Asn'
aa_3let['P'] = 'Pro'
aa_3let['Q'] = 'Gln'
aa_3let['R'] = 'Arg'
aa_3let['S'] = 'Ser'
aa_3let['T'] = 'Thr'
aa_3let['V'] = 'Val'
aa_3let['W'] = 'Trp'
aa_3let['Y'] = 'Tyr'

# Secondary-Structure code to name dictionary.
sndstr = dict()
sndstr['C'] = 'Coil'
sndstr['T'] = 'Turn'
sndstr['H'] = 'Helix'
sndstr['E'] = 'Sheet'
sndstr['B'] = 'Bridge'
sndstr['b'] = 'Bridge'
sndstr['G'] = '3-10 Helix'
sndstr['I'] = 'Pi Helix'
sndstr['X'] = 'All'
sndstr[None] = 'All'

# Secondary-structure conversion to common structure types dictionary.
common_sndstr = dict()
common_sndstr['C'] = 'C'
common_sndstr['T'] = 'C'
common_sndstr['H'] = 'H'
common_sndstr['E'] = 'E'
common_sndstr['B'] = 'E'
common_sndstr['b'] = 'E'
common_sndstr['G'] = 'H'
common_sndstr['I'] = 'H'
common_sndstr['X'] = 'X'

# Secondary-structure conversion to common Secondary-Structure tuple
# dictionary.
similar_sndstr = dict()
similar_sndstr['C'] = ('C', 'T')
similar_sndstr['T'] = ('C', 'T')
similar_sndstr['H'] = ('H', 'G', 'I')
similar_sndstr['G'] = ('H', 'G', 'I')
similar_sndstr['I'] = ('H', 'G', 'I')
similar_sndstr['E'] = ('E', 'B', 'b')
similar_sndstr['B'] = ('E', 'B', 'b')
similar_sndstr['b'] = ('E', 'B', 'b')

# Amino-acid atom name in sets dictionary.
aa_atoms = dict()
aa_atoms['A'] = {'H', 'HA', 'HB1', 'HB2', 'HB3',
                 'C', 'CA', 'CB',
                 'N', 'O'}

aa_atoms['C'] = {'H', 'HA', 'HB2', 'HB3', 'HG',
                 'C', 'CA', 'CB',
                 'N', 'O', 'SG'}

aa_atoms['E'] = {'H', 'HA', 'HB2', 'HB3', 'HG2', 'HG3', 'HE2',
                 'C', 'CA', 'CB', 'CG', 'CD',
                 'N', 'O', 'OE1', 'OE2'}

aa_atoms['D'] = {'H', 'HA', 'HB2', 'HB3', 'HD2',
                 'C', 'CA', 'CB', 'CG',
                 'N', 'O', 'OD1', 'OD2'}

aa_atoms['F'] = {'H', 'HA', 'HB2', 'HB3', 'HD1', 'HD2', 'HE1', 'HE2', 'HZ',
                 'C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ',
                 'N', 'O'}

aa_atoms['G'] = {'H', 'HA2', 'HA3',
                 'C', 'CA',
                 'N', 'O'}

aa_atoms['I'] = {'H', 'HA', 'HB', 'HG12', 'HG13', 'HG21', 'HG22', 'HG23',
                 'HD11', 'HD12', 'HD13',
                 'C', 'CA', 'CB', 'CG1', 'CG2', 'CD1',
                 'N', 'O'}

aa_atoms['H'] = {'H', 'HA', 'HB2', 'HB3', 'HD1', 'HD2', 'HE1', 'HE2',
                 'C', 'CA', 'CB', 'CG', 'CD2', 'CE1',
                 'N', 'ND1', 'NE2', 'O'}

aa_atoms['K'] = {'H', 'HA', 'HB2', 'HB3', 'HG2', 'HG3', 'HD2', 'HD3', 'HE2',
                 'HE3', 'HZ1', 'HZ2', 'HZ3',
                 'C', 'CA', 'CB', 'CG', 'CD', 'CE',
                 'N', 'NZ', 'O'}

aa_atoms['M'] = {'H', 'HA', 'HB2', 'HB3', 'HG2', 'HG3', 'HE1', 'HE2', 'HE3',
                 'C', 'CA', 'CB', 'CG', 'CE',
                 'N', 'O', 'SD'}

aa_atoms['L'] = {'H', 'HA', 'HB2', 'HB3', 'HG', 'HD11', 'HD12', 'HD13', 'HD21',
                 'HD22', 'HD23',
                 'C', 'CA', 'CB', 'CG', 'CD1', 'CD2',
                 'N', 'O'}

aa_atoms['N'] = {'H', 'HA', 'HB2', 'HB3', 'HD21', 'HD22',
                 'C', 'CA', 'CB', 'CG',
                 'N', 'ND2', 'O', 'OD1'}

aa_atoms['P'] = {'H2', 'H3', 'HA', 'HB2', 'HB3', 'HG2', 'HG3', 'HD2', 'HD3',
                 'C', 'CA', 'CB', 'CG', 'CD',
                 'N', 'O'}

aa_atoms['Q'] = {'H', 'HA', 'HB2', 'HB3', 'HG2', 'HG3', 'HE21', 'HE22',
                 'C', 'CA', 'CB', 'CG', 'CD',
                 'N', 'NE2', 'O', 'OE1'}

aa_atoms['R'] = {'H', 'HA', 'HB2', 'HB3', 'HG2', 'HG3', 'HD2', 'HD3', 'HE',
                 'HH11', 'HH12', 'HH21', 'HH22',
                 'C', 'CA', 'CB', 'CG', 'CD', 'CZ',
                 'N', 'NE', 'NH1', 'NH2', 'O'}

aa_atoms['S'] = {'H', 'HA', 'HB2', 'HB3', 'HG',
                 'C', 'CA', 'CB',
                 'N', 'O', 'OG'}

aa_atoms['T'] = {'H', 'HA', 'HB', 'HG1', 'HG21', 'HG22', 'HG23',
                 'C', 'CA', 'CB', 'CG2',
                 'N', 'O', 'OG1'}

aa_atoms['V'] = {'H', 'HA', 'HB', 'HG11', 'HG12', 'HG13', 'HG21', 'HG22',
                 'HG23',
                 'C', 'CA', 'CB', 'CG1', 'CG2',
                 'N', 'O'}

aa_atoms['W'] = {'H', 'HA', 'HB2', 'HB3', 'HD1', 'HE1', 'HE3', 'HZ2', 'HZ3',
                 'HH2',
                 'C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE2', 'CE3', 'CZ2',
                 'CZ3', 'CH2',
                 'N', 'NE1', 'O'}

aa_atoms['Y'] = {'H', 'HA', 'HB2', 'HB3', 'HD1', 'HD2', 'HE1', 'HE2', 'HH',
                 'C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ',
                 'N', 'O', 'OH'}


# Amino-acid graphs dictionary.
# Ready set go.
aa_graph = dict()
aa_graph['A'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'HB1', 'HB2', 'HB3'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB1': {'CB'},
                 'HB2': {'CB'},
                 'HB3': {'CB'}}

aa_graph['C'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'SG', 'HB2', 'HB3'},
                 'SG': {'CB', 'HG'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'},
                 'HB3': {'CB'},
                 'HG': {'SG'}}

aa_graph['D'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'OD1', 'OD2'},
                 'OD1': {'CG'},
                 'OD2': {'CG', 'HD2'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'},
                 'HB3': {'CB'},
                 'HD2': {'OD2'}}

aa_graph['E'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD', 'HG2', 'HG3'},
                 'CD': {'CG', 'OE1', 'OE2'},
                 'OE1': {'CD'},
                 'OE2': {'CD', 'HE2'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'},
                 'HB3': {'CB'},
                 'HG2': {'CG'},
                 'HG3': {'CG'},
                 'HE2': {'OE2'}}

aa_graph['F'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD1', 'CD2'},
                 'CD1': {'CG', 'CE1', 'HD1'},
                 'CD2': {'CG', 'CE2', 'HD2'},
                 'CE1': {'CD1', 'CZ', 'HE1'},
                 'CE2': {'CD2', 'CZ', 'HE2'},
                 'CZ': {'CE1', 'CE2', 'HZ'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HD1': {'CD1'}, 'HD2': {'CD2'},
                 'HE1': {'CE1'}, 'HE2': {'CE2'},
                 'HZ': {'CZ'}}

aa_graph['G'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'N', 'HA2', 'HA3'},
                 'H': {'N'},
                 'HA2': {'CA'},
                 'HA3': {'CA'}}

aa_graph['H'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O', 'HA'},
                 'CA': {'C', 'CB', 'N'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'ND1', 'CD2'},
                 'ND1': {'CG', 'CE1', 'HD1'},
                 'CD2': {'CG', 'NE2', 'HD2'},
                 'CE1': {'ND1', 'NE2', 'HE1'},
                 'NE2': {'CD2', 'CE1', 'HE2'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HD1': {'ND1'}, 'HD2': {'CD2'},
                 'HE1': {'CE1'}, 'HE2': {'NE2'}}

aa_graph['I'] = {'N': {'CA', 'H'},
                 'O': set('C'),
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG1', 'CG2', 'HB'},
                 'CG1': {'CB', 'CD1', 'HG12', 'HG13'},
                 'CG2': {'CB', 'HG21', 'HG22', 'HG23'},
                 'CD1': {'CG1', 'HD11', 'HD12', 'HD13'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB': {'CB'},
                 'HG12': {'CG1'}, 'HG13': {'CG1'},
                 'HG21': {'CG2'}, 'HG22': {'CG2'}, 'HG23': {'CG2'},
                 'HD11': {'CD1'}, 'HD12': {'CD1'}, 'HD13': {'CD1'}}

aa_graph['K'] = {'N': {'CA', 'H'},
                 'O': set('C'),
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD', 'HG2', 'HG3'},
                 'CD': {'CG', 'CE', 'HD2', 'HD3'},
                 'CE': {'CD', 'NZ', 'HE2', 'HE3'},
                 'NZ': {'CE', 'HZ1', 'HZ2', 'HZ3'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG2': {'CG'}, 'HG3': {'CG'},
                 'HD2': {'CD'}, 'HD3': {'CD'},
                 'HE2': {'CE'}, 'HE3': {'CE'},
                 'HZ1': {'NZ'}, 'HZ2': {'NZ'}, 'HZ3': {'NZ'}}

aa_graph['L'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD1', 'CD2', 'HG'},
                 'CD1': {'CG', 'HD11', 'HD12', 'HD13'},
                 'CD2': {'CG', 'HD21', 'HD22', 'HD23'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG': {'CG'},
                 'HD11': {'CD1'}, 'HD12': {'CD1'}, 'HD13': {'CD1'},
                 'HD21': {'CD2'}, 'HD22': {'CD2'}, 'HD23': {'CD2'}}

aa_graph['M'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'SD', 'HG2', 'HG3'},
                 'SD': {'CG', 'CE'},
                 'CE': {'SD', 'HE1', 'HE2', 'HE3'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG2': {'CG'}, 'HG3': {'CG'},
                 'HE1': {'CE'}, 'HE2': {'CE'}, 'HE3': {'CE'}}

aa_graph['N'] = {'N': {'CA', 'H'},
                 'O': set('C'),
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'OD1', 'ND2'},
                 'OD1': {'CG'},
                 'ND2': {'CG', 'HD21', 'HD22'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HD21': {'ND2'}, 'HD22': {'ND2'}}

aa_graph['P'] = {'N': {'CA', 'CD', 'H2', 'H3'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD', 'HG2', 'HG3'},
                 'CD': {'CG', 'N', 'HD2', 'HD3'},
                 'H2': {'N'}, 'H3': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG2': {'CG'}, 'HG3': {'CG'},
                 'HD2': {'CD'}, 'HD3': {'CD'}}

aa_graph['Q'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD', 'HG2', 'HG3'},
                 'CD': {'CG', 'OE1', 'NE2'},
                 'OE1': {'CD'},
                 'NE2': {'CD', 'HE21', 'HE22'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG2': {'CG'}, 'HG3': {'CG'},
                 'HE21': {'NE2'}, 'HE22': {'NE2'}}

aa_graph['R'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD', 'HG2', 'HG3'},
                 'CD': {'CG', 'NE', 'HD2', 'HD3'},
                 'NE': {'CD', 'CZ', 'HE'},
                 'CZ': {'NE', 'NH1', 'NH2'},
                 'NH1': {'CZ', 'HH11', 'HH12'},
                 'NH2': {'CZ', 'HH21', 'HH22'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG2': {'CG'}, 'HG3': {'CG'},
                 'HD2': {'CD'}, 'HD3': {'CD'},
                 'HE': {'NE'},
                 'HH11': {'NH1'}, 'HH12': {'NH1'},
                 'HH21': {'NH2'}, 'HH22': {'NH2'}}

aa_graph['S'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'OG', 'HB2', 'HB3'},
                 'OG': {'CB', 'HG'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HG': {'OG'}}

aa_graph['T'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'OG1', 'CG2', 'HB'},
                 'OG1': {'CB', 'HG1'},
                 'CG2': {'CB', 'HG21', 'HG22', 'HG23'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB': {'CB'},
                 'HG1': {'OG1'},
                 'HG21': {'CG2'}, 'HG22': {'CG2'}, 'HG23': {'CG2'}}

aa_graph['V'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG1', 'CG2', 'HB'},
                 'CG1': {'CB', 'HG11', 'HG12', 'HG13'},
                 'CG2': {'CB', 'HG21', 'HG22', 'HG23'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB': {'CB'},
                 'HG11': {'CG1'}, 'HG12': {'CG1'}, 'HG13': {'CG1'},
                 'HG21': {'CG2'}, 'HG22': {'CG2'}, 'HG23': {'CG2'}}

aa_graph['W'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD1', 'CD2'},
                 'CD1': {'CG', 'NE1', 'HD1'},
                 'CD2': {'CG', 'CE2', 'CE3'},
                 'NE1': {'CD1', 'CE2', 'HE1'},
                 'CE2': {'CD2', 'NE1', 'CZ2'},
                 'CE3': {'CD2', 'CZ3', 'HE3'},
                 'CZ2': {'CE2', 'CH2', 'HZ2'},
                 'CZ3': {'CE3', 'CH2', 'HZ3'},
                 'CH2': {'CZ2', 'CZ3', 'HH2'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HD1': {'CD1'},
                 'HE1': {'NE1'},
                 'HE3': {'CE3'},
                 'HZ2': {'CZ2'},
                 'HZ3': {'CZ3'},
                 'HH2': {'CH2'}}

aa_graph['Y'] = {'N': {'CA', 'H'},
                 'O': {'C'},
                 'C': {'CA', 'O'},
                 'CA': {'C', 'CB', 'N', 'HA'},
                 'CB': {'CA', 'CG', 'HB2', 'HB3'},
                 'CG': {'CB', 'CD1', 'CD2'},
                 'CD1': {'CG', 'CE1', 'HD1'},
                 'CD2': {'CG', 'CE2', 'HD2'},
                 'CE1': {'CD1', 'CZ', 'HE1'},
                 'CE2': {'CD2', 'CZ', 'HE2'},
                 'CZ': {'CE1', 'CE2', 'OH'},
                 'OH': {'CZ', 'HH'},
                 'H': {'N'},
                 'HA': {'CA'},
                 'HB2': {'CB'}, 'HB3': {'CB'},
                 'HD1': {'CD1'}, 'HD2': {'CD2'},
                 'HE1': {'CE1'}, 'HE2': {'CE2'},
                 'HH': {'OH'}}


def traverse_atoms(res, start, end, path=None):
    """
    Returns all the possible ways to traverse between two atoms of a residue,
    without repeating any atoms.

    :param res: One letter amino-acid code
    :param start: Starting atom in BMRB nomenclature.
    :param end: Ending atom in BMRB nomenclature.
    :param path: Any known part of traverse. Used by the (recursive) function,
                 normally not used by user.

    :rtype : list
    """
    if not path:
        path = []
    path = path + [start]

    if start == end:
        # Note the critical brackets!
        return [path]

    paths = []
    try:
        graph = aa_graph[res][start]
        for node in graph:
            if node not in path:
                new_paths = traverse_atoms(res, node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return map(tuple, paths)

    except KeyError:
        if res not in aa_list:
            raise ValueError(
                '{} is not a supported amino-acid.'.format(res))
        elif start not in aa_atoms[res]:
            raise ValueError('{} is not an atom in {}.'.format(start, res))
        elif end not in aa_atoms[res]:
            raise ValueError('{} is not an atom in {}.'.format(end, res))
        # Used for debugging.
        else:
            print('Unknown Error: Please fix and/or report.')
            raise


def bonds_between_atoms(res, start, end):
    """
    Returns the number of bonds between two atoms for a given amino-acid.

    :param res: One letter amino-acid code
    :param start: Starting atom in BMRB nomenclature.
    :param end: Ending atom in BMRB nomenclature.

    :rtype bonds : int
    """

    paths = traverse_atoms(res, start, end)
    short_path = sorted(paths, key=len)[0]
    bonds = len(short_path) - 1
    return bonds
