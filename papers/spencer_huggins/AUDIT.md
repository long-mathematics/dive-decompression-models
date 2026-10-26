# Version 1.1 audit record

Date: 26 October 2026. Author: Christopher D. Long.

## Verified in this revision

- All 15 existing Huggins tests rerun without changing the original fixture or model.
- Four new integer-structure tests pass: 91 transitions, 25 anchors, 66 genuine predictions, 63 exact predictions, and the three one-minute exceptions L/I, L/J, L/K.
- The exact certificate is unchanged: 998 profile–interval combinations, 5,988 compartment inequalities, and a rational lower margin greater than 0.06069657 fsw.
- The 1981 formula, maxima, rounding instruction, and group percentages checked against printed pages 4–5; 1987 printed page 13 and Appendix D page 99 inspected for the documented arrows and the second chart witness.
- Manuscript compiled twice and all eight rendered pages inspected. No overfull boxes or undefined references/citations were reported.

## Interpretation correction

Near row–column additivity is not a proof of one common group clock. The simplest rule `L(g,j) = ceil(tau_g - tau_j + c)` cannot fit the data: its triangle quantities must lie in one interval of length three, whereas the D/B/A and D/C/A quantities are 9 and 3. The note therefore labels a richer scalar model with distinct departure and arrival cutoffs as a **historical hypothesis**, not an established generator.

The earlier suggestion of a specific later correction to RNT A/110 is not needed for the results and is not treated as a confirmed erratum here. The source-preserving 1981 value remains 2, while the candidate formula gives 3. The two intermediate-pressure errors remain probable printing/copying errors, not proven historical production events.

## Scope and open questions

No reanalysis of Spencer's raw observations; no claim of original calculator recovery; no medical validation. Open questions concern the exact surface-interval generator, remaining display/RNT conventions, minimum dimension after refitting, and empirical recovery of the Spencer limits.

## Reproducibility

Run the commands in README.md. `output/pdf/spencer_huggins_manifest.json` records input/output hashes and, in the publication workflow, the exact source commit. An internal audit is not independent refereeing.
