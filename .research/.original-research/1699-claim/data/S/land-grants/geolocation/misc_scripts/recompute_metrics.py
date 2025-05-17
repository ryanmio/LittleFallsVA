#!/usr/bin/env python3
"""recompute_metrics.py – post-processing helper to fix blank error_km fields
caused by overly-strict DMS parsing in the original run.

Usage
-----
python3 recompute_metrics.py \
    --results-file "runs/<run_id>/results_*.csv" \
    --evalset "validation - TEST-FULL-H1.csv" \
    --output-file "runs/<run_id>/results_cleaned.csv"

The script:
1. Loads the evaluation set and keeps only rows with has_ground_truth == 1
   (same logic as run_experiment.py) so row_index alignment matches.
2. Re-parses each prediction with an improved DMS regex that accepts
   *integer* seconds as well as fractional seconds.
3. Recomputes the Haversine error_km; if the original field was empty and
   parsing now succeeds, it is populated.
4. Writes a new CSV (default suffix "_cleaned") preserving column order.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path

# ---------------------------------------------------------------------
# Improved DMS parsing helpers (copied from run_experiment with a patch)
# ---------------------------------------------------------------------

def dms_to_decimal(dms_str: str):
    """Convert DMS (Degrees°Minutes'Seconds"[NSEW]) to decimal degrees.

    Seconds now accept integer or float (e.g. 30" or 30.123")."""
    m = re.match(r"(\d+)°(\d+)'(\d+(?:\.\d+)?)\"([NSEW])", dms_str)
    if not m:
        return None
    degrees, minutes, seconds, direction = m.groups()
    decimal = float(degrees) + float(minutes) / 60.0 + float(seconds) / 3600.0
    if direction in {"S", "W"}:
        decimal = -decimal
    return decimal


def extract_coords_from_text(text: str):
    """Try to extract (lat, lon) from prediction text (decimal or DMS)."""
    # Decimal pair with comma
    m = re.search(r"([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)", text)
    if m:
        return float(m.group(1)), float(m.group(2))

    # DMS pattern (now integer or float seconds)
    dms_pattern = r"(\d{1,3}°\s*\d{1,2}'\s*\d+(?:\.\d+)?\"\s*[NSEW])"
    matches = re.findall(dms_pattern, text, flags=re.IGNORECASE)
    if len(matches) >= 2:
        lat = dms_to_decimal(matches[0].replace(" ", ""))
        lon = dms_to_decimal(matches[1].replace(" ", ""))
        return lat, lon
    return None, None


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c  # km


def _parse_ground_truth(gt):
    if gt is None:
        return None, None
    if isinstance(gt, (list, tuple)) and len(gt) == 2:
        try:
            return float(gt[0]), float(gt[1])
        except Exception:
            return None, None
    if not isinstance(gt, str):
        return None, None
    gt = gt.strip()
    if not gt:
        return None, None
    # decimal lat,lon
    m = re.match(r"\s*([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)", gt)
    if m:
        return float(m.group(1)), float(m.group(2))
    # space separated pair
    parts = gt.split()
    if len(parts) == 2:
        try:
            return float(parts[0]), float(parts[1])
        except Exception:
            pass
    # DMS pair
    lat, lon = extract_coords_from_text(gt)
    return lat, lon


# ---------------------------------------------------------------------
# CLI + main logic
# ---------------------------------------------------------------------

def load_evalset(path: Path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if "has_ground_truth" in (reader.fieldnames or []):
        rows = [r for r in rows if r.get("has_ground_truth") == "1"]
    return rows


def recompute(args):
    eval_rows = load_evalset(Path(args.evalset))
    # Map row_index (1-based in results) → ground-truth string
    gt_by_index = {idx + 1: r.get("latitude/longitude", "") for idx, r in enumerate(eval_rows)}

    results_path = Path(args.results_file)
    out_path = Path(args.output_file or (results_path.with_stem(results_path.stem + "_cleaned")))

    with open(results_path, newline="", encoding="utf-8") as fin, open(out_path, "w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        fixed_count = 0
        for row in reader:
            if row.get("error_km"):
                writer.writerow(row)
                continue  # already present, leave untouched
            # attempt recompute
            pred = row.get("prediction", "")
            lat_gt, lon_gt = _parse_ground_truth(gt_by_index.get(int(row["row_index"])))
            lat_pred, lon_pred = extract_coords_from_text(pred)
            if None not in (lat_gt, lon_gt, lat_pred, lon_pred):
                row["error_km"] = f"{haversine(lat_gt, lon_gt, lat_pred, lon_pred):.6f}"
                fixed_count += 1
            writer.writerow(row)

    # --------------------
    # Validation summary
    # --------------------
    orig_blank = 0
    with open(results_path, newline="", encoding="utf-8") as f_orig:
        for r in csv.DictReader(f_orig):
            if not r.get("error_km"):
                orig_blank += 1

    new_blank = 0
    with open(out_path, newline="", encoding="utf-8") as f_new:
        for r in csv.DictReader(f_new):
            if not r.get("error_km"):
                new_blank += 1

    msg = (
        f"Re-wrote {out_path}\n"
        f"• originally blank error_km: {orig_blank}\n"
        f"• filled during patch   : {fixed_count}\n"
        f"• still blank afterwards : {new_blank}\n"
    )
    print(msg)

    # Write a small reproducibility report next to the cleaned CSV
    report_path = out_path.with_suffix(".md")
    with open(report_path, "w", encoding="utf-8") as rep:
        rep.write("# Post-processing Metrics Fix Report\n\n")
        rep.write(f"**Source results:** `{results_path}`  \n")
        rep.write(f"**Cleaned results:** `{out_path}`  \n\n")
        rep.write("| Metric | Count |\n|---|---|\n")
        rep.write(f"| Rows with blank error_km (original) | {orig_blank} |\n")
        rep.write(f"| Rows fixed by script | {fixed_count} |\n")
        rep.write(f"| Remaining blank error_km | {new_blank} |\n\n")
        rep.write("Script version: recompute_metrics.py (patched DMS regex).\n")

    print(f"Validation report saved → {report_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Recompute missing error_km with improved DMS parser")
    p.add_argument("--results-file", required=True)
    p.add_argument("--evalset", required=True)
    p.add_argument("--output-file", required=False, help="Where to write the cleaned CSV")
    recompute(p.parse_args()) 