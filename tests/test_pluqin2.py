"""
Unit tests for pluqin2

KJF 2014-21-05
"""

import unittest
from shapely.geometry import Polygon, MultiPolygon
import pluq.base as base
from pluq.aminoacids import aa_list


class PLUQinRegionsCC(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.corr_regions = base.load_2d_regions()
        self.aa_list = sorted(list(aa_list))

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.corr_regions
        del self.aa_list

    def test_regions_type(self):
        """
        All regions should be type: `shapely.Polygon` or `shapely.MultiPolygon`
        """
        for corr, region in self.corr_regions.items():
            self.assertIn(type(region), [Polygon, MultiPolygon])

    def test_all_available_corr(self):
        """
        Possible correlation for the experiment type and the 20 amino acids are in the
        shapefile except the diagonal (the diagonal is not a 2D correlation it is 1D).
        And any specifically listed.
        """

        res_types = base.ProteinSeq(self.aa_list)
        CC_PDSD = base.CSExperiment(('C', 'C'), bonds=2, symmetric=True)
        all_corrs = res_types.relevant_correlations(CC_PDSD,
                                                    structure=True,
                                                    ignoresymmetry=False,
                                                    offdiagonal=False)

        all_corrs = set(all_corrs)

        # TODO: Remove Exceptions!! from 2D 2-bonds, consider "buffering" the average.
        exceptions = {base.Correlation('H', ('CA', 'CG'), 'H'),
                      base.Correlation('H', ('CA', 'CG'), 'C'),
                      base.Correlation('H', ('CA', 'CG'), 'E'),
                      base.Correlation('H', ('CB', 'CG'), 'H'),
                      base.Correlation('H', ('CB', 'CG'), 'C'),
                      base.Correlation('H', ('CB', 'CG'), 'E'),
                      base.Correlation('W', ('CA', 'CG'),  'E'),
                      base.Correlation('W', ('CA', 'CG'),  'H'),
                      base.Correlation('W', ('CA', 'CG'),  'C'),
                      base.Correlation('W', ('CB', 'CG'),  'E'),
                      base.Correlation('W', ('CB', 'CG'),  'H'),
                      base.Correlation('W', ('CB', 'CG'),  'C'),
                      base.Correlation('W', ('CB', 'CD2'), 'C'),
                      base.Correlation('W', ('CG', 'CE3'), 'X'),
                      base.Correlation('W', ('CG', 'CD1'), 'X'),
                      base.Correlation('W', ('CG', 'CD2'), 'X'),
                      base.Correlation('W', ('CG', 'CE2'), 'X'),
                      base.Correlation('W', ('CD1', 'CD2'), 'X'),
                      base.Correlation('W', ('CE2', 'CD2'), 'X'),
                      }

        exceptions_conterpart = [x.counterpart() for x in exceptions]
        exceptions = exceptions.union(exceptions_conterpart)

        all_corrs = all_corrs.difference(exceptions)

        for corr in all_corrs:
            self.assertTrue(corr in self.corr_regions, msg='{}'.format(corr))

    def test_low_level_in_big(self):
        """
        Test that the regions with lower levels are always contained within regions with
        higher levels. A sanity check.
        """
        low_corr_regions = base.load_2d_regions(level=68)

        for corr, large_region in self.corr_regions.items():
            self.assertTrue(low_corr_regions[corr].within(large_region))

if __name__ == '__main__':
    unittest.main()






