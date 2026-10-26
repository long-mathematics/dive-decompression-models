# Dive Decompression Models

**Mathematical reconstruction, verification, and analysis of decompression algorithms and published dive tables.**

Manuscript author: **Christopher D. Long**.

> **Research software only — not for dive planning or live dive-computer use.** No model, code, table, or numerical result in this repository has been certified for diver safety. A mathematically accurate reconstruction of a historical table is not clinical validation.

## Current manuscript

**The Spencer–Huggins No-Decompression Tables: Reconstruction, Numerical Audit, and Open Questions** — Version 1.1, 26 October 2026.

[PDF](output/pdf/spencer_huggins_reconstruction.pdf) · [LaTeX source](papers/spencer_huggins/spencer_huggins_reconstruction.tex) · [Audit record](papers/spencer_huggins/AUDIT.md) · [Reproducibility instructions](papers/spencer_huggins/README.md)

The eight-page note recovers all six calibrated limits, reproduces 70 of 72 intermediate pressure entries, identifies a nearly additive surface-interval structure, and supplies a limited exact certificate for 5,988 compartment inequalities. Nineteen Huggins-specific tests cover the calculations. The historical model and all three chart transcriptions are preserved separately. Probable printing errors and undocumented generator choices remain hypotheses or open questions, not established historical explanations.

The simplest single-clock, common-buffer ceiling model is ruled out; a richer scalar-cutoff explanation remains open. Complete HP-67 generator recovery, minimum dimension after refitting, and physiological validation are not claimed.

## Research highlights and mathematical targets

- **Reconstruct major published dive tables.** Reproduce original entries from documented equations, parameters, ascent conventions, repetitive-dive rules, and rounding. Record exactly what is sourced, inferred, or not publicly specified.
- **Find minimal compartment models.** Determine the smallest number of compartments needed to reproduce a specified published table within a stated tolerance (initial target: one minute). Distinguish table equivalence from physiological equivalence.
- **Exact NDL threshold calculation.** For a fixed-depth hold followed by a fixed linear-Haldane ascent, each compartment's surfacing-limit diagnostic is an exponential in hold duration. Its first crossing can be calculated analytically rather than by an arbitrary search cutoff. [Implementation](models/dsat/dsat1994_planner.py) · [Tests](tests/test_dsat.py).
- **Sharp bounds from incomplete depth histories.** A single known compartment loading and a bounded depth history imply explicit extremal bounds for other Haldane compartments. These are mathematical statements within the linear model, not validated decompression schedules. [Theorem, proof, and scope](mathematics/EXPO_KERNEL_BOUNDS.md) · [Reference implementation](mathematics/envelopes.py).
- **Probabilistic model assessment.** Compare reported outcomes and bubble observations with independently held-out predictions; track exposure definitions, dataset overlap, ascertainment, and uncertainty.

## Questions and open problems

1. **Exact reconstruction:** Which historical tables can be reproduced exactly, including rounding, ascent, repetitive, and multilevel rules? For which versions are essential proprietary ingredients missing?
2. **Minimum dimension:** Can we certify a lower bound on the number of compartments needed to match a given family of no-stop and repetitive-dive outputs?
3. **Partial history:** How do sharp loading envelopes change under a finite history length, rate-limited ascent/descent, time-stamped depth samples, and gas-switch uncertainty?
4. **Identifiability:** Can different compartment parameter sets induce the same rounded published table? What additional experiments or profiles distinguish them?
5. **Predictive validation:** Does a reconstructed or refined model improve out-of-sample DCS prediction, without confusing table reproduction with physiological validation?

For the empirical origin of the RDP equation, including the distinct early $C=510$ fit and final shifted $C=803$ curve, see [DSAT empirical calibration and historical evidence](docs/EMPIRICAL_CALIBRATION.md).

## Model inventory

| Family | Status | Next step |
| --- | --- | --- |
| **Spencer–Huggins (1981)** | [Reconstruction and audit](models/huggins_1981/README.md); six compartments, three charts, explicit unresolved differences | Historical generator conventions and minimal refitted dimension remain open |
| **DSAT / PADI RDP (1994)** | [Working reconstruction](models/dsat/README.md); first-dive curve and 14-compartment parameters; some display conventions unresolved | Audit original publication and repetitive/metric rules |
| **Bühlmann ZH-L16 (variants A/B/C)** | Planned | Versioned coefficients, gradient-factor conventions, fixtures |
| **U.S. Navy (historical, Rev. 6/7)** | Planned | Separate revisions and asymmetric ascent/stop rules |
| **NOAA air/nitrox** | Planned | Match each published edition |
| **French MN90** | Planned | Compare tabulated outputs and underlying algorithm |
| **Canadian DCIEM** | Planned | Serial-compartment reconstruction and inverse identification |
| **BSAC '88, NAUI, other families** | Planned | Distinguish documented reconstruction from output-only fitting |

See the [reconstruction registry](docs/TABLE_REGISTRY.md) for scope and exactness criteria.

## Repository structure

- [`models/huggins_1981/`](models/huggins_1981/) — source-preserving reconstruction and chart-structure audit.
- [`models/dsat/`](models/dsat/) — active DSAT research reconstruction and assumptions.
- [`archive/2026-03/`](archive/2026-03/) — recovered, superseded March 2026 snapshots; not normative references.
- [`papers/`](papers/) — mathematical manuscripts, build scripts, and audit records.
- [`output/pdf/`](output/pdf/) — compiled manuscript and hash manifest, generated after testing.
- [`mathematics/`](mathematics/) — independently specified theorems, proofs, and computational bounds.
- [`tests/`](tests/) — executable regression and mathematical property tests.
- [`docs/`](docs/) — [research status](docs/RESEARCH_STATUS.md), [roadmap](docs/ROADMAP.md), [rendering conventions](docs/RENDERING.md), and [source registry](docs/TABLE_REGISTRY.md).
- [`data/`](data/) — external dataset registry; no restricted data or personal dive records included.

## Reproduce the numerical checks

Python 3.10+ is sufficient; the test suite has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python models/dsat/dsat1994_planner.py selftest
python models/huggins_1981/huggins.py --audit-dir validation/huggins_1981
python -m models.huggins_1981.surface_structure --audit-dir validation/huggins_1981
```

The DSAT command compares a fitted historical curve, published table anchors, and a separately defined 14-compartment surfacing-limit diagnostic. Their predictions need not coincide. Do not use these outputs to plan or conduct dives.

## Provenance and status

- Huggins sources and the two-witness chart transcription are documented in the [manuscript](papers/spencer_huggins/README.md) and [fixture](tests/fixtures/huggins_1981.json).
- DSAT source: Hamilton, Rogers, Powell, and Vann (1994), *Development and validation of no-stop decompression procedures for recreational diving: The DSAT Recreational Dive Planner*. Page-specific extraction is retained with the model.
- [DSAT working notes](papers/dsat-1994-reconstruction/) and [old sources](archive/2026-03/) are labeled; archival files may contain errors and are retained for traceability.
- We distinguish source-transcribed, derived within a specified model, numerically tested, independently validated, and unresolved statements.
- No priority claim is made without a literature review; numerical correctness does not establish reduced DCS risk.
- GitHub mathematics uses inline `$...$` and separate-block `$$...$$`, with braces for compound subscripts. See [rendering rules](docs/RENDERING.md).

## Licensing and attribution

This repository uses a permissive mixed license. The [root license and provenance policy](LICENSE) specifies its scope.

- **Software** (Python, tests, configuration, synthetic examples): [Apache License 2.0](LICENSES/Apache-2.0.txt).
- **Original mathematical papers and explanatory documentation**: [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt). Attribute Christopher D. Long, the relevant title and version, and indicate modifications.
- **Third-party published tables, quoted content, and clinical or external datasets** retain their source rights. No third-party material is relicensed merely because it is cited or appears here.

File-specific SPDX declarations are in [REUSE.toml](REUSE.toml). Neither license certifies the models or software for real-world decompression planning.
