# External data sources and analysis rules

**No research-participant records are bundled in this repository.** Access permissions, licensing, consent conditions, and de-identification rules must be checked before import.

## Candidate sources

- [Zenodo record 15068564](https://zenodo.org/records/15068564) — open post-dive venous-gas-embolism grades and accompanying R analysis scripts; verify file licenses and schema before inclusion.
- [DAN Diving Safety Laboratory DCS analysis](https://pubmed.ncbi.nlm.nih.gov/41914190/) — large published cohort; individual-level data reportedly available **on reasonable request**, not assumed openly downloadable.
- [Historical U.S. Navy probabilistic risk paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172665) — points to historical NMRC 99-02 volumes and associated exposure/outcome records. Raw data extraction and field verification required.
- [NOAA diver resources](https://www.omao.noaa.gov/diving-program/resources-divers) — published reference tables, **not** independent clinical outcomes.

The prior conversation also identified a 2026 VGE Doppler audio/archive study. Its download endpoint and license should be verified before adding a permanent identifier.

## Analysis requirements

1. Define the unit of observation: diver, dive, exposure series, or Doppler reading.
2. Separate decompression-sickness outcomes from bubble grades; one is not a surrogate with perfect sensitivity/specificity.
3. Prevent participant leakage and historical database overlap across training/test sets.
4. Distinguish DCS incidence from detection/ascertainment; quantify selection bias and follow-up.
5. Preserve algorithm edition, table parameters, gas mix, ascent behavior, measured versus planned depth-time profile.
6. Report calibration, discrimination, uncertainty and external validity, including low event counts.
7. Retain source links, versions, codebook, transformation scripts and checksums; do not mirror restricted data.

This document is a candidate registry, **not** evidence that a specific dataset has been downloaded and verified.
