# Explaining the Spencer–Huggins (1981) chart discrepancies

**Research note, 2026-10-26.** Explanations below are classified as **directly stated**, **numerically demonstrated**, **historical version evidence**, or **hypothesis**. None is physiological validation.

## Sources and direct comments

1. Karl E. Huggins, *New No-Decompression Tables Based on No-Decompression Limits Determined by Doppler Ultrasonic Bubble Detection* (1981), NOAA https://repository.library.noaa.gov/view/noaa/42176 , pp. 1–6. States: six-compartment Haldane update; maxima over Spencer endpoints; M-values **rounded down** to nearest 0.5 fsw; group A starts at 63% of M0 and groups rise in 3% steps, with N at 100%. Does **not** specify the full HP-67 program or every display convention.
2. Karl E. Huggins, *Microprocessor Applications to Multi-Level Air Decompression Problems* (1987), https://repository.library.noaa.gov/view/noaa/40558/noaa_40558_DS1.pdf , printed pp. 12–13 (PDF pp. 21–22), Appendix D p. 99 (PDF p. 108). **Directly explains the first-chart arrows:** move right to obtain the repetitive group. Explicitly says groups reflect all six compartments, unlike U.S. Navy's single 120-minute compartment. Gives Spencer's formula $t=(465/D)^2$ (minutes, fsw).
3. J. Lippmann, discussion of Huggins tables, *SPUMS Journal* 18(2), 1988, printed pp. 72–73, https://dhmjournal.com/images/18/SPUMSJ_June1988.pdf . Contemporary independent reproduction of the Huggins charts and discussion of all-compartment groups.
4. Interview with Huggins, *Scientific American* (2012), https://www.scientificamerican.com/blog/expeditions/usc-dornsife-scientific-diving-an-interview-with-karl-huggins/ . Confirms his motivation to prevent the Navy 120-minute-only group approximation from misrepresenting faster compartments; **not** an explanation of particular numerical discrepancies.
5. Revised HUGI card labeled 15 October 2001 (embedded in historical tables compilation, https://www.divetable.info/skripte/Historical_Divetables.pdf ) adds explicit operational advice that stops extending beyond the no-stop limit put the diver in group N. This is a later **different edition**, not retrospective proof of the 1981 generation rule.

## Printed intermediate-pressure errors: likely mechanistic explanation

At 35 fsw, 165 min, 40-min half-time, Table 2 reads **52.41** while the formula gives **52.14**: the last two digits appear transposed.

At 60 fsw, 50 min, 120-min half-time, Table 2 reads **39.96** while the formula gives **37.96**. Notably **39.96** is also the correct value immediately above, at 50 fsw, 75 min, 120-min half-time. Thus copy-forward from the previous row is plausible.

Both hypotheses explain the specific digits, but no contemporaneous written erratum has been found. Neither affects any of the six M-values.

## Endpoint and nonuniform grid

Huggins preserves twelve Spencer-derived empirical no-decompression limits as inputs and then **rounds the resulting model calibration down** to 0.5 fsw. Seven terminal group-N chart times slightly exceed these rounded limits. This is an inevitable possibility whenever one calibrates on empirical endpoints and subsequently rounds their maxima downward; it is not explained away by floating-point formatting.

The early Spencer relation $t=(465/D)^2$ in Huggins (1987) is a smooth motivating formula, not an exact representation of every tabulated endpoint (e.g. at 130 fsw it gives approximately 12.8 minutes versus a tabulated five minutes). The practical lookup grid and historical exposure limits remain independent evidence.

Huggins (1987) explicitly states the rightward-arrow instruction; do **not** treat these as absent data. The exact choice of other grid entries (5, 7, 10, 13, etc.) is undocumented and not reproduced by simply flooring every continuous crossing.

## RNT version evidence: a possible corrected typo

The 1981 scan prints **group A, 110 fsw, 2 minutes**. The 1987 Appendix D reproduction, and the 1988 SPUMS reprint, show **3 minutes** at the same location, which also agrees with the independently derived ceiling of the continuous first crossing.

This is strong evidence for an unannounced correction or a 1981 transcription error, but an explicit statement of correction was **not located**. The source-preserving 1981 fixture remains 2; version-specific variants should be kept separate.

The first-crossing candidate matches **169 of 179 finite RNT** entries. The deeper group-N discrepancies partly track the separately retained Spencer terminal limits; several one-minute differences and the printed L/20 dash require further investigation. They are not all proven typographical errors.

## New structural diagnostic: near-exact additive surface-interval clock

Write $S(g,j)$ for the published **lower endpoint in whole minutes** of the surface-interval range moving from departure group $g$ to destination group $j$, with groups A–N in increasing order.

**New arithmetic observation (source fixture, not yet an explanation of generator).** For each of the 91 strict downward transitions, define the prediction from the A destination row and N departure column:

$$
\widehat S(g,j)=S(g,A)-S(N,A)+S(N,j).
$$

Of the 91 entries, **88 satisfy $S(g,j)=\widehat S(g,j)$ exactly**. Of these 91, 25 are the anchoring entries used to construct the formula; among the remaining **66 genuine predictions, 63 are exact and three differ by one minute upward**:

| Departure | Destination | Printed | Additive prediction |
| --- | --- | ---: | ---: |
| L | I | 61 | 60 |
| L | J | 42 | 41 |
| L | K | 24 | 23 |

This nearly rank-one/additively separable table structure is stronger evidence than the crude fit of a universal 10-minute buffer. It suggests that a **single scalar washout clock or a set of per-group time potentials**, followed by integer-minute rounding, generated the surface-interval chart. It does **not** uniquely identify the historical starting and ending pressure cutoffs or the HP-67 method.

By contrast, direct propagation of the nominal group upper fractions with ordinary Haldane washout predicts shorter surface thresholds. The 91 printed lower endpoints exceed these direct bounds by roughly **3.19 to 20.65 minutes**, nonuniformly. An unexplained global 10-minute additive offset cannot account for this variation.

**Next investigation:** fit latent per-group clock potentials from all 91 entries with integer inequality constraints on rounding, then compare their implied 120-minute-compartment pressure cutoffs with the historical 3% bins and any documented 10-minute minimum interval. Independently check all cells against the 1987 and 1988 printings before attributing discrepancies to intentional decisions or transcription.

## Not established

- No author statement directly explaining the two 1981 Table 2 pressure errors has been found.
- No original calculator listing or official errata sheet defining the complete rounding procedure has been located.
- No evidence that the 2001 HUGI card must be numerically identical to the 1981 edition.
- No model-only explanation for the extra surface-interval delay has yet been proven.

This note is for historical/mathematical reconstruction, not operational dive planning.
