#!/usr/bin/env python3
"""
Patent Abstract Extractor for Northern Virginia Land Grants (1660-1730)

This script extracts structured data from Cavaliers and Pioneers OCR text,
focusing on land grants in Northern Virginia counties during 1660-1730.

IMPORTANT VOLUME LIMITATIONS:
- Volume 1 (1623-1666): Available in OCR'd text form (cavalierspioneer00nuge_hocr_searchtext.txt)
- Volume 2 (1666-1695): Not currently available in OCR'd form
- Volume 3 (1695-1732): Not currently available in OCR'd form

These volume limitations severely impact our ability to analyze land grants after 1666,
particularly for the Northern Neck Proprietary grants that would be most relevant
for the Falls Church area circa 1699.

Input: OCR'd text from "Cavaliers and Pioneers" (Nugent)
Output: CSV with fields: grantee, acreage, county, date, snippet
"""

import re
import csv
import os
from datetime import datetime
import argparse
from pathlib import Path

# Constants
TARGET_COUNTIES = [
    'fairfax', 'loudoun', 'prince william', 'stafford', 'westmoreland', 
    'northumberland', 'lancaster', 'richmond', 'king george', 'arlington', 
    'alexandria'
]

DATE_RANGE = (1660, 1730)  # Min and max years to include

# Default paths for Volume 1 (1623-1666)
DEFAULT_INPUTS = {
    'vol1': '../patent_abstracts/cavalierspioneer00nuge_hocr_searchtext.txt',
    # Placeholders for future volumes if/when OCR'd text becomes available
    'vol2': None,  # 1666-1695
    'vol3': None   # 1695-1732
}

# Updated output paths to save in patent_abstracts folder
OUTPUT_CSV = '../patent_abstracts/northern_va_land_grants_1660_1730.csv'
SUMMARY_FILE = '../patent_abstracts/northern_va_land_grants_summary.md'

def extract_date(text):
    """Extract date from text in various formats."""
    # Try to find dates in format like "20 May 1639" or "May 20, 1639"
    date_patterns = [
        r'(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})',            # 20 May 1639
        r'([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})',          # May 20, 1639
        r'(\d{1,2})(?:th|st|nd|rd)?\s+of\s+([A-Za-z]+)\.?\s+(\d{4})',  # 20th of May 1639
        r'last\s+(?:day\s+)?of\s+([A-Za-z]+)\.?\s+(\d{4})',  # last of May 1639
        r'(?:in|anno)\s+(\d{4})',                           # in 1703 or anno 1703
        r'dated\s+(\d{1,2})?\s*([A-Za-z]+)?\s*(\d{4})',     # dated 5 June 1712 or dated 1712
    ]
    
    for pattern in date_patterns:
        matches = re.search(pattern, text, re.IGNORECASE)
        if matches:
            groups = matches.groups()
            
            # Handle different pattern matches based on group count
            if len(groups) == 1:  # Just year (e.g., "in 1703")
                year = groups[0]
                month_num = 1  # Default to January
                day = 1      # Default to 1st
            elif len(groups) == 2:  # Month and year (e.g., "last of May 1639")
                month, year = groups
                month_num = get_month_number(month) if month else 1
                day = 28  # Approximate for "last of month"
            else:  # Day, Month, Year (e.g., "20 May 1639")
                # Check order (could be day-month-year or month-day-year)
                try:
                    # Try assuming day-month-year
                    day, month, year = groups
                    day = int(day) if day else 1
                except ValueError:
                    # Must be month-day-year
                    month, day, year = groups
                    day = int(day) if day else 1
                
                month_num = get_month_number(month) if month else 1
            
            try:
                year = int(year)
                if DATE_RANGE[0] <= year <= DATE_RANGE[1]:
                    return f"{year}-{month_num:02d}-{int(day):02d}"
            except (ValueError, TypeError):
                pass
    
    # If no specific date found but year is in text, return year only
    year_pattern = r'\b(1[6-7][0-9][0-9])\b'  # Matches years 1600-1799
    year_matches = re.findall(year_pattern, text)
    
    # Filter to years in our target range
    valid_years = [int(y) for y in year_matches if DATE_RANGE[0] <= int(y) <= DATE_RANGE[1]]
    
    if valid_years:
        # Use the first valid year found
        return f"{valid_years[0]}-01-01"  # Default to January 1st when only year is known
    
    return None

def get_month_number(month_str):
    """Convert month name to number."""
    if not month_str:
        return 1
    
    month_mapping = {
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
        'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
        'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
        'nov': 11, 'november': 11, 'dec': 12, 'december': 12
    }
    
    try:
        return month_mapping[month_str.lower().strip('.')]
    except (KeyError, AttributeError):
        return 1  # Default to January if month can't be determined

def extract_acreage(text):
    """Extract acreage from text."""
    # Pattern: number followed by "acs." or "acres"
    acreage_patterns = [
        r'(\d{1,5}(?:,\d{3})?)(?:\s+|\-)(?:acs?\.?|acres?)',  # 200 acs. or 1,200 acres
        r'(\d{1,5}(?:,\d{3})?)(?:\s+|\-)(?:ac\.?)',           # 200 ac.
    ]
    
    for pattern in acreage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            acreage_str = match.group(1).replace(',', '')
            try:
                return int(acreage_str)
            except ValueError:
                pass
    
    return None

def extract_grantee(text):
    """Extract grantee name from text."""
    # Often the grantee is the first name in the entry
    first_line = text.split('\n')[0].strip()
    
    # Find names in ALL CAPS or special patterns indicating a grantee
    grantee_patterns = [
        r'^([A-Z][A-Z\s\.,]+),\s+\d+\s+acs',             # NAME, 200 acs.
        r'^([A-Z][A-Z\s\.,]+)(?:,|\sto\s|\.)(?!\s+acs)', # NAME, or NAME. or NAME to 
        r'^([A-Z][A-Z\s]+)$',                           # NAME by itself
    ]
    
    for pattern in grantee_patterns:
        match = re.search(pattern, first_line)
        if match:
            return match.group(1).strip(',. ')
    
    # If no pattern matched, use first words before first comma
    comma_split = first_line.split(',', 1)
    if comma_split:
        candidate = comma_split[0].strip()
        # Skip if it's too short or contains special patterns
        if len(candidate) > 3 and not re.search(r'\d+\s+acs\.?', candidate, re.IGNORECASE):
            return candidate
    
    return None

def extract_county(text):
    """Extract county from text, focusing on Northern Virginia counties."""
    # Look for county names followed by "Co." or "County"
    for county in TARGET_COUNTIES:
        county_patterns = [
            rf'\b{county}\s+Co\.?,', 
            rf'\b{county}\s+County\b',
            rf'\bin\s+{county}\b'
        ]
        
        for pattern in county_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return county.title()
    
    # Special case for Stafford, which might be mentioned differently
    if re.search(r'\bStafford\b', text, re.IGNORECASE) and not re.search(r'\bStafford[a-z]{2,}', text, re.IGNORECASE):
        return 'Stafford'
    
    # Check for mentions of Potomac River, which could indicate Northern VA
    if re.search(r'Potom|Patom', text, re.IGNORECASE) and not re.search(r'Stafford', text, re.IGNORECASE):
        # Check if any specific county is mentioned
        for county in ['Fairfax', 'Prince William', 'Stafford', 'King George']:
            if re.search(fr'\b{county}\b', text, re.IGNORECASE):
                return county
        
        # Default to Stafford for early Potomac grants
        year_match = re.search(r'\b1[67]\d\d\b', text)
        if year_match:
            year = int(year_match.group(0))
            if year < 1730:
                return 'Stafford'  # Most Potomac River grants before 1730 were in Stafford
    
    return None

def clean_text(text):
    """Clean up OCR artifacts."""
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove common OCR artifacts
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
    return text.strip()

def process_one_volume(input_file, volume_name, volume_period):
    """Process a single volume of the patent abstracts."""
    entries = []
    if not input_file or not os.path.exists(input_file):
        print(f"Skipping {volume_name} (not available) - covers {volume_period}")
        return entries
    
    print(f"Processing {volume_name} - covers {volume_period}...")
    
    # Read the entire file
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(f"Successfully read {volume_name} ({len(content)} characters)")
    except Exception as e:
        print(f"Error reading {volume_name}: {e}")
        return entries
    
    # Split the content into entries
    # Each entry typically starts with a name in ALL CAPS and contains acreage
    # We'll use this pattern to identify entries
    entry_pattern = r'([A-Z][A-Z\s\.,]+),\s+\d+\s+acs\.?'
    entry_indices = [m.start() for m in re.finditer(entry_pattern, content)]
    
    print(f"Found {len(entry_indices)} potential entries in {volume_name}")
    
    # Add the end of the file as the last index
    entry_indices.append(len(content))
    
    # Track date distribution for debugging
    date_distribution = {}
    
    # Process each entry
    for i in range(len(entry_indices) - 1):
        start = entry_indices[i]
        end = entry_indices[i + 1]
        entry_text = content[start:end].strip()
        
        # Basic cleaning
        entry_text = clean_text(entry_text)
        
        # Extract information
        grantee = extract_grantee(entry_text)
        acreage = extract_acreage(entry_text)
        date = extract_date(entry_text)
        county = extract_county(entry_text)
        
        # Track date distribution for reporting
        if date:
            year = int(date.split('-')[0])
            decade = (year // 10) * 10
            date_distribution[decade] = date_distribution.get(decade, 0) + 1
        
        # Skip entries without essential data
        if not grantee or not acreage or not date:
            continue
        
        # Skip entries outside our date range
        if date and not (DATE_RANGE[0] <= int(date.split('-')[0]) <= DATE_RANGE[1]):
            continue
        
        # Create entry dictionary
        entry = {
            'grantee': grantee,
            'acreage': acreage,
            'date': date,
            'county': county,
            'snippet': entry_text[:500] + ('...' if len(entry_text) > 500 else ''),
            'volume': volume_name
        }
        
        # If this is a Northern Virginia county, add to our list
        if county:
            entries.append(entry)
    
    print(f"Found {len(entries)} Northern Virginia land grants in {volume_name}")
    
    # Print date distribution for debugging
    print(f"\nDate distribution for {volume_name}:")
    for decade, count in sorted(date_distribution.items()):
        print(f"  {decade}s: {count} entries")
    
    return entries

def process_abstracts(input_files, output_csv):
    """Extract relevant land grant data from OCR'd text across multiple volumes."""
    all_entries = []
    
    # Process each volume
    for volume_name, input_file in input_files.items():
        if volume_name == 'vol1':
            volume_period = "1623-1666"
        elif volume_name == 'vol2':
            volume_period = "1666-1695"
        elif volume_name == 'vol3':
            volume_period = "1695-1732"
        else:
            volume_period = "unknown period"
        
        entries = process_one_volume(input_file, volume_name, volume_period)
        all_entries.extend(entries)
    
    # Sort entries by date
    all_entries.sort(key=lambda x: x['date'])
    
    print(f"\nTotal Northern Virginia land grants found: {len(all_entries)}")
    
    # Write the results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['grantee', 'acreage', 'county', 'date', 'snippet', 'volume']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in all_entries:
            writer.writerow(entry)
    
    print(f"Wrote {len(all_entries)} entries to {output_csv}")
    return all_entries

def generate_summary(entries, output_file, missing_volumes):
    """Generate a summary of land grants by decade."""
    print("Generating summary...")
    
    # Count grants by decade
    decades = {}
    counties = {}
    volumes = {}
    
    for entry in entries:
        if entry['date']:
            year = int(entry['date'].split('-')[0])
            decade = (year // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1
        
        if entry['county']:
            counties[entry['county']] = counties.get(entry['county'], 0) + 1
        
        if 'volume' in entry:
            volumes[entry['volume']] = volumes.get(entry['volume'], 0) + 1
    
    # Sort counts
    sorted_decades = sorted(decades.items())
    sorted_counties = sorted(counties.items(), key=lambda x: x[1], reverse=True)
    sorted_volumes = sorted(volumes.items())
    
    # Generate Markdown summary
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Northern Virginia Land Grants (1660-1730)\n\n")
        f.write("This summary provides an overview of land grants in Northern Virginia counties.\n\n")
        
        f.write("## Source Volumes and Limitations\n\n")
        f.write("**Cavaliers and Pioneers** by Nell Marion Nugent contains abstracts of Virginia Land Patents and Grants:\n\n")
        f.write("- **Volume 1 (1623-1666)**: Available and processed\n")
        f.write("- **Volume 2 (1666-1695)**: " + ("Available and processed" if 'vol2' not in missing_volumes else "Not available in OCR'd form") + "\n")
        f.write("- **Volume 3 (1695-1732)**: " + ("Available and processed" if 'vol3' not in missing_volumes else "Not available in OCR'd form") + "\n\n")
        
        # Note about volume limitations
        if missing_volumes:
            f.write("**IMPORTANT LIMITATION**: ")
            if 'vol2' in missing_volumes and 'vol3' in missing_volumes:
                f.write("Volumes 2 and 3 are not available in OCR'd form, which severely limits our analysis for the period 1666-1732. ")
            elif 'vol2' in missing_volumes:
                f.write("Volume 2 is not available in OCR'd form, which limits our analysis for the period 1666-1695. ")
            elif 'vol3' in missing_volumes:
                f.write("Volume 3 is not available in OCR'd form, which limits our analysis for the period 1695-1732. ")
            
            f.write("This is particularly significant because these volumes would include the Northern Neck Proprietary grants most relevant to the Falls Church area circa 1699.\n\n")
        
        f.write("## Data Extraction Process\n\n")
        f.write("The data was extracted from the OCR'd text of 'Cavaliers and Pioneers', ")
        f.write("focusing on Northern Virginia counties including Fairfax, Loudoun, Prince William, ")
        f.write("Stafford, Westmoreland, Northumberland, Lancaster, Richmond, King George, Arlington, and Alexandria.\n\n")
        
        f.write("## Chronological Distribution\n\n")
        f.write("| Decade | Number of Grants |\n")
        f.write("|--------|----------------:|\n")
        
        # Make sure all decades in our range are represented, even if zero
        for decade in range(DATE_RANGE[0], DATE_RANGE[1]+1, 10):
            count = decades.get(decade, 0)
            f.write(f"| {decade}s | {count} |\n")
        
        f.write("\n## County Distribution\n\n")
        f.write("| County | Number of Grants |\n")
        f.write("|--------|----------------:|\n")
        
        for county, count in sorted_counties:
            f.write(f"| {county} | {count} |\n")
        
        if sorted_volumes:
            f.write("\n## Volume Distribution\n\n")
            f.write("| Volume | Number of Grants |\n")
            f.write("|--------|----------------:|\n")
            
            for volume, count in sorted_volumes:
                f.write(f"| {volume} | {count} |\n")
        
        f.write("\n## Total Grants\n\n")
        f.write(f"Total Northern Virginia land grants from 1660-1730: **{len(entries)}**\n\n")
        
        f.write("## Data Quality Notes\n\n")
        f.write("- This data is based on OCR'd text and may contain errors or omissions.\n")
        f.write("- Some grants may be missing county information and thus not included in this analysis.\n")
        
        if missing_volumes:
            f.write("- The Northern Neck Proprietary grants (Lord Fairfax) are severely underrepresented due to missing volumes.\n")
        
        f.write("\n## Research Implications\n\n")
        if 'vol2' in missing_volumes and 'vol3' in missing_volumes:
            f.write("The significant gap in data for the period 1666-1730 means that this dataset alone is insufficient for analyzing ")
            f.write("the historical plausibility of settlement in the Falls Church area circa 1699. ")
        
        f.write("To address these limitations, we recommend:\n\n")
        f.write("1. Obtaining OCR'd versions of Volumes 2 and 3 of Nugent's compilation\n")
        f.write("2. Accessing the Northern Neck Grant Books directly from the Library of Virginia\n")
        f.write("3. Seeking county-specific historical records for Fairfax, Prince William, and Stafford counties\n\n")
        
        f.write("The current data does provide a baseline for understanding the earlier land settlement patterns in Northern Virginia, ")
        f.write("particularly along the Northern Neck peninsula (Lancaster, Northumberland, Westmoreland) in the 1660s, ")
        f.write("which preceded the inland settlement push toward what is now Falls Church.\n")
    
    print(f"Summary written to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Extract Northern Virginia land grant data from OCR text')
    parser.add_argument('--vol1', default=DEFAULT_INPUTS['vol1'], help='Input OCR text file for Volume 1 (1623-1666)')
    parser.add_argument('--vol2', default=DEFAULT_INPUTS['vol2'], help='Input OCR text file for Volume 2 (1666-1695), if available')
    parser.add_argument('--vol3', default=DEFAULT_INPUTS['vol3'], help='Input OCR text file for Volume 3 (1695-1732), if available')
    parser.add_argument('--output', default=OUTPUT_CSV, help='Output CSV file path')
    parser.add_argument('--summary', default=SUMMARY_FILE, help='Output summary markdown file')
    parser.add_argument('--debug', action='store_true', help='Print additional debug information')
    
    args = parser.parse_args()
    
    # Prepare input files
    input_files = {
        'vol1': args.vol1,
        'vol2': args.vol2,
        'vol3': args.vol3
    }
    
    # Track missing volumes
    missing_volumes = []
    for volume, file_path in input_files.items():
        if not file_path or not os.path.exists(file_path):
            missing_volumes.append(volume)
    
    # Create parent directories if they don't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.summary), exist_ok=True)
    
    # Process the abstracts
    entries = process_abstracts(input_files, args.output)
    
    # Generate a summary
    generate_summary(entries, args.summary, missing_volumes)
    
    print("Done!")

if __name__ == "__main__":
    main() 