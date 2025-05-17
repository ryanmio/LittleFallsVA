#!/usr/bin/env python3
"""Merge multiple validation CSVs into a single file.

Defaults:
    --inputs validation-test.csv validation-test-extra.csv
    --output validation-test-full.csv

The script normalises columns to:
    subject_id, volume, book, raw_entry, set, has_ground_truth, latitude/longitude
and drops any extra blank columns present in earlier files.
"""

import argparse
import csv
from pathlib import Path
from typing import List, Dict

DEFAULT_INPUTS = [
    "validation-test.csv",
    "validation-test-extra.csv",
]
DEFAULT_OUTPUT = "validation-test-full.csv"
NORMALISED_FIELDS = [
    "subject_id",
    "volume",
    "book",
    "raw_entry",
    "set",
    "has_ground_truth",
    "latitude/longitude",
]


def read_rows(path: Path) -> List[Dict[str, str]]:
    """Read CSV rows, dropping any blank column header."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            # Remove accidental blank column
            row.pop("", None)
            rows.append(row)
        return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge multiple validation CSVs.")
    parser.add_argument(
        "--inputs",
        nargs="*",
        default=DEFAULT_INPUTS,
        help="Input CSV files in merge order (default: validation-test.csv validation-test-extra.csv)",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Output CSV file (default: validation-test-full.csv)",
    )

    args = parser.parse_args()

    merged_rows: List[Dict[str, str]] = []
    seen_subject_ids = set()

    for fname in args.inputs:
        path = Path(fname)
        if not path.exists():
            raise SystemExit(f"ERROR: input file {fname} not found")
        for row in read_rows(path):
            sid = row.get("subject_id")
            if sid in seen_subject_ids:
                print(f"[WARN] Duplicate subject_id {sid} in {fname}; skipping")
                continue
            seen_subject_ids.add(sid)
            # Normalise column set
            merged_rows.append({field: row.get(field, "") for field in NORMALISED_FIELDS})

    if not merged_rows:
        raise SystemExit("No rows merged. Is input empty?")

    out_path = Path(args.output)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=NORMALISED_FIELDS)
        writer.writeheader()
        writer.writerows(merged_rows)

    print(f"Merged {len(merged_rows)} rows → {out_path}")


if __name__ == "__main__":
    main() 