"""Exact-envelope checks using deterministic randomized depth histories."""
import math
import random
import unittest

from mathematics.envelopes import compartment_envelope


class EnvelopeTests(unittest.TestCase):
    def test_reference_compartment_is_exact(self):
        for horizon in (None, 60.0, 480.0):
            a = 0.25
            e = compartment_envelope(0.791 * 120 * a, 60, 120,
                                     history_minutes=horizon)
            self.assertAlmostEqual(e.lower, 0.791 * 120 * a, places=9)
            self.assertAlmostEqual(e.upper, 0.791 * 120 * a, places=9)

    def test_extremizers(self):
        scale = 0.791 * 100
        a = 0.3
        fast = compartment_envelope(scale * a, 20, 100)
        self.assertAlmostEqual(fast.lower / scale, a ** 3, places=12)
        self.assertAlmostEqual(fast.upper / scale, 1 - (1-a)**3, places=12)
        slow = compartment_envelope(scale * a, 120, 100)
        self.assertAlmostEqual(slow.lower / scale, 1-math.sqrt(1-a), places=12)
        self.assertAlmostEqual(slow.upper / scale, math.sqrt(a), places=12)

    def test_bounded_history(self):
        a = 0.25
        horizon = 60.0
        b = 0.5
        scale = 0.791 * 80
        e = compartment_envelope(scale * a, 20, 80, history_minutes=horizon)
        self.assertAlmostEqual(e.lower / scale, (b+a)**3-b**3, places=11)
        self.assertAlmostEqual(e.upper / scale, 1-(1-a)**3, places=11)

    def test_arbitrary_profiles_inside_envelope(self):
        rng = random.Random(8319)
        n = 64
        for ht in (5, 20, 40, 60, 120, 480):
            r = 60 / ht
            for _ in range(30):
                z = [rng.random() for _ in range(n)]
                a = sum(z)/n
                y = sum(z[j] * (((j+1)/n)**r - (j/n)**r)
                        for j in range(n))
                scale = 0.791 * 100
                e = compartment_envelope(scale*a, ht, 100)
                self.assertLessEqual(e.lower, scale*y + 1e-9)
                self.assertGreaterEqual(e.upper, scale*y - 1e-9)

    def test_infeasible_or_bad_inputs(self):
        with self.assertRaises(ValueError):
            compartment_envelope(100, 60, 10)
        with self.assertRaises(ValueError):
            compartment_envelope(0.791 * 100 * 0.6, 60, 100,
                                 history_minutes=60)
        with self.assertRaises(ValueError):
            compartment_envelope(0, -1, 100)
        with self.assertRaises(ValueError):
            compartment_envelope(0, 60, float('nan'))


if __name__ == '__main__':
    unittest.main()
