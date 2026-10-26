# Research status and audit boundaries

Updated: 2026-10-25.

## Established within explicitly stated mathematical models

| Item | Status | Qualifications |
| --- | --- | --- |
| DSAT fitted first-dive NDL curve | **Source-transcribed** | Parameters from the recovered Hamilton et al. (1994) reconstruction; not equal to every printed table cell |
| DSAT 14 compartment half-times and surfacing limits | **Source-transcribed** | Historical Table III values; no claim of full operational RDP equivalence |
| Haldane and Schreiner updates | **Classical formulas** | Linear, prescribed inspired inert-gas pressure |
| Fixed-ascent, post-hold surfacing-limit crossing time | **Derived and numerically tested** | Exact only for a specified linear model and *fixed* subsequent ascent; not a whole-ascent ceiling constraint |
| Sharp excess-loading envelopes from one reference compartment | **Derived, proof in repository** | Rate-unconstrained measurable depth histories, initially equilibrated, single inert gas, bounded depth |
| Finite-horizon loading envelope | **Derived, proof in repository** | No rate bound; zero depth before finite history interval |

## Recovered, not yet fully audited

- The March 2026 DSAT reconstruction manuscript and Python planner. The working code uses a deliberately chosen implementation of pressure groups and residual nitrogen time; not all historical quantization rules were printed explicitly.
- Disagreement between 1994 fitted curve and direct-ascent Table III diagnostic is documented, **not** resolved by equating them.
- Surface-interval off-gassing conventions, metric depth presentation, complete multilevel table generation, and detailed operational overlays need comparison against the original publication and actual table printings.
- An older manuscript uses inconsistent fitted-curve constants and should not be cited as the corrected DSAT specification; it is in the archival source directory.
- A legacy Python diagnostic mixes a Bühlmann-style water-vapor correction with DSAT M-values. It remains available for historical provenance, not as the canonical DSAT convention.

## Open / not claimed

- Exact reproduction of every PADI RDP table card and Wheel rule.
- Formal proof of optimal compartment count for any complete published table.
- Extrema under finite ascent/descent-rate constraints or noisy sensors.
- Clinical validation, improved decompression-risk prediction, medical certification, or reduced DCS incidence.
- Priority/novelty of the envelope theorem in the broader optimal-control literature (requires dedicated literature review).

## Numerical testing is not physiological validation

The automated tests check algebra, numerical agreement with an independent root-finding oracle, and extremal inequality properties. They **do not** establish a safe dive profile, an acceptable risk threshold, or conformity with any dive computer or regulator.
