"""Regression tests for research diagnostics, NOT operational dive safety."""
import math
import random
import unittest

from models.dsat import dsat1994_planner as dsat


def bisect_reference(state, depth):
    """Slow independent finite-horizon reference, only for tests."""
    def admissible(t):
        after = dsat.advance_hold(state, depth, t)
        return dsat.is_no_stop_surface_state(dsat.direct_ascent_surface_state(after, depth))
    if not admissible(0):
        return 0.0
    upper = 1e6
    if admissible(upper):
        return math.inf
    lo = 0.0
    for _ in range(70):
        mid = (lo + upper)/2
        if admissible(mid):
            lo = mid
        else:
            upper = mid
    return lo


class DsatTests(unittest.TestCase):
    def test_published_anchor_curve_is_not_table(self):
        self.assertAlmostEqual(dsat.no_stop_curve_minutes(60), 55.54, delta=0.02)
        self.assertEqual(len(dsat.TABLE_II_DEPTHS_FSW), 10)
        self.assertEqual(len(dsat.M0_RDP_FSW), 14)

    def test_closed_form_matches_numeric_reference(self):
        rng = random.Random(20261025)
        for depth in (22, 40, 60, 80, 100, 120, 130):
            for _ in range(30):
                state = dsat.clean_surface_state()
                state = dsat.advance_linear(state, 0, depth)
                state = dsat.advance_hold(state, depth, rng.uniform(0, 70))
                exact = dsat.current_direct_ascent_ndl_minutes(state, depth)
                numeric = bisect_reference(state, depth)
                if math.isinf(numeric):
                    self.assertTrue(math.isinf(exact))
                else:
                    self.assertAlmostEqual(exact, numeric, delta=1e-6)

    def test_shallow_cutoff_bug_is_fixed(self):
        state = dsat.advance_linear(dsat.clean_surface_state(), 0, 22)
        ndl = dsat.current_direct_ascent_ndl_minutes(state, 22)
        self.assertTrue(math.isfinite(ndl))
        self.assertGreater(ndl, 1000)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            dsat.no_stop_curve_minutes(float('nan'))
        with self.assertRaises(ValueError):
            dsat.advance_hold(dsat.clean_surface_state(), 50, -3)
        with self.assertRaises(ValueError):
            dsat.surface_interval(dsat.clean_surface_state(), -20)


if __name__ == '__main__':
    unittest.main()
