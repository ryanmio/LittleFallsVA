import csv, statistics, pathlib, collections, math
import random
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------
# Length-stratified accuracy analysis
# ---------------------------------------------------------------
# Goal: investigate whether model error correlates with the *length* of the
# patent abstract.
#
# Operational definition of length
# -------------------------------
# The raw abstract text is not stored alongside the model outputs; however
# each call logged in `full_results.csv` records `input_tokens`, i.e. the number
# of tokens sent to the OpenAI API (prompt + abstract).
#
# • The prompt component is **constant** for all one-shot calls (≈30 tokens).
# • Tool-chain calls include additional system messages and function schemas,
#   so their `input_tokens` are inflated relative to the same abstract.
#
# To obtain a tool-agnostic proxy for abstract length we therefore take, **for
# each row_index**, the *minimum* `input_tokens` observed across all methods.
# This minimum always corresponds to a one-shot call and is thus
# (prompt-constant + abstract-tokens).  Subtracting the prompt constant is
# unnecessary because it would shift all lengths equally and therefore not
# affect the median split.
#
# Analysis steps
# 1. First pass: collect the minimum input_tokens for every `row_index` that
#    has a ground-truth coordinate (`is_locatable == 1`).
# 2. Compute the median of those minima to divide entries into "short" and
#    "long" cohorts.
# 3. Second pass: aggregate error_km by cohort and by method.
# 4. Write a Markdown report with overall and per-method means.
# ---------------------------------------------------------------

# `length_stratification.py` lives in geolocation/analysis/length_stratification/
# We need the geolocation root (two levels up) to access analysis/full_results.csv
ROOT = pathlib.Path(__file__).resolve().parents[2]
CSV = ROOT / "analysis" / "full_results.csv"

# NEW PARAMETERS
VALIDATION_CSV = ROOT / "validation - TEST-FULL-H1.csv"
BOOT_ITERS = 1000  # for CI of mean error per cohort

# ---------------------------------------------------------------
# Build length map from validation file (word count of raw_entry)
# ---------------------------------------------------------------
length_map: dict[int, int] = {}
with VALIDATION_CSV.open() as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        rid = int(row["subject_id"].split("_")[-1]) if row.get("subject_id") else None
        if rid is None:
            continue
        if row.get("has_ground_truth") not in {"1", "true", "True"}:
            continue
        raw_text = row.get("raw_entry", "").strip()
        length_map[rid] = len(raw_text.split())  # word count

median_len = statistics.median(length_map.values())

# Containers for stats (excluding H-1)
errors_by_len = collections.defaultdict(list)
errors_by_len_method = collections.defaultdict(lambda: collections.defaultdict(list))
# Collect (length, error) pairs for continuous analysis
xy_pairs: list[tuple[int, float]] = []

with CSV.open() as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        if row.get("is_locatable") not in {"1", "true", "True"}:
            continue
        if row["method_id"] == "H-1":
            continue  # exclude human baseline
        rid = int(row["row_index"])
        if rid not in length_map:
            continue
        length_cat = "short" if length_map[rid] <= median_len else "long"
        err_str = row.get("error_km", "")
        if not err_str:
            continue
        err = float(err_str)
        errors_by_len[length_cat].append(err)
        errors_by_len_method[length_cat][row["method_id"]].append(err)
        xy_pairs.append((length_map[rid], err))  # for regression

# helper for bootstrap CI
def boot_ci(arr):
    if not arr:
        return math.nan, math.nan, math.nan
    mean = statistics.mean(arr)
    reps = [statistics.mean(random.choices(arr, k=len(arr))) for _ in range(BOOT_ITERS)]
    reps.sort()
    return mean, reps[int(0.025*BOOT_ITERS)], reps[int(0.975*BOOT_ITERS)]

random.seed(42)

# ---------------------------------------------------------------
# Build Markdown report
# ---------------------------------------------------------------
report_lines = [
    "# Length-stratified accuracy (LLM methods only)\n",
    f"Length proxy = word-count of raw_entry (median = {median_len})\n\n",
]

for cat in ("short", "long"):
    errs = errors_by_len[cat]
    if not errs:
        continue
    mean_err, lo, hi = boot_ci(errs)
    report_lines.append(f"## {cat.capitalize()} abstracts (n = {len(errs)})\n")
    report_lines.append(f"Overall mean error: **{mean_err:.2f} km**  (95 % CI {lo:.2f}–{hi:.2f})\n\n")
    report_lines.append("| Method | n | Mean km |\n|---|---|---|\n")
    for m, elist in sorted(errors_by_len_method[cat].items()):
        report_lines.append(f"| {m} | {len(elist)} | {statistics.mean(elist):.2f} |\n")
    report_lines.append("\n")

# ---------------------------------------------------------------
# Continuous length–error relationship
# ---------------------------------------------------------------

def pearson_r(pairs):
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    mean_x, mean_y = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    return num / (den_x * den_y) if den_x and den_y else math.nan


def linreg(pairs):
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    mean_x, mean_y = statistics.mean(xs), statistics.mean(ys)
    denom = sum((x - mean_x) ** 2 for x in xs)
    slope = (
        sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denom
        if denom else math.nan
    )
    intercept = mean_y - slope * mean_x if slope is not math.nan else math.nan
    # R^2
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1 - ss_res / ss_tot if ss_tot else math.nan
    return slope, intercept, r2

# Overall regression & correlation
slope, intercept, r2 = linreg(xy_pairs)
r_val = pearson_r(xy_pairs)

# Bootstrap CI for slope
slope_samples = []
for _ in range(BOOT_ITERS):
    sample = random.choices(xy_pairs, k=len(xy_pairs))
    s, _, _ = linreg(sample)
    slope_samples.append(s)
slope_samples.sort()
s_lo = slope_samples[int(0.025 * BOOT_ITERS)]
s_hi = slope_samples[int(0.975 * BOOT_ITERS)]

report_lines.extend(
    [
        "## Continuous length–error relationship\n",
        f"Across **{len(xy_pairs)}** LLM predictions, an OLS fit yields:\n\n",
        f"error_km = {intercept:.2f}  +  {slope:.3f} · length_words\n\n",
        f"Slope: **{slope:.3f} km per word**  (95 % CI {s_lo:.3f}–{s_hi:.3f})\n\n",
        f"Pearson r = {r_val:.3f};  R² = {r2:.3f}\n",
    ]
)

# ---------------------------------------------------------------
# Scatter plot figure
# ---------------------------------------------------------------
fig_dir = ROOT / "analysis" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)
fig_path = fig_dir / "length_vs_error.png"

lengths = [p[0] for p in xy_pairs]
errors = [p[1] for p in xy_pairs]

plt.figure(figsize=(6, 4))
plt.scatter(lengths, errors, s=18, color="#666", alpha=0.6, label="Predictions")

# Regression line and CI band
x_vals = np.linspace(min(lengths), max(lengths), 100)
y_pred = intercept + slope * x_vals
y_lo = intercept + s_lo * x_vals
y_hi = intercept + s_hi * x_vals

plt.plot(x_vals, y_pred, color="red", lw=2, label="OLS fit")
plt.fill_between(x_vals, y_lo, y_hi, color="red", alpha=0.15, label="95% CI")

plt.xlabel("Abstract length (words)")
plt.ylabel("Great-circle error (km)")
plt.title("Length vs geolocation error for LLM predictions")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(fig_path, dpi=300)
plt.close()

report_lines.append("\n![Length vs Error](../figures/length_vs_error.png){#fig:length-vs-error width=\"80%\"}\n")

out_dir = ROOT / "analysis" / "length_stratification"
out_dir.mkdir(exist_ok=True)
report_path = out_dir / "length_stratification_stats.md"
report_path.write_text("".join(report_lines))
print("Report written to", report_path.relative_to(ROOT)) 