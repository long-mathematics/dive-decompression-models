# Spencer–Huggins (1981): reconstruction and numerical audit

**Research only. Not for dive planning or live dive-computer use.**

The continuous six-compartment model and historical charts are separate objects. The code preserves unexplained printed entries instead of replacing them with model predictions.

[Eight-page manuscript, version 1.1](../../output/pdf/spencer_huggins_reconstruction.pdf) · [Source and audit](../../papers/spencer_huggins/README.md) · [Data fixture](../../tests/fixtures/huggins_1981.json)

## Reproduce

```bash
python -m unittest discover -s tests -p 'test_huggins*.py' -v
python models/huggins_1981/huggins.py --audit-dir validation/huggins_1981
python -m models.huggins_1981.surface_structure --audit-dir validation/huggins_1981
sh papers/spencer_huggins/build.sh
```

Python 3.10+ and the standard library suffice for all 19 Huggins-specific tests; the final command also requires TeX.

## Established calculations

| Check | Result |
| --- | --- |
| Rounded surfacing M-values | All 6 reproduced |
| Intermediate pressures | 70 of 72 agree; original discrepancies preserved |
| First-dive numerical endpoints | 120 of 127 satisfy nominal group bounds; 7 terminal exceptions |
| Finite RNT entries | 169 of 179 match the explicitly stated first-crossing candidate |
| Surface intervals | All 105 ranges transcribed; 91 downward transitions exceed the derived box bound |
| Additive structure | 25 anchors; 63 of 66 genuine predictions exact, 3 one-minute exceptions |
| First-dive/surface certificate | 998 combinations; 5,988 exact rational inequalities pass |

A row offset plus a column offset is not one common group clock. A single-potential model with a fixed buffer and uniform upward rounding is ruled out by two triangle quantities (9 and 3). More general scalar-cutoff explanations are hypotheses, not recovered historical rules.

The certificate covers initially equilibrated square first dives followed by one printed surface interval. It does not cover arbitrary repetitive or multilevel histories or physiological outcomes.

## Sources and edition control

Primary source: Huggins (1981), MICHU-SG-81-205, printed pp. 1–6. [NOAA record](https://repository.library.noaa.gov/view/noaa/42176).

Columns J and K clipped from the supplied scan are recovered only from the author's 1987 reproduction, Appendix D, printed p. 99. [NOAA record](https://repository.library.noaa.gov/view/noaa/40558). Legible 1981 entries take precedence, including RNT A/110 = 2. Source hashes and cell provenance are in the unchanged fixture. This reconstructs Spencer's limits as tabulated by Huggins, not Spencer's raw Doppler observations.

## Hypotheses and open questions

The two intermediate-pressure discrepancies plausibly reflect transposition/copying errors. The full first-dive grid, remaining RNT adjustments, surface-interval generator, minimum dimension after refitting, and empirical recovery of the selected limits remain open. No exact HP-67 recovery or physiological validation is asserted.

Original code is Apache-2.0 and exposition is CC BY 4.0; historical-source rights remain separate.
