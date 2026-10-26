# Research roadmap

Five standing objectives. A reconstructed historical table is **not** evidence of physiological safety.

## I. Reconstruct published tables

Reproduce versioned PADI/DSAT, Bühlmann ZH-L16, U.S. Navy, NOAA, MN90, DCIEM, BSAC, NAUI, and other important models. Preserve original published entries as fixtures where redistribution permits. Log actual deviations, rounding conventions, ascent assumptions, gas fractions, pressure units, surface intervals, and multilevel behavior.

**Completion criterion for each edition:** public source and exact version identified; parameters transcribed; tests against individual cells and whole tables; reproducible discrepancy report; unknown/proprietary rules explicitly documented.

## II. Minimum compartment complexity

For each finite table, investigate the smallest number of exponential compartments sufficient to reproduce the table to an agreed tolerance, initially **±1 minute** at specified depths. Examine both exact and rounded tables, and extend to repetitive/multilevel profiles.

**Research questions:** uniqueness, identifiability, constructive upper bounds, certified lower bounds, and the impact of additional profile families. A table-equivalent reduced model is not physiologically interchangeable.

## III. Improved probabilistic decompression models

Study independent calibration against DCS and venous-gas-embolism observations. Distinguish outcome definitions, participants, pressure profiles, bubbles, and follow-up times. Quantify uncertainty, nonindependence across dives, covariates, missingness, selection effects, and dataset overlap. Reserve held-out cohorts for external validation.

**Criterion:** reproducible predictive comparisons; no claim of superior safety without appropriate evidence.

## IV. Correct and independently testable software

Maintain an explicit model registry, unit-aware parameters, transparent numerical core, property tests, regression fixtures, and reproducible benchmark outputs. Separate continuous compartment kinetics, published table display logic, risk estimation, and operational constraints.

Use analytic threshold calculations when available. Explicitly reject invalid inputs and mark unsupported features. **Research implementation only; never treat tests as a certified dive computer.**

## V. Robust inference from incomplete dive histories

Given observed compartment loadings, maximum depths, partial profile samples, pressure groups, and uncertainty bounds, derive **sharp** envelopes for all feasible tissue states.

Initial theorem: exponential-kernel rearrangement bounds for one reference compartment, with finite-horizon variant. Next: ascent/descent rate constraints; intermittent measurements; inert-gas changes; multiple known compartments; inverse identification and computational certificates.

## Immediate milestones

1. Preserve recovered March 2026 artifacts and document inconsistencies.
2. Establish reproducible DSAT curve and 14-compartment diagnostic tests.
3. Complete historical DSAT RDP table and repetitive-dive reconstruction with a source-by-source reconciliation.
4. Reconstruct a reference Bühlmann ZH-L16 variant and a specified U.S. Navy edition.
5. Prove extremal-history structure under finite rate bounds.
6. Obtain and properly document downloadable public datasets; seek separate access where necessary.
