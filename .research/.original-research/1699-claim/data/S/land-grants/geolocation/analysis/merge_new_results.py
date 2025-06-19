import csv
import os
import re
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

# -----------------------------------------------------------------------------
# Paths – update these if the directory layout changes
# -----------------------------------------------------------------------------
GEODIR = Path(__file__).resolve().parents[1]  # geolocation directory
ANALYSIS_DIR = Path(__file__).parent

MASTER_CSV = ANALYSIS_DIR / "full_results.csv"
OUTPUT_CSV = ANALYSIS_DIR / "full_results_v2.csv"

# Incoming new result files
ENSEMBLE_FULL = GEODIR / "runs/validation---TEST-FULL-H1-final_20250617_075802/results_validation - TEST-FULL-H1-final.csv"
ENSEMBLE_REDACT = GEODIR / "runs/validation---TEST-FULL-H1-final_20250617_142523/results_validation - TEST-FULL-H1-final.csv"

CC_FILE = Path("/Users/ryanmioduskiimac/Downloads/mordecai/county_centroid_predictions.csv")
MORDECAI_FILE = Path("/Users/ryanmioduskiimac/Downloads/mordecai/mordecai3_predictions_enhanced.csv")

# Evaluation set with ground-truth
EVAL_CSV = GEODIR / "validation - TEST-FULL-H1-final.csv"

# -----------------------------------------------------------------------------
# Geo helpers (adapted from run_experiment.py, simplified for decimals)
# -----------------------------------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):
    """Return great-circle distance (km) between two points."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c  # Earth radius km


def extract_decimal_pair(text: str):
    """Return (lat, lon) floats from a string containing a decimal pair."""
    if not text:
        return None, None
    m = re.search(r"([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)", text)
    if m:
        return float(m.group(1)), float(m.group(2))
    # space-sep fallback
    parts = text.strip().split()
    if len(parts) == 2:
        try:
            return float(parts[0].rstrip(',')), float(parts[1])
        except ValueError:
            pass
    return None, None


def calc_error(pred_text: str, gt_text: str):
    lat_gt, lon_gt = extract_decimal_pair(gt_text)
    lat_pr, lon_pr = extract_decimal_pair(pred_text)
    if None in (lat_gt, lon_gt, lat_pr, lon_pr):
        return ""
    return haversine(lat_gt, lon_gt, lat_pr, lon_pr)

# -----------------------------------------------------------------------------
# Load ground-truth mapping (subject_id -> (row_index, gt_coord_str))
# -----------------------------------------------------------------------------
row_map = {}
with open(EVAL_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    counter = 0
    for r in reader:
        if r.get("has_ground_truth") == "1":
            counter += 1
            row_map[r["subject_id"]] = (counter, r["latitude/longitude"])  # store gt

print(f"Ground-truth rows: {counter} (mapping size {len(row_map)})")

# -----------------------------------------------------------------------------
# Helper to normalise and append a row dict
# -----------------------------------------------------------------------------
FIELDNAMES = [
    "row_index",
    "method_id",
    "model",
    "pipeline",
    "prompt_id",
    "prompt_version",
    "prediction",
    "input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "total_tokens",
    "latency_s",
    "error_km",
    "is_mock",
    "is_locatable",
]

def load_csv(path: Path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# -----------------------------------------------------------------------------
# 1. Start with master rows
# -----------------------------------------------------------------------------
rows = load_csv(MASTER_CSV)
existing_keys = {(r["row_index"], r["method_id"]) for r in rows}
print(f"Loaded master rows: {len(rows)}")

# -----------------------------------------------------------------------------
# 2. Append E-1 / E-2 rows (already have error_km)
# -----------------------------------------------------------------------------
for p in (ENSEMBLE_FULL, ENSEMBLE_REDACT):
    for r in load_csv(p):
        mid = "E-1" if r["method_id"] == "o3_ensemble5" else "E-2"
        key = (r["row_index"], mid)
        if key in existing_keys:
            continue
        r["method_id"] = mid
        r.setdefault("is_locatable", "1")
        if (r["row_index"], r["method_id"]) not in existing_keys:
            rows.append(r)
            existing_keys.add(key)
print("Added ensemble rows")

# -----------------------------------------------------------------------------
# 3. County centroid + Mordecai baselines
# -----------------------------------------------------------------------------

def ingest_baseline(path: Path, mid: str, model: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            sid = r["subject_id"].strip()
            if sid not in row_map:
                continue
            row_idx, gt = row_map[sid]
            pred_lat = r[list(r.keys())[1]]  # first lat column
            pred_lon = r[list(r.keys())[2]]  # first lon column
            pred_text = f"{pred_lat}, {pred_lon}"
            err = calc_error(pred_text, gt)
            row = {
                "row_index": str(row_idx),
                "method_id": mid,
                "model": model,
                "pipeline": "static",
                "prompt_id": "static",
                "prompt_version": "1",
                "prediction": pred_text,
                "input_tokens": "0",
                "output_tokens": "0",
                "reasoning_tokens": "0",
                "total_tokens": "0",
                "latency_s": "0",
                "error_km": f"{err}" if err != "" else "",
                "is_mock": "0",
                "is_locatable": "1" if err != "" else "0",
            }
            key = (row["row_index"], mid)
            if key not in existing_keys:
                rows.append(row)
                existing_keys.add(key)

ingest_baseline(CC_FILE, "H-4", "CC")
ingest_baseline(MORDECAI_FILE, "H-3", "M3_PP")
print("Added heuristic baselines")

# -----------------------------------------------------------------------------
# 4. Sort rows (row_index asc, then method_id)
# -----------------------------------------------------------------------------
rows.sort(key=lambda r: (int(r["row_index"]), r["method_id"]))

# -----------------------------------------------------------------------------
# 5. Write out
# -----------------------------------------------------------------------------
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to {OUTPUT_CSV}") 