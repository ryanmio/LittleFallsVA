import pandas as pd
import numpy as np
from pathlib import Path

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
CSV_PATH = Path(__file__).resolve().parent.parent / "full_results_v2.csv"
OUT_MD = Path(__file__).resolve().parent / "bootstrap_ci.md"
N_BOOT = 1000
ALPHA = 0.05  # for 95% CI

# ----------------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------------

df = pd.read_csv(CSV_PATH)
# drop un-locatable rows per instructions
df = df[~df["row_index"].isin([10, 38])]
# guard : ensure error_km numeric
if df["error_km"].dtype == object:
    df["error_km"] = pd.to_numeric(df["error_km"], errors="coerce")

report_lines = [
    "# Bootstrap 95% confidence intervals for mean error\n",
    "| method_id | N | mean_km | ci_low | ci_high | median_km |",
    "|-----------|---|---------|--------|---------|-----------|",
]

rng = np.random.default_rng(seed=42)

for method, g in df.groupby("method_id"):
    errors = g["error_km"].dropna().values
    n = len(errors)
    if n == 0:
        continue
    mean_val = errors.mean()
    median_val = np.median(errors)
    # bootstrap means
    boot_means = []
    for _ in range(N_BOOT):
        sample = rng.choice(errors, size=n, replace=True)
        boot_means.append(sample.mean())
    ci_low, ci_high = np.percentile(boot_means, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
    report_lines.append(
        f"| {method} | {n} | {mean_val:.2f} | {ci_low:.2f} | {ci_high:.2f} | {median_val:.2f} |"
    )

# write markdown
OUT_MD.write_text("\n".join(report_lines))
print(f"Bootstrap CI report written to {OUT_MD.relative_to(Path(__file__).parent.parent)}") 