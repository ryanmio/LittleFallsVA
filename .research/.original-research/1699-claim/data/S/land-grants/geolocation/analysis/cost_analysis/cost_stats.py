from __future__ import annotations

"""Cost analysis by method
Calculates total API cost per method (T- / M- / H- etc.) using token counts in
`analysis/full_results.csv` and unit prices from `analysis/pricing.yaml`.
Produces a markdown report (`cost_stats.md`) in the same folder with:
• total spend per method
• cost per geolocated grant (is_locatable==1)
• extrapolated cost per 1 000 geolocated grants
• extra columns identifying the underlying model string
"""

import csv
import math
import yaml
from pathlib import Path
from typing import Dict, List

GEOL_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = GEOL_ROOT / "analysis"
FULL_RESULTS_CSV = ANALYSIS_DIR / "full_results.csv"
PRICING_YAML = GEOL_ROOT / "pricing.yaml"
REPORT_PATH = Path(__file__).with_suffix(".md")

# ---------------------------------------------------------------------------
# Load pricing
# ---------------------------------------------------------------------------
with PRICING_YAML.open() as fh:
    PRICES_RAW: List[Dict[str, float]] = yaml.safe_load(fh)

# Build helper to resolve a model string (from full_results) to a pricing entry.
# We use longest-prefix matching.
price_map: Dict[str, Dict[str, float]] = {p["model"]: p for p in PRICES_RAW}
price_keys_sorted = sorted(price_map.keys(), key=len, reverse=True)  # longest first

def resolve_pricing(model_name: str) -> Dict[str, float]:
    for key in price_keys_sorted:
        if model_name.startswith(key):
            return price_map[key]
    # For unpriced models (e.g., human), treat cost as zero tokens cost.
    return {"input_per_m": 0.0, "output_per_m": 0.0}

# ---------------------------------------------------------------------------
# Aggregate results by method
# ---------------------------------------------------------------------------
class MethodAgg:
    def __init__(self, model_str: str):
        self.model_str = model_str
        self.entries = 0
        self.locatable = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.cost_usd = 0.0

    def add(self, row: Dict[str, str]):
        self.entries += 1
        if row.get("is_locatable") in {"1", "true", "True"}:  # treat empty as 0
            self.locatable += 1
        in_tok = int(row.get("input_tokens", 0) or 0)
        out_tok = int(row.get("output_tokens", 0) or 0)
        self.input_tokens += in_tok
        self.output_tokens += out_tok
        pricing = resolve_pricing(self.model_str)
        self.cost_usd += (
            in_tok * pricing["input_per_m"] +
            out_tok * pricing["output_per_m"]
        ) / 1_000_000

method_aggs: Dict[str, MethodAgg] = {}

with FULL_RESULTS_CSV.open() as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        method = row["method_id"]
        model_str = row["model"]
        if method not in method_aggs:
            method_aggs[method] = MethodAgg(model_str)
        method_aggs[method].add(row)

# Manual cost overrides (e.g., human labor not captured by token pricing)
MANUAL_COST_OVERRIDES = {"H-1": 140.0}  # total USD for the method
for m_id, manual_cost in MANUAL_COST_OVERRIDES.items():
    if m_id in method_aggs:
        method_aggs[m_id].cost_usd = manual_cost

# ---------------------------------------------------------------------------
# Build Markdown report
# ---------------------------------------------------------------------------
md: List[str] = [
    "# Cost analysis by method\n",
    "Prices sourced from `analysis/pricing.yaml`. Costs include all entries (regardless of accuracy).",
    "\n### Per-method breakdown\n",
    "| Method | Underlying model | Entries | Located | Input tok | Output tok | Total cost (USD) | Cost per located grant | Cost per 1k located |",
    "|---|---|---|---|---|---|---|---|---|",
]

for method_id, agg in sorted(method_aggs.items()):
    cost_per_loc = agg.cost_usd / agg.locatable if agg.locatable else math.inf
    cost_per_1k = cost_per_loc * 1000 if math.isfinite(cost_per_loc) else math.inf
    md.append(
        f"| {method_id} | {agg.model_str} | {agg.entries} | {agg.locatable} | {agg.input_tokens:,} | {agg.output_tokens:,} | "
        f"${agg.cost_usd:,.2f} | ${cost_per_loc:,.6f} | ${cost_per_1k:,.2f} |"
    )

# ---------------------------------------------------------------------------
# Roll-up: M- vs T- methods
# ---------------------------------------------------------------------------
md.append("\n### Roll-up: M vs T methods\n")
md.append("| Category | Entries | Located | Total cost (USD) | Cost per located grant | Cost per 1k located |")
md.append("|---|---|---|---|---|---|")
cat_aggs = {"M": MethodAgg("mixed"), "T": MethodAgg("mixed")}
for method_id, agg in method_aggs.items():
    cat = method_id.split("-")[0]  # 'M', 'T', 'H', etc.
    if cat in cat_aggs:
        cagg = cat_aggs[cat]
        cagg.entries += agg.entries
        cagg.locatable += agg.locatable
        cagg.input_tokens += agg.input_tokens
        cagg.output_tokens += agg.output_tokens
        cagg.cost_usd += agg.cost_usd
for cat in ["M", "T"]:
    cagg = cat_aggs[cat]
    if cagg.entries == 0:
        continue
    cost_per_loc = cagg.cost_usd / cagg.locatable if cagg.locatable else math.inf
    cost_per_1k = cost_per_loc * 1000 if math.isfinite(cost_per_loc) else math.inf
    md.append(f"| {cat}-methods | {cagg.entries} | {cagg.locatable} | ${cagg.cost_usd:,.2f} | ${cost_per_loc:,.6f} | ${cost_per_1k:,.2f} |")

# ---------------------------------------------------------------------------
# Roll-up: by underlying model
# ---------------------------------------------------------------------------
model_aggs: Dict[str, MethodAgg] = {}
for method_id, agg in method_aggs.items():
    model = agg.model_str
    if model not in model_aggs:
        model_aggs[model] = MethodAgg(model)
    magg = model_aggs[model]
    magg.entries += agg.entries
    magg.locatable += agg.locatable
    magg.input_tokens += agg.input_tokens
    magg.output_tokens += agg.output_tokens
    magg.cost_usd += agg.cost_usd

md.append("\n### Roll-up: by model (all methods)\n")
md.append("| Model | Entries | Located | Total cost (USD) | Cost per located grant | Cost per 1k located |")
md.append("|---|---|---|---|---|---|")
for model, agg in sorted(model_aggs.items()):
    cost_per_loc = agg.cost_usd / agg.locatable if agg.locatable else math.inf
    cost_per_1k = cost_per_loc * 1000 if math.isfinite(cost_per_loc) else math.inf
    md.append(f"| {model} | {agg.entries} | {agg.locatable} | ${agg.cost_usd:,.2f} | ${cost_per_loc:,.6f} | ${cost_per_1k:,.2f} |")

REPORT_PATH.write_text("\n".join(md))
print(f"Report written to {REPORT_PATH.relative_to(GEOL_ROOT)}") 