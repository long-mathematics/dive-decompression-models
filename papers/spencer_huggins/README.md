# Spencer–Huggins tables: reconstruction and audit

**Christopher D. Long — Version 1.1, 26 October 2026.**

[Compiled PDF](../../output/pdf/spencer_huggins_reconstruction.pdf) · [LaTeX source](spencer_huggins_reconstruction.tex) · [Audit checklist](AUDIT.md) · [Numerical ledgers](../../validation/huggins_1981/) · [Model](../../models/huggins_1981/README.md)

The eight-page note separates established calculations from historical hypotheses and open questions. It recovers six M-values, audits all three charts, records 63 exact nontrivial additive predictions and three one-minute exceptions, and gives a narrowly scoped exact rational certificate. It does not claim full recovery of the unpublished HP-67 routines, a minimum among refitted compartment models, or physiological validation.

Full table transcriptions are in the unchanged source fixture. Version 1.0 and its full-chart appendices remain in Git history; version 1.1 keeps the main exposition focused.

## Reproduce

```bash
python -m unittest discover -s tests -p 'test_huggins*.py' -v
python models/huggins_1981/huggins.py --audit-dir validation/huggins_1981
python -m models.huggins_1981.surface_structure --audit-dir validation/huggins_1981
sh papers/spencer_huggins/build.sh
python papers/spencer_huggins/write_manifest.py
```

Python 3.10+ suffices for all 19 Huggins-specific tests. The PDF build requires a standard TeX installation. The publication workflow tests and builds the source before committing only its generated PDF, manifest, and audit outputs. The manifest records the source commit and SHA-256 values.

**Status:** internal mathematical and numerical audit; not independent peer review or medical certification. Historical table values remain distinct from candidate formulas. Original exposition is CC BY 4.0; software is Apache-2.0; source-material rights remain separate.
