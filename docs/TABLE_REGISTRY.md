# Published-table and model reconstruction registry

Record an **edition**, not merely a brand name. Each entry needs bibliographic source, parameter tables, assumptions, comparison fixtures, and discrepancy report. Entries below are research targets, not completion claims.

| Family | Edition / target | Primary obstacle | Status |
| --- | --- | --- | --- |
| PADI / DSAT RDP | Hamilton–Rogers–Powell–Vann 1994 and documented table editions | Repetitive groups, printed table quantization, Wheel/metric rules | Working reconstruction; not exact-complete |
| Bühlmann | ZH-L16A, B, C as separate variants | Variant-specific coefficients, gas mixing, gradient factors, stop conventions | Planned |
| U.S. Navy | Historical air tables; separately Rev. 6 and Rev. 7 | Edition-specific ascent/decompression and repetitive rules | Planned |
| NOAA | Separately dated air and nitrox tables | Identify actual generating algorithms rather than simply table reuse | Planned |
| French Navy MN90 | Documented editions | Underlying assumptions and surface-interval table rules | Planned |
| DCIEM | Canadian original serial-compartment tables | Complete serial-model specification and numerical parameters | Planned |
| BSAC | BSAC '88 | Generating algorithm completeness/availability | Inverse-reconstruction candidate |
| NAUI | Historical and later tables by edition | Separate models and proprietary versions | Planned |
| Other manufacturer algorithms | Version/device-specific | Often proprietary and underidentified by observed outputs | Output-based equivalence only |

## Verification tiers

- **Tier A — historical exact:** complete specified edition, every relevant published cell including rounding and display.
- **Tier B — numerical reconstruction:** published mathematical model reproduced and compared, but display/operational conventions incomplete.
- **Tier C — black-box fit:** matches selected outputs; generating model not uniquely established.
- **Tier D — planned:** source not yet audited or implementation not started.

Nothing in these tiers expresses validated diving safety.

## Reference resources

- [U.S. Navy diving publications](https://www.navsea.navy.mil/Home/SUPSALV/00C3-Diving/Diving-Publications/)
- [NOAA diver resources](https://www.omao.noaa.gov/diving-program/resources-divers)
- [R DiveR package table documentation](https://gowachin.github.io/DiveR/reference/table.html)
- Hamilton, R. W., Rogers, R. E., Powell, M. R., and Vann, R. D., *Development and validation of no-stop decompression procedures for recreational diving: The DSAT Recreational Dive Planner* (1994).
