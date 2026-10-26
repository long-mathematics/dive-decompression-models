"""Spencer--Huggins historical reconstruction and numerical audit.

Copyright 2026 Christopher D. Long. SPDX-License-Identifier: Apache-2.0
RESEARCH ONLY. NOT FOR DIVE PLANNING OR LIVE DIVE-COMPUTER USE.

The mathematical model and historical chart are deliberately separate APIs.
The chart preserves unexplained entries; it is not manufactured from the model.
All pressures are nitrogen partial pressures in fsw-equivalent units. Depth is
sea-water gauge depth, not absolute pressure. No water-vapor correction or
finite-rate travel is introduced into this square-exposure reconstruction.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction
from functools import lru_cache
import json
import math
from pathlib import Path
from typing import Sequence

HALF_TIMES = (5.0, 10.0, 20.0, 40.0, 80.0, 120.0)
M_VALUES = (102.0, 85.0, 67.5, 54.5, 47.5, 43.0)
GROUPS = "ABCDEFGHIJKLMN"
FRACTIONS = tuple(v / 100 for v in range(63, 100, 3)) + (1.0,)
SURFACE = 0.79 * 33.0
LN2 = math.log(2.0)
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "huggins_1981.json"


def nonnegative(value: float, name: str) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def group_index(group: str) -> int:
    if group not in GROUPS or len(group) != 1:
        raise ValueError("Group must be one letter A through N")
    return GROUPS.index(group)


def loadings(depth: float, minutes: float, *, literal_0693: bool = False) -> tuple[float, ...]:
    """Square exposure from surface equilibrium, with instantaneous travel.

    Default: exact half-time convention, 2**(-t/h). The paper displays 0.693;
    literal_0693=True computes that rounded constant literally for the audit.
    """
    nonnegative(depth, "depth"); nonnegative(minutes, "minutes")
    k = 0.693 if literal_0693 else LN2
    return tuple(SURFACE + 0.79 * depth * (-math.expm1(-k * minutes / h))
                 for h in HALF_TIMES)


def loading_decimal(depth: int, minutes: int, half_time: int,
                    *, literal_0693: bool = False) -> Decimal:
    """Independent 50-digit oracle; prevents binary 67.545 rounding artifacts."""
    with localcontext() as ctx:
        ctx.prec = 50
        f = Decimal('0.79'); h = Decimal(half_time); t = Decimal(minutes)
        exponent = -t / h
        decay = (Decimal('0.693') * exponent).exp() if literal_0693 else Decimal(2) ** exponent
        return f * Decimal(33) + f * Decimal(depth) * (1 - decay)


def rounded_pressure(value: Decimal) -> str:
    return str(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def threshold_components(depth: float, group: str) -> tuple[float, ...]:
    """Times each compartment reaches its group fraction; infinity if unreachable."""
    nonnegative(depth, "depth")
    alpha = FRACTIONS[group_index(group)]
    inspired = SURFACE + 0.79 * depth
    result = []
    for h, m in zip(HALF_TIMES, M_VALUES):
        target = alpha * m
        if target <= SURFACE:
            result.append(0.0)
        elif target >= inspired:
            result.append(math.inf)
        else:
            # log1p form is stable near a small loading threshold.
            result.append(h / LN2 * math.log1p((target - SURFACE) / (inspired - target)))
    return tuple(result)


def group_crossing(depth: float, group: str) -> float:
    """First time max_i P_i/M_i reaches this group's upper fraction."""
    return min(threshold_components(depth, group))


def analytic_surface_threshold(start: str, target: str) -> float:
    """Worst-case surface washout over the box P_i <= alpha_start*M_i.

    This is a derived model bound, not a claim about the historical calculator
    program. It does NOT reproduce the printed surface-interval numbers.
    """
    g, j = group_index(start), group_index(target)
    if j > g:
        raise ValueError("Target group cannot exceed starting group")
    if j == g:
        return 0.0
    upper, goal = FRACTIONS[g], FRACTIONS[j]
    return max(h / LN2 * math.log((upper*m-SURFACE)/(goal*m-SURFACE))
               for h, m in zip(HALF_TIMES, M_VALUES))


def ceil_candidate_rnt(depth: float, group: str) -> int | None:
    """Diagnostic candidate ceil(first crossing); NOT a universal safe RNT."""
    t = group_crossing(depth, group)
    return math.ceil(t) if math.isfinite(t) else None


class HistoricalChart:
    """Read-only source-preserving chart, with provenance in its JSON fixture.

    No arbitrary-profile or live-dive planner is supplied. The table's
    undocumented rules and unresolved entries are intentionally preserved.
    """
    def __init__(self, path: Path = FIXTURE):
        self.data = json.loads(path.read_text())

    def residual_nitrogen_time(self, depth: int, group: str) -> int | None:
        try:
            d = self.data['depths_fsw'].index(depth)
        except ValueError as exc:
            raise ValueError("Exact printed depth required; no interpolation") from exc
        return self.data['rnt_min'][group_index(group)][d]

    def surface_range(self, start: str, target: str) -> tuple[int, int]:
        g, j = group_index(start), group_index(target)
        if j > g:
            raise ValueError("Target group cannot exceed starting group")
        rows = self.data['surface_lower_min_by_destination']
        lower = rows[j][g-j]
        upper = self.data['surface_max_min'] if j == 0 else rows[j-1][g-j+1]-1
        return lower, upper


@lru_cache(maxsize=None)
def dyadic_decay_bounds(minutes: int, half_time: int, bits: int = 32) -> tuple[Fraction, Fraction]:
    """Exact rational enclosure of 2**(-minutes/half_time), by integer powers.

    Find floor(2**bits * 2**(-minutes/half_time)) without floating point.
    The comparison n**half_time <= 2**(bits*half_time-minutes) is exact.
    """
    if minutes < 0 or half_time <= 0 or bits <= 0:
        raise ValueError("Nonnegative integer time and positive integer half-time/bits required")
    denominator = 1 << bits
    exponent = bits*half_time-minutes
    if exponent < 0:
        return Fraction(0), Fraction(1, denominator)
    target = 1 << exponent
    lo, hi = 0, denominator+1
    while hi-lo > 1:
        mid = (lo+hi)//2
        if pow(mid, half_time) <= target:
            lo = mid
        else:
            hi = mid
    lower = Fraction(lo, denominator)
    if pow(lo, half_time) == target:
        return lower, lower
    return lower, Fraction(lo+1, denominator)


def certify_first_dive_surface_intervals() -> dict:
    """Exact-arithmetic certificate for charted first dives followed by one SI.

    A displayed end time upper-bounds all smaller times assigned that group.
    Loadings decrease throughout the surface interval. It suffices to test
    every displayed first-dive endpoint against each applicable SI lower bound.
    This does not certify repetitive dives, DCS risk, or a safe diving procedure.
    """
    chart = HistoricalChart(); checked=0; minimum=None; violations=[]
    surface=Fraction(2607,100); f=Fraction(79,100)
    for depth,row in zip(chart.data['depths_fsw'],chart.data['first_dive_cells']):
        for g,t in zip(GROUPS,row):
            if not isinstance(t,int): continue
            for j in GROUPS[:group_index(g)+1]:
                s,_=chart.surface_range(g,j)
                alpha=Fraction(chart.data['group_percentages'][group_index(j)],100)
                for half,m in zip(HALF_TIMES,M_VALUES):
                    # P_after = P_surface + f*d*(2**(-s/h)-2**(-(s+t)/h)).
                    _,up=dyadic_decay_bounds(s,int(half))
                    low,_=dyadic_decay_bounds(s+t,int(half))
                    upper_pressure=surface+f*depth*(up-low)
                    margin=alpha*Fraction(str(m))-upper_pressure
                    if minimum is None or margin<minimum: minimum=margin
                    if margin < 0: violations.append([depth,t,g,j,s,int(half),str(margin)])
                checked+=1
    return dict(profile_interval_combinations=checked, compartment_inequalities=6*checked,
                exact_rational_certified=not violations, violations=violations,
                minimum_margin_lower_bound_fsw=str(minimum),
                minimum_margin_lower_bound_decimal=float(minimum),
                enclosure_bits=32,
                scope='Square first-dive endpoints followed by one printed surface interval; not arbitrary repetitive histories or physiological validation.')


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    if not rows:
        raise ValueError("Cannot export an empty audit table")
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def audit(output_dir: Path | None = None) -> dict:
    """Audit every transcribed cell against an explicitly labeled candidate rule."""
    chart = HistoricalChart(); f = chart.data
    depths = f['depths_fsw']; limits = f['spencer_limits_min']
    pressure_rows = []; exact_rows = []; literal_matches = 0
    for n, (d, t) in enumerate(zip(depths[1:], limits[1:])):
        exact = []
        for i, h in enumerate(HALF_TIMES):
            p = loading_decimal(d, t, int(h)); exact.append(p)
            observed = f['table2_pressures_fsw'][n][i]
            rounded = rounded_pressure(p)
            literal = rounded_pressure(loading_decimal(d, t, int(h), literal_0693=True))
            literal_matches += Decimal(literal) == Decimal(str(observed))
            pressure_rows.append(dict(depth_fsw=d, exposure_min=t, half_time_min=int(h),
                printed_fsw=f'{observed:.2f}', calculated_fsw=str(p),
                rounded_half_up=rounded, literal_0693=literal,
                agrees=Decimal(rounded)==Decimal(str(observed))))
        exact_rows.append(exact)
    maxima = [max(row[i] for row in exact_rows) for i in range(6)]
    m = [float((p*2)//1/2) for p in maxima]
    first_rows = []; rnt_rows = []; si_rows = []; continuous_rows = []
    for d, limit, observed in zip(depths, limits, f['first_dive_cells']):
        for g, cell in zip(GROUPS, observed):
            crossing = group_crossing(d, g)
            numeric = isinstance(cell, (int, float))
            first_rows.append(dict(depth_fsw=d, group=g,
                printed_cell='' if cell is None else cell,
                source='Huggins 1987 p.99' if g in 'JK' else 'Huggins 1981 pp.2-3',
                continuous_crossing_min=crossing,
                satisfies_group_bound=(cell <= crossing+1e-10) if numeric else '',
                numeric=numeric))
            continuous_rows.append(dict(depth_fsw=d,group=g,crossing_min=crossing))
        for g in GROUPS:
            observed_rnt = chart.residual_nitrogen_time(d, g)
            candidate = ceil_candidate_rnt(d,g)
            rnt_rows.append(dict(depth_fsw=d,group=g,printed_rnt_min=observed_rnt,
                candidate_ceil_first_crossing_min=candidate,
                agrees=observed_rnt==candidate,
                source='Huggins 1981 p.3'))
    for g in GROUPS:
        for j in GROUPS[:group_index(g)+1]:
            low, high = chart.surface_range(g,j)
            analytic = analytic_surface_threshold(g,j)
            si_rows.append(dict(start_group=g,target_group=j,
                printed_lower_min=low,printed_upper_min=high,
                analytic_threshold_min=analytic,
                printed_minus_analytic_min=low-analytic,
                conservative_over_group_box=low+1e-10>=analytic,
                source='Huggins 1987 p.99' if g in 'JK' else 'Huggins 1981 pp.2-3'))
    discrepancies = {
        'pressure': [row for row in pressure_rows if not row['agrees']],
        'first_dive_group_bound': [row for row in first_rows if row['numeric'] and not row['satisfies_group_bound']],
        'rnt_candidate': [row for row in rnt_rows if not row['agrees']],
    }
    finite_rnt = [row for row in rnt_rows if row['printed_rnt_min'] is not None]
    numeric_first = [row for row in first_rows if row['numeric']]
    offdiag = [row for row in si_rows if row['start_group']!=row['target_group']]
    summary = dict(
        first_surface_certificate=certify_first_dive_surface_intervals(),
        pressure_cells=len(pressure_rows),
        pressure_matches=sum(row['agrees'] for row in pressure_rows),
        literal_0693_pressure_matches=literal_matches,
        calibrated_m0=m, published_m0=list(M_VALUES),
        m0_matches=sum(x==y for x,y in zip(m,M_VALUES)),
        first_dive_cells=len(first_rows), first_dive_numeric_cells=len(numeric_first),
        first_dive_numeric_satisfying_group_bound=sum(row['satisfies_group_bound'] for row in numeric_first),
        first_dive_numeric_matching_simple_floor=sum(
            row['printed_cell']==math.floor(row['continuous_crossing_min'])
            for row in numeric_first if math.isfinite(row['continuous_crossing_min'])),
        rnt_cells=len(rnt_rows),rnt_finite_cells=len(finite_rnt),
        rnt_candidate_matches=sum(row['agrees'] for row in rnt_rows),
        rnt_candidate_finite_matches=sum(row['agrees'] for row in finite_rnt),
        rnt_unexplained_candidates=discrepancies['rnt_candidate'],
        surface_ranges=len(si_rows), surface_transitions=len(offdiag),
        surface_conservative_transitions=sum(row['conservative_over_group_box'] for row in offdiag),
        surface_ceil_threshold_matches=sum(row['printed_lower_min']==math.ceil(row['analytic_threshold_min']) for row in offdiag),
        surface_extra_min=min(row['printed_minus_analytic_min'] for row in offdiag),
        surface_extra_max=max(row['printed_minus_analytic_min'] for row in offdiag),
        pressure_discrepancies=discrepancies['pressure'],
        first_dive_group_exceedances=discrepancies['first_dive_group_bound'],
        statement='Historical reconstruction with a discrepancy ledger, not complete recovery of the unpublished HP-67 program or physiological validation.'
    )
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        for name,rows in [('pressure_audit',pressure_rows),('first_dive_audit',first_rows),
                          ('rnt_audit',rnt_rows),('surface_interval_audit',si_rows),
                          ('continuous_thresholds',continuous_rows)]:
            write_csv(output_dir/f'{name}.csv',rows)
        (output_dir/'audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-dir', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.audit_dir),indent=2))


if __name__ == '__main__':
    main()
