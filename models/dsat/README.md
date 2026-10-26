# DSAT/RDP (1994) — provisional reconstruction

**Research use only; not a dive-computer algorithm or operational diving guidance.**

## What is implemented

- Rogers' empirical first-dive fitted NDL curve as transcribed from the historical report: $D-20.15=803\,t^{-0.7476}$ in feet of seawater.
- Fourteen half-times and surfacing $M_0$ values (Table III).
- Classical Haldane constant-depth kinetics and Schreiner linear-travel kinetics, using DSAT's nitrogen-equivalent pressure convention, *without* a Bühlmann-style water-vapor correction.
- Fixed-rate ascent **surfacing-limit** test and exact analytic extra-dwell threshold (not a complete decompression-ceiling test).
- Model-based pressure-group and residual-nitrogen-time reconstructions labeled as inferred rather than exact printed RDP conventions.
- A JSON profile-processing CLI and comparative self-test.

## What is **not** implemented or certified

- Proven equivalence to all commercial RDP cards and Wheel editions, particularly metric depth conversion, surface washout, multilevel guardrails, ascent convention, and all display rounding.
- Accurate pressure-dependent M-values for arbitrary decompression-stop schedules.
- Medical DCS-risk probabilities or clinical validation.
- Protection against violations of all published operational rules: some guards remain warnings.

## Run

```bash
python models/dsat/dsat1994_planner.py selftest
python models/dsat/dsat1994_planner.py plan examples/dsat_two_dive_demo.json
```

The example is **synthetic** and for regression demonstration only. The reporting is not a dive recommendation.

## Source provenance

- Hamilton, Rogers, Powell, Vann (1994), model development and parameters, report pp. 19–23.
- [Transcribed extraction](recovered_dsat_rdp_extraction.md), March 2026.
- [Historical code](../../archive/2026-03/), kept unchanged for comparison.
- [Working manuscript](../../papers/dsat-1994-reconstruction/) with remaining gaps explicitly labeled.

The original code's binary search could misclassify a finite but long model-based threshold as infinite. The active copy computes the crossing exactly. The research model's original choices for surface washout and grouping remain provisional.
