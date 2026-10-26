"""Sharp Haldane compartment envelopes from one observed excess loading.

Mathematical research only; not a dive-planning or safety algorithm.
The model assumes a nonnegative bounded depth history, constant inert-gas
fraction, initially equilibrated compartments, and linear Haldane kinetics.
"""
from __future__ import annotations

import math
from typing import NamedTuple


class LoadingEnvelope(NamedTuple):
    lower: float
    upper: float


def compartment_envelope(
    reference_excess: float,
    target_half_time_min: float,
    max_depth_fsw: float,
    *,
    reference_half_time_min: float = 60.0,
    inert_fraction: float = 0.791,
    history_minutes: float | None = None,
) -> LoadingEnvelope:
    """Return sharp possible *excess* target pressure bounds (fsw-equivalent).

    `reference_excess` is the observed excess in the reference compartment
    beyond equilibrium at the current surface pressure; depths are gauge fsw.
    If `history_minutes` is provided, depth was zero before that horizon.
    Otherwise an arbitrarily long bounded measurable history is permitted.

    This optimizes over all histories 0 <= depth(t) <= max_depth_fsw,
    allowing instantaneous depth transitions. Rate bounds change extrema.
    """
    values = (reference_excess, target_half_time_min, max_depth_fsw,
              reference_half_time_min, inert_fraction)
    if not all(math.isfinite(x) for x in values):
        raise ValueError("All numerical inputs must be finite")
    if reference_excess < 0 or target_half_time_min <= 0 or max_depth_fsw < 0:
        raise ValueError("Excess/depth must be nonnegative and half-times positive")
    if reference_half_time_min <= 0 or not (0 < inert_fraction <= 1):
        raise ValueError("Invalid reference half-time or inert fraction")
    if history_minutes is not None and (
        not math.isfinite(history_minutes) or history_minutes < 0
    ):
        raise ValueError("History duration must be finite and nonnegative")
    scale = inert_fraction * max_depth_fsw
    if scale == 0:
        if reference_excess != 0:
            raise ValueError("Positive loading impossible when maximum depth is zero")
        return LoadingEnvelope(0.0, 0.0)
    a = reference_excess / scale
    k0 = math.log(2.0) / reference_half_time_min
    b = math.exp(-k0 * history_minutes) if history_minutes is not None else 0.0
    if a < 0 or a > 1 - b + 1e-12:
        raise ValueError("Observed excess is infeasible under history bound")
    a = min(a, 1 - b)
    r = reference_half_time_min / target_half_time_min

    # Exposure concentrated at most recent times: largest exponential weights.
    recent = 1.0 if a == 1.0 else -math.expm1(r * math.log1p(-a))
    # Exposure concentrated in the oldest portion of the allowed history.
    old = (b + a) ** r - b ** r
    return LoadingEnvelope(scale * min(recent, old), scale * max(recent, old))
