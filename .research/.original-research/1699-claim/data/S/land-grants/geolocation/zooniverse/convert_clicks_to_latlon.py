#!/usr/bin/env python3
"""Convert Zooniverse pin clicks (pixel x/y) into lat/lon.

Usage
-----
python convert_clicks_to_latlon.py  \
    --input colonial-virginia-land-grants-mapping-the-past-classifications.csv \
    --output clicks_latlon.csv

The script expects each CSV row to contain:
• annotations          – JSON string with at least one {x, y, frame} entry
• subject_data         – JSON string where each subject has:
    • #center_lat, #center_lon (float)
    • either #zoom OR image filenames containing `_z{zoom}`

If multiple zoom-level images exist, the `frame` index maps to the
corresponding filename (image1, image2, …) so the correct zoom is used.

The Web-Mercator equations follow the slippy-map conventions at 256-px tiles.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

# ---------------------------------------------------------------------------
# Web-Mercator helpers
# ---------------------------------------------------------------------------

TILE_SIZE = 256  # Web-Mercator base tile size in px


def lonlat_to_pixels(lon: float, lat: float, zoom: int) -> Tuple[float, float]:
    """Convert lon/lat in degrees → world pixel X/Y at given zoom."""
    scale = TILE_SIZE * 2 ** zoom
    x = (lon + 180.0) / 360.0 * scale
    sin_lat = math.sin(math.radians(lat))
    y = (
        0.5
        - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)
    ) * scale
    return x, y


def pixels_to_lonlat(px: float, py: float, zoom: int) -> Tuple[float, float]:
    """Convert world pixel X/Y → lon/lat degrees at given zoom."""
    scale = TILE_SIZE * 2 ** zoom
    lon = px / scale * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * py / scale
    lat = math.degrees(math.atan(math.sinh(n)))
    return lon, lat


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

ZOOM_RE = re.compile(r"_z(\d{1,2})")
# Hard-coded default mapping of frame index → Web-Mercator zoom level
DEFAULT_FRAME_ZOOMS = {
    0: 9,
    1: 11,
    2: 14,
    3: 16,
}


def parse_zoom(subject: Dict[str, Any], frame: int) -> int:
    """Return the Web-Mercator zoom level for the given frame (0-indexed).

    Priority order
    1. Hard-coded DEFAULT_FRAME_ZOOMS mapping, because all subjects in this
       project follow a fixed zoom stack (z9, z11, z14, z16).
    2. If the frame index exceeds the mapping, attempt to extract the zoom
       from the image filename. This keeps behaviour reasonable if the subject
       contains additional frames that deviate from the 4-level stack.
    3. Finally, fall back to a #zoom key (single-image subjects only).
    """
    # 1. Project-specific fixed mapping
    if frame in DEFAULT_FRAME_ZOOMS:
        return DEFAULT_FRAME_ZOOMS[frame]

    # 2. Try filename pattern `_z{zoom}`
    key = f"image{frame + 1}"
    fname = subject.get(key) or subject.get("Filename")
    if fname:
        m = ZOOM_RE.search(fname)
        if m:
            return int(m.group(1))

    # 3. Fallback to #zoom field (single-image subjects)
    maybe = subject.get("#zoom")
    if maybe and str(maybe).isdigit():
        return int(maybe)

    raise ValueError(
        f"Could not determine zoom for frame {frame}. Subject data keys: {list(subject.keys())}"
    )


# ---------------------------------------------------------------------------
# Main conversion logic
# ---------------------------------------------------------------------------


def convert_row(row: Dict[str, str], *, subject_meta: Optional[Dict[str, Dict[str, Any]]] = None, extra_fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Given one CSV classification row, return one or more dicts with lat/lon.

    Parameters
    ----------
    row : Dict[str, str]
        Row from the classifications CSV.
    subject_meta : Optional[Dict[str, Dict[str, Any]]]
        Optional mapping of Zooniverse subject_id → parsed metadata dict from the
        subjects export. Used to fill in missing metadata (e.g. #center_lat) and
        to pull additional columns requested via *extra_fields*.
    extra_fields : Optional[List[str]]
        List of metadata keys to copy from the subject metadata into the output
        (e.g. ["subject_id", "raw_entry", "#is_gold"]).
    """
    extra_fields = extra_fields or []
    out: List[Dict[str, Any]] = []

    # Parse subject_data JSON: expects exactly one subject per row
    subj_bulk = json.loads(row["subject_data"])
    if len(subj_bulk) != 1:
        raise ValueError("Each classification should reference exactly one subject")
    subj_id = next(iter(subj_bulk.keys()))
    subject = subj_bulk[subj_id]

    # Merge in authoritative metadata from the subjects CSV (if any)
    if subject_meta and subj_id in subject_meta:
        # The classifications copy may be stale; update/extend with subject CSV version.
        subject_from_csv = subject_meta[subj_id]
        merged = subject_from_csv.copy()
        merged.update(subject)  # keep click-specific overrides
        subject = merged

    if "#center_lat" not in subject or "#center_lon" not in subject:
        raise ValueError("#center_lat/#center_lon missing for subject")

    center_lat = float(subject["#center_lat"])
    center_lon = float(subject["#center_lon"])

    # Parse annotations
    ann_list = json.loads(row["annotations"])
    if not ann_list:
        return out  # No clicks
    clicks = ann_list[0]["value"]  # Only one task (pin placement)

    # Some metadata may report naturalWidth/Height; fall back to 512
    meta = json.loads(row["metadata"])
    dims = meta.get("subject_dimensions", [{}])
    width = dims[0].get("naturalWidth", 512)
    height = dims[0].get("naturalHeight", 512)

    # Prepare any extra field values once (same for all clicks in this row)
    extras: Dict[str, Any] = {}
    for field in extra_fields:
        if field == "internal_id":
            # Special case: map to the project's own subject identifier stored in metadata
            extras[field] = subject.get("subject_id")
        else:
            extras[field] = subject.get(field)

    for idx, click in enumerate(clicks):
        x_px = click["x"]
        y_px = click["y"]
        frame = click.get("frame", 0)

        zoom = parse_zoom(subject, frame)

        # World pixels of the center
        center_px, center_py = lonlat_to_pixels(center_lon, center_lat, zoom)

        # Offset from image center (assume image is centered on subject center)
        offset_x = x_px - width / 2
        offset_y = y_px - height / 2  # Positive downward in pixels

        # New world pixel coords
        new_px = center_px + offset_x
        new_py = center_py + offset_y

        lon, lat = pixels_to_lonlat(new_px, new_py, zoom)

        rec: Dict[str, Any] = {
            "classification_id": row["classification_id"],
            "subject_id": subj_id,
            "click_index": idx,
            "user_name": row.get("user_name"),
            "frame": frame,
            "zoom": zoom,
            "x_px": x_px,
            "y_px": y_px,
            "lat": lat,
            "lon": lon,
        }
        rec.update(extras)
        out.append(rec)
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(description="Convert Zooniverse pin clicks to lat/lon.")
    p.add_argument("--input", required=True, help="Classification CSV file to read")
    p.add_argument("--output", required=True, help="Destination CSV with lat/lon added")
    p.add_argument("--subjects", help="Subjects CSV export – used to append metadata", default=None)
    p.add_argument(
        "--extra-fields",
        help="Comma-separated list of metadata keys to copy into output (default: raw_entry,internal_id)",
        default="raw_entry,internal_id",
    )
    args = p.parse_args()

    rows_out: List[Dict[str, Any]] = []

    # Pre-load subjects metadata if requested
    subject_meta: Optional[Dict[str, Dict[str, Any]]] = None
    if args.subjects:
        subject_meta = {}
        with open(args.subjects, newline="", encoding="utf-8") as fh:
            rsubj = csv.DictReader(fh)
            for srow in rsubj:
                meta_json = srow.get("metadata", "{}")
                try:
                    meta_parsed = json.loads(meta_json)
                except json.JSONDecodeError:
                    meta_parsed = {}
                subject_meta[srow["subject_id"]] = meta_parsed

    extra_fields = [f.strip() for f in args.extra_fields.split(",") if f.strip()]

    with open(args.input, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                rows_out.extend(
                    convert_row(
                        row,
                        subject_meta=subject_meta,
                        extra_fields=extra_fields,
                    )
                )
            except Exception as exc:
                print(f"[WARN] Skipping row {row.get('classification_id')} – {exc}")

    # Write results
    base_fields = [
        "classification_id",
        "subject_id",
        "click_index",
        "user_name",
        "frame",
        "zoom",
        "x_px",
        "y_px",
        "lat",
        "lon",
    ]

    # Combine with extras, preserving order and avoiding duplicates
    fieldnames = base_fields + [f for f in extra_fields if f not in base_fields]
    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for rec in rows_out:
            writer.writerow(rec)
    print(f"Wrote {len(rows_out)} clicks → {args.output}")


if __name__ == "__main__":
    main() 