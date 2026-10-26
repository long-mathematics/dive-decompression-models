#!/usr/bin/env python3
"""Continuous DSAT/PADI-style no-stop calculator.

This script separates two layers that are easy to conflate:

1. The *published first-dive no-stop curve* used to generate the RDP.
   In the 1994 DSAT report, Rogers describes the RDP no-stop limits via a
   fitted curve with a shallow asymptote. The 14-compartment M0 values were
   then back-calculated from that curve.

2. A 14-compartment *shadow model* using the RDP half-times and timed-descent
   M0 values from Table III. This is useful diagnostically, especially for
   identifying the controlling compartment, but it is not the primary object
   that originally generated the first-dive table.

So, by default, this script reports the continuous first-dive PADI/DSAT NDL
from the no-stop curve, and also reports the 14-compartment shadow-model NDL.

Notes
-----
* Depth input is in metres seawater.
* The special metric-table issue is handled: if the nominal depth entered is
  exactly 10.0 m, it is treated as 10.5 m actual pressure depth unless
  disabled.
* This script intentionally does NOT hardcode the table or its depth/time bins.
* Repetitive-dive groups, multilevel wheel logic, and altitude corrections are
  documented in the DSAT report, but are not implemented here because the
  original script only computed first-dive NDLs and the uploaded references do
  not fully specify all of the display-layer/grouping rules.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable, List, Optional

# ---- DSAT/PADI first-dive no-stop curve (Hamilton/Rogers/Powell/Vann, 1994) ----
# Equation on the no-stop-limits page: D - A = C * t^(-x), with D in fsw.
# Constants read from the report.
SHALLOW_ASYMPTOTE_FSW = 20.15
CURVE_C = 803.0
CURVE_X = 0.7476

# ---- 14-compartment shadow model (same report, Table III) ----
HALF_TIMES_MIN = [5, 10, 20, 30, 40, 60, 80, 100, 120, 160, 200, 240, 360, 480]
# Timed-descent RDP M0 values from Table III, in fsw.
M0_RDP_FSW = [99.08, 82.63, 66.89, 59.74, 55.73, 51.44, 49.21,
              47.85, 46.93, 45.78, 45.07, 44.60, 43.81, 43.40]

# Physics / convention constants used in the modern inert-gas formulation.
SURFACE_PRESSURE_MSW = 10.0      # 1 ata approximated as 10 msw
WATER_VAPOR_MSW = 0.627          # Buhlmann-style water vapour correction in msw
FN2_AIR = 0.791                  # modern nitrogen fraction noted in the DSAT report
DESCENT_RATE_M_PER_MIN = 18.0    # 60 fsw/min
MSW_PER_FSW = 10.0 / 33.0
FSW_PER_MSW = 33.0 / 10.0


def msw_to_fsw(depth_m: float) -> float:
    return depth_m * FSW_PER_MSW


def fsw_to_msw(depth_fsw: float) -> float:
    return depth_fsw * MSW_PER_FSW


def effective_metric_depth(depth_m: float, use_metric_10m_actual: bool = True) -> float:
    """Treat the nominal 10 m metric RDP column as 10.5 m actual pressure depth."""
    if use_metric_10m_actual and math.isclose(depth_m, 10.0, abs_tol=1e-12):
        return 10.5
    return depth_m


def padi_curve_ndl_minutes(depth_m: float, use_metric_10m_actual: bool = True) -> float:
    """Continuous first-dive RDP no-stop time from the DSAT curve."""
    actual_m = effective_metric_depth(depth_m, use_metric_10m_actual)
    depth_fsw = msw_to_fsw(actual_m)
    if depth_fsw <= SHALLOW_ASYMPTOTE_FSW:
        return math.inf
    return (CURVE_C / (depth_fsw - SHALLOW_ASYMPTOTE_FSW)) ** (1.0 / CURVE_X)


@dataclass(frozen=True)
class ShadowResult:
    ndl_minutes: float
    controlling_compartment: int
    controlling_half_time_min: float
    controlling_m0_msw: float
    actual_depth_m: float
    descent_time_min: float
    tissue_pressures_end_descent_msw: List[float]
    per_compartment_total_times_min: List[float]


# Schreiner equation for linearly changing inspired inert-gas pressure.
def schreiner(pt0: float, pi0: float, rate: float, k: float, t: float) -> float:
    return pi0 + rate * (t - 1.0 / k) - (pi0 - pt0 - rate / k) * math.exp(-k * t)


# Surface-equilibrated nitrogen compartment pressure on a first dive of the day.
def surface_equilibrium_n2_msw() -> float:
    return (SURFACE_PRESSURE_MSW - WATER_VAPOR_MSW) * FN2_AIR


def inspired_n2_at_depth_msw(depth_m: float) -> float:
    return (SURFACE_PRESSURE_MSW + depth_m - WATER_VAPOR_MSW) * FN2_AIR


def shadow_m0_msw_values() -> List[float]:
    return [fsw_to_msw(x) for x in M0_RDP_FSW]


def shadow_14_compartment_ndl(depth_m: float,
                              use_metric_10m_actual: bool = True) -> ShadowResult:
    """14-compartment timed-descent NDL using the RDP Table III M0 values.

    This is a shadow/diagnostic model. It is *not* the original no-stop curve
    generator; the M0 values were back-calculated from that curve.
    """
    actual_m = effective_metric_depth(depth_m, use_metric_10m_actual)
    t_desc = actual_m / DESCENT_RATE_M_PER_MIN
    pi_surface = surface_equilibrium_n2_msw()
    pi_bottom = inspired_n2_at_depth_msw(actual_m)
    rate = FN2_AIR * DESCENT_RATE_M_PER_MIN

    end_descent_pressures: List[float] = []
    total_times: List[float] = []
    m0_vals = shadow_m0_msw_values()

    for ht, m0 in zip(HALF_TIMES_MIN, m0_vals):
        k = math.log(2.0) / ht
        pt_desc = schreiner(pi_surface, pi_surface, rate, k, t_desc)
        end_descent_pressures.append(pt_desc)

        # Sport-diving on-gassing case: Pi > M0 > current tissue pressure.
        if pi_bottom > m0 > pt_desc:
            tau = -(1.0 / k) * math.log((pi_bottom - m0) / (pi_bottom - pt_desc))
            total_times.append(t_desc + tau)
        elif m0 <= pt_desc:
            # Already at or beyond the compartment's surfacing limit.
            total_times.append(0.0)
        else:
            # This compartment never controls at this depth.
            total_times.append(math.inf)

    ndl = min(total_times)
    idx = total_times.index(ndl)

    return ShadowResult(
        ndl_minutes=ndl,
        controlling_compartment=idx + 1,
        controlling_half_time_min=HALF_TIMES_MIN[idx],
        controlling_m0_msw=m0_vals[idx],
        actual_depth_m=actual_m,
        descent_time_min=t_desc,
        tissue_pressures_end_descent_msw=end_descent_pressures,
        per_compartment_total_times_min=total_times,
    )


def legacy_square_ndl(depth_m: float) -> ShadowResult:
    """Original uploaded code, but with inf instead of 1000.

    This keeps the original simplifications:
    * instantaneous descent,
    * no water-vapour correction,
    * FN2 = 0.79,
    * legacy M0 values already stored in msw.
    """
    legacy_m0 = [30.42, 25.37, 20.54, 18.34, 17.11, 15.79, 15.11,
                 14.69, 14.41, 14.06, 13.84, 13.69, 13.45, 13.33]
    pi_surface = 0.79 * SURFACE_PRESSURE_MSW
    pi_bottom = 0.79 * (SURFACE_PRESSURE_MSW + depth_m)

    total_times: List[float] = []
    for ht, m0 in zip(HALF_TIMES_MIN, legacy_m0):
        if pi_bottom > m0 > pi_surface:
            total_times.append(ht * math.log2((pi_bottom - pi_surface) / (pi_bottom - m0)))
        else:
            total_times.append(math.inf)

    ndl = min(total_times)
    idx = total_times.index(ndl)
    return ShadowResult(
        ndl_minutes=ndl,
        controlling_compartment=idx + 1,
        controlling_half_time_min=HALF_TIMES_MIN[idx],
        controlling_m0_msw=legacy_m0[idx],
        actual_depth_m=depth_m,
        descent_time_min=0.0,
        tissue_pressures_end_descent_msw=[pi_surface] * len(HALF_TIMES_MIN),
        per_compartment_total_times_min=total_times,
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Continuous DSAT/PADI-style no-stop calculator")
    p.add_argument("depth", type=float, help="Depth in metres seawater")
    p.add_argument("--no-10p5", action="store_true",
                   help="Do not treat the nominal 10 m metric column as 10.5 m actual")
    p.add_argument("--mode", choices=["padi", "shadow14", "legacy"], default="padi",
                   help=("padi = first-dive continuous no-stop curve (default); "
                         "shadow14 = 14-compartment timed-descent diagnostic model; "
                         "legacy = original uploaded square-profile model"))
    p.add_argument("--verbose", action="store_true", help="Show extra diagnostics")
    return p


def main() -> None:
    args = build_parser().parse_args()
    use_10p5 = not args.no_10p5

    if args.mode == "padi":
        ndl = padi_curve_ndl_minutes(args.depth, use_metric_10m_actual=use_10p5)
        shadow = shadow_14_compartment_ndl(args.depth, use_metric_10m_actual=use_10p5)
        actual_m = effective_metric_depth(args.depth, use_metric_10m_actual=use_10p5)

        print(f"Depth label (m): {args.depth:.3f}")
        print(f"Actual model depth (m): {actual_m:.3f}")
        print(f"PADI continuous NDL (min): {ndl:.6f}")
        print(f"Shadow 14-comp NDL (min): {shadow.ndl_minutes:.6f}")
        print(f"Shadow controlling compartment: {shadow.controlling_compartment}")
        print(f"Shadow controlling half-time (min): {shadow.controlling_half_time_min}")
        print(f"Shadow controlling M0 (msw): {shadow.controlling_m0_msw:.6f}")
        if args.verbose:
            print(f"Descent time included in shadow model (min): {shadow.descent_time_min:.6f}")
            print("Per-compartment shadow NDLs (min):")
            for i, (ht, t) in enumerate(zip(HALF_TIMES_MIN, shadow.per_compartment_total_times_min), start=1):
                val = f"{t:.6f}" if math.isfinite(t) else "inf"
                print(f"  {i:2d}  ht={ht:>3}  total={val}")

    elif args.mode == "shadow14":
        shadow = shadow_14_compartment_ndl(args.depth, use_metric_10m_actual=use_10p5)
        print(f"Depth label (m): {args.depth:.3f}")
        print(f"Actual model depth (m): {shadow.actual_depth_m:.3f}")
        print(f"14-compartment timed-descent NDL (min): {shadow.ndl_minutes:.6f}")
        print(f"Controlling compartment: {shadow.controlling_compartment}")
        print(f"Controlling half-time (min): {shadow.controlling_half_time_min}")
        print(f"Controlling M0 (msw): {shadow.controlling_m0_msw:.6f}")
        if args.verbose:
            print(f"Descent time (min): {shadow.descent_time_min:.6f}")
            print("Per-compartment total times (min):")
            for i, (ht, t, p_end) in enumerate(zip(HALF_TIMES_MIN,
                                                   shadow.per_compartment_total_times_min,
                                                   shadow.tissue_pressures_end_descent_msw), start=1):
                val = f"{t:.6f}" if math.isfinite(t) else "inf"
                print(f"  {i:2d}  ht={ht:>3}  end_descent={p_end:.6f}  total={val}")

    else:
        legacy = legacy_square_ndl(args.depth)
        print(f"Legacy square-profile NDL (min): {legacy.ndl_minutes:.6f}")
        print(f"Controlling compartment: {legacy.controlling_compartment}")
        print(f"Controlling half-time (min): {legacy.controlling_half_time_min}")
        print(f"Controlling M0 (msw): {legacy.controlling_m0_msw:.6f}")


if __name__ == "__main__":
    main()