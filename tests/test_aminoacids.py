"""
Unit tests for aminoacids.py module.

KJF 2014-21-05
"""

import unittest
import pluq.aminoacids as aminoacids


class CompleteGraphs(unittest.TestCase):
    def test_all_aa_graph_keys(self):
        """Sanity check to make sure all graphs have all elements as keys."""
        for res in aminoacids.aa_list:
            for atom in aminoacids.aa_atoms[res]:
                self.assertIn(atom, aminoacids.aa_graph[res],
                              msg='{} is not a key in aa_graphs[{}]'.format(
                                  atom, res))

    def test_all_aa_graphs_correct_atoms(self):
        """ Test to make sure every atom in aa_graphs is correct."""
        for res in aminoacids.aa_list:
            atoms = set()
            for atom in aminoacids.aa_atoms[res]:
                atoms = atoms.union(aminoacids.aa_graph[res][atom])

            self.assertEqual(atoms, aminoacids.aa_atoms[res],
                             msg="Problem Atoms in aa_graphs[{}].".format(res))


class KnownAtomTraverse(unittest.TestCase):
    # At least one case for every residue.r
    known_paths = [(('A', 'C', 'CB'), ('C', 'CA', 'CB')),
                   (('C', 'C', 'SG'), ('C', 'CA', 'CB', 'SG')),
                   (('D', 'CB', 'N'), ('CB', 'CA', 'N')),
                   (('E', 'OE1', 'OE2'), ('OE1', 'CD', 'OE2')),
                   (('F', 'CB', 'CE1'), ('CB', 'CG', 'CD1', 'CE1')),
                   (('G', 'C', 'HA2'), ('C', 'CA', 'HA2')),
                   (('H', 'ND1', 'NE2'), ('ND1', 'CE1', 'NE2')),
                   (('I', 'C', 'CB'), ('C', 'CA', 'CB')),
                   (('K', 'NZ', 'HE3'), ('NZ', 'CE', 'HE3')),
                   (('L', 'C', 'CB'), ('C', 'CA', 'CB')),
                   (('M', 'HG2', 'HE1'), ('HG2', 'CG', 'SD', 'CE', 'HE1')),
                   (('N', 'C', 'CB'), ('C', 'CA', 'CB')),
                   (('P', 'N', 'HG2'), ('N', 'CD', 'CG', 'HG2')),
                   (('Q', 'CB', 'H'), ('CB', 'CA', 'N', 'H')),
                   (('R', 'NE', 'NH2'), ('NE', 'CZ', 'NH2')),
                   (('S', 'HB2', 'CA'), ('HB2', 'CB', 'CA')),
                   (('T', 'CA', 'HG23'), ('CA', 'CB', 'CG2', 'HG23')),
                   (('V', 'CG2', 'CA'), ('CG2', 'CB', 'CA')),
                   (('W', 'CG', 'CE2'), ('CG', 'CD2', 'CE2')),
                   (('Y', 'HH', 'HE1'), ('HH', 'OH', 'CZ', 'CE1', 'HE1'))]

    # If there is two "equivalent" ways just pick one.
    edge_case = (('F', 'CB', 'CZ'),
                 (('CB', 'CG', 'CD1', 'CE1', 'CZ'),
                  ('CB', 'CG', 'CD2', 'CE2', 'CZ')))

    def test_traverse_atoms_edge(self):
        """ Test that one of the correct path is found if both are okay.
        """
        res, atom1, atom2 = self.edge_case[0]
        paths = aminoacids.traverse_atoms(res, atom1, atom2)
        short_path = sorted(paths, key=len)[0]
        self.assertIn(short_path, self.edge_case[1])

    def test_traverse_atoms(self):
        """ Test that the correct path is returned between bonds."""
        for group, path in self.known_paths:
            res, atom1, atom2 = group
            paths = aminoacids.traverse_atoms(res, atom1, atom2)
            short_path = sorted(paths, key=len)[0]
            self.assertEqual(path, short_path)


class BadInputAtomTraverse(unittest.TestCase):

    # A few example of bad inputs.
    bad_inputs = [('X', 'CA', 'CB'),
                  ('I', 'HG1', 'CA'),
                  ('R', 'HN21', 'HN23')]

    def test_bad_input_atom_traverse(self):
        for bad_input in self.bad_inputs:
            res, atom1, atom2 = bad_input
            self.assertRaises(ValueError,
                              lambda: aminoacids.traverse_atoms(res, atom1, atom2))


class KnownBondDistance(unittest.TestCase):
    # Not an exhaustive case list but a small sampling.
    known_bonds = [(('A', 'O', 'HB1'), 4),
                   (('A', 'CA', 'CA'), 0),
                   (('C', 'H', 'HA'), 3),
                   (('D', 'H', 'CG'), 4),
                   (('E', 'N', 'CA'), 1),
                   (('H', 'N', 'ND1'), 4),
                   (('H', 'H', 'HD2'), 6),
                   (('I', 'C', 'CD1'), 4),
                   (('I', 'CD1', 'CG2'), 3),
                   (('P', 'CA', 'CD'), 2),
                   (('W', 'O', 'HE3'), 7)]

    def test_bonds_between_atoms(self):
        """
        Test ability to determine the number of bonds between atoms
        in the 20 common amino-acids.
        """

        for group, bonds in self.known_bonds:
            res, atom1, atom2 = group
            result = aminoacids.bonds_between_atoms(res, atom1, atom2)
            self.assertEqual(bonds, result)


if __name__ == '__main__':
    unittest.main()

