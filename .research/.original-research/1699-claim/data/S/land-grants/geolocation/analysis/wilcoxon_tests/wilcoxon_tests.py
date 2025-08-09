import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
CSV_PATH = Path(__file__).resolve().parent.parent / "full_results_v2.csv"
OUT_MD = Path(__file__).resolve().parent / "wilcoxon_tests.md"
REFERENCE_ID = "E-1"
EXCLUDE_IDS = {"E-2"}

# ----------------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------------

df = pd.read_csv(CSV_PATH)
# drop un-locatable rows per instructions
df = df[~df["row_index"].isin([10, 38])]
if df["error_km"].dtype == object:
    df["error_km"] = pd.to_numeric(df["error_km"], errors="coerce")

# pivot to wide format: rows by row_index, columns by method_id
pivot = df.pivot(index="row_index", columns="method_id", values="error_km")

if REFERENCE_ID not in pivot.columns:
    raise ValueError(f"Reference method_id {REFERENCE_ID} not found in data.")

report_lines = [
    "# Paired Wilcoxon signed-rank tests (alternative='greater')\n",
    "| compared_to | W_stat | p_value |",
    "|-------------|--------|---------|",
]

ref_errors = pivot[REFERENCE_ID]

for method in pivot.columns:
    if method == REFERENCE_ID or method in EXCLUDE_IDS:
        continue
    paired = pivot[[REFERENCE_ID, method]].dropna()
    if paired.empty:
        continue
    # We want to test if baseline (method) errors are GREATER than E-1 errors.
    # SciPy tests the median of (x - y) where x is first argument.
    # Therefore pass baseline first, E-1 second so diff = baseline - E1.
    w_stat, p_val = stats.wilcoxon(paired[method], paired[REFERENCE_ID], alternative="greater")
    report_lines.append(f"| {method} | {w_stat:.0f} | {p_val:.4e} |")

OUT_MD.write_text("\n".join(report_lines))
print(f"Wilcoxon test report written to {OUT_MD.relative_to(Path(__file__).parent.parent)}") 