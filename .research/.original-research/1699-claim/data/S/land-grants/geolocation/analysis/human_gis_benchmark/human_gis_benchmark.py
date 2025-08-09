import pandas as pd
from pathlib import Path
from textwrap import dedent

# Paths - use ONLY full_results.csv
ANALYSIS_DIR = Path(__file__).resolve().parents[1]  # analysis directory
FULL_RESULTS_CSV = ANALYSIS_DIR / "full_results.csv"

# Output path (markdown table next to this script)
OUTPUT_MD = Path(__file__).with_suffix('.md')

# Load data from full_results.csv only
full_df = pd.read_csv(FULL_RESULTS_CSV)

# Extract human rows from full_results.csv
human_df = full_df[full_df['method_id'] == 'H-1'].copy()

# Filter to rows that have a non-null error (ground-truth inferred) AND are marked as locatable
valid_df = human_df[(human_df['error_km'].notna()) & (human_df['is_locatable'] == 1)].copy()
print(f"Found {len(valid_df)} locatable points with valid error values")

# Since we don't have accuracy categories from validation file, we'll create simple categories
# based on error ranges for the human baseline
def categorize_accuracy(error_km):
    if pd.isna(error_km):
        return 'Unlocatable'
    elif error_km <= 25:
        return 'High (≤25 km)'
    elif error_km <= 75:
        return 'Medium (25-75 km)'
    else:
        return 'Low (>75 km)'

valid_df['accuracy_cat'] = valid_df['error_km'].apply(categorize_accuracy)

# Prepare category information
cat_order = [
    'High (≤25 km)',
    'Medium (25-75 km)', 
    'Low (>75 km)',
    'Unlocatable',
]

# Compute statistics
cat_counts = valid_df['accuracy_cat'].value_counts().reindex(cat_order, fill_value=0)
cat_shares = cat_counts / len(valid_df) * 100
err_stats = (
    valid_df.groupby('accuracy_cat')['error_km']
    .agg(['mean', 'median'])
    .reindex(cat_order)
)

overall_n = len(valid_df)
overall_mean = valid_df['error_km'].mean()
overall_median = valid_df['error_km'].median()

# Build markdown table
md_lines = [
    '| Accuracy Category | N | Share (%) | Mean Error (km) | Median Error (km) |',
    '|---|---|---|---|---|',
    f"| Overall | {overall_n} | 100.0 | {overall_mean:.2f} | {overall_median:.2f} |",
]

def _fmt(x: float) -> str:
    return '—' if pd.isna(x) else f'{x:.2f}'

for cat in cat_order:
    n = cat_counts[cat]
    share = cat_shares[cat]
    mean_err = err_stats.loc[cat, 'mean']
    median_err = err_stats.loc[cat, 'median']
    md_lines.append(
        f"| {cat} | {n} | {share:.1f} | {_fmt(mean_err)} | {_fmt(median_err)} |"
    )

md_table = "\n".join(md_lines)
print(md_table)

# Save markdown file
OUTPUT_MD.write_text(md_table)
print(f"Saved {OUTPUT_MD.relative_to(ANALYSIS_DIR)}") 