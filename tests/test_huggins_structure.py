"""Integer checks for a chart identity; not a fitted physiological model.
SPDX-License-Identifier: Apache-2.0
"""
import unittest
from models.huggins_1981.surface_structure import analyze_surface_structure


class SurfaceStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = analyze_surface_structure()

    def test_anchor_and_prediction_counts(self):
        self.assertEqual(self.report['transitions'], 91)
        self.assertEqual(self.report['anchoring_entries'], 25)
        self.assertEqual(self.report['nontrivial_predictions'], 66)
        self.assertEqual(self.report['exact_nontrivial_predictions'], 63)

    def test_three_one_minute_exceptions(self):
        rows = self.report['exceptions']
        self.assertEqual([(r['departure'], r['destination'], r['printed_min'],
                           r['predicted_min'], r['residual_min']) for r in rows],
                         [('L', 'I', 61, 60, 1), ('L', 'J', 42, 41, 1),
                          ('L', 'K', 24, 23, 1)])

    def test_anchor_equalities_are_not_counted_as_predictions(self):
        for row in self.report['rows']:
            self.assertEqual(row['anchor'], row['destination'] == 'A' or row['departure'] == 'N')
            if row['anchor']:
                self.assertEqual(row['residual_min'], 0)

    def test_single_potential_fixed_buffer_ceiling_is_insufficient(self):
        values = self.report['single_potential_triangle_witnesses']
        self.assertEqual(values, {'D-B-A': 9, 'D-C-A': 3})
        self.assertGreater(max(values.values()) - min(values.values()), 3)


if __name__ == '__main__':
    unittest.main()
