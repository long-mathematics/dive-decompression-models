"""Additive structure of the transcribed surface-interval chart.

Copyright 2026 Christopher D. Long. SPDX-License-Identifier: Apache-2.0
Research only. This audits integers in a historical chart, not diver safety.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from models.huggins_1981.huggins import GROUPS, HistoricalChart, group_index


def analyze_surface_structure() -> dict:
    """Separate anchoring identities from genuine cross-cell predictions.

    The fitted form is a departure offset plus an arrival offset. It does not
    identify a single common group potential, physiological state, or generator.
    """
    chart = HistoricalChart()

    def lower(g: str, j: str) -> int:
        return chart.surface_range(g, j)[0]

    rows = []
    for g in GROUPS[1:]:
        for j in GROUPS[:group_index(g)]:
            predicted = lower(g, 'A') + lower('N', j) - lower('N', 'A')
            actual = lower(g, j)
            rows.append(dict(departure=g, destination=j, printed_min=actual,
                             predicted_min=predicted, residual_min=actual-predicted,
                             anchor=(j == 'A' or g == 'N')))
    predictions = [r for r in rows if not r['anchor']]
    exceptions = [r for r in predictions if r['residual_min']]
    # A pure single-potential model plus one fixed buffer, uniformly rounded
    # upward, requires all these triangle quantities to lie in an interval of
    # length 3. The observed 9 and 3 are incompatible with that simple model.
    triangles = {
        'D-B-A': lower('D', 'B') + lower('B', 'A') - lower('D', 'A'),
        'D-C-A': lower('D', 'C') + lower('C', 'A') - lower('D', 'A'),
    }
    return dict(
        transitions=len(rows),
        anchoring_entries=sum(r['anchor'] for r in rows),
        nontrivial_predictions=len(predictions),
        exact_nontrivial_predictions=sum(r['residual_min'] == 0 for r in predictions),
        max_absolute_prediction_error_min=max(abs(r['residual_min']) for r in predictions),
        exceptions=exceptions,
        single_potential_triangle_witnesses=triangles,
        interpretation='Near row-column additive structure. Historical generating rule is not identified.',
        rows=rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-dir', type=Path)
    args = parser.parse_args()
    report = analyze_surface_structure()
    if args.audit_dir is not None:
        args.audit_dir.mkdir(parents=True, exist_ok=True)
        (args.audit_dir / 'surface_structure.json').write_text(
            json.dumps(report, indent=2) + '\n', encoding='utf-8')
        with (args.audit_dir / 'surface_structure.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(report['rows'][0]))
            writer.writeheader()
            writer.writerows(report['rows'])
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
