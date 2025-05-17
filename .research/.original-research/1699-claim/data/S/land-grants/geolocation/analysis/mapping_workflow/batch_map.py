"""batch_map.py – generate maps for every validation row that has ground-truth coordinates.

Usage:
  python batch_map.py [M-2,M-4]

Optional positional arg: comma-separated list of AI method_ids to display.
Output PNGs are written to ./map_outputs/ as grant_{row}.png
"""
from pathlib import Path
import sys
import os
import pandas as pd

# import plotting helper by path
from map_one_grant import THIS_DIR, GEOLOCATION_DIR, ANALYSIS_DIR, parse_latlon, _DMS_RE, _dms_to_dd  # noqa
import map_one_grant as single

METHODS = [m.strip() for m in (sys.argv[1] if len(sys.argv) > 1 else "M-2,M-4,M-5,T-1,T-4").split(",") if m.strip()]

VAL_CSV = GEOLOCATION_DIR / "validation - TEST-FULL-H1.csv"
RES_CSV = ANALYSIS_DIR / "full_results.csv"
OUT_DIR = THIS_DIR / "map_outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

val = pd.read_csv(VAL_CSV)
res = pd.read_csv(RES_CSV)

locatable = val[(val["has_ground_truth"] == 1) & (val["latitude/longitude"].notna())]

print(f"[batch_map] Generating maps for {len(locatable)} locatable grants …")

for _, row in locatable.iterrows():
    row_idx = int(row["results_row_index"])
    outfile = OUT_DIR / f"grant_{row_idx}_map.png"
    try:
        single.ROW_INDEX = row_idx
        single.METHODS = METHODS
        single.OUTFILE = outfile
        single.main()
    except Exception as e:
        print(f"  ! grant {row_idx} failed: {e}")

print("[batch_map] Done.") 