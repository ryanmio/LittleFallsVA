import os
import re
import sys
from pathlib import Path

import pandas as pd

# Attempt to import heavy geo stack lazily
try:
    import geopandas as gpd
    import contextily as cx
except ImportError as e:
    sys.stderr.write(
        "[map_one_grant] Required geopandas/contextily not installed.\n"
        "Run `pip install geopandas contextily` (plus deps) and retry.\n"
    )
    raise e

import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from pyproj import Geod

# ---------------------------------------------------------------------------
# CONFIG --------------------------------------------------------------
# ---------------------------------------------------------------------------
THIS_DIR = Path(__file__).resolve().parent
GEOLOCATION_DIR = THIS_DIR.parent.parent  # geolocation/
ANALYSIS_DIR = THIS_DIR.parent            # geolocation/analysis/

VAL_CSV = GEOLOCATION_DIR / "validation - TEST-FULL-H1-final.csv"
RES_CSV = ANALYSIS_DIR / "full_results.csv"

# Grant row to plot (default via env or CLI)
ROW_INDEX = int(os.getenv("GRANT_ROW", sys.argv[1] if len(sys.argv) > 1 else 10))
# Which AI methods to show (comma-separated env or CLI second arg)
METHODS = os.getenv("AI_METHODS", sys.argv[2] if len(sys.argv) > 2 else "T-1,M-1")
METHODS = [m.strip() for m in METHODS.split(",") if m.strip()]

# Output file
OUTFILE = THIS_DIR / f"grant_{ROW_INDEX}_map.png"

# ---------------------------------------------------------------------------
# Helper functions -----------------------------------------------------
# ---------------------------------------------------------------------------

_DMS_RE = re.compile(
    r"(?P<deg>\d+)[^\d]+(?P<min>\d+)[^\d]+(?P<sec>[\d\.]+)[^A-Za-z]*(?P<hemi>[NSEW])",
    re.I,
)


def _dms_to_dd(match_dict):
    deg = float(match_dict["deg"])
    minutes = float(match_dict["min"])
    seconds = float(match_dict["sec"])
    hemi = match_dict["hemi"].upper()
    sign = -1 if hemi in {"S", "W"} else 1
    return sign * (deg + minutes / 60.0 + seconds / 3600.0)


def parse_latlon(raw: str):
    """Return (lat, lon) as float from decimal or DMS string."""
    raw = raw.strip()
    if not raw:
        raise ValueError("Empty lat/lon string")
    # Decimal pair like "37.7, -77.1"
    if "," in raw and "°" not in raw:
        lat_s, lon_s = raw.split(",")
        return float(lat_s), float(lon_s)
    # Otherwise treat as DMS – expect two matches (lat then lon)
    parts = _DMS_RE.findall(raw)
    if len(parts) < 2:
        raise ValueError(f"Unparsable lat/lon DMS: {raw}")
    lat = _dms_to_dd(dict(zip(["deg", "min", "sec", "hemi"], parts[0])))
    lon = _dms_to_dd(dict(zip(["deg", "min", "sec", "hemi"], parts[1])))
    return lat, lon

# ---------------------------------------------------------------------------
# MAIN ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    # 1) Load CSVs
    val = pd.read_csv(VAL_CSV)
    res = pd.read_csv(RES_CSV)

    if ROW_INDEX not in val["results_row_index"].values:
        raise SystemExit(f"Row {ROW_INDEX} not found in validation file.")

    row = val.loc[val["results_row_index"] == ROW_INDEX].iloc[0]

    # ground truth
    if pd.isna(row["latitude/longitude"]):
        raise SystemExit("Selected row lacks ground-truth coordinates.")
    gt_lat, gt_lon = map(float, str(row["latitude/longitude"]).split(","))

    # human baseline
    h1_lat, h1_lon = float(row["h1_latitude"]), float(row["h1_longitude"])

    records = [
        {"label": "Ground truth", "method": "GT", "geometry": Point(gt_lon, gt_lat)},
        {"label": "Human GIS (H-1)", "method": "H-1", "geometry": Point(h1_lon, h1_lat)},
    ]

    geod = Geod(ellps="WGS84")

    # AI predictions requested
    for meth in METHODS:
        subset = res.query("row_index == @ROW_INDEX and method_id == @meth")
        if subset.empty:
            sys.stderr.write(f"[map_one_grant] WARNING: no prediction for {meth}\n")
            continue
        pred = subset.iloc[0]["prediction"]
        lat, lon = parse_latlon(str(pred))

        # get error_km from results if available else compute
        err_km = subset.iloc[0].get("error_km", None)
        if pd.isna(err_km) or err_km is None:
            _, _, dist_m = geod.inv(gt_lon, gt_lat, lon, lat)
            err_km = dist_m / 1000.0

        records.append({
            "label": f"{meth} prediction", "method": meth,
            "geometry": Point(lon, lat), "error_km": err_km,
        })

    # add error_km for H-1
    _, _, h1_dist = geod.inv(gt_lon, gt_lat, h1_lon, h1_lat)
    records[1]["error_km"] = h1_dist / 1000.0

    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326").to_crs(3857)  # Web-Mercator

    # ---------------- PLOT ----------------
    fig, ax = plt.subplots(figsize=(6, 6))

    # Fixed series colours for reproducibility and legend consistency
    M_COLOR = "#1f77b4"  # blue
    T_COLOR = "#d62728"  # red

    style = {
        "GT": ("*", "black"),
        "H-1": ("o", "orange"),
    }

    # Assign fixed colours by series
    for meth in METHODS:
        if meth.startswith("T"):
            style[meth] = ("^", T_COLOR)
        elif meth.startswith("M"):
            style[meth] = ("s", M_COLOR)
        else:
            style[meth] = ("s", "gray")

    # --- plot points and optionally annotate ---
    # first compute map extents for label offset
    minx, miny, maxx, maxy = gdf.total_bounds
    width = maxx - minx
    height = maxy - miny
    lbl_dx = width * 0.01
    lbl_dy = height * 0.01

    for _, rec in gdf.iterrows():
        mark, col = style.get(rec["method"], ("x", "red"))

        # For GT and H-1 we keep legend; for AI predictions skip legend to avoid clutter
        legend_label = rec["label"] if rec["method"] in {"GT", "H-1"} else None

        gpd.GeoSeries([rec.geometry]).plot(
            ax=ax,
            marker=mark,
            color=col,
            markersize=100,
            zorder=3,
            label=legend_label,
        )

        # Annotate AI predictions (boxes/triangles) with method id near marker
        if rec["method"] not in {"GT", "H-1"}:
            ax.text(
                rec.geometry.x + lbl_dx,
                rec.geometry.y + lbl_dy,
                rec["method"],
                fontsize=7,
                color=col,
                weight="bold",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", alpha=0.8, ec="none"),
            )

    # error lines from GT
    gt_point = gdf.loc[gdf["method"] == "GT", "geometry"].values[0]
    for _, rec in gdf.iterrows():
        if rec["method"] == "GT":
            continue
        ls = LineString([gt_point, rec.geometry])
        gpd.GeoSeries([ls], crs=gdf.crs).plot(ax=ax, color="gray", linestyle="--", linewidth=1)

        # place distance label slightly offset from the line
        x_mid = (gt_point.x + rec.geometry.x) / 2
        y_mid = (gt_point.y + rec.geometry.y) / 2

        # perpendicular offset (5 % of line length)
        dx = rec.geometry.x - gt_point.x
        dy = rec.geometry.y - gt_point.y
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length:
            offset = 0.05 * length  # 5 %
            off_x = -dy / length * offset
            off_y = dx / length * offset
            x_mid += off_x
            y_mid += off_y

        err_km = rec.get("error_km", None)
        if err_km is not None:
            ax.text(x_mid, y_mid, f"{err_km:.0f} km", fontsize=8, color="gray", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.1", fc="white", alpha=0.6, ec="none"))

    # set extent to include all points with padding, then expand shorter side
    pad = 0.1  # 10 %
    pad_w = (maxx - minx) * pad
    pad_h = (maxy - miny) * pad

    if width >= height:
        extra = (width - height) / 2
        miny -= extra
        maxy += extra
    else:
        extra = (height - width) / 2
        minx -= extra
        maxx += extra

    ax.set_xlim(minx - pad_w, maxx + pad_w)
    ax.set_ylim(miny - pad_h, maxy + pad_h)

    # basemap with fallback chain
    basemap_added = False
    for provider in [
        cx.providers.OpenStreetMap.Mapnik,
        cx.providers.CartoDB.Positron,
    ]:
        try:
            cx.add_basemap(ax, crs=gdf.crs, source=provider, attribution=False, zoom=10)
            basemap_added = True
            break
        except Exception:
            continue
    if not basemap_added:
        sys.stderr.write("[map_one_grant] Basemap skipped – network unavailable or providers unreachable.\n")

    # Add dummy lines for the legend to represent M-series and T-series
    from matplotlib.lines import Line2D
    
    # Use fixed representative colours to match plotted markers
    m_color = M_COLOR
    t_color = T_COLOR
    
    # Create custom legend elements
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor='black', 
               markersize=10, label='Ground truth'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
               markersize=10, label='Human GIS (H-1)'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=m_color, 
               markersize=10, label='M-series (one-shot)'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor=t_color, 
               markersize=10, label='T-series (tool-chain)'),
    ]

    # Add scale bar
    from matplotlib_scalebar.scalebar import ScaleBar
    try:
        # Try to add scale bar - fallback if library not available
        scale_bar = ScaleBar(1, units='m', dimension='si-length', location='lower left',
                          pad=0.5, border_pad=0.5, sep=5, frameon=True, 
                          color='black', box_color='white', box_alpha=0.7)
        ax.add_artist(scale_bar)
    except (ImportError, NameError):
        # Fallback manual scale bar at 10km
        # Convert 10km to meters in web mercator
        scale_length_m = 10000  # 10 km
        # Get units for scale bar (assuming coordinates are in web mercator)
        xmin, xmax = ax.get_xlim()
        scale_width = (xmax - xmin) * 0.2  # 20% of the plot width
        
        # Create scale bar at bottom left
        scale_x = xmin + (xmax - xmin) * 0.05
        scale_y = miny + (maxy - miny) * 0.05
        ax.plot([scale_x, scale_x + scale_width], [scale_y, scale_y], 'k-', lw=2)
        ax.text(scale_x + scale_width/2, scale_y - height*0.01, 
                '10 km (approx)', ha='center', va='top', fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax.set_axis_off()
    ax.set_title(f"Grant row {ROW_INDEX}: ground truth vs predictions")
    ax.legend(handles=legend_elements, frameon=False, loc="lower right")

    plt.tight_layout()
    fig.savefig(OUTFILE, dpi=300)
    plt.close(fig)
    print(f"[map_one_grant] Saved {OUTFILE.relative_to(THIS_DIR)}")


if __name__ == "__main__":
    main() 