#!/usr/bin/env python3
"""
Sample additional candidate grants from Cavaliers & Pioneers Books 9–14
without overlapping previously selected validation rows.

Usage
-----
python3 sample_additional_candidates.py \
    --extra-size 75 \
    --output validation-extra.csv

By default it looks for:
• split_books9-14.csv               (full corpus with dev/test split)
• validation-dev-A.csv              (existing candidate set A)
• validation-dev-B.csv              (existing candidate set B)
• validation-test.csv               (existing 50-row candidate set)

It writes the new sample to the specified output file and initialises
`has_ground_truth = 0` and an empty `latitude/longitude` column.
"""

import argparse
import csv
import random
from pathlib import Path
from typing import List, Tuple

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SPLIT_DATASET_PATH = SCRIPT_DIR / "split_books9-14.csv"
EXISTING_CANDIDATE_FILES = [
    SCRIPT_DIR / "validation-dev-A.csv",
    SCRIPT_DIR / "validation-dev-B.csv",
    SCRIPT_DIR / "validation-test.csv",
]
DEFAULT_EXTRA_SIZE = 75
DEFAULT_OUTPUT = "validation-extra.csv"
DEFAULT_SEED = 42


# ----------------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------------

def load_rows(path: Path) -> List[dict]:
    """Read a CSV into a list of dicts (empty list if file missing)."""
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def row_key(row: dict) -> Tuple[str, str, str]:
    """Return a tuple uniquely identifying a grant entry."""
    return (
        row.get("volume", ""),
        row.get("book", ""),
        row.get("raw_entry", ""),
    )


# ----------------------------------------------------------------------------
# Main logic
# ----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sample additional candidate land-grant entries without overlap.",
    )
    parser.add_argument("--extra-size", type=int, default=DEFAULT_EXTRA_SIZE, help="Number of new candidate rows to sample (default 75).")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT, help="Output CSV path (default validation-extra.csv).")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed for reproducibility.")

    args = parser.parse_args()

    random.seed(args.seed)

    # ---------------------------------------------------------------------
    # Load corpus and build exclusion set
    # ---------------------------------------------------------------------
    corpus_rows = load_rows(SPLIT_DATASET_PATH)
    if not corpus_rows:
        raise SystemExit(f"ERROR: could not read corpus CSV at {SPLIT_DATASET_PATH}")

    existing_keys = set()
    for cand_path in EXISTING_CANDIDATE_FILES:
        for row in load_rows(cand_path):
            existing_keys.add(row_key(row))

    # Filter available rows
    available_rows = [r for r in corpus_rows if row_key(r) not in existing_keys]
    if len(available_rows) < args.extra_size:
        raise SystemExit(
            f"Requested {args.extra_size} new rows but only {len(available_rows)} remain after exclusions."
        )

    extra_rows = random.sample(available_rows, args.extra_size)

    # Ensure required columns exist
    for row in extra_rows:
        row.setdefault("has_ground_truth", "0")
        row.setdefault("latitude/longitude", "")

    # ---------------------------------------------------------------------
    # Write output
    # ---------------------------------------------------------------------
    output_path = SCRIPT_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(extra_rows[0].keys()))
        writer.writeheader()
        writer.writerows(extra_rows)

    print(f"Sampled {len(extra_rows)} new candidates → {output_path.relative_to(SCRIPT_DIR)}")


if __name__ == "__main__":
    main() 