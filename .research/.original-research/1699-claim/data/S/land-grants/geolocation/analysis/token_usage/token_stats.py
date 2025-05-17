from __future__ import annotations
"""Token usage analysis by method.
Aggregates input_tokens, output_tokens, and reasoning_tokens per method from
`analysis/full_results.csv`.
Generates markdown report (`token_stats.md`) with:
• per-method totals and per-located-grant averages
• roll-ups for M vs T categories
• roll-ups by underlying model.
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
        self.t_in = 0  # input_tokens
        self.t_out = 0  # output_tokens
        self.t_reason = 0  # reasoning_tokens

    def add(self, row: Dict[str, str]):
        self.entries += 1
        if row.get("is_locatable") in {"1", "true", "True"}:
            self.located += 1
        self.t_in += int(row.get("input_tokens", 0) or 0)
        self.t_out += int(row.get("output_tokens", 0) or 0)
        self.t_reason += int(row.get("reasoning_tokens", 0) or 0)

method_aggs: Dict[str, Agg] = {}

with FULL_RESULTS_CSV.open() as fh:
    for row in csv.DictReader(fh):
        m_id = row["method_id"]
        model = row["model"]
        if m_id not in method_aggs:
            method_aggs[m_id] = Agg(model)
        method_aggs[m_id].add(row)

# Build markdown
md: List[str] = [
    "# Token usage analysis by method\n",
    "Source: `analysis/full_results.csv`\n",
    "### Per-method breakdown\n",
    "| Method | Model | Entries | Located | Input tok | Output tok | Reasoning tok | Tokens per located | Tokens/1k located |",
    "|---|---|---|---|---|---|---|---|---|",
]
for mid, agg in sorted(method_aggs.items()):
    per_loc = (agg.t_in + agg.t_out + agg.t_reason) / agg.located if agg.located else math.inf
    per_1k = per_loc * 1000 if math.isfinite(per_loc) else math.inf
    md.append(
        f"| {mid} | {agg.model} | {agg.entries} | {agg.located} | {agg.t_in:,} | {agg.t_out:,} | {agg.t_reason:,} | {per_loc:,.2f} | {per_1k:,.0f} |"
    )

# Roll-up M vs T
md.append("\n### Roll-up: M vs T methods\n")
md.append("| Category | Entries | Located | Input tok | Output tok | Reasoning tok | Tokens per located | Tokens/1k located |")
md.append("|---|---|---|---|---|---|---|---|")
cat_aggs = {"M": Agg("mixed"), "T": Agg("mixed")}
for mid, a in method_aggs.items():
    cat = mid.split("-")[0]
    if cat in cat_aggs:
        c = cat_aggs[cat]
        c.entries += a.entries
        c.located += a.located
        c.t_in += a.t_in
        c.t_out += a.t_out
        c.t_reason += a.t_reason
for cat in ["M", "T"]:
    a = cat_aggs[cat]
    if a.entries == 0:
        continue
    per_loc = (a.t_in + a.t_out + a.t_reason) / a.located if a.located else math.inf
    per_1k = per_loc * 1000 if math.isfinite(per_loc) else math.inf
    md.append(f"| {cat}-methods | {a.entries} | {a.located} | {a.t_in:,} | {a.t_out:,} | {a.t_reason:,} | {per_loc:,.2f} | {per_1k:,.0f} |")

# Roll-up by model
model_aggs: Dict[str, Agg] = {}
for mid, a in method_aggs.items():
    m = a.model
    if m not in model_aggs:
        model_aggs[m] = Agg(m)
    ma = model_aggs[m]
    ma.entries += a.entries
    ma.located += a.located
    ma.t_in += a.t_in
    ma.t_out += a.t_out
    ma.t_reason += a.t_reason
md.append("\n### Roll-up: by model\n")
md.append("| Model | Entries | Located | Input tok | Output tok | Reasoning tok | Tokens per located | Tokens/1k located |")
md.append("|---|---|---|---|---|---|---|---|")
for m, a in sorted(model_aggs.items()):
    per_loc = (a.t_in + a.t_out + a.t_reason) / a.located if a.located else math.inf
    per_1k = per_loc * 1000 if math.isfinite(per_loc) else math.inf
    md.append(f"| {m} | {a.entries} | {a.located} | {a.t_in:,} | {a.t_out:,} | {a.t_reason:,} | {per_loc:,.2f} | {per_1k:,.0f} |")

REPORT_PATH.write_text("\n".join(md))
print(f"Report written to {REPORT_PATH.relative_to(GEOL_ROOT)}") 