"""build_manifest.py
Create a Zooniverse-ready manifest CSV that pairs each land-grant entry with the
static-map PNGs produced by `make_static_maps.py`.

The manifest will include:
    subject_id, image1, image2, raw_entry,
    #center_lat, #center_lon, #zoom, #is_gold
Hidden columns (prefixed with `#`) survive the Zooniverse round-trip but remain
invisible to volunteers. They are essential for later pixel→lat/lon conversion
and QC analysis.

Run after you have generated all PNGs::

    python3 build_manifest.py \
        --csv zooniverse-50-grants.csv \
        --png-dir imgs \
        --out manifest.csv
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from typing import List, Dict, Tuple, Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Helper functions (re-use from make_static_maps)
# ---------------------------------------------------------------------------


def pick_coordinates(row: pd.Series) -> Optional[Tuple[float, float]]:
    """Return (lat, lon) using seed or gold columns; None if unavailable."""
    lat, lon = row.get("seed_lat"), row.get("seed_lon")
    if pd.notna(lat) and pd.notna(lon):
        return float(lat), float(lon)
    lat, lon = row.get("gold_lat"), row.get("gold_lon")
    if pd.notna(lat) and pd.notna(lon):
        return float(lat), float(lon)
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build Zooniverse manifest CSV from grant data and PNGs.")
    parser.add_argument("--csv", type=pathlib.Path, default="zooniverse-50-grants.csv", help="Input grants CSV.")
    parser.add_argument("--png-dir", type=pathlib.Path, default="imgs", help="Directory containing generated PNGs.")
    parser.add_argument("--out", type=pathlib.Path, default="manifest.csv", help="Output manifest CSV path.")
    parser.add_argument("--zooms", type=int, nargs="*", default=[11, 14], help="Zoom levels that have PNGs.")
    args = parser.parse_args(argv)

    df = pd.read_csv(args.csv)
    rows: List[Dict[str, str]] = []
    skipped = 0

    for _, row in df.iterrows():
        subject_id = row["subject_id"]
        coords = pick_coordinates(row)
        if coords is None:
            print(f"[SKIP] {subject_id}: no coordinates available – will not be in manifest.")
            skipped += 1
            continue
        lat, lon = coords
        # Ensure PNGs exist for each zoom
        images: list[str] = []
        for z in args.zooms:
            fname = f"{subject_id}_z{z}.png"
            path = args.png_dir / fname
            if not path.is_file():
                raise FileNotFoundError(f"Expected PNG not found: {path}. Run make_static_maps first.")
            images.append(fname)

        manifest_row: Dict[str, str] = {
            "subject_id": subject_id,
            "raw_entry": row["raw_entry"].replace("\n", " ").strip(),
            "#center_lat": f"{lat}",
            "#center_lon": f"{lon}",
            "#zoom": str(args.zooms[0]),  # primary context zoom
            "#is_gold": str(int(row.get("is_gold", 0)))
        }
        # Add image columns dynamically
        for idx, img_name in enumerate(images, start=1):
            manifest_row[f"image{idx}"] = img_name

        rows.append(manifest_row)

    # Determine fieldnames dynamically to include all image columns
    base = ["subject_id"] + [f"image{i+1}" for i in range(len(args.zooms))] + ["raw_entry", "#center_lat", "#center_lon", "#zoom", "#is_gold"]
    fieldnames = base

    with args.out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote manifest with {len(rows)} subjects (skipped {skipped}). -> {args.out}")


if __name__ == "__main__":
    main() 