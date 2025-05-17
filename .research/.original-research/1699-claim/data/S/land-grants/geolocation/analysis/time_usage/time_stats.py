from __future__ import annotations
"""Latency/time analysis by method.
Sums `latency_s` from `analysis/full_results.csv` for each method.
For H-1 we override total hours to 9.33 ( $140 / $15 ).
Produces markdown report (`time_stats.md`) with per-method and roll-up tables.
"""
import csv
import math
from pathlib import Path
from typing import Dict, List

GEOL_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = GEOL_ROOT / "analysis"
FULL_RESULTS_CSV = ANALYSIS_DIR / "full_results.csv"
REPORT_PATH = Path(__file__).with_suffix(".md")

class Agg:
    def __init__(self, model: str):
        self.model = model
        self.entries = 0
        self.located = 0
        self.sec = 0.0  # total seconds

    def add(self, row: Dict[str, str]):
        self.entries += 1
        if row.get("is_locatable") in {"1", "true", "True"}:
            self.located += 1
        try:
            self.sec += float(row.get("latency_s", 0) or 0)
        except ValueError:
            pass

method_aggs: Dict[str, Agg] = {}

with FULL_RESULTS_CSV.open() as fh:
    for row in csv.DictReader(fh):
        m_id = row["method_id"]
        model = row["model"]
        if m_id not in method_aggs:
            method_aggs[m_id] = Agg(model)
        method_aggs[m_id].add(row)

# Manual override for human method total hours
HOURS_OVERRIDE = {"H-1": 9.33}
for m_id, hours in HOURS_OVERRIDE.items():
    if m_id in method_aggs:
        method_aggs[m_id].sec = hours * 3600  # convert to seconds

# Helper to get hours

def secs_to_hours(sec: float) -> float:
    return sec / 3600.0

# Build markdown
md: List[str] = [
    "# Time/latency analysis by method\n",
    "Source: `analysis/full_results.csv` – `latency_s` is wall-clock time from request to final answer and therefore includes model thinking + any tool latency. `H-1` cost converted to **9.33 h** ( $140 / $15 ).\n",
    "### Per-method breakdown\n",
    "| Method | Model | Entries | Located | Total hours | Hours per located | Hours/1k located |",
    "|---|---|---|---|---|---|---|",
]
for mid, a in sorted(method_aggs.items()):
    hours_total = secs_to_hours(a.sec)
    per_loc = hours_total / a.located if a.located else math.inf
    per_1k = per_loc * 1000 if math.isfinite(per_loc) else math.inf
    md.append(
        f"| {mid} | {a.model} | {a.entries} | {a.located} | {hours_total:,.3f} | {per_loc:,.4f} | {per_1k:,.3f} |"
    )

# Roll-up M vs T
md.append("\n### Roll-up: M vs T methods\n")
md.append("| Category | Entries | Located | Total hours | Hours per located | Hours/1k located |")
md.append("|---|---|---|---|---|---|")
cat_aggs = {"M": Agg("mixed"), "T": Agg("mixed")}
for mid, a in method_aggs.items():
    cat = mid.split("-")[0]
    if cat in cat_aggs:
        c = cat_aggs[cat]
        c.entries += a.entries
        c.located += a.located
        c.sec += a.sec
for cat in ["M", "T"]:
    c = cat_aggs[cat]
    if c.entries == 0:
        continue
    hrs = secs_to_hours(c.sec)
    per_loc = hrs / c.located if c.located else math.inf
    per_1k = per_loc * 1000 if math.isfinite(per_loc) else math.inf
    md.append(f"| {cat}-methods | {c.entries} | {c.located} | {hrs:,.3f} | {per_loc:,.4f} | {per_1k:,.3f} |")

# Roll-up by model
model_aggs: Dict[str, Agg] = {}
for mid, a in method_aggs.items():
    m = a.model
    if m not in model_aggs:
        model_aggs[m] = Agg(m)
    ma = model_aggs[m]
    ma.entries += a.entries
    ma.located += a.located
    ma.sec += a.sec
md.append("\n### Roll-up: by model\n")
md.append("| Model | Entries | Located | Total hours | Hours per located | Hours/1k located |")
md.append("|---|---|---|---|---|---|")
for m, a in sorted(model_aggs.items()):
    hrs = secs_to_hours(a.sec)
    per_loc = hrs / a.located if a.located else math.inf
    per_1k = per_loc * 1000 if math.isfinite(per_loc) else math.inf
    md.append(f"| {m} | {a.entries} | {a.located} | {hrs:,.3f} | {per_loc:,.4f} | {per_1k:,.3f} |")

REPORT_PATH.write_text("\n".join(md))
print(f"Report written to {REPORT_PATH.relative_to(GEOL_ROOT)}") 