"""create_coordinates_csv.py - Create a CSV with all coordinates for locatable grants.

This script generates a CSV containing grant numbers, text entries, ground truth coordinates,
and prediction coordinates for all methods (H-1, M-2, M-4, M-5, T-1, T-4).
"""

# Standard libs
import pandas as pd
from pathlib import Path
import sys
import re
import unicodedata

# Optional dependency for advanced text-fixing (mojibake, etc.)
try:
    import ftfy  # type: ignore

    def _fix_text(text: str) -> str:  # noqa: D401
        """Return text passed through ftfy.fix_text if library is present."""
        return ftfy.fix_text(text)

except ImportError:  # pragma: no cover – ftfy is optional

    def _fix_text(text: str) -> str:  # noqa: D401
        """Best-effort fallback when *ftfy* is unavailable.

        Tries a common mojibake repair by interpreting the text's bytes as
        Latin-1 and decoding them as UTF-8. If that fails, the original text
        is returned unchanged.
        """
        try:
            # Encode to bytes assuming the current (already-decoded) text was
            # *incorrectly* decoded from Latin-1; then decode those bytes
            # properly as UTF-8 to repair typical "Ã¤"-style issues.
            return text.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text

# More relaxed pattern to match various DMS formats
DEGREE_PATTERN = re.compile(r'(\d+)(?:[^\d\w]+|°|¬∞|¬¨‚àû)(\d+)(?:[^\d\w]+|\'|′)(\d+(?:\.\d*)?)(?:[^\d\w]+|"|″)([NSEW])', re.IGNORECASE)

# Paths
THIS_DIR = Path(__file__).resolve().parent
GEOLOCATION_DIR = THIS_DIR.parent.parent  # geolocation/
ANALYSIS_DIR = THIS_DIR.parent            # geolocation/analysis/

VAL_CSV = GEOLOCATION_DIR / "validation - TEST-FULL-H1.csv"
RES_CSV = ANALYSIS_DIR / "full_results.csv"
OUTPUT_CSV = THIS_DIR / "grant_coordinates_summary.csv"

def truncate_text(text, max_length=150):
    """Truncate text to max_length and add ellipsis if needed."""
    if not isinstance(text, str):
        return text
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def normalize_text(text: str):  # noqa: D401
    """Return *text* with common encoding issues repaired/normalized.

    Steps:
    1. Attempt to auto-repair mojibake using *ftfy* (if available).
    2. Replace curly quotes and similar typography with ASCII equivalents.
    3. Apply NFKD unicode normalisation to strip combining marks.
    """

    if not isinstance(text, str):
        return text

    # First, attempt automated fixing of mojibake / bad encodings
    text = _fix_text(text)

    # Replace common "smart" punctuation with ASCII equivalents
    replacements = {
        "’": "'",
        "‘": "'",
        "‚": "'",
        "“": '"',
        "”": '"',
        "″": '"',
        "′": "'",
        "–": "-",
        "—": "-",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Finally, normalise the string to NFKD form
    text = unicodedata.normalize("NFKD", text)

    return text

def normalize_coordinates(coord_text):
    """Fix encoding issues in coordinate text, especially degree signs."""
    if not isinstance(coord_text, str):
        return coord_text
    
    # For decimal coordinates (no degree sign issues)
    if ',' in coord_text and '°' not in coord_text and '¬' not in coord_text:
        return coord_text
    
    # Handle common encoding issues first
    coord_text = coord_text.replace('¬∞', '°').replace('¬¨‚àû', '°')
    
    # For DMS coordinates with encoding issues
    def replace_dms(match):
        deg, minutes, seconds, direction = match.groups()
        # Clean up any trailing zeros in seconds
        if '.' in seconds:
            seconds = seconds.rstrip('0').rstrip('.') if '.' in seconds else seconds
        return f"{deg}°{minutes}'{seconds}\"{direction}"
    
    # Try to fix broken degree coordinates
    coord_text = DEGREE_PATTERN.sub(replace_dms, coord_text)
    
    return coord_text

def main():
    print(f"Reading validation data from {VAL_CSV}")
    val = pd.read_csv(VAL_CSV)
    
    print(f"Reading results data from {RES_CSV}")
    res = pd.read_csv(RES_CSV)
    
    # Filter to only locatable grants (those with ground truth)
    locatable = val[(val["has_ground_truth"] == 1) & (val["latitude/longitude"].notna())]
    
    # Exclude grants 10 and 38
    excluded_grants = [10, 38]
    locatable = locatable[~locatable["results_row_index"].astype(int).isin(excluded_grants)]
    
    print(f"Found {len(locatable)} locatable grants")
    
    # Create output dataframe
    output_data = []
    
    # Define methods to include
    methods = ["H-1", "M-2", "M-4", "M-5", "T-1", "T-4"]
    
    # Prepare data
    for _, row in locatable.iterrows():
        row_idx = int(row["results_row_index"])
        
        # Get grant text entry - properly handle newlines and quotes
        grant_entry = str(row["raw_entry"]).replace("\n", " ").strip()
        grant_entry = truncate_text(grant_entry)
        grant_entry = normalize_text(grant_entry)
        
        # Get ground truth coordinates
        gt_coords = row["latitude/longitude"]
        
        # Create row data
        grant_data = {
            "Grant #": row_idx,
            "Grant Entry": grant_entry,
            "Ground Truth": gt_coords,
        }
        
        # Add H-1 coordinates
        h1_lat = row["h1_latitude"]
        h1_lon = row["h1_longitude"]
        if pd.notna(h1_lat) and pd.notna(h1_lon):
            grant_data["H-1"] = f"{h1_lat}, {h1_lon}"
        else:
            grant_data["H-1"] = "N/A"
        
        # Add AI method predictions
        for method in [m for m in methods if m != "H-1"]:
            subset = res.query("row_index == @row_idx and method_id == @method")
            if not subset.empty:
                pred = subset.iloc[0]["prediction"]
                pred = normalize_coordinates(pred)
                grant_data[method] = pred
            else:
                grant_data[method] = "N/A"
        
        output_data.append(grant_data)
    
    # Create and save DataFrame
    output_df = pd.DataFrame(output_data)
    
    # Reorder columns to match requested format
    column_order = ["Grant #", "Grant Entry", "Ground Truth"] + methods
    output_df = output_df[column_order]
    
    # Save to CSV with proper quoting to handle commas and special characters
    output_df.to_csv(OUTPUT_CSV, index=False, quoting=1, encoding='utf-8')  # QUOTE_ALL=1
    print(f"CSV saved to {OUTPUT_CSV}")

    # Also save an Excel version which may be easier to read
    excel_output = str(OUTPUT_CSV).replace(".csv", ".xlsx")
    try:
        output_df.to_excel(excel_output, index=False, engine='openpyxl')
        print(f"Excel version saved to {excel_output}")
    except:
        print("Could not save Excel version - make sure openpyxl is installed")
        print("Run: pip install openpyxl")
        
    return output_df

if __name__ == "__main__":
    main() 