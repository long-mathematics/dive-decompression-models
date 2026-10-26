# Spencer–Huggins discrepancies: established facts and open explanations

Updated for manuscript version 1.1, 26 October 2026. See the [note and audit record](../papers/spencer_huggins/README.md). Earlier exploratory commentary is retained in Git history.

## Documented construction

Huggins (1981), printed pages 4–5, specifies the six half-times, column-maxima calibration, downward 0.5-fsw rounding, and group fractions 63%, 66%, ..., 99%, 100%. [Primary report](https://repository.library.noaa.gov/view/noaa/42176).

Huggins (1987), printed page 13, explains the first-chart arrows as rightward group-selection instructions and confirms all-six-compartment grouping. Appendix D, page 99, supplies the clipped J/K columns. [Author's later report](https://repository.library.noaa.gov/view/noaa/40558).

## Established numerical differences

- Table 2 gives 52.41 instead of the formula's 52.14 for 35 fsw / 165 min / 40-min compartment; and 39.96 instead of 37.96 for 60 fsw / 50 min / 120-min compartment. Neither affects a calibrated maximum.
- Seven empirical terminal limits exceed the downward-rounded M-values. The calibration and independent retention of the input endpoints explain this distinction.
- The simple first-crossing ceiling matches 169 of 179 finite RNT values, not all of them. A/110 remains the printed 2 while the candidate gives 3. This revision does not treat an alleged later change as a verified erratum.
- Every strict printed surface transition exceeds the derived nominal-group-box bound; the excess is not ordinary minute rounding.

## The additive pattern, stated precisely

Let $L(g,j)$ be a printed strict-transition lower endpoint. Set

$$
\widehat L(g,j)=L(g,A)+L(N,j)-L(N,A).
$$

There are 25 anchoring identities and 66 nontrivial predictions. Of the latter, 63 are exact; L/I, L/J, and L/K are one minute higher than predicted (61 versus 60, 42 versus 41, 24 versus 23).

This is near **row–column additivity**, not proof of one common group potential. The simple model `L(g,j) = ceil(tau_g - tau_j + c)` is impossible: its triangle quantities must lie in an interval of length three, while the printed D/B/A and D/C/A quantities are 9 and 3.

## Hypotheses, not historical findings

Digit transposition plausibly explains 52.41; copying the preceding row plausibly explains 39.96. A scalar washout coordinate with **distinct departure and destination cutoffs**, rounding, or corrections could explain the surface chart. These mechanisms are not established by the sources.

## Open questions

Recover the exact chart generator and remaining display/RNT conventions; determine minimal dimension after refitting; reconstruct the selected Spencer limits from the original experiments. These gaps do not prevent publication of the reproducible calculations and finite certificate. No physiological validation is claimed.
