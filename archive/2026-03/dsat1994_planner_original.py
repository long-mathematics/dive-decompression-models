
#!/usr/bin/env python3
"""
dsat1994_planner.py

A documented reconstruction of the *core* 1994 DSAT Recreational Dive Planner
(RDP) model from:

    Hamilton, R. W., Rogers, R. E., Powell, M. R., and Vann, R. D. (1994),
    Development and validation of no-stop decompression procedures for
    recreational diving: The DSAT Recreational Dive Planner.

What this program implements
----------------------------
1. Native imperial (fsw) first-dive no-stop curve:
       D - A = C * t^{-x}
   with A = 20.15 fsw, C = 803, x = 0.7476.
   See DSAT report, p. 20 (Table II and Eq. (4)).

2. The final 14 RDP half-times:
       5, 10, 20, 30, 40, 60, 80, 100, 120, 160, 200, 240, 360, 480 min.
   See DSAT report, pp. 20-21.

3. The final RDP M0 values (Table III, RDP column), in fsw-equivalent inert-gas
   pressure:
       99.08, 82.63, 66.89, 59.74, 55.73, 51.44, 49.21, 47.85,
       46.93, 45.78, 45.07, 44.60, 43.81, 43.40
   See DSAT report, p. 21.

4. Timed travel segments using Haldane / Schreiner updates, with the report's
   60 fsw/min descent/ascent convention where applicable.
   The report states that, when the RDP M0 values were calculated from the
   no-stop curve, the descent used was a timed descent at 60 fsw/min beginning
   at the beginning of bottom time; see p. 21.

5. The RDP repetitive-diving display layer based on the 60-minute compartment
   and 26 pressure groups A-Z; see p. 22.

6. The explicit multilevel restrictions from Table IV; see p. 22.

What this program does NOT claim
--------------------------------
- It does not reproduce every printed flat-table artifact exactly. The report is
  explicit about the native model and several display-layer rules, but the
  precise imperial/metric card artwork and every printed quantization artifact
  are a separate presentation layer.
- It does not compute altitude or flying-after-diving corrections. The report
  explicitly says the flat RDP does not calculate those directly; see p. 23.
- It is not a substitute for training, manufacturer validation, or medical
  judgment. It is a mathematical reconstruction for audit and study.

Design philosophy
-----------------
This file keeps two layers separate:

(A) Core model:
    - first-dive curve,
    - 14-compartment nitrogen-equivalent state propagation,
    - direct-ascent M0 check.

(B) RDP display/planning layer:
    - 60-minute pressure groups A-Z,
    - residual nitrogen time (RNT) from the 60-minute compartment,
    - Table IV multilevel guardrails.

Units
-----
All internal depths and pressures are in feet of seawater (fsw). Tissue tensions
are tracked as "fsw-equivalent nitrogen pressure" using the 79.1% nitrogen
convention noted on p. 21 of the DSAT report. We do NOT introduce an alveolar
water-vapour offset here because the report's explicit numerical distinction on
p. 21 is the 0.79 vs 0.791 inert-gas ratio issue, not a Bühlmann PH2O
adjustment.

Input convention
----------------
Dive level times are specified as *hold times at level*, excluding travel.
Travel between levels and to/from the surface is simulated explicitly at
60 fsw/min. This is the most transparent convention for a programmable planner.
For comparison to the report's first-dive curve and flat tables, note that the
report's discussion of bottom-time conventions on p. 21 arose in the
back-calculation of M0 values from the no-stop curve.

JSON profile format
-------------------
{
  "events": [
    {"type": "dive",
     "name": "Dive 1",
     "levels": [{"depth_fsw": 60, "time_min": 35}]},
    {"type": "surface_interval", "time_min": 75},
    {"type": "dive",
     "name": "Dive 2",
     "levels": [{"depth_fsw": 50, "time_min": 25}]}
  ]
}

CLI
---
python dsat1994_planner.py selftest
python dsat1994_planner.py plan profile.json
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Sequence

# ---------------------------------------------------------------------------
# Constants from the DSAT 1994 report
# ---------------------------------------------------------------------------

SURFACE_PRESSURE_FSW = 33.0
FN2 = 0.791  # DSAT report, p. 21: "modern perspective" / 79.1% nitrogen.

DESCENT_RATE_FSW_PER_MIN = 60.0
ASCENT_RATE_FSW_PER_MIN = 60.0

# First-dive no-stop curve, DSAT report, p. 20, Eq. (4).
CURVE_A_FSW = 20.15
CURVE_C = 803.0
CURVE_X = 0.7476

# Table II anchor values, DSAT report, p. 20.
TABLE_II_DEPTHS_FSW = [40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
TABLE_II_RDP_NDL_MIN = [140, 80, 55, 40, 30, 25, 20, 17, 14, 12]

# Final 14 half-times, DSAT report, pp. 20-21.
HALF_TIMES_MIN = [5, 10, 20, 30, 40, 60, 80, 100, 120, 160, 200, 240, 360, 480]

# Table III, RDP column, DSAT report, p. 21.
M0_RDP_FSW = [99.08, 82.63, 66.89, 59.74, 55.73, 51.44, 49.21,
              47.85, 46.93, 45.78, 45.07, 44.60, 43.81, 43.40]

# Table IV, DSAT report, p. 22. Keys are (lo, hi) ranges for the current level;
# value is the maximum allowable depth for the next level.
TABLE_IV_RULES = [
    ((120.0, 140.0), 80.0),
    ((95.0, 110.0), 70.0),
    ((80.0, 90.0), 60.0),
    ((65.0, 75.0), 50.0),
    ((50.0, 60.0), 40.0),
]

# 60-minute compartment chosen for repetitive-diving display, DSAT report, p. 22.
REPETITIVE_HALF_TIME_MIN = 60.0
REPETITIVE_INDEX = HALF_TIMES_MIN.index(60)

LN2 = math.log(2.0)
K_VALUES = [LN2 / ht for ht in HALF_TIMES_MIN]
K60 = LN2 / REPETITIVE_HALF_TIME_MIN

SURFACE_N2_FSW = FN2 * SURFACE_PRESSURE_FSW
MAX_EXCESS_60_FSW = M0_RDP_FSW[REPETITIVE_INDEX] - SURFACE_N2_FSW
GROUP_STEP_FSW = MAX_EXCESS_60_FSW / 26.0


def inspired_n2_fsw(depth_fsw: float) -> float:
    """Nitrogen-equivalent inspired pressure at constant depth, in fsw-equivalent."""
    return FN2 * (SURFACE_PRESSURE_FSW + depth_fsw)


def no_stop_curve_minutes(depth_fsw: float) -> float:
    """
    First-dive RDP no-stop curve from DSAT report p. 20:
        D - A = C t^{-x}
    """
    if depth_fsw <= CURVE_A_FSW:
        return math.inf
    return (CURVE_C / (depth_fsw - CURVE_A_FSW)) ** (1.0 / CURVE_X)


def haldane_update(p0: float, pi: float, k: float, t: float) -> float:
    """Constant-depth Haldane update."""
    if t <= 0.0:
        return p0
    return pi + (p0 - pi) * math.exp(-k * t)


def schreiner_update(p0: float, pi0: float, rate: float, k: float, t: float) -> float:
    """
    Schreiner equation for linearly changing inspired gas pressure:
        Pi(t) = pi0 + rate * t
    """
    if t <= 0.0:
        return p0
    return pi0 + rate * (t - 1.0 / k) - (pi0 - p0 - rate / k) * math.exp(-k * t)


def advance_hold(state: Sequence[float], depth_fsw: float, time_min: float) -> List[float]:
    """Advance the full 14-compartment state at constant depth."""
    pi = inspired_n2_fsw(depth_fsw)
    return [haldane_update(p, pi, k, time_min) for p, k in zip(state, K_VALUES)]


def advance_linear(state: Sequence[float],
                   start_depth_fsw: float,
                   end_depth_fsw: float,
                   rate_fsw_per_min: float = 60.0) -> List[float]:
    """
    Advance the full 14-compartment state along a linear depth change at fixed rate.
    Positive rate corresponds to increasing depth. Negative rate corresponds to ascent.
    """
    if math.isclose(start_depth_fsw, end_depth_fsw, abs_tol=1e-12):
        return list(state)
    direction = 1.0 if end_depth_fsw > start_depth_fsw else -1.0
    signed_rate_depth = direction * abs(rate_fsw_per_min)
    duration = abs(end_depth_fsw - start_depth_fsw) / abs(rate_fsw_per_min)
    pi0 = inspired_n2_fsw(start_depth_fsw)
    rate_n2 = FN2 * signed_rate_depth
    return [schreiner_update(p0, pi0, rate_n2, k, duration)
            for p0, k in zip(state, K_VALUES)]


def direct_ascent_surface_state(state_at_depth: Sequence[float], depth_fsw: float) -> List[float]:
    """Ascent to surface at the report's 60 fsw/min convention."""
    return advance_linear(state_at_depth, depth_fsw, 0.0, ASCENT_RATE_FSW_PER_MIN)


def no_stop_margin(state_at_surface: Sequence[float]) -> List[float]:
    """Positive margin means below the M0 limit on surfacing."""
    return [m - p for p, m in zip(state_at_surface, M0_RDP_FSW)]


def is_no_stop_surface_state(state_at_surface: Sequence[float]) -> bool:
    return all(p <= m + 1e-12 for p, m in zip(state_at_surface, M0_RDP_FSW))


def current_direct_ascent_ndl_minutes(state: Sequence[float], current_depth_fsw: float) -> float:
    """
    Additional dwell time available at the current depth before a direct 60 fsw/min
    ascent would first violate some M0 limit.
    """
    ascent_now = direct_ascent_surface_state(state, current_depth_fsw)
    if not is_no_stop_surface_state(ascent_now):
        return 0.0

    # Grow an upper bracket.
    lo = 0.0
    hi = 5.0
    while hi < 5000.0:
        mid_state = advance_hold(state, current_depth_fsw, hi)
        surf_state = direct_ascent_surface_state(mid_state, current_depth_fsw)
        if not is_no_stop_surface_state(surf_state):
            break
        lo = hi
        hi *= 2.0
    else:
        return math.inf

    # Binary search.
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        mid_state = advance_hold(state, current_depth_fsw, mid)
        surf_state = direct_ascent_surface_state(mid_state, current_depth_fsw)
        if is_no_stop_surface_state(surf_state):
            lo = mid
        else:
            hi = mid
    return lo


def pressure_group_index_from_state(state_at_surface: Sequence[float]) -> int:
    """
    RDP repetitive display layer, DSAT report p. 22:
    possible excess gas loading in the 60-minute compartment is divided evenly
    into 26 groups using the entire alphabet.

    We reconstruct the natural conservative map as:
        excess in (0, step]      -> A
        excess in (step, 2 step] -> B
        ...
        excess in (25 step, 26 step] -> Z
    and 0 if clean / below the first group.
    """
    excess = max(0.0, state_at_surface[REPETITIVE_INDEX] - SURFACE_N2_FSW)
    if excess <= 0.0:
        return 0
    idx = math.ceil(excess / GROUP_STEP_FSW - 1e-12)
    return max(0, min(26, idx))


def pressure_group_label(index: int) -> str:
    if index <= 0:
        return "-"
    return chr(ord("A") + index - 1)


def residual_nitrogen_time_minutes(state_at_surface: Sequence[float], next_depth_fsw: float) -> float:
    """
    RNT from the 60-minute compartment. This is the natural one-compartment
    equivalent-time construction described in the report's repetitive-diving
    section (p. 22): convert the residual 60-minute loading at the start of the
    repetitive dive into an equivalent penalty time at the next depth.

    The equation is the constant-depth Haldane inverse:
        P_res = Pi + (P_surf - Pi) e^{-k t}
    solved for t.
    """
    pres = state_at_surface[REPETITIVE_INDEX]
    pi = inspired_n2_fsw(next_depth_fsw)
    if pres <= SURFACE_N2_FSW + 1e-12:
        return 0.0
    if pres >= pi - 1e-12:
        return math.inf
    return -(1.0 / K60) * math.log((pi - pres) / (pi - SURFACE_N2_FSW))


def next_level_max_depth_fsw(current_level_depth_fsw: float) -> Optional[float]:
    """
    Table IV guardrail, DSAT report p. 22.
    Returns None if the report does not give an explicit next-level limit for this range.
    """
    for (lo, hi), mx in TABLE_IV_RULES:
        if lo <= current_level_depth_fsw <= hi:
            return mx
    return None


@dataclass
class Level:
    depth_fsw: float
    time_min: float  # dwell time at level, excluding travel


@dataclass
class DiveResult:
    name: str
    levels: List[Level]
    start_pg: str
    end_pg: str
    end_state_surface: List[float]
    violated_no_stop: bool
    controlling_compartment: Optional[int]
    max_over_m0_fsw: float
    notes: List[str] = field(default_factory=list)
    per_level_report: List[dict] = field(default_factory=list)


def clean_surface_state() -> List[float]:
    return [SURFACE_N2_FSW for _ in HALF_TIMES_MIN]


def execute_dive(levels: Sequence[Level],
                 start_state_surface: Sequence[float],
                 name: str = "Dive") -> DiveResult:
    """
    Execute a dive with one or more levels.

    Times at level exclude travel. Travel is simulated explicitly at 60 fsw/min.
    """
    if not levels:
        raise ValueError("Dive must contain at least one level.")

    state = list(start_state_surface)
    current_depth = 0.0
    notes: List[str] = []
    per_level_report: List[dict] = []

    start_pg_idx = pressure_group_index_from_state(start_state_surface)
    start_pg = pressure_group_label(start_pg_idx)

    # Report-table view for the first level only.
    first_depth = levels[0].depth_fsw
    first_curve_ndl = no_stop_curve_minutes(first_depth)
    first_rnt = residual_nitrogen_time_minutes(start_state_surface, first_depth)
    first_adjusted_table_time = first_curve_ndl - first_rnt if math.isfinite(first_rnt) else -math.inf

    if first_adjusted_table_time < 0:
        notes.append("RDP repetitive-layer adjusted available time at first level is already exhausted.")

    for j, level in enumerate(levels):
        if level.depth_fsw < 0 or level.time_min < 0:
            raise ValueError("Depths and times must be nonnegative.")

        # Multilevel guardrail from Table IV for every level after the first.
        if j >= 1:
            prev_depth = levels[j - 1].depth_fsw
            max_next = next_level_max_depth_fsw(prev_depth)
            if level.depth_fsw >= prev_depth - 1e-12:
                notes.append(
                    f"Level {j+1}: report requires each subsequent level to be shallower than the previous one."
                )
            if max_next is not None and level.depth_fsw > max_next + 1e-12:
                notes.append(
                    f"Level {j+1}: Table IV maximum next-level depth after {prev_depth:.1f} fsw is {max_next:.1f} fsw."
                )
            if level.time_min < 5.0 - 1e-12:
                notes.append(
                    f"Level {j+1}: report says calculations provide at least 5 minutes at any subsequent level."
                )

        # Travel to this level.
        state = advance_linear(state, current_depth, level.depth_fsw, DESCENT_RATE_FSW_PER_MIN)
        current_depth = level.depth_fsw

        ndl_remaining = current_direct_ascent_ndl_minutes(state, current_depth)

        per_level_report.append({
            "level": j + 1,
            "depth_fsw": current_depth,
            "planned_hold_min": level.time_min,
            "direct_ascent_ndl_remaining_min_at_level_start": ndl_remaining,
        })

        # Hold at the level.
        state = advance_hold(state, current_depth, level.time_min)

    # Ascend to surface at the report's 60 fsw/min convention.
    state_surface = direct_ascent_surface_state(state, current_depth)
    margins = no_stop_margin(state_surface)
    violated = not all(m >= -1e-12 for m in margins)
    max_over = max(0.0, max(-m for m in margins))
    ctrl = None
    if margins:
        ctrl = 1 + min(range(len(margins)), key=lambda i: margins[i])

    end_pg_idx = pressure_group_index_from_state(state_surface)
    end_pg = pressure_group_label(end_pg_idx)

    # Safety-stop advisory from p. 23.
    if any(level.depth_fsw >= 100.0 - 1e-12 for level in levels):
        notes.append("Safety-stop advisory: report calls for 3 min at 15 fsw for any dive to 100 fsw or greater.")

    # Conservative proximity-to-limit proxy using end pressure group.
    if end_pg_idx >= 24:  # X, Y, Z
        notes.append("Safety-stop advisory: end pressure group is within 3 groups of Z (report, p. 23).")

    if violated:
        notes.append(
            "Direct ascent at 60 fsw/min violates at least one Table III M0 limit; report-style emergency-stop guidance applies."
        )

    notes.insert(
        0,
        f"First-level table layer: curve NDL at {first_depth:.1f} fsw = {first_curve_ndl:.2f} min; "
        f"RNT from current 60-min state = {first_rnt:.2f} min; "
        f"adjusted available table time = {first_adjusted_table_time:.2f} min."
    )

    return DiveResult(
        name=name,
        levels=list(levels),
        start_pg=start_pg,
        end_pg=end_pg,
        end_state_surface=state_surface,
        violated_no_stop=violated,
        controlling_compartment=ctrl,
        max_over_m0_fsw=max_over,
        notes=notes,
        per_level_report=per_level_report,
    )


def surface_interval(state_surface: Sequence[float], time_min: float) -> List[float]:
    """Surface interval at 0 fsw."""
    return advance_hold(state_surface, 0.0, time_min)


def summarize_state(state_surface: Sequence[float]) -> dict:
    pg_idx = pressure_group_index_from_state(state_surface)
    return {
        "pressure_group": pressure_group_label(pg_idx),
        "pressure_group_index": pg_idx,
        "tension_60_fsw": state_surface[REPETITIVE_INDEX],
        "excess_60_fsw": max(0.0, state_surface[REPETITIVE_INDEX] - SURFACE_N2_FSW),
    }


def run_profile(events: Sequence[dict]) -> dict:
    """
    Run a multi-event profile consisting of dives and surface intervals.
    """
    state = clean_surface_state()
    reports = []
    depth_current = 0.0
    if depth_current != 0.0:
        raise RuntimeError("Internal error: profile must start at surface.")

    for idx, event in enumerate(events, start=1):
        etype = event["type"]
        if etype == "surface_interval":
            minutes = float(event["time_min"])
            state = surface_interval(state, minutes)
            reports.append({
                "event_index": idx,
                "type": "surface_interval",
                "time_min": minutes,
                "summary": summarize_state(state),
            })
        elif etype == "dive":
            name = event.get("name", f"Dive {idx}")
            levels = [Level(float(x["depth_fsw"]), float(x["time_min"])) for x in event["levels"]]
            result = execute_dive(levels, state, name=name)
            state = result.end_state_surface
            reports.append({
                "event_index": idx,
                "type": "dive",
                "name": result.name,
                "start_pg": result.start_pg,
                "end_pg": result.end_pg,
                "violated_no_stop": result.violated_no_stop,
                "controlling_compartment": result.controlling_compartment,
                "max_over_m0_fsw": result.max_over_m0_fsw,
                "per_level_report": result.per_level_report,
                "notes": result.notes,
                "summary": summarize_state(state),
            })
        else:
            raise ValueError(f"Unknown event type: {etype}")

    return {"final_state_summary": summarize_state(state), "reports": reports}


def selftest() -> str:
    """
    Diagnostic report:
    1. Compare the no-stop curve with Table II anchors.
    2. Compare the direct-ascent 14-compartment clean-dive NDLs with the curve.
    """
    lines: List[str] = []

    lines.append("DSAT 1994 self-test")
    lines.append("=" * 72)
    lines.append("Table II comparison (curve vs printed anchor values)")
    lines.append("Depth  TableII  Curve    Error")
    total_abs = 0.0
    worst = 0.0
    for d, ttab in zip(TABLE_II_DEPTHS_FSW, TABLE_II_RDP_NDL_MIN):
        tcurve = no_stop_curve_minutes(d)
        err = tcurve - ttab
        total_abs += abs(err)
        worst = max(worst, abs(err))
        lines.append(f"{d:>5.0f}  {ttab:>7.2f}  {tcurve:>7.2f}  {err:>+7.2f}")
    mae = total_abs / len(TABLE_II_DEPTHS_FSW)
    lines.append(f"Mean abs error = {mae:.3f} min")
    lines.append(f"Worst abs error = {worst:.3f} min")
    lines.append("")

    lines.append("Clean-dive direct-ascent 14-compartment NDL at Table II depths")
    lines.append("Depth  Curve    14-comp")
    for d in TABLE_II_DEPTHS_FSW:
        state = clean_surface_state()
        ndl = current_direct_ascent_ndl_minutes(
            advance_linear(state, 0.0, d, DESCENT_RATE_FSW_PER_MIN),
            d,
        )
        tcurve = no_stop_curve_minutes(d)
        lines.append(f"{d:>5.0f}  {tcurve:>7.2f}  {ndl:>7.2f}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconstructed DSAT 1994 RDP planner.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("selftest", help="Run built-in diagnostics against report tables.")

    p_plan = sub.add_parser("plan", help="Run a profile from a JSON file.")
    p_plan.add_argument("json_file", type=str, help="Path to JSON profile.")

    args = parser.parse_args()

    if args.cmd == "selftest":
        print(selftest())
    elif args.cmd == "plan":
        path = Path(args.json_file)
        data = json.loads(path.read_text())
        result = run_profile(data["events"])
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()