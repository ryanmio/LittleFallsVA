"""make_static_maps.py
Generates static-map PNGs (OpenStreetMap tiles) for each land-grant row in
`zooniverse-50-grants.csv`.  By default it processes only the *first* row so you
can verify that the mapping pipeline and image formatting look correct before
batch-generating hundreds of images.

Usage
-----
python make_static_maps.py \
    --csv zooniverse-50-grants.csv \
    --out imgs_test \
    --limit 1  # change to None to process all rows

Dependencies
------------
- pandas
- pillow
- staticmap  (pure-python static map renderer)

Install them with:  pip install pandas pillow staticmap
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import pandas as pd
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def pick_coordinates(row: pd.Series) -> tuple[float, float] | None:
    """Choose latitude/longitude for a row.

    Preference order:
    1. seed_lat/seed_lon  (AI or human guess)
    2. gold_lat/gold_lon  (verified ground truth)

    Returns (lat, lon) or None if neither is present.
    """
    lat = row.get("seed_lat")
    lon = row.get("seed_lon")
    if pd.notna(lat) and pd.notna(lon):
        return float(lat), float(lon)

    lat = row.get("gold_lat")
    lon = row.get("gold_lon")
    if pd.notna(lat) and pd.notna(lon):
        return float(lat), float(lon)

    return None


def render_static_map(lat: float, lon: float, zoom: int, size_px: int = 512) -> "PIL.Image.Image":
    """Return a Pillow image of a static map centred on (lon, lat)."""
    m = StaticMap(size_px, size_px, url_template="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    marker = CircleMarker((lon, lat), "red", 12)
    m.add_marker(marker)
    return m.render(zoom=zoom)


def add_caption(img: "PIL.Image.Image", text: str, caption_h: int = 80) -> "PIL.Image.Image":
    """Overlay a semi-transparent caption band with wrapped *text* at the bottom of *img*.

    Keeps overall image size the same (512×512). We draw over the bottom
    *caption_h* pixels so the mapping maths remain unchanged.
    """
    draw = ImageDraw.Draw(img, "RGBA")

    # Semi-transparent white rectangle
    w, h = img.size
    band_top = h - caption_h
    draw.rectangle([(0, band_top), (w, h)], fill=(255, 255, 255, 230))

    # Text wrapping
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()

    margin = 5
    text_box_width = w - 2 * margin
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textlength(test, font=font) <= text_box_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    y = band_top + margin
    for line in lines[:5]:  # truncate after ~5 lines to avoid overflow
        draw.text((margin, y), line, font=font, fill=(0, 0, 0))
        y += font.getbbox(line)[3] - font.getbbox(line)[1] + 2

    return img


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate static map PNGs for Zooniverse subjects.")
    parser.add_argument("--csv", type=pathlib.Path, default="zooniverse-50-grants.csv", help="Path to input CSV.")
    parser.add_argument("--out", type=pathlib.Path, default="imgs", help="Output directory for PNGs.")
    parser.add_argument("--limit", type=int, default=1, help="Number of rows to process (use <=0 for all).")
    parser.add_argument("--zooms", type=int, nargs="*", default=[9, 11, 14, 16], help="Zoom levels to render (e.g. 9 11 14 16).")
    args = parser.parse_args(argv)

    out_dir: pathlib.Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.csv)
    n_total = len(df)
    n_process = n_total if args.limit is None or args.limit <= 0 else min(args.limit, n_total)

    print(f"Loaded {n_total} rows from {args.csv}. Processing {n_process} row(s)...")

    processed = 0
    skipped = 0
    for idx, row in df.head(n_process).iterrows():
        coords = pick_coordinates(row)
        if coords is None:
            print(f"[WARN] Skipping {row['subject_id']} – no coordinates found.")
            skipped += 1
            continue

        lat, lon = coords
        subject_id = row["subject_id"]
        for zoom in args.zooms:
            img = render_static_map(lat, lon, zoom)
            img = add_caption(img, row["raw_entry"])
            fname = f"{subject_id}_z{zoom}.png"
            img.save(out_dir / fname)
            print(f"[OK] Wrote {fname}")
        processed += 1

    print(f"Done. Generated images for {processed} subject(s); skipped {skipped}.")

    print(f"Default zoom levels (if not specified with --zooms) are 9, 11, 14, and 16 so each subject gets four frames: regional context, county context, local area, and close-up.")


if __name__ == "__main__":
    main() 