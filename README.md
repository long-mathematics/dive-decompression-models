# Dive Decompression Models

**Mathematical reconstruction, verification, and analysis of decompression algorithms and published dive tables.**

Manuscript author: **Christopher D. Long**.

> **Research software only — not for dive planning or live dive-computer use.** No model, code, table, or numerical result in this repository has been certified for diver safety. A mathematically accurate reconstruction of a historical table is not clinical validation.

## Research highlights and mathematical targets

- **Reconstruct major published dive tables.** Reproduce original entries from documented equations, parameters, ascent conventions, repetitive-dive rules, and rounding. Record exactly what is sourced, inferred, or not publicly specified.
- **Find minimal compartment models.** Determine the smallest number of compartments needed to reproduce a specified published table within a stated tolerance (initial target: one minute). Distinguish table equivalence from physiological equivalence.
- **Exact NDL threshold calculation.** For a fixed-depth hold followed by a fixed linear-Haldane ascent, each compartment's *surfacing-limit diagnostic* is an exponential in hold duration. Its first crossing can be calculated analytically rather than by an arbitrary search cutoff. [Implementation](models/dsat/dsat1994_planner.py) · [Tests](tests/test_dsat.py).
- **Sharp bounds from incomplete depth histories.** A single known compartment loading and a bounded depth history imply explicit extremal bounds for other Haldane compartments. These are mathematical statements within the linear model, not validated decompression schedules. [Theorem, proof, and scope](mathematics/EXPO_KERNEL_BOUNDS.md) · [Reference implementation](mathematics/envelopes.py).
- **Probabilistic model assessment.** Compare reported outcomes and bubble observations with independently held-out predictions; track exposure definitions, dataset overlap, ascertainment, and uncertainty.

## Questions and open problems

1. **Exact reconstruction:** Which historical tables can be reproduced *exactly*, including rounding, ascent, repetitive, and multilevel rules? For which versions are essential proprietary ingredients missing?
2. **Minimum dimension:** Can we certify a lower bound on the number of compartments needed to match a given family of no-stop and repetitive-dive outputs?
3. **Partial history:** How do sharp loading envelopes change under a finite history length, rate-limited ascent/descent, time-stamped depth samples, and gas-switch uncertainty?
4. **Identifiability:** Can different compartment parameter sets induce the same rounded published table? What additional experiments or profiles distinguish them?
5. **Predictive validation:** Does a reconstructed or refined model improve out-of-sample DCS prediction, without confusing table reproduction with physiological validation?

For the **empirical origin of the RDP equation**, including the distinct early $C=510$ fit and the final shifted $C=803$ curve, see [DSAT empirical calibration and historical evidence](docs/EMPIRICAL_CALIBRATION.md).

## Model inventory

| Family | Status | Next step |
| --- | --- | --- |
| **DSAT / PADI RDP (1994)** | [Working reconstruction](models/dsat/README.md); first-dive curve and 14-compartment parameters; some display conventions unresolved | Audit original RDP publication and all repetitive/metric rules |
| **Bühlmann ZH-L16 (variants A/B/C)** | Planned | Versioned coefficients, gradient-factor conventions, fixtures |
| **U.S. Navy (historical, Rev. 6/7)** | Planned | Separate revisions and asymmetric ascent/stop rules |
| **NOAA air/nitrox** | Planned | Match each published edition |
| **French MN90** | Planned | Compare tabulated outputs and underlying algorithm |
| **Canadian DCIEM** | Planned | Serial-compartment reconstruction and inverse identification |
| **BSAC '88, NAUI, other families** | Planned | Distinguish documented reconstruction from output-only fitting |

See the [reconstruction registry](docs/TABLE_REGISTRY.md) for scope and exactness criteria.

## Repository structure

- [`models/dsat/`](models/dsat/) — active DSAT research reconstruction and assumptions.
- [`archive/2026-03/`](archive/2026-03/) — recovered, **superseded** March 2026 source snapshots; not normative references.
- [`papers/`](papers/) — working mathematical manuscripts and source notes.
- [`mathematics/`](mathematics/) — independently specified theorems, proofs, and computational bounds.
- [`tests/`](tests/) — executable regression and mathematical property tests.
- [`docs/`](docs/) — [research status](docs/RESEARCH_STATUS.md), [roadmap](docs/ROADMAP.md), [rendering conventions](docs/RENDERING.md), and [source registry](docs/TABLE_REGISTRY.md).
- [`data/`](data/) — external dataset registry; **no restricted data or personal dive records included**.

## Reproduce the current numerical checks

Python 3.10+ is sufficient; the initial test suite has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python models/dsat/dsat1994_planner.py selftest
```

The DSAT command compares a fitted historical no-stop curve, its published table anchors, and a separately defined 14-compartment *surfacing-limit diagnostic*. Their predictions need not coincide. **Do not use its outputs to plan or conduct dives.**

## Provenance and status

- Historical reconstruction source: Hamilton, Rogers, Powell, and Vann (1994), *Development and validation of no-stop decompression procedures for recreational diving: The DSAT Recreational Dive Planner*. Page-specific extraction is retained with the model.
- [Working notes](papers/dsat-1994-reconstruction/) and [old sources](archive/2026-03/) are clearly labeled; archival files may contain errors and are retained for traceability, not as final claims.
- We distinguish **source-transcribed**, **derived within a specified model**, **numerically tested**, **independently validated**, and **open or unresolved**.
- No claim of a new result's priority is made without a literature review; no claimed safety or DCS-risk reduction follows from numerical correctness.
- GitHub mathematics is written with inline `$...$` and separate-block `$$...$$`; use braces for compound subscripts. See [rendering rules](docs/RENDERING.md).

## Licensing and attribution

This repository uses a **permissive mixed license**. The [root license and provenance policy](LICENSE) specifies what each license covers.

- **Software** (Python, tests, configuration, synthetic examples): [Apache License 2.0](LICENSES/Apache-2.0.txt), including an explicit patent grant and standard warranty disclaimer.
- **Original mathematical papers and explanatory documentation** (Markdown, LaTeX, proofs): [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt). Cite **Christopher D. Long**, the relevant document title, and a version or repository URL; indicate substantive modifications.
- **Third-party published tables, quoted content, and clinical or external datasets** retain their source rights. No third-party material is relicensed merely because it is cited or appears here; follow each source's provenance and conditions.

File-specific SPDX declarations are in [REUSE.toml](REUSE.toml), preserving the March 2026 archival snapshots unchanged. Neither license certifies these mathematical models or the software for real-world decompression planning.
