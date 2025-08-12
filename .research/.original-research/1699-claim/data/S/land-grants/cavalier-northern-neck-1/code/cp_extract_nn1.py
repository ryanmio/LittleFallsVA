#!/usr/bin/env python3
"""cp_extract_nn1.py

Parse Cavaliers & Pioneers abstracts (Northern Neck Supplement, NN1) into a
structured CSV matching the cp_grants schema used previously.

Input CSV format (from books_combined.csv):
    volume,book,raw_entry

Output CSV format (cp_grants-style):
    grant_id,name_std,acreage,year,county_text,raw_entry

grant_id convention: "<VOLUME>_<BOOK>_<ROW_INDEX>" e.g., "NN1_1_0".
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import pandas as pd

# Ensure we can import the proven extractor from the Volume 2 pipeline
VOL2_CODE_DIR = "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/code"
if VOL2_CODE_DIR not in sys.path:
    sys.path.append(VOL2_CODE_DIR)

from cp_extract_volume2 import (  # type: ignore
    _extract_from_text as _base_extract_from_text,
)

# Local lightweight county pattern for fallback within-entry resolution
_FALLBACK_COUNTY_RE = re.compile(
    r"([A-Z][A-Za-z &'\u2018\u2019\.\-:]{2,25})\s*(?:Co|Cnty|County|City|Citty)\b",
    re.IGNORECASE,
)

_SD_COUNTY_PAT = re.compile(r"\b(?:sd\.|said)\s+(?:co\.?|cnty|county|city|citty)\b", re.IGNORECASE)


def _extract_from_text(text: str) -> Tuple[Optional[str], Optional[float], Optional[int], Optional[str]]:
    """Wrapper around the base extractor that also resolves 'sd. county' to the
    last explicit county mentioned earlier in the same entry.
    """
    name, acreage, year, county = _base_extract_from_text(text)

    if county is None and _SD_COUNTY_PAT.search(text):
        # Find the last explicit county mention in the entry and reuse it
        candidates: List[str] = []
        for m in _FALLBACK_COUNTY_RE.finditer(text):
            token = m.group(1).strip()
            # Skip generic words
            if token.lower() in {"par", "parish", "same"}:
                continue
            candidates.append(token)
        if candidates:
            # Use the most recent explicit county cue in the entry
            county = " ".join(w.capitalize() for w in candidates[-1].split())

    return name, acreage, year, county


def build_cp_grants_table(input_csv: Path, output_csv: Path) -> pd.DataFrame:
    df_raw = pd.read_csv(input_csv)
    assert {"volume", "book", "raw_entry"}.issubset(df_raw.columns)

    records: List[Dict[str, object]] = []
    misses = 0
    same_count = 0
    prev_name: Optional[str] = None
    prev_year: Optional[int] = None
    prev_county: Optional[str] = None

    for idx, row in df_raw.iterrows():
        name, acreage, year, county = _extract_from_text(row.raw_entry)

        low_head = str(row.raw_entry).lstrip().lower()[:120]
        is_same_entry = low_head.startswith("same")
        if is_same_entry:
            same_count += 1
            same_loc = ("location" in low_head or "loc." in low_head or "co." in low_head or " county" in low_head)
            same_date = "date" in low_head
            if name is None and prev_name:
                name = prev_name
            if (same_loc or county is None) and prev_county:
                county = prev_county
            if (same_date or year is None) and prev_year:
                year = prev_year

        grant_id = f"{row.volume}_{row.book}_{idx}"
        if name is None or acreage is None or year is None or county is None:
            misses += 1
        records.append({
            "grant_id": grant_id,
            "name_std": name,
            "acreage": acreage,
            "year": year,
            "county_text": county,
            "raw_entry": row.raw_entry,
        })

        if not is_same_entry:
            if name and name.lower() != 'same':
                prev_name = name
            if year:
                prev_year = year
            if county:
                prev_county = county

    df = pd.DataFrame(records)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    extracted = len(df) - misses
    print(f"C&P abstracts parsed: {extracted}/{len(df)} fully-extracted rows. → {output_csv}")
    print(f"'Same' entries found: {same_count}")
    if misses:
        missing_name = df['name_std'].isna().sum()
        missing_acreage = df['acreage'].isna().sum()
        missing_year = df['year'].isna().sum()
        missing_county = df['county_text'].isna().sum()
        print(f"WARNING: {misses} rows missing at least one cue. Missing: {missing_name} names, {missing_acreage} acreage, {missing_year} years, {missing_county} counties")

    return df


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract cp_grants-style table for NN1 (Northern Neck Supplement)")
    p.add_argument("--input", type=Path, default=Path("../combined/books_combined.csv"))
    p.add_argument("--output", type=Path, default=Path("../combined/cp_grants_nn1.csv"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    build_cp_grants_table(args.input, args.output)


if __name__ == "__main__":
    main()
