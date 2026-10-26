# The empirical calibration and smoothing of the original DSAT RDP

**Audit note (2026-10-26).** Do not flatten two successive empirical curve fits into one and do not confuse the 1988 RDP table with the subsequent 1994 DSAT *computer* model.

## Primary source

R. W. Hamilton, R. E. Rogers, M. R. Powell, R. D. Vann (1994), *Development and validation of no-stop decompression procedures for recreational diving: The DSAT Recreational Dive Planner*, section III(a), p. 20; section III(c), p. 21.

Digitized original: https://www.angelofarina.it/Public/Scubapro/NEDU-reports/DSAT_1994_unsecured_opt.pdf

Historical steps, with distinct status:

1. The U.S. Navy first-dive no-stop limits were irregular in part because of five-minute rounding and finite observations. Rogers argued for a smooth allowable-depth/time relation, tried interpolating half-times, and described the need to **“massage”** the USN data to obtain a smooth curve (p. 20).
2. The Hempleman *P-root-t* relation motivated the preliminary simple law $D=Ct^{-x}$, with **$C=510$, $x=0.53$**, after a conservatism adjustment informed by Merrill Spencer's Doppler bubble data (p. 20). The report describes a target of about 15% post-dive detectable bubbles for single dives; bubble positivity is not DCS probability.
3. Shallow-water empirical observations motivated a further modification with the shallow asymptote **$A=20.15$ fsw** (chosen conservatively relative to reported estimates around 22 fsw). The final reported three-parameter curve is

$$
D-A=Ct^{-x},\qquad A=20.15\ \mathrm{fsw},\quad C=803,\quad x=0.7476.
$$

4. The 14 surfacing $M_0$ values in Table III were then **back-calculated from the smoothed no-stop curve**, with the reported timed-descent convention of 60 fsw/min starting at the beginning of bottom time (p. 21).
5. Published Table II values were checked against existing no-stop diving data. The report also documents subsequent pressure-group, repetitive, multilevel, and printed-presentation conventions, not all of which follow from the single curve equation.

**Important distinction:** The published table is not claimed to arise by blindly rounding the final equation. Nor is there presently evidence that its ten Table II cells were individually re-fitted to new experiments *after* the final curve was specified. Reconstruct both the model-building sequence and the later operational/table discretization layer, and audit this question independently.

## Earlier March 2026 ScubaBoard discussion

We recovered the following passage supplied by the project author, attributed to Dr. Michael Powell (Dr. Deco), regarding what Dr. Ray Rogers did: “I actually do not recall what Dr Rogers did - it was 1985. I suspect that it was only smoothing the curve.”

Powell's surrounding remarks described deriving NDLs from human laboratory diving studies and subsequent Spencer Doppler adjustments, then calculating the controlling half-times and $M_0$ values from the **smoothed** NDLs. His recollection is explicitly uncertain. The original ScubaBoard URL and direct text have not been independently verified; do not cite this exchange as primary-document proof without recovering the thread. The Hamilton et al. report supplies the independent documentary evidence.

## Separate downstream model

R. E. Rogers (1994), *Developing the DSAT Dive Computer Model*, *SPUMS Journal* **24**(4), 233–237:
https://www.dhmjournal.com/images/IndividArticles/24Dec/Rogers_SPUMSJ.24.4.233-237.pdf

This later computer design **modified** the RDP's model, using simulated variable-depth profiles and IAPM experimental exposures to determine stricter $M$ values, plus surface-interval penalties. It is not identical to the printed RDP table. In particular, Rogers explicitly states that computer-table equivalence does not mean equality (pp. 233–236).

## Manuscript audit instruction

- Document both pre-asymptote and final RDP equations, without calling $C=510$ simply a computational error.
- Keep the causal chain visible: experimental observations and USN constraints $\to$ empirical smoothing $\to$ final no-stop curve $\to$ derived compartment parameters $\to$ repetitive/operational rules $\to$ printed table.
- Distinguish evidence-based adjustments from practical smoothing and conventional rounding.
- Separate **RDP historical table reconstruction** from **later DSAT dive-computer-model calibration**.
