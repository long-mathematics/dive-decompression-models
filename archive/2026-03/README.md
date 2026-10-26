# March 2026 snapshots — historical, superseded

These original working files are preserved for provenance. They are **not** the active implementation and must not be used for dive planning.

- `dsat_algorithm.tex`: earlier wide-ranging reconstruction; uses an earlier unshifted empirical fit ($C=510$, $x=0.53$) that the original report also records before its final shallow-asymptote correction. See [empirical calibration chronology](../../docs/EMPIRICAL_CALIBRATION.md).
- `rdp_padi14.py`: earlier curve/shadow-model demonstration; mixes a Bühlmann-style alveolar water-vapor correction with DSAT Table III coefficients. Kept verbatim for audit only.
- `dsat1994_planner_original.py`: recovered later research planner; includes an arbitrary upper-bound failure mode in the numeric NDL search, fixed analytically in the active copy.

The active mathematical diagnostic is at [models/dsat/dsat1994_planner.py](../../models/dsat/dsat1994_planner.py). Changes should not silently alter these archival sources.
