from __future__ import annotations
"""Accuracy analysis for geolocation results.

Methodology
-----------
• Dataset: `analysis/full_results.csv` (only rows where `is_locatable == 1`).
• Metric of accuracy: great-circle error (km) in column `error_km`.
• All rows with a numeric error are included; non-numeric / missing values are ignored.
• Statistics per group:
  – count (n)
  – mean, median, population SD (pstdev)
  – min, 25th percentile (Q1), 75th percentile (Q3), max
  – hit-rates: share of rows with error ≤ 1 km, ≤ 5 km, ≤ 10 km, ≤ 25 km

Groups reported
• Per method (table for reference)
• Roll-ups: (a) M-methods vs T-methods, (b) by underlying model
• Tool-vs-non-tool comparison for models that appear in both forms (e.g. o4-mini: M-1 vs T-1, gpt-4.1: M-4 vs T-4)

The analysis is descriptive; no inferential tests are performed.
"""
import csv
import math
import statistics as stats
from pathlib import Path
from typing import Dict, List, Tuple

GEOL_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = GEOL_ROOT / "analysis"
CSV_PATH = ANALYSIS_DIR / "full_results.csv"
REPORT_PATH = Path(__file__).with_suffix(".md")

THRESHOLDS = [1, 5, 10, 25, 50]  # km

class AccAgg:
    def __init__(self, name: str):
        self.name = name
        self.errors: List[float] = []  # km

    # ------------------------------------------------------------------
    def add(self, err: float):
        self.errors.append(err)

    # ------------------------------------------------------------------
    def stats_row(self) -> Tuple:
        n = len(self.errors)
        if n == 0:
            return (0, "-", "-", "-", "-", "-", "-", "-", *["-"] * len(THRESHOLDS))
        mean = stats.mean(self.errors)
        med = stats.median(self.errors)
        sd = stats.pstdev(self.errors) if n > 1 else 0.0
        mn, mx = min(self.errors), max(self.errors)
        q1, q3 = stats.quantiles(self.errors, n=4)[0], stats.quantiles(self.errors, n=4)[2]
        hits = [sum(1 for e in self.errors if e <= t) / n * 100 for t in THRESHOLDS]
        return (n, f"{mean:.2f}", f"{med:.2f}", f"{sd:.2f}", f"{mn:.2f}", f"{q1:.2f}", f"{q3:.2f}", f"{mx:.2f}") + tuple(f"{h:.1f}%" for h in hits)

# ---------------------------------------------------------------------------
# Collect data
# ---------------------------------------------------------------------------
method_aggs: Dict[str, AccAgg] = {}
model_aggs: Dict[str, AccAgg] = {}
cat_aggs: Dict[str, AccAgg] = {"M": AccAgg("M-methods"), "T": AccAgg("T-methods")}
# For tool vs non-tool per model
per_model_tool: Dict[Tuple[str, str], AccAgg] = {}  # (model, category)-> agg

with CSV_PATH.open() as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        if row.get("is_locatable") not in {"1", "true", "True"}:
            continue
        try:
            err = float(row["error_km"])
        except (ValueError, KeyError):
            continue
        method = row["method_id"]
        model = row["model"]
        cat = method.split("-")[0]

        method_aggs.setdefault(method, AccAgg(method)).add(err)
        model_aggs.setdefault(model, AccAgg(model)).add(err)
        if cat in cat_aggs:
            cat_aggs[cat].add(err)

        key = (model, cat)
        per_model_tool.setdefault(key, AccAgg(f"{model}-{cat}")).add(err)

# Identify models present in both M & T
models_both = {m for (m, c) in per_model_tool if (m, "M") in per_model_tool and (m, "T") in per_model_tool}

# ---------------------------------------------------------------------------
# Build Markdown report
# ---------------------------------------------------------------------------
FIXED_HEADER_COLS = ["n", "mean", "median", "sd", "min", "Q1", "Q3", "max"]
HITS_COLS = [f"≤{t} km" for t in THRESHOLDS]
ALL_COLS = FIXED_HEADER_COLS + HITS_COLS

def make_header(first: str) -> List[str]:
    header = [first] + ALL_COLS
    md_line = "| " + " | ".join(header) + " |"
    sep = "|" + "---|" * len(header)
    return [md_line, sep]

def stats_row(name: str, agg: AccAgg) -> str:
    return "| " + " | ".join([name] + list(map(str, agg.stats_row()))) + " |"

md: List[str] = [
    "# Coordinate accuracy statistics\n",
    "Only locatable grants (`is_locatable == 1`). Error in kilometres (great-circle distance to gold).\n",
]

# Per-method
md.append("### Per-method breakdown\n")
md.extend(make_header("Method"))
for m in sorted(method_aggs):
    md.append(stats_row(m, method_aggs[m]))

# M vs T
md.append("\n### Roll-up: M vs T\n")
md.extend(make_header("Category"))
for cat in ["M", "T"]:
    md.append(stats_row(f"{cat}-methods", cat_aggs[cat]))

# By underlying model
md.append("\n### Roll-up: by underlying model\n")
md.extend(make_header("Model"))
for model in sorted(model_aggs):
    md.append(stats_row(model, model_aggs[model]))

# Tool vs non-tool
md.append("\n### Tool vs non-tool comparison (models with both M & T runs)\n")
# Build header with two leading columns
tool_header = ["Model", "Category"] + ALL_COLS
md.append("| " + " | ".join(tool_header) + " |")
md.append("|" + "---|" * len(tool_header))

for model in sorted(models_both):
    for cat in ["M", "T"]:
        agg = per_model_tool[(model, cat)]
        stats_values = list(map(str, agg.stats_row()))
        md.append("| " + " | ".join([model, f"{cat}-method"] + stats_values) + " |")

# ------------------------------------------------------------------
# Delta comparison: improvement from M to T per model
# ------------------------------------------------------------------
md.append("\n### Effect of tool usage (T vs M)\n")
comp_header = ["Model", "n (M)", "n (T)", "Mean M", "Mean T", "Δ Mean %", "Δ ≤1 km pp", "Δ ≤5 km pp", "Δ ≤10 km pp", "Δ ≤25 km pp", "Δ ≤50 km pp"]
md.append("| " + " | ".join(comp_header) + " |")
md.append("|" + "---|" * len(comp_header))
for model in sorted(models_both):
    agg_m = per_model_tool[(model, "M")]
    agg_t = per_model_tool[(model, "T")]
    n_m = len(agg_m.errors)
    n_t = len(agg_t.errors)
    mean_m = stats.mean(agg_m.errors) if agg_m.errors else math.nan
    mean_t = stats.mean(agg_t.errors) if agg_t.errors else math.nan
    delta_pct = ((mean_m - mean_t) / mean_m * 100) if mean_m else math.nan
    # hit rates list in same order as THRESHOLDS
    def hit_rate(agg, thr):
        return sum(1 for e in agg.errors if e <= thr) / len(agg.errors) * 100 if agg.errors else 0.0
    deltas = [hit_rate(agg_t, thr) - hit_rate(agg_m, thr) for thr in THRESHOLDS]
    md.append(
        f"| {model} | {n_m} | {n_t} | {mean_m:.2f} | {mean_t:.2f} | {delta_pct:.1f}% | "
        + " | ".join(f"{d:+.1f} pp" for d in deltas) + " |")

md.append("\n> Note: The 'Effect of tool usage' table only includes models that have both M and T runs, isolating the change introduced by enabling the tool chain. For a full category-level view, refer to the earlier M-vs-T roll-up.\n")

# ------------------------------------------------------------------
# Best-performing method in each category
# ------------------------------------------------------------------
md.append("\n### Best-performing method per category (lowest mean error)\n")
md.extend(make_header("Category/Method"))
for cat in ["M", "T"]:
    # filter methods of this category
    best_method = None
    best_mean = math.inf
    for m_id, agg in method_aggs.items():
        if m_id.startswith(cat + "-") and agg.errors:
            mu = stats.mean(agg.errors)
            if mu < best_mean:
                best_mean = mu
                best_method = m_id
    if best_method:
        md.append(stats_row(f"{cat} ({best_method})", method_aggs[best_method]))

REPORT_PATH.write_text("\n".join(md))
print(f"Report written to {REPORT_PATH.relative_to(GEOL_ROOT)}") 