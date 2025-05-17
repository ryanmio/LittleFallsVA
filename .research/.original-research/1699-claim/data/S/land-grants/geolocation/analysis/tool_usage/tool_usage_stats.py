"""Tool-usage analysis for T-methods (T-1, T-4)
------------------------------------------------
For each method we compute:
• Per-entry distribution of tool calls (geocode_place, compute_centroid, total)
  – mean, std-dev, median, min, max
• Aggregate ratio of geocode to centroid calls
• Search-efficiency metrics – at which tool-call index did the final answer derive?
  – average selected index, share of answers derived from first call, etc.
The results are exported as a Markdown report adjacent to this script.
"""

from __future__ import annotations

import json
import re
import statistics as stats
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import csv

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
RE_FLOAT = re.compile(r"-?\d+\.\d+")


def parse_coords(s: str) -> Optional[Tuple[float, float]]:
    """Extract the first two decimal numbers from *s* as (lat, lng)."""
    nums = [float(x) for x in RE_FLOAT.findall(s)]
    if len(nums) >= 2:
        return nums[0], nums[1]
    return None


def coords_close(a: Tuple[float, float], b: Tuple[float, float], tol: float = 1e-4) -> bool:
    """Return True if the two (lat, lng) pairs are within *tol* of each other."""
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
GEOL_ROOT = Path(__file__).resolve().parents[2]  # geolocation/
RUNS_DIR = GEOL_ROOT / "runs"
RUN_NAME = "validation---TEST-FULL-H1_20250505_191624"
CALLS_JSONL = RUNS_DIR / RUN_NAME / "calls.jsonl"

METHODS = ["T-1", "T-4"]
TOOLS = ["geocode_place", "compute_centroid"]

FULL_RESULTS_CSV = GEOL_ROOT / "analysis" / "full_results.csv"

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
class EntryMetrics:
    """Metrics for a single (row_index, method) invocation."""

    def __init__(self):
        self.num_calls: Dict[str, int] = {t: 0 for t in TOOLS}
        self.total_calls: int = 0
        self.selected_index: Optional[int] = None  # 1-based index of tool call that produced answer
        self.selected_tool: Optional[str] = None


entries: Dict[str, List[EntryMetrics]] = {m: [] for m in METHODS}

# Add collection of raw rows
all_rows: List[Tuple[int, str, int, int, int, Optional[int], Optional[str]]] = []  # row_index, method, geo, cent, total, selected_idx, selected_tool

# Build set of row indices that are locatable (is_locatable == 1)
LOCATABLE_ROWS: set[int] = set()
if FULL_RESULTS_CSV.exists():
    with FULL_RESULTS_CSV.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                idx = int(row.get("row_index", ""))
            except ValueError:
                continue
            flag = str(row.get("is_locatable", "1")).strip().lower()
            if flag in {"1", "true", "yes"}:
                LOCATABLE_ROWS.add(idx)
# If CSV absent assume all rows locatable.
else:
    LOCATABLE_ROWS = set()

# ---------------------------------------------------------------------------
# Parsing calls.jsonl
# ---------------------------------------------------------------------------
with CALLS_JSONL.open() as fh:
    for raw in fh:
        if not raw.strip():
            continue
        rec = json.loads(raw)
        method = rec.get("method_id")
        if method not in METHODS:
            continue

        # Skip non-locatable rows if LOCATABLE_ROWS populated
        row_idx = rec.get("row_index")
        if LOCATABLE_ROWS and row_idx not in LOCATABLE_ROWS:
            continue

        # Gather tool trace list
        tool_trace = []
        if isinstance(rec.get("response"), dict):
            tool_trace = rec["response"].get("tool_trace", [])
        tool_trace = tool_trace or rec.get("tool_trace", [])

        # Extract final answer text (assistant message)
        final_coords: Optional[Tuple[float, float]] = None
        resp = rec.get("response", {})
        if isinstance(resp, dict):
            for chunk in resp.get("response", {}).get("output", []):
                if chunk.get("role") == "assistant":
                    for c in chunk.get("content", []):
                        if c.get("type") == "output_text":
                            maybe = parse_coords(c.get("text", ""))
                            if maybe:
                                final_coords = maybe
                                break
                if final_coords:
                    break
        if not final_coords:
            # Fallback: try top-level content (rare schema)
            maybe = parse_coords(json.dumps(rec))
            if maybe:
                final_coords = maybe

        metrics = EntryMetrics()

        # Iterate tool calls – maintain index
        for idx, call in enumerate(tool_trace, 1):
            tool_name = call.get("tool_name")
            if tool_name in TOOLS:
                metrics.num_calls[tool_name] += 1
            metrics.total_calls += 1

            # Did this call's result match final answer?
            if final_coords and metrics.selected_index is None:
                result = call.get("result", {})
                if isinstance(result, dict) and {"lat", "lng"} <= result.keys():
                    call_coords = (float(result["lat"]), float(result["lng"]))
                    if coords_close(call_coords, final_coords):
                        metrics.selected_index = idx
                        metrics.selected_tool = tool_name

        # Inside parsing loop, after updating metrics and before appending to entries, also add row to all_rows.
        all_rows.append((
            rec["row_index"],
            method,
            metrics.num_calls["geocode_place"],
            metrics.num_calls["compute_centroid"],
            metrics.total_calls,
            metrics.selected_index,
            metrics.selected_tool
        ))

        entries[method].append(metrics)

# ---------------------------------------------------------------------------
# Aggregate statistics helpers
# ---------------------------------------------------------------------------

def summarise(values: List[int]) -> str:
    if not values:
        return "-"
    return (
        f"mean={stats.mean(values):.2f}, sd={stats.pstdev(values):.2f}, "
        f"median={stats.median(values):.0f}, min={min(values)}, max={max(values)}"
    )


# Add a helper to return individual stats dict

def calc_stats(values: List[int]) -> Dict[str, str]:
    """Return a dictionary with mean, sd, median, min, max formatted strings (or '-' if empty)."""
    if not values:
        return {k: "-" for k in ("mean", "sd", "median", "min", "max")}
    return {
        "mean": f"{stats.mean(values):.2f}",
        "sd": f"{stats.pstdev(values):.2f}",
        "median": f"{stats.median(values):.0f}",
        "min": str(min(values)),
        "max": str(max(values)),
    }


# ---------------------------------------------------------------------------
# Build Markdown report
# ---------------------------------------------------------------------------
md = [
    f"# Tool-usage statistics for run `{RUN_NAME}`\n",
    "Analyzing only T-methods (T-1, T-4). All coordinates are compared to the tool-call results to estimate *which* call fed the final answer.",
    "\n## Summary by method\n",
]

# ---------------------------------------------------------------------------
# Quick summary table by method
# ---------------------------------------------------------------------------
md.append("| Method | Entries | Mean calls | Geo:Cent ratio | First-call success |")
md.append("|---|---|---|---|---|")
for m in METHODS:
    rows_m = entries[m]
    n_m = len(rows_m)
    if n_m == 0:
        continue
    totals_m = [r.total_calls for r in rows_m]
    geocodes_m = [r.num_calls["geocode_place"] for r in rows_m]
    centroids_m = [r.num_calls["compute_centroid"] for r in rows_m]
    mean_calls_m = stats.mean(totals_m)
    total_geo_m = sum(geocodes_m)
    total_cent_m = sum(centroids_m)
    ratio_m = "∞" if total_cent_m == 0 else f"{total_geo_m / total_cent_m:.2f}:1"
    first_call_pct_m = (sum(1 for r in rows_m if r.selected_index == 1) / n_m * 100)
    md.append(f"| {m} | {n_m} | {mean_calls_m:.2f} | {ratio_m} | {first_call_pct_m:.1f}% |")
md.append("")

# ---------------------------------------------------------------------------
# Raw data section
# ---------------------------------------------------------------------------
md.append("## Raw tool-call data (one line per grant)\n")
md.append("| Row | Method | geocode_place | compute_centroid | Total calls | Selected call idx | Selected tool |")
md.append("|---|---|---|---|---|---|---|")
for row in sorted(all_rows, key=lambda x: (x[1], x[0])):
    md.append("| {row} | {m} | {g} | {c} | {tot} | {sel} | {tool} |".format(
        row=row[0], m=row[1], g=row[2], c=row[3], tot=row[4], sel=row[5] or "-", tool=row[6] or "-"))

md.append("\n## Statistical summary by method\n")

for m in METHODS:
    rows = entries[m]
    n = len(rows)
    if n == 0:
        continue

    totals = [r.total_calls for r in rows]
    geocodes = [r.num_calls["geocode_place"] for r in rows]
    centroids = [r.num_calls["compute_centroid"] for r in rows]
    selected = [r.selected_index for r in rows if r.selected_index]

    md.append(f"### Method {m}\n")
    md.append(f"*Entries analysed*: **{n}**\n")

    # -------------------------------------------------------------------
    # Tool-call distribution table
    # -------------------------------------------------------------------
    geo_stats = calc_stats(geocodes)
    cent_stats = calc_stats(centroids)
    total_stats = calc_stats(totals)

    md.append("\n#### Tool-call distribution (per entry)\n")
    md.append("| Statistic | geocode_place | compute_centroid | Total |")
    md.append("|---|---|---|---|")
    for label in ["mean", "sd", "median", "min", "max"]:
        pretty = label.capitalize() if label != "sd" else "SD"
        md.append(f"| {pretty} | {geo_stats[label]} | {cent_stats[label]} | {total_stats[label]} |")

    # -------------------------------------------------------------------
    # Aggregate counts
    # -------------------------------------------------------------------
    total_geo = sum(geocodes)
    total_cent = sum(centroids)
    ratio = total_geo / max(1, total_cent) if total_cent else float('inf')

    md.append("\n#### Aggregate call counts\n")
    md.append("| geocode_place | compute_centroid | Ratio geo:cent |")
    md.append("|---|---|---|")
    md.append(f"| {total_geo} | {total_cent} | {ratio:.2f}:1 |")

    # -------------------------------------------------------------------
    # Search efficiency
    # -------------------------------------------------------------------
    md.append("\n#### Search efficiency\n")
    if selected:
        first_hit = sum(1 for x in selected if x == 1)
        md.append("| Mean selected-call index | Median | First-call success |")
        md.append("|---|---|---|")
        md.append(
            f"| {stats.mean(selected):.2f} | {stats.median(selected):.0f} | {first_hit/len(selected):.1%} |"
        )
    else:
        md.append("No matching of outputs to tool-calls for this method.")

    md.append("\n\n")

# After per-method loop add overall summary
all_geocodes = [r[2] for r in all_rows]
all_centroids = [r[3] for r in all_rows]
all_totals = [r[4] for r in all_rows]
all_selected = [r[5] for r in all_rows if r[5]]

overall_geo = sum(all_geocodes)
overall_cent = sum(all_centroids)
ratio_all = overall_geo / max(1, overall_cent) if overall_cent else float('inf')

md.append("## Overall tool usage across T-methods\n")
md.append("| Metric | geocode_place | compute_centroid | Total | Notes |")
md.append("|---|---|---|---|---|")
md.append(f"| Calls (sum) | {overall_geo} | {overall_cent} | {overall_geo+overall_cent} | ratio geo:cent = {ratio_all:.2f}:1 |")
md.append(f"| Calls per entry (mean) | {stats.mean(all_geocodes):.2f} | {stats.mean(all_centroids):.2f} | {stats.mean(all_totals):.2f} | across {len(all_rows)} entries |")
if all_selected:
    md.append(f"| Selected-call index (mean) | - | - | - | {stats.mean(all_selected):.2f} average index (first-call success {(sum(1 for x in all_selected if x==1)/len(all_selected)):.1%}) |")

# ---------------------------------------------------------------------------
# Save report
# ---------------------------------------------------------------------------
REPORT_PATH = Path(__file__).with_suffix(".md")
REPORT_PATH.write_text("\n".join(md))
print(f"Report written to {REPORT_PATH.relative_to(GEOL_ROOT)}") 