#!/usr/bin/env python3
"""cp_extract_gray_nn.py

Parse Gray Northern Neck abstracts into cp_grants-style CSV.

Input CSV (combined/books_combined.csv):
  volume,book,raw_entry

Output CSV:
  grant_id,name_std,acreage,year,county_text,raw_entry
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import pandas as pd

# Reuse proven extractor from Volume 2 codebase
VOL2_CODE_DIR = "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/code"
if VOL2_CODE_DIR not in sys.path:
    sys.path.append(VOL2_CODE_DIR)
from cp_extract_volume2 import _extract_from_text as _base_extract_from_text  # type: ignore
from cp_extract_volume2 import _normalise_county  # type: ignore

# Patterns for Gray-specific fallback
_OF_COUNTY_RE = re.compile(r"\bof\s+([A-Z][A-Za-z '&\u2018\u2019\.-]{2,25})\s+(?:Co\.?|Cnty|County|City|Citty)\b", re.IGNORECASE)
_SAID_COUNTY_REF_RE = re.compile(r"\bin\s+(?:the\s+)?(?:sd\.|said)\s+(?:co\.?|cnty|county|city|citty)\b", re.IGNORECASE)
# Parish ... <County> Co. pattern
_PARISH_COUNTY_RE = re.compile(
    r"\b(?:in\s+)?(?:St\.?\s+)?[A-Z][A-Za-z\.'\u2018\u2019\- ]+?\s+Par(?:\.|ish)?\.?\s+([A-Z][A-Za-z '&\u2018\u2019\.-]{2,25})\s+(?:Co\.?|Cnty|County|City|Citty)\b",
    re.IGNORECASE,
)


def _extract_from_text(text: str) -> Tuple[Optional[str], Optional[float], Optional[int], Optional[str]]:
    """Gray-aware wrapper around the base extractor.

    Fallbacks:
    - If county is None and text has "in said Co./County" while the header has
      "of X Co.", infer county X.
    - If county is still None and we find "<Parish> Par. <County> Co.", use that county.
    """
    name, acreage, year, county = _base_extract_from_text(text)

    if county is None and _SAID_COUNTY_REF_RE.search(text):
        m_of = _OF_COUNTY_RE.search(text[:300])  # look near the start/headline
        if m_of:
            raw_cty = m_of.group(1).strip()
            norm = _normalise_county(raw_cty)
            county = norm or " ".join(w.capitalize() for w in raw_cty.split())

    if county is None:
        m_par = _PARISH_COUNTY_RE.search(text)
        if m_par:
            raw_cty = m_par.group(1).strip()
            norm = _normalise_county(raw_cty)
            county = norm or " ".join(w.capitalize() for w in raw_cty.split())

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
    print(f"Gray abstracts parsed: {extracted}/{len(df)} fully-extracted rows. → {output_csv}")
    print(f"'Same' entries found: {same_count}")

    return df


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract cp_grants-style table for Gray Northern Neck")
    p.add_argument("--input", type=Path, default=Path("../combined/books_combined.csv"))
    p.add_argument("--output", type=Path, default=Path("../combined/cp_grants_gray_nn.csv"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    build_cp_grants_table(args.input, args.output)


if __name__ == "__main__":
    main()
