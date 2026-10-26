"""Record publication inputs and generated artifacts; standard library only.
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path

root = Path(__file__).resolve().parents[2]
files = [
    'papers/spencer_huggins/spencer_huggins_reconstruction.tex',
    'papers/spencer_huggins/build.sh',
    'papers/spencer_huggins/write_manifest.py',
    'models/huggins_1981/huggins.py',
    'models/huggins_1981/surface_structure.py',
    'tests/test_huggins1981.py',
    'tests/test_huggins_structure.py',
    'tests/fixtures/huggins_1981.json',
    'output/pdf/spencer_huggins_reconstruction.pdf',
]
files += [p.relative_to(root).as_posix() for p in
          sorted((root / 'validation/huggins_1981').glob('*')) if p.is_file()]
entries = []
for name in files:
    data = (root / name).read_bytes()
    entries.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
manifest = dict(title='The Spencer-Huggins No-Decompression Tables', version='1.1',
                source_commit=os.environ.get('HUGGINS_SOURCE_COMMIT'),
                huggins_tests=19, files=entries,
                scope='Internal numerical and mathematical audit; no physiological validation.')
(root / 'output/pdf/spencer_huggins_manifest.json').write_text(
    json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
