#!/usr/bin/env python3
"""cp_extract_volume2.py

Parse Cavaliers & Pioneers abstracts (Volume II, books 6–8) into a structured CSV
matching the schema used by cp_grants.csv in the OSS validation repo.

Input CSV format (from books6-8.csv):
    volume,book,raw_entry

Output CSV format (cp_grants-style):
    grant_id,name_std,acreage,year,county_text,raw_entry

grant_id convention: "<VOLUME>_<BOOK>_<ROW_INDEX>" e.g., "II_6_0".
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import pandas as pd


# ---------------------------------------------------------------------------
# Regex patterns (ported from oss_preprocessing/cp_extract.py)
# ---------------------------------------------------------------------------

# Title words to strip
_TITLE_RE = re.compile(r"^(?:COL\.|CAPT\.|MR\.?\,|MRS\.|LT\.|MAJ\.|GEN\.|DR\.)\s+", re.IGNORECASE)
# Name ends at first comma
_NAME_RE = re.compile(r"^([A-Za-z .'&\-]{3,}?),")
# Acreage like "5000a", "400 acres", "99.5 acs." etc.
_ACRE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*a(?:c|cs|cres|res)?\.?", re.IGNORECASE)
# 4-digit year pattern
_YEAR_RE = re.compile(r"(16|17|18)\d{2}")
# Capture words before Co/County/City/Go (handle OCR corruption)
_COUNTY_RE = re.compile(
    r"([A-Z][A-Za-z &'\.\-:8é!]{2,15})"  # candidate county words
    r"\s*[,:';]?\s*"
    r"(?:Co|Go)\b"                      # explicit word-boundary after Co/Go
    r"(?:\s+[a-z]{1,3})?"               # allow trailing OCR garbage like 'cn'
    r"\s*[\.,:;']?",
    re.IGNORECASE,
)

# Canonicalise common abbreviations / shorthand seen in OCR
_COUNTY_ABBR_MAP: Dict[str, str] = {
    # King & Queen
    "K&Q": "King & Queen",
    "KANDQ": "King & Queen",
    "KQ": "King & Queen",
    "K & Q": "King & Queen",
    "K 8& Q": "King & Queen",
    # Henrico
    "HNCO": "Henrico",
    "HN": "Henrico",
    # Spotsylvania
    "SPCO": "Spotsylvania",
    "SP": "Spotsylvania",
    "SPOTSYL": "Spotsylvania",
    "SPOTSYLVA": "Spotsylvania",
    "SPOTSYLV": "Spotsylvania",
    "SPOTSYLVANIA": "Spotsylvania",
    # Prince George variants
    "PR GEO": "Prince George",
    "PR. GEO": "Prince George",
    "PR GEO CO": "Prince George",
    "PR GEO.": "Prince George",
    "PR. GEO.": "Prince George",
    "PRGEO": "Prince George",
    "GEO": "Prince George",
    # Prince William shortcuts
    "PR WM": "Prince William",
    "PR. WM": "Prince William",
    # Brunswick
    "BRUNSW": "Brunswick",
    "BRUNSWCO": "Brunswick",
    # Appomattox
    "APCO": "Appomattox",
    # Frederick abbreviation
    "FREDERIC": "Frederick",
    "FREDER": "Frederick",
    # Charles City abbreviations
    "CHAS": "Charles City",
    "CHASCITY": "Charles City",
    "CHARLESCITY": "Charles City",
    "CHAS CITY": "Charles City",
    # Princess Anne
    "PRANNE": "Princess Anne",
    "PRINCEANNE": "Princess Anne",
    "PRINCESSAN": "Princess Anne",
    "ANNE": "Princess Anne",
    # Isle of Wight
    "WIGHT": "Isle Of Wight",
    "ISLEWIGHT": "Isle Of Wight",
    "ISOFWIGHT": "Isle Of Wight",
    "ISLEOFWIGHT": "Isle Of Wight",
    "IS OF WIGHT": "Isle Of Wight",
    # James City
    "JAMES": "James City",
    "JAMESCITY": "James City",
    "JAS": "James City",
    # Gloucester misspell
    "GLOCESTER": "Gloucester",
    "GLOUCESTER": "Gloucester",
    # Nansemond misspell
    "NANSAMOND": "Nansemond",
    "NANSEMOND": "Nansemond",
    "NANSEMND": "Nansemond",
    # Norfolk abbreviations
    "NORF": "Norfolk",
    "NORFOL": "Norfolk",
    "NORFOLK": "Norfolk",
    # Northampton abbreviations
    "NAMPTON": "Northampton",
    "NORTHAMPTON": "Northampton",
    "AMPTON": "Northampton",
    # King William
    "KINGWM": "King William",
    "KINGWILLIAM": "King William",
    # Surry variants
    "SURRV": "Surry",
    "SURRY": "Surry",
    # Essex variants
    "ESSEX": "Essex",
    "ESX": "Essex",
    "ESSX": "Essex",
    # Elizabeth City
    "ELIZ": "Elizabeth City",
    "ELIZABETH": "Elizabeth City",
    "ELIZ CITY": "Elizabeth City",
    "ELIZCITY": "Elizabeth City",
    "ELIZA CITY": "Elizabeth City",
    "ELIZA": "Elizabeth City",
    # King William truncation fixes
    "WM": "King William",
    "KING WM": "King William",
    # James City truncation fixes
    "JAS CITY": "James City",
    "JASCITY": "James City",
    # Handle common "Of X" patterns
    "OF WIGHT": "Isle Of Wight",
    "OF NANSEMOND": "Nansemond",
    "OF SURRY": "Surry",
    "OF HANOVER": "Hanover",
    "OF PR GEO": "Prince George",
    "OF K & Q": "King & Queen",
    "OF HENRICO": "Henrico",
    "OF MIDDLESEX": "Middlesex",
    "OF JAMES CITY": "James City",
    "OF YORK": "York",
    "OF GLOUCESTER": "Gloucester",
    "OF NANSAMOND": "Nansemond",
    "OF NENSEMOND": "Nansemond",
    # Handle "In X" patterns
    "IN K & Q": "King & Queen",
    "IN HENRICO": "Henrico",
    "IN KING WM": "King William",
    "IN HANOVER": "Hanover",
    "IN SPOTSYL": "Spotsylvania",
    "IN PR GEO": "Prince George",
    "IN ESSEX": "Essex",
    "IN CHAS CITY": "Charles City",
    "IN ACCOMACK": "Accomack",
    "IN SURRY": "Surry",
    "IN ELIZA": "Elizabeth City",
    "IN GLOUCESTER": "Gloucester",
    "IN NEW KENT": "New Kent",
    "IN KING & QUEEN": "King & Queen",
    "IN WARWICK": "Warwick",
    "IN GOOCHLAND": "Goochland",
    # Handle "Acs X" patterns (acres in X county)
    "ACS K & Q": "King & Queen",
    "ACS NORF": "Norfolk",
    "ACS MIDDLESEX": "Middlesex",
    "ACS HENRICO": "Henrico",
    "ACS YORK": "York",
    "ACS CHAS CITY": "Charles City",
    "ACS NEW KENT": "New Kent",
    "ACS NANSEMOND": "Nansemond",
    "ACS ACCOMACK": "Accomack",
    "ACS SURRY": "Surry",
    "ACS WARWICK": "Warwick",
    "ACS GOOCHLAND": "Goochland",
    "ACS GLOCESTER": "Gloucester",
    "ACS JAS CITY": "James City",
    "ACS PR ANNE": "Princess Anne",
    # Common misspellings / OCR noise
    "HENTICO": "Henrico",
    "HENSICO": "Henrico",
    "SURTY": "Surry",
    "GLOSTER": "Gloucester",
    "GLOUSTER": "Gloucester",
    "PR ANN": "Princess Anne",
    "SPOTSYLY": "Spotsylvania",
    "SPOTYL": "Spotsylvania",
    "SPORSYL": "Spotsylvania",
    "SPOTSVL": "Spotsylvania",
    "SPOTSVLV": "Spotsylvania",
    "SPOTSVLY": "Spotsylvania",
    "IA SPOTSYL": "Spotsylvania",
    "YORKE": "York",
    "HENRI": "Henrico",
    "HENRICE": "Henrico",
    "NEW KENT": "New Kent",
    "NEWKENT": "New Kent",
    "NEW-KENT": "New Kent",
    "BRANSWICK": "Brunswick",
    "PZ ANN": "Princess Anne",
    "AC COMACK": "Accomack",
    "INKQ": "King & Queen",
    "IN K Q": "King & Queen",
    "IN K   Q": "King & Queen",
    "ACS K Q": "King & Queen",
    # Additional mappings
    "SPOTSY": "Spotsylvania",
    "IGHT": "Isle Of Wight",
    "OF WICHT": "Isle Of Wight",
    "IN PR ANNE": "Princess Anne",
}

_CANONICAL_COUNTIES = {
    "HENRICO","PRINCE GEORGE","SURRY","ISLE OF WIGHT","SPOTSYLVANIA","HANOVER","BRUNSWICK",
    "NANSEMOND","KING WILLIAM","GOOCHLAND","KING & QUEEN","NEW KENT","ESSEX","NORFOLK",
    "PRINCESS ANNE","CHARLES CITY","MIDDLESEX","JAMES CITY","GLOUCESTER","ACCOMACK",
    "CAROLINE","WARWICK","YORK","NORTHAMPTON","ELIZABETH CITY"
}


def _normalise_name(raw: str) -> str:
    raw = _TITLE_RE.sub("", raw).strip()
    if "," in raw:
        raw = raw.split(",", 1)[0]
    return " ".join(w.capitalize() for w in raw.split())


def _normalise_county(raw: str) -> Optional[str]:
    key = re.sub(r"[^A-Za-z ]", "", raw)
    key = re.sub(r"\s+", " ", key).strip().upper()
    mapped = _COUNTY_ABBR_MAP.get(key)
    if mapped:
        return mapped
    key_no_space = key.replace(" ", "")
    mapped = _COUNTY_ABBR_MAP.get(key_no_space)
    if mapped:
        return mapped
    candidate = " ".join(w.capitalize() for w in raw.split())
    if candidate.upper() not in _CANONICAL_COUNTIES:
        return None
    return candidate


def _extract_from_text(text: str) -> Tuple[Optional[str], Optional[float], Optional[int], Optional[str]]:
    name: Optional[str] = None
    acreage: Optional[float] = None
    year: Optional[int] = None
    county: Optional[str] = None

    clean = text.replace("\u2014", "-").replace("\u2013", "-")
    clean = re.sub(r"\s+", " ", clean.strip())
    head = clean[:800]

    m_name = _NAME_RE.match(head)
    if m_name:
        candidate = _normalise_name(m_name.group(1))
        if candidate.lower() != "same":
            name = candidate

    m_ac = _ACRE_RE.search(head)
    acre_end = 0
    if m_ac:
        try:
            acreage = float(m_ac.group(1))
        except ValueError:
            pass
        acre_end = m_ac.end()

    year_match = None
    if m_ac:
        year_match = _YEAR_RE.search(head[m_ac.end():])
    if year_match is None:
        year_match = _YEAR_RE.search(head)
    if year_match is None and m_ac:
        year_match = _YEAR_RE.search(clean[m_ac.end():])
    if year_match is None:
        ocr_match = re.search(r"[iI\(](6|7|8)\d{2}", head)
        if ocr_match:
            yr_str = '1' + ocr_match.group(1) + ocr_match.group(0)[2:]
            try:
                yr_int = int(yr_str)
                if 1600 <= yr_int <= 1932:
                    year = yr_int
            except ValueError:
                pass
    else:
        yr_int = int(year_match.group(0))
        if 1600 <= yr_int <= 1932:
            year = yr_int

    if name is None and m_ac:
        pre = head[:m_ac.start()].strip()
        pre = re.sub(r"\bof\s+[A-Z].*", "", pre, flags=re.IGNORECASE)
        pre = re.split(r",|\.", pre)[0].strip()
        if 3 <= len(pre) <= 60 and pre.lower() != "same":
            name = _normalise_name(pre)

    def _clean_raw_cty(raw: str) -> str:
        raw = raw.replace(".", "").replace("8&", "&").replace("::", "s").replace("é", "e").replace("ém", "e")
        raw = re.sub(r"['`]", "", raw)
        raw = re.sub(r"\s+", " ", raw)
        if ' of ' in raw.lower():
            raw = raw.split(' of ')[-1]
        raw = raw.strip().lstrip('-')
        if raw.upper().startswith(('UP', 'LOW')):
            tokens = raw.split()
            if len(tokens) > 1:
                raw = ' '.join(tokens[1:])
        if raw.lower().startswith('is') and 'wight' in raw.lower():
            return 'Is of Wight'
        if raw.upper().startswith(('ACS ', 'AES ')):
            raw = raw[4:].strip()
        raw = re.sub(r'^[\d% ]+', '', raw)
        return raw

    county_candidates: List[str] = []
    if acre_end > 0:
        for m in _COUNTY_RE.finditer(head):
            if m.start() > acre_end:
                raw_cty = _clean_raw_cty(m.group(1))
                if raw_cty.lower() == "same":
                    continue
                norm_cty = _normalise_county(raw_cty)
                if norm_cty and norm_cty.upper() not in {"PAR", "PARISH", "SAME"}:
                    county_candidates.append(norm_cty)
    if not county_candidates:
        for m in _COUNTY_RE.finditer(head):
            raw_cty = _clean_raw_cty(m.group(1))
            if raw_cty.lower() == "same":
                continue
            norm_cty = _normalise_county(raw_cty)
            if norm_cty and norm_cty.upper() not in {"PAR", "PARISH", "SAME"}:
                county_candidates.append(norm_cty)
    if not county_candidates:
        for m in _COUNTY_RE.finditer(clean):
            raw_cty = _clean_raw_cty(m.group(1))
            if raw_cty.lower() == "same":
                continue
            norm_cty = _normalise_county(raw_cty)
            if norm_cty and norm_cty.upper() not in {"PAR", "PARISH", "SAME"}:
                county_candidates.append(norm_cty)
    if county_candidates:
        county = county_candidates[0]

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
    p = argparse.ArgumentParser(description="Extract cp_grants-style table for Volume II")
    p.add_argument("--input", type=Path, default=Path("../combined/books6-8.csv"))
    p.add_argument("--output", type=Path, default=Path("../combined/cp_grants_volume2.csv"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    build_cp_grants_table(args.input, args.output)


if __name__ == "__main__":
    main()


