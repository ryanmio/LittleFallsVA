#!/usr/bin/env python3
"""Cross-match 1723 Stafford County rent roll with pre-1724 land-patent holders.

This script implements a "risk-set" approach to match land patents with rent-roll entries.
It considers owners who had reached their improvement covenant deadline by the roll date.

Key parameters:
- ROLL_YEAR: The year of the rent roll (default: 1723)
- IMPROVEMENT_PERIOD: Months given to patent holders to establish improvements (default: 12)
- YEAR_CUTOFF: The latest year a patent could be issued to be eligible (default: roll - improvement)

The script does the following:
1. Parses all markdown files in ../S/land-grants/patent_bounds/ to extract
   grantee names and the earliest 4-digit year mentioned near the top of
   each file (usually the patent year).
2. Retains only patents with *year ≤ YEAR_CUTOFF* (i.e., owners who were liable
   for quit-rents by the roll date) from any patent in the patent_bounds directory.
3. Extracts the *surname* and *first initial* for each unique patent holder.
4. Reads the 1723 Stafford County rent-roll transcription and extracts
   surnames and first initials from the first column of each data row.
5. Computes:
     • *k* – number of patent-holder entries that appear on the rent roll (matching both surname and first initial when available).
     • *n* – total number of unique patent-holder entries from patents dated ≤ YEAR_CUTOFF.
6. Prints the match report and Beta-prior parameters that would populate
   `rent-rolls_patent_holders_1723.md`.
7. If run with the `--update` flag, the script will patch that markdown
   file, filling in `k`, `n`, `alpha`, `beta`, `mean`, and the 95 % CI.

USAGE
-----
    python crossmatch_patents_rentroll.py [--update] [--year-cutoff YEAR] [--improvement-period MONTHS]

Dependencies: only the Python stdlib (re, pathlib, argparse, math, yaml).

Notes
-----
• Owner-name normalisation extracts both surname and first initial.
• First initial matching prevents false positives like "Gabriel Adams" matching "John Adams".
• Rent-roll entries with honorifics ("Col", "Capt") or status tags
  ("orph", "heirs", "widd") are stripped before name extraction.
• For geographic filtering, future versions could incorporate spatial data
  to limit to a specific radius, but the current approach uses all available patents.
"""

from __future__ import annotations
import argparse
import math
import re
import datetime
from pathlib import Path
from typing import List, Set, Tuple, Dict, Optional

import yaml  # PyYAML

# --------------------------------------------------
# Path configuration (relative to this script's dir)
# --------------------------------------------------
THIS_DIR = Path(__file__).resolve().parent               # …/data/S/rent-rolls
DATA_S_DIR = THIS_DIR.parent                             # …/data/S
PROJECT_ROOT = DATA_S_DIR.parent                         # …/data
ROOT_DIR = PROJECT_ROOT.parent                           # …/1699-claim

# Paths
PATENT_DIR = DATA_S_DIR / "land-grants" / "patent_bounds"   # All patent markdowns
RENTROLL_FILE = ROOT_DIR.parent.parent / "primary_sources" / "Prince William County Government" / "stafford-county-rent-roll-1723-full.md"
EVIDENCE_MD = DATA_S_DIR / "rent-rolls_patent_holders_1723.md"  # Updated location

# Default parameters - these can be overridden with CLI arguments
ROLL_YEAR = 1723  # Default rent roll year
IMPROVEMENT_PERIOD = 12  # Default improvement period in months
YEAR_CUTOFF = ROLL_YEAR  # Default to cutoff = roll year
ALPHA0, BETA0 = 1, 1  # Uniform hyper-prior

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def extract_name_parts(name: str) -> Tuple[str, Optional[str]]:
    """Return (lower-case surname, first initial) from a full name.
    
    Non-alphabetic chars are stripped. First initial may be None if not available.
    """
    # Handle special case for suffixes like "Sr." or "Jr."
    normalized = name.lower().strip()
    
    # Remove common honorifics
    normalized = re.sub(r"(^|\s)(capt|col|dr|rev|mr|mrs|miss|ms)\.?\s", " ", normalized)
    
    # Skip suffixes for surname extraction
    suffix_match = re.search(r"\s+(sr|jr|[ivx]+)\.?$", normalized)
    suffix = ""
    if suffix_match:
        suffix = suffix_match.group(1)
        normalized = normalized[:suffix_match.start()]
    
    # Clean and get tokens
    clean = re.sub(r"[^a-z ]", " ", normalized)
    tokens = [t for t in clean.split() if t]
    
    if not tokens:
        return "", None
        
    # Extract first initial if available
    first_initial = None
    if len(tokens) > 1:
        first_initial = tokens[0][0] if tokens[0] else None
    
    # For compound surnames with 'van', 'de', etc., keep multiple tokens
    if len(tokens) > 1 and tokens[-2] in ('van', 'de', 'la', 'du', 'del'):
        return f"{tokens[-2]} {tokens[-1]}", first_initial
    
    return tokens[-1], first_initial

def surname(name: str) -> str:
    """Return just the surname portion (for backward compatibility)."""
    surname_part, _ = extract_name_parts(name)
    return surname_part


def extract_patent_info(md_path: Path) -> Tuple[List[Tuple[str, str, Optional[str]]], int | None]:
    """Extract owner names and the first 4-digit year from a patent markdown.
    
    Returns:
    - List of tuples (original_name, surname, first_initial)
    - Patent year (or None if not found)
    """
    owners: List[Tuple[str, str, Optional[str]]] = []
    year: int | None = None
    pattern_year = re.compile(r"(1[6-9]\d{2})")
    filename = md_path.name
    
    # Skip template file
    if filename == "patent_template.md":
        return [], None

    with md_path.open() as f:
        content = f.read()
        
        # Check for grantee section
        grantee_match = re.search(r"\*\*Grantee(?:s)?\:\*\*\s*([^\n]+)", content)
        if grantee_match:
            grantee_text = grantee_match.group(1)
            # Clean up parentheticals
            grantee_text = re.sub(r"\([^)]*\)", "", grantee_text)
            # Split on various separators
            for part in re.split(r"&| and | \& ", grantee_text):
                part = part.strip()
                if part:
                    # Handle special case for Fitzhugh which is sometimes in the file name
                    if "fitzhugh" in md_path.stem.lower() and "fitzhugh" not in part.lower():
                        original_name = "William Fitzhugh"
                        surname_part, first_initial = "fitzhugh", "w"
                    else:
                        original_name = part
                        surname_part, first_initial = extract_name_parts(part)
                    
                    owners.append((original_name, surname_part, first_initial))
        
        # Check for year
        date_match = re.search(r"\*\*Date Issued:\*\*\s*([^\n]+)", content)
        if date_match:
            year_match = pattern_year.search(date_match.group(1))
            if year_match:
                year = int(year_match.group(1))
    
    # Print debug info for checking
    if not owners:
        print(f"WARNING: No owners found in {filename}")
        # Special case for readme and template
        if filename.lower() != "readme.md" and filename != "patent_template.md":
            # Try to extract from filename
            name_parts = md_path.stem.split('_')
            if len(name_parts) >= 2 and name_parts[0] != "patent":
                # Build a name from first two parts
                first_name = name_parts[0].capitalize()
                last_name = name_parts[1].capitalize()
                original_name = f"{first_name} {last_name}"
                owners.append((original_name, last_name.lower(), first_name[0].lower()))
                print(f"  Extracted {original_name} from filename")
    elif year is None:
        owner_names = [o[0] for o in owners]
        print(f"INFO: No year found in {filename} for owners: {owner_names}")
    else:
        owner_names = [o[0] for o in owners]
        print(f"INFO: Found {owner_names} ({year}) in {filename}")
        
    return owners, year


def gather_patent_entries(year_cutoff: int) -> List[Tuple[str, str, Optional[str]]]:
    """Return list of unique (original_name, surname, first_initial) for patents with year ≤ year_cutoff.

    If a patent markdown lacks an explicit year, we conservatively *include* it
    (assuming it could be ≤ year_cutoff).
    """
    patent_entries: List[Tuple[str, str, Optional[str]]] = []
    unique_entries: Set[Tuple[str, Optional[str]]] = set()  # (surname, first_initial) for deduplication
    patent_count = 0
    included_count = 0
    readme_count = 0
    included_patents = []

    for md_file in PATENT_DIR.glob("*.md"):
        patent_count += 1
        
        # Skip README
        if md_file.stem.lower() == "readme":
            readme_count += 1
            continue
            
        owners, year = extract_patent_info(md_file)
        include = (year is None) or (year <= year_cutoff)
        if not include:
            continue
        
        included_count += 1
        included_patents.append((md_file.stem, year, [o[0] for o in owners]))
        
        for original_name, surname_part, first_initial in owners:
            # Only add unique surname/initial combinations
            key = (surname_part, first_initial)
            if key not in unique_entries and surname_part:
                unique_entries.add(key)
                patent_entries.append((original_name, surname_part, first_initial))
            
    print(f"\nProcessed {patent_count} patent files ({readme_count} README files skipped)")
    print(f"Included {included_count} patents with year ≤ {year_cutoff} or unknown year:")
    for patent_name, patent_year, patent_owners in sorted(included_patents, key=lambda x: (x[1] or 9999, x[0])):
        year_str = str(patent_year) if patent_year else "unknown"
        print(f"  - {patent_name}: {year_str} - {', '.join(patent_owners)}")
    
    # Output unique entries for debugging
    surnames_list = sorted(set(entry[1] for entry in patent_entries))
    print(f"\nUnique surnames extracted: {', '.join(surnames_list)}")
    return patent_entries


def gather_rentroll_entries() -> Tuple[List[Tuple[str, str, Optional[str]]], List[List[str]]]:
    """Extract surname and first initial from the 1723 rent roll.
    
    Returns tuple of:
    - list of (original_name, surname, first_initial) tuples
    - full_entries: list of complete table row entries [name, acres, tobacco, money, notes]
    """
    pattern_strip = re.compile(r"\b(orps?|orph\*?|heirs?|widd[\w\d]*|capt?\.?|col\.?|maj\.?|rev\.?|idem|sen')\b", re.I)
    rent_roll_entries: List[Tuple[str, str, Optional[str]]] = []
    names_found = 0
    lines_processed = 0
    full_entries = []    # Keep complete table rows for validation
    
    # Pattern to detect table header lines
    header_pattern = re.compile(r"\|\s*persons\s+Names\s*\|", re.I)

    with open(RENTROLL_FILE) as f:
        for line in f:
            lines_processed += 1
            line = line.strip()
            if not line.startswith("|"):
                continue
            
            # Skip table header lines
            if header_pattern.search(line):
                continue
            
            cells = [c.strip() for c in line.split("|")]
            if len(cells) < 2:
                continue
            
            raw_name = cells[1]
            # Store full entry for validation
            if len(cells) >= 5:
                full_entries.append(cells[1:6])  # [name, acres, tobacco, money, notes]
            
            # Clean up the name
            cleaned_name = pattern_strip.sub("", raw_name)
            if not cleaned_name.strip():
                continue
                
            surname_part, first_initial = extract_name_parts(cleaned_name)
            if surname_part:
                names_found += 1
                rent_roll_entries.append((raw_name, surname_part, first_initial))
                
    print(f"\nProcessed {lines_processed} lines in rent roll")
    print(f"Found {names_found} names in rent roll")
    
    # Print sample of extracted names
    print("\nSample of extracted names from rent roll:")
    for i, (raw, surname_part, first_initial) in enumerate(sorted(rent_roll_entries)[:10]):
        init_str = first_initial if first_initial else "None"
        print(f"  {i+1}. '{raw}' -> surname: '{surname_part}', initial: '{init_str}'")
    
    return rent_roll_entries, full_entries


def beta_ci(alpha: float, beta: float, prob: float = 0.95) -> Tuple[float, float]:
    from math import erf, sqrt
    # Rough normal approximation for 95 % CI if scipy not available
    mean = alpha / (alpha + beta)
    var = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
    z = 1.96  # for 95 %
    half_width = z * math.sqrt(var)
    return max(0.0, mean - half_width), min(1.0, mean + half_width)


def calculate_cutoff_year(roll_year: int, improvement_period: int) -> int:
    """Calculate the year cutoff based on roll year and improvement period.
    
    Patents issued after this cutoff would not yet be required to have
    improvements and thus not subject to quit-rent in the roll year.
    
    Args:
        roll_year: Year of the rent roll
        improvement_period: Months given to establish improvements
        
    Returns:
        Year cutoff (int)
    """
    # Convert months to years (integer division, floor)
    years_lag = improvement_period // 12
    # If partial year remains, subtract one more year
    if improvement_period % 12 > 0:
        years_lag += 1
    # Calculate cutoff
    return roll_year - years_lag


# --------------------------------------------------
# Main CLI
# --------------------------------------------------

def main(update: bool = False, roll_year: int = ROLL_YEAR, improvement_period: int = IMPROVEMENT_PERIOD, 
         year_cutoff: Optional[int] = None) -> None:
    """Run the cross-match analysis.
    
    Args:
        update: Whether to update the evidence file
        roll_year: Year of the rent roll
        improvement_period: Months given to establish improvements
        year_cutoff: Latest patent year to include (default: calculate from roll_year and improvement_period)
    """
    # Calculate cutoff if not provided
    if year_cutoff is None:
        year_cutoff = calculate_cutoff_year(roll_year, improvement_period)
    
    # Print analysis parameters
    print(f"===== ANALYSIS PARAMETERS =====")
    print(f"Rent Roll Year: {roll_year}")
    print(f"Improvement Period: {improvement_period} months")
    print(f"Year Cutoff: {year_cutoff} (patents must be issued by this year to be liable for quit-rent)")
    print(f"================================")
    
    # Get all patents with their full name information
    patent_entries = gather_patent_entries(year_cutoff)
    rentroll_entries, full_entries = gather_rentroll_entries()

    # Handle variant spellings of common names - keep these in sync with first_initial matches
    name_aliases = {
        "pearson": ["pearson", "pierson", "parson", "peirson", "person"],
        "fitzhugh": ["fitzhugh", "fitz hugh", "fitz"],
        "trammell": ["trammell", "trammel", "tramell"],
        "darrell": ["darrell", "dorrell", "darell"],
        "sr": ["senior", "sen", "sr"],  # Skip Sr. suffix entirely
        "adams": ["adams", "adam"],
        "going": ["going", "goin", "gowen"],
        "harrison": ["harrison", "harryson"],
        "harle": ["harle", "harl", "hurle"],
        "brown": ["brown", "browne"],
        "payne": ["payne", "paine", "pain"],
        "reagan": ["reagan", "regan"],
        "gunnell": ["gunnell", "gunnel", "gunnel"],
        "broadwater": ["broadwater", "brodwater"],
        "neale": ["neale", "neel", "neal"],
        "junior": ["junior", "jr"],
    }
    
    # First initial aliases - handle abbreviations and variants
    initial_aliases = {
        "w": ["will", "william", "wm", "w"],
        "j": ["john", "jonathan", "j"],
        "t": ["thomas", "thos", "t"],
        "g": ["gabriel", "g"],
        "s": ["simon", "samuel", "s"],
        "c": ["charles", "chris", "c"],
        "m": ["michael", "m"],
    }
    
    # Create reverse lookup for surnames
    surname_alias_map = {}
    for primary, variants in name_aliases.items():
        for variant in variants:
            surname_alias_map[variant] = primary
    
    # Create reverse lookup for initials
    initial_alias_map = {}
    for primary, variants in initial_aliases.items():
        for variant in variants:
            initial_alias_map[variant[0].lower()] = primary
            
    # Extract rentroll lookup data
    rentroll_lookup = {}
    for raw_name, surname_part, first_initial in rentroll_entries:
        # Normalize surname and initial
        norm_surname = surname_alias_map.get(surname_part, surname_part)
        norm_initial = initial_alias_map.get(first_initial, first_initial) if first_initial else None
        
        # Create keys for both with and without initial
        key_with_init = (norm_surname, norm_initial)
        key_without_init = norm_surname
        
        # Add to lookup dictionary
        if key_with_init not in rentroll_lookup:
            rentroll_lookup[key_with_init] = []
        rentroll_lookup[key_with_init].append(raw_name)
        
        # Also add to surname-only index
        if key_without_init not in rentroll_lookup:
            rentroll_lookup[key_without_init] = []
        if raw_name not in rentroll_lookup[key_without_init]:
            rentroll_lookup[key_without_init].append(raw_name)
            
    # Find matches with normalized names and first initials
    matches = []
    non_matches = []
    match_details = {}  # Store match details for validation
    
    # Process each patent entry
    for original_name, surname_part, first_initial in patent_entries:
        # Normalize surname and initial
        norm_surname = surname_alias_map.get(surname_part, surname_part)
        norm_initial = initial_alias_map.get(first_initial, first_initial) if first_initial else None
        
        # First check for surname match in the rent roll
        if norm_surname in rentroll_lookup:
            matched = False
            conflict = False
            
            # Look for exact initial match if we have one
            if norm_initial and (norm_surname, norm_initial) in rentroll_lookup:
                matches.append((original_name, surname_part, first_initial))
                match_details[(surname_part, first_initial)] = [
                    f"matched '{raw_name}' with surname+initial" 
                    for raw_name in rentroll_lookup[(norm_surname, norm_initial)]
                ]
                matched = True
            
            # If not matched by exact initial, check if any rentroll entries have no initial
            if not matched:
                # Find all rent roll entries with this surname
                no_initial_entries = []
                for raw_name in rentroll_lookup[norm_surname]:
                    _, _, rent_initial = next((e for e in rentroll_entries if e[0] == raw_name), (None, None, None))
                    if rent_initial is None:
                        # Rent roll entry has no first initial - this is a match
                        no_initial_entries.append(raw_name)
                    elif norm_initial and rent_initial != norm_initial:
                        # Different first initial - this is a conflict
                        conflict = True
                
                # If we found entries with no first initial, it's a match
                if no_initial_entries:
                    matches.append((original_name, surname_part, first_initial))
                    match_details[(surname_part, first_initial)] = [
                        f"matched '{raw_name}' with surname only (no initial in rent roll)" 
                        for raw_name in no_initial_entries
                    ]
                    matched = True
            
            # If not matched and there's a conflict, this is a non-match
            if not matched and conflict:
                non_matches.append((original_name, surname_part, first_initial))
            # If not matched and no conflict (no entries found), also a non-match
            elif not matched:
                non_matches.append((original_name, surname_part, first_initial))
        else:
            # No surname match at all
            non_matches.append((original_name, surname_part, first_initial))
    
    k = len(matches)
    n = len(patent_entries)
    alpha, beta = ALPHA0 + k, BETA0 + n - k
    mean = alpha / (alpha + beta)
    ci_low, ci_high = beta_ci(alpha, beta)

    # Report
    print("\n=== Cross-Match Results ===")
    print(f"Year cutoff: {year_cutoff} (patents must be issued by this year to be included)")
    print(f"Patent holder entries: {n} total unique name entries (with given name when available)")
    print(f"k = {k} matches / n = {n} total")
    print(f"Posterior Beta({alpha:.1f}, {beta:.1f}) → mean = {mean:.3f}, 95 % CI ≈ [{ci_low:.3f}, {ci_high:.3f}]")
    
    # Show matches
    print("\nMatched patent entries:")
    for i, (original_name, surname_part, first_initial) in enumerate(sorted(matches, key=lambda x: x[1])):
        init_str = f" ({first_initial})" if first_initial else ""
        print(f"  {i+1}. {original_name} - surname: {surname_part}{init_str}")
    
    # Show non-matches
    print("\nNon-matched patent entries:")
    for i, (original_name, surname_part, first_initial) in enumerate(sorted(non_matches, key=lambda x: x[1])):
        init_str = f" ({first_initial})" if first_initial else ""
        print(f"  {i+1}. {original_name} - surname: {surname_part}{init_str}")

    # Detailed validation - show complete entries for matched names
    print("\n\n=== MATCH VALIDATION ===")
    print("Showing complete rent roll entries for each matched surname:\n")
    
    # Collect all matches by surname for simplification in output
    surname_to_matches = {}
    for original_name, surname_part, first_initial in matches:
        key = surname_part
        if key not in surname_to_matches:
            surname_to_matches[key] = []
        surname_to_matches[key].append((original_name, first_initial))
    
    # For each matched surname, show the full entries
    for surname_part in sorted(surname_to_matches.keys()):
        patent_names = [f"{name} ({init})" if init else name for name, init in surname_to_matches[surname_part]]
        match_notes = []
        
        # Get all notes for this surname
        for name, first_initial in surname_to_matches[surname_part]:
            notes = match_details.get((surname_part, first_initial), [])
            match_notes.extend(notes)
        
        print(f"MATCH: '{surname_part}' - {match_notes}")
        print(f"  Patent entries: {', '.join(patent_names)}")
        
        # Find all rentroll entries with this surname
        rent_entries = []
        for raw_name, rent_surname, rent_initial in rentroll_entries:
            norm_rent_surname = surname_alias_map.get(rent_surname, rent_surname)
            norm_surname = surname_alias_map.get(surname_part, surname_part)
            if norm_rent_surname == norm_surname:
                rent_entries.append(raw_name)
        
        if rent_entries:
            print(f"  Found {len(rent_entries)} entries with this surname in rent roll")
            print("  FULL ENTRIES from rent roll:")
            
            # Find full entries for each extracted name
            entries_found = 0
            for entry in full_entries:
                full_name = entry[0]
                if any(name.replace(" ", "") in full_name.replace(" ", "") for name in rent_entries):
                    print(f"    - {' | '.join(entry)}")
                    entries_found += 1
                    
            if entries_found == 0:
                print("    WARNING: Could not locate complete entries in rent roll")
        else:
            print("  WARNING: No matching entries found in rent roll despite match")
    
    # Optional: update markdown evidence file
    if update:
        if not EVIDENCE_MD.exists():
            print(f"Evidence file not found: {EVIDENCE_MD}")
            return
        with open(EVIDENCE_MD) as f:
            text = f.read()
        if not text.lstrip().startswith('---'):
            print(f"Evidence file lacks YAML front-matter: {EVIDENCE_MD}")
            return
        front, body = text.split('---', 2)[1:]  # discard leading empty
        meta = yaml.safe_load(front)
        meta.update({
            'k': k,
            'n': n,
            'alpha': alpha,
            'beta': beta,
            'mean': round(mean, 4),
            'ci_lower': round(ci_low, 4),
            'ci_upper': round(ci_high, 4),
        })
        new_front = yaml.dump(meta, sort_keys=False)
        new_text = f"---\n{new_front}---{body}"
        with open(EVIDENCE_MD, 'w') as f:
            f.write(new_text)
        print(f"Evidence file updated: {EVIDENCE_MD}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cross-match patents with 1723 rent roll using a risk-set approach",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--update', action='store_true', help='Write results into evidence markdown')
    parser.add_argument('--roll-year', type=int, default=ROLL_YEAR, 
                        help='Year of the rent roll')
    parser.add_argument('--improvement-period', type=int, default=IMPROVEMENT_PERIOD, 
                        help='Months given to establish improvements')
    parser.add_argument('--year-cutoff', type=int, default=None,
                        help='Latest patent year to include (default: calculate from roll-year and improvement-period)')
    args = parser.parse_args()
    
    main(update=args.update, roll_year=args.roll_year, 
         improvement_period=args.improvement_period, 
         year_cutoff=args.year_cutoff) 