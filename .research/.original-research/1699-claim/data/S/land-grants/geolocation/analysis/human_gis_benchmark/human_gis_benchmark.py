import pandas as pd
from pathlib import Path
from textwrap import dedent

# Paths
GEOL_ROOT = Path(__file__).resolve().parents[2]  # geolocation directory
ANALYSIS_DIR = GEOL_ROOT / "analysis"
DATA_ROOT = GEOL_ROOT  # where the validation CSV lives

FULL_RESULTS_CSV = ANALYSIS_DIR / "full_results.csv"
VAL_CSV = DATA_ROOT / "validation - TEST-FULL-H1.csv"

# Output path (markdown table next to this script)
OUTPUT_MD = Path(__file__).with_suffix('.md')

# Load data
full_df = pd.read_csv(FULL_RESULTS_CSV)
val_df = pd.read_csv(VAL_CSV)

# Ensure numeric row index exists in validation file so we can merge
if 'row_index' not in val_df.columns:
    val_df = val_df.reset_index().rename(columns={'index': 'row_index'})
    val_df['row_index'] += 1  # make 1-based like full_results

# Keep only columns we need
val_df = val_df[['row_index', 'h1_accuracy', 'has_ground_truth']]

# Extract human rows from full_results.csv
human_df = full_df[full_df['method_id'] == 'H-1'].copy()

# Merge on row_index (1-to-1 alignment guaranteed by row numbering)
merged = human_df.merge(val_df, on='row_index', how='left', validate='one_to_one')

# Filter to rows that have a non-null error (ground-truth inferred) AND are marked as locatable
valid_df = merged[(merged['error_km'].notna()) & (merged['is_locatable'] == 1)].copy()
print(f"Found {len(valid_df)} locatable points with valid error values")

# Accuracy category column (falls back to Unlocatable if missing)
valid_df['accuracy_cat'] = valid_df['h1_accuracy'].fillna('Unlocatable')

# Prepare category information
cat_order = [
    'High (County + Landmarks)',
    'Medium (County centroid)',
    'Low (State-level)',
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
print(f"Saved {OUTPUT_MD.relative_to(GEOL_ROOT)}") 