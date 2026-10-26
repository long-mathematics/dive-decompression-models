"""Numerical and transcription tests, not physiological validation.
SPDX-License-Identifier: Apache-2.0
"""
import math
import random
import unittest
from decimal import Decimal
from models.huggins_1981 import huggins as h


class HugginsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart = h.HistoricalChart()
        cls.report = h.audit()

    def test_surface_equilibrium(self):
        self.assertEqual(h.loadings(0, 500), (h.SURFACE,)*6)
        self.assertEqual(h.loadings(90, 0), (h.SURFACE,)*6)

    def test_half_time(self):
        for i, half in enumerate(h.HALF_TIMES):
            self.assertAlmostEqual(h.loadings(40, half)[i], h.SURFACE+0.79*40/2)

    def test_independent_decimal_loading_oracle(self):
        for d,t in zip(self.chart.data['depths_fsw'][1:],self.chart.data['spencer_limits_min'][1:]):
            for i,half in enumerate(h.HALF_TIMES):
                self.assertAlmostEqual(h.loadings(d,t)[i],float(h.loading_decimal(d,t,int(half))),places=11)

    def test_exact_halfway_rounding(self):
        p=h.loading_decimal(70,40,20)
        self.assertEqual(p,Decimal('67.545'))
        self.assertEqual(h.rounded_pressure(p),'67.55')

    def test_calibration_and_two_preserved_discrepancies(self):
        self.assertEqual(self.report['m0_matches'],6)
        self.assertEqual(self.report['pressure_matches'],70)
        self.assertEqual([(x['depth_fsw'],x['half_time_min']) for x in self.report['pressure_discrepancies']],[(35,40),(60,120)])
        self.assertEqual(self.chart.data['table2_pressures_fsw'][1][3],52.41)
        self.assertEqual(self.chart.data['table2_pressures_fsw'][4][5],39.96)

    def test_literal_printed_constant_is_not_silently_substituted(self):
        self.assertEqual(self.report['literal_0693_pressure_matches'],49)

    def test_inverse_against_independent_bisection(self):
        rng=random.Random(1981)
        for _ in range(200):
            d=rng.uniform(25,130); group=rng.choice(h.GROUPS)
            alpha=h.FRACTIONS[h.group_index(group)]
            limit=h.group_crossing(d,group)
            if not math.isfinite(limit):
                self.assertLessEqual(max((h.SURFACE+0.79*d)/m for m in h.M_VALUES),alpha)
                continue
            lo,hi=0.0,1.0
            def reaches(t):
                return max(p/m for p,m in zip(h.loadings(d,t),h.M_VALUES))>=alpha
            while not reaches(hi): hi*=2
            for _ in range(70):
                mid=(lo+hi)/2
                if reaches(mid):hi=mid
                else:lo=mid
            self.assertAlmostEqual(limit,(hi+lo)/2,delta=1e-8)

    def test_all_six_fixed_compartments_are_active(self):
        observed={min(range(6),key=lambda i:h.threshold_components(d,'N')[i])
                  for d in (30,40,50,70,100,110)}
        self.assertEqual(observed,set(range(6)))

    def test_seven_empirical_endpoints_exceed_rounded_limits(self):
        self.assertEqual(self.report['first_dive_numeric_cells'],127)
        self.assertEqual(self.report['first_dive_numeric_satisfying_group_bound'],120)
        self.assertEqual({x['group'] for x in self.report['first_dive_group_exceedances']},{'N'})

    def test_rnt_is_not_overclaimed(self):
        self.assertEqual(self.report['rnt_finite_cells'],179)
        self.assertEqual(self.report['rnt_candidate_finite_matches'],169)
        self.assertEqual(self.chart.residual_nitrogen_time(110,'A'),2)
        self.assertEqual(h.ceil_candidate_rnt(110,'A'),3)
        self.assertIsNone(self.chart.residual_nitrogen_time(20,'L'))
        self.assertEqual(h.ceil_candidate_rnt(20,'L'),570)

    def test_historical_surface_ranges_partition_integer_minutes(self):
        for g in h.GROUPS:
            last=9
            for j in reversed(h.GROUPS[:h.group_index(g)+1]):
                lo,hi=self.chart.surface_range(g,j)
                self.assertEqual(lo,last+1)
                self.assertGreaterEqual(hi,lo)
                last=hi
            self.assertEqual(last,720)

    def test_surface_bounds_and_all_printed_transition_margins(self):
        self.assertEqual(self.report['surface_conservative_transitions'],91)
        self.assertEqual(self.report['surface_ceil_threshold_matches'],0)
        for g in h.GROUPS:
            for j in h.GROUPS[:h.group_index(g)]:
                s=h.analytic_surface_threshold(g,j)
                for half,m in zip(h.HALF_TIMES,h.M_VALUES):
                    p=h.SURFACE+(h.FRACTIONS[h.group_index(g)]*m-h.SURFACE)*2**(-s/half)
                    self.assertLessEqual(p,h.FRACTIONS[h.group_index(j)]*m+1e-10)

    def test_surface_closed_form_matches_120_minute_compartment(self):
        for g in h.GROUPS[1:]:
            for j in h.GROUPS[:h.group_index(g)]:
                expected=120*math.log2((h.FRACTIONS[h.group_index(g)]*43-h.SURFACE)/
                                       (h.FRACTIONS[h.group_index(j)]*43-h.SURFACE))
                self.assertAlmostEqual(h.analytic_surface_threshold(g,j),expected,places=10)

    def test_exact_rational_first_surface_certificate(self):
        cert=self.report['first_surface_certificate']
        self.assertEqual(cert['profile_interval_combinations'],998)
        self.assertEqual(cert['compartment_inequalities'],5988)
        self.assertTrue(cert['exact_rational_certified'])
        self.assertGreater(cert['minimum_margin_lower_bound_decimal'],0.0606)

    def test_invalid_inputs(self):
        for bad in (-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): h.loadings(bad,20)
            with self.assertRaises(ValueError): h.loadings(20,bad)
        for bad in ('','AA','O','a'):
            with self.assertRaises(ValueError): h.group_index(bad)
        with self.assertRaises(ValueError): self.chart.residual_nitrogen_time(42,'B')
        with self.assertRaises(ValueError): h.analytic_surface_threshold('A','N')

if __name__=='__main__': unittest.main()
