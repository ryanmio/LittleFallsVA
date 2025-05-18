from __future__ import annotations
"""Extended accuracy analysis
Adds:
• 95% bootstrap CI around mean error per method and per model.
• CDF table (0–150 km, 1 km bins) for overall locatable entries.
• Top-N outlier rows per method (largest errors).
• Basic cost-vs-accuracy table comparing two best-performing methods (mean error) with their cost per located grant.
"""
import csv
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple
import statistics as stats
import yaml

GEOL_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = GEOL_ROOT / "analysis"
CSV_PATH = ANALYSIS_DIR / "full_results.csv"
PRICING_YAML = GEOL_ROOT / "pricing.yaml"
OUT_DIR = Path(__file__).parent
REPORT_PATH = OUT_DIR / "extended_accuracy_stats.md"
CDF_PATH = OUT_DIR / "cdf_overall.csv"

THRESHOLDS = [1, 5, 10, 25, 50]
BOOT_ITERS = 1000
OUTLIER_TOP_N = 10

class Agg:
    def __init__(self, name: str):
        self.name = name
        self.errors: List[float] = []
        self.row_ids: List[str] = []

    def add(self, row_id: str, err: float):
        self.errors.append(err)
        self.row_ids.append(row_id)

    # Mean and 95% bootstrap CI
    def mean_ci(self) -> Tuple[float, float, float]:
        if not self.errors:
            return math.nan, math.nan, math.nan
        mean = stats.mean(self.errors)
        if len(self.errors) == 1:
            return mean, mean, mean
        reps = []
        for _ in range(BOOT_ITERS):
            sample = random.choices(self.errors, k=len(self.errors))
            reps.append(stats.mean(sample))
        reps.sort()
        lower = reps[int(0.025 * BOOT_ITERS)]
        upper = reps[int(0.975 * BOOT_ITERS)]
        return mean, lower, upper

    def hit_rate(self, thr: float) -> float:
        if not self.errors:
            return 0.0
        return sum(1 for e in self.errors if e <= thr) / len(self.errors) * 100

# ------------------------------------------------------------------
# Load pricing for cost comparison
with PRICING_YAML.open() as fh:
    PRICES = {d['model']: d for d in yaml.safe_load(fh)}
keys_sorted = sorted(PRICES, key=len, reverse=True)

def price_for(model: str):
    for k in keys_sorted:
        if model.startswith(k):
            return PRICES[k]
    return {"input_per_m": 0.0, "output_per_m": 0.0}

# ------------------------------------------------------------------
method_aggs: Dict[str, Agg] = {}
model_aggs: Dict[str, Agg] = {}
all_errors: List[float] = []
# For cost comparison
cost_per_loc: Dict[str, float] = {}
cost_per_loc_model: Dict[str, float] = {}
located_counts_model: Dict[str, int] = {}

# For global outlier list
global_pairs: List[Tuple[str, str, str, float]] = []  # row_id, method, model, error

with CSV_PATH.open() as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        if row.get("is_locatable") not in {"1", "true", "True"}:
            continue
        try:
            err = float(row['error_km'])
        except (ValueError, KeyError):
            continue
        row_id = str(row['row_index'])
        method = row['method_id']
        model = row['model']
        all_errors.append(err)
        method_aggs.setdefault(method, Agg(method)).add(row_id, err)
        model_aggs.setdefault(model, Agg(model)).add(row_id, err)
        global_pairs.append((row_id, method, model, err))
        # accumulate cost per located per method/model
        pricing = price_for(model)
        in_tok = int(row.get('input_tokens', 0) or 0)
        out_tok = int(row.get('output_tokens', 0) or 0)
        cost_row = (in_tok * pricing['input_per_m'] + out_tok * pricing['output_per_m']) / 1_000_000
        cost_per_loc[method] = cost_per_loc.get(method, 0.0) + cost_row
        cost_per_loc_model[model] = cost_per_loc_model.get(model, 0.0) + cost_row
        located_counts_model[model] = located_counts_model.get(model, 0) + 1

# compute cost per located grant for each method
located_counts = {m: len(a.errors) for m, a in method_aggs.items()}
for m in cost_per_loc:
    if located_counts[m]:
        cost_per_loc[m] /= located_counts[m]

# compute cost per located per model
for model in cost_per_loc_model:
    if located_counts_model[model]:
        cost_per_loc_model[model] /= located_counts_model[model]

# Manual override for human-gis labor cost (140 USD for 44 located)
if "human-gis" in located_counts_model and located_counts_model["human-gis"]:
    cost_per_loc_model["human-gis"] = 140.0 / located_counts_model["human-gis"]

# Identify two best methods by mean error
best_methods = sorted(method_aggs.keys(), key=lambda x: stats.mean(method_aggs[x].errors))[:2]

# ------------------------------------------------------------------
# Write CDF CSV
cdf_lines = ["threshold_km,cumulative_pct\n"]
max_thr = 150
if all_errors:
    n_total = len(all_errors)
    for km in range(max_thr + 1):
        pct = sum(1 for e in all_errors if e <= km) / n_total * 100
        cdf_lines.append(f"{km},{pct:.2f}\n")

# write overall CDF
CDF_PATH.write_text("".join(cdf_lines))

# ------------------------------------------------------------------
# Per-model CDFs
# ------------------------------------------------------------------
MODEL_CDF_DIR = OUT_DIR / "cdf_models"
MODEL_CDF_DIR.mkdir(exist_ok=True)
max_thr_model = 150
for model, agg in model_aggs.items():
    if not agg.errors:
        continue
    lines = ["threshold_km,cumulative_pct\n"]
    n_tot = len(agg.errors)
    for km in range(max_thr_model + 1):
        pct = sum(1 for e in agg.errors if e <= km) / n_tot * 100
        lines.append(f"{km},{pct:.2f}\n")
    (MODEL_CDF_DIR / f"cdf_{model}.csv").write_text("".join(lines))

# ------------------------------------------------------------------
# Build Markdown report
md: List[str] = [
    "# Extended accuracy analysis\n",
    "Includes 95% bootstrap CIs, overall CDF data, top outliers, and cost-accuracy trade-off.\n",
]

# Precision table per method
md.append("## Mean error with 95% CI (per method)\n")
md.append("| Method | n | Mean km | 95% CI |")
md.append("|---|---|---|---|")
for m, agg in sorted(method_aggs.items()):
    mean, lo, hi = agg.mean_ci()
    md.append(f"| {m} | {len(agg.errors)} | {mean:.2f} | [{lo:.2f}, {hi:.2f}] |")

# Global Outliers
md.append("\n## Top outliers overall\n")
md.append("| Row index | Method | Model | Error km |")
md.append("|---|---|---|---|")
global_pairs.sort(key=lambda x: x[3], reverse=True)
for rid, method, model, err in global_pairs[:OUTLIER_TOP_N]:
    md.append(f"| {rid} | {method} | {model} | {err:.2f} |")

# Cost vs accuracy for all models
md.append("\n## Cost-accuracy trade-off by model\n")
md.append("| Model | Mean error km | ≤10 km hit-rate | Cost per 1k located (USD) | Cost per +1% ≤10 km hit (USD) |")
md.append("|---|---|---|---|---|")

# Prepare Pareto CSV
PARETO_PATH = OUT_DIR / "pareto_points.csv"
pareto_lines = ["model,cost_per_1k,mean_error_km\n"]

# Prepare sorted list by mean error
model_sorted = sorted(model_aggs.items(), key=lambda kv: stats.mean(kv[1].errors))
for model, agg in model_sorted:
    mean_err = stats.mean(agg.errors)
    cost_loc = cost_per_loc_model.get(model, math.nan)
    cost_1k = cost_loc * 1000 if math.isfinite(cost_loc) else math.nan
    # hit rate <=10 km
    hit10 = sum(1 for e in agg.errors if e <= 10) / len(agg.errors) * 100 if agg.errors else 0.0
    cost_per_pct = cost_1k / hit10 if hit10 else math.nan
    md.append(f"| {model} | {mean_err:.2f} | {hit10:.1f}% | ${cost_1k:,.2f} | ${cost_per_pct:,.2f} |")
    pareto_lines.append(f"{model},{cost_1k:.2f},{mean_err:.2f}\n")

# write pareto csv
PARETO_PATH.write_text("".join(pareto_lines))

# CDF & Pareto note
md.append("\n*Full CDF data saved to* `" + str(CDF_PATH.relative_to(GEOL_ROOT)) + "`. Pareto points for plotting saved to `" + str(PARETO_PATH.relative_to(GEOL_ROOT)) + "`.")

REPORT_PATH.write_text("\n".join(md))
print(f"Report written to {REPORT_PATH.relative_to(GEOL_ROOT)}") 