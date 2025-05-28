import pandas as pd
import yaml
from pathlib import Path
from textwrap import dedent
import json
from collections import defaultdict

# Paths (relative to repo root)
ROOT = Path(__file__).resolve().parents[1]  # analysis directory
RESULTS_CSV = ROOT / "full_results.csv"  # Use the full_results.csv in analysis directory
PRICING_YAML = ROOT.parent / "pricing.yaml"  # pricing.yaml is in the parent directory

# Load data - full_results.csv should have all the data we need
results_df = pd.read_csv(RESULTS_CSV)

# The full_results.csv should already have the ground truth filtering built in
# Filter to only rows that are locatable and have ground truth
df = results_df[(results_df['is_locatable'] == 1) & (results_df['error_km'].notna())]

# Ensure numeric columns
for col in ['error_km', 'latency_s', 'total_tokens', 'input_tokens', 'output_tokens']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Load pricing config
with open(PRICING_YAML) as f:
    pricing_raw = yaml.safe_load(f)

# Normalize to dict of model->rates
pricing = {}
for item in pricing_raw:
    model = item['model']
    pricing[model] = (item['input_per_m'], item['output_per_m'])

# Helper: map model id to base pricing key
def match_model(model_id: str):
    for base in pricing.keys():
        if model_id.startswith(base):
            return base
    raise KeyError(f"No pricing entry for model id {model_id}")

def compute_token_cost(row):
    try:
        base = match_model(row['model'])
    except KeyError:
        return None
    in_rate, out_rate = pricing[base]
    cost = (row['input_tokens'] * in_rate + row['output_tokens'] * out_rate) / 1_000_000
    return cost

df['token_cost'] = df.apply(compute_token_cost, axis=1)

# Google API calls & cost - if this data is in full_results.csv, use it directly
# Otherwise set to 0 for methods that don't use tools
if 'google_calls' in df.columns:
    df['google_cost'] = df['google_calls'] * 0.005
else:
    df['google_calls'] = 0
    df['google_cost'] = 0.0

# Aggregate per method_id
rows = []
for method_id, g in df.groupby('method_id'):
    n = len(g)
    errors = g['error_km'].dropna()
    mean_err = errors.mean()
    median_err = errors.median()
    p25 = errors.quantile(0.25)
    p75 = errors.quantile(0.75)

    # Accuracy bands
    high = (errors < 1).sum()
    med = ((errors >= 1) & (errors < 10)).sum()
    low = (errors >= 10).sum()
    high_pct = high / n * 100 if n else 0
    med_pct = med / n * 100 if n else 0
    low_pct = low / n * 100 if n else 0

    # Success rate (error not null)
    success = errors.count()
    success_rate = success / n * 100 if n else 0

    mean_lat = g['latency_s'].mean()
    token_total = g['total_tokens'].sum()
    cost_token = g['token_cost'].sum()
    google_calls = g['google_calls'].sum()
    google_cost = g['google_cost'].sum()

    fixed_cost = 140.0 if method_id == 'H-1' else 0.0

    rows.append(dict(method_id=method_id, N=n,
                     mean_err=mean_err, median_err=median_err,
                     p25=p25, p75=p75,
                     high_pct=high_pct, med_pct=med_pct, low_pct=low_pct,
                     success_rate=success_rate,
                     mean_latency=mean_lat,
                     token_total=token_total,
                     token_cost=cost_token,
                     google_calls=google_calls,
                     google_cost=google_cost,
                     fixed_human_cost=fixed_cost))

# Convert to DataFrame & sort
out_df = pd.DataFrame(rows)
out_df = out_df.sort_values('mean_err', ascending=True)

# Build Markdown table
def fmt(f):
    if pd.isna(f):
        return '—'
    if isinstance(f, int):
        return str(f)
    return f"{f:.2f}"

cols_order = ['method_id', 'N', 'mean_err', 'median_err', 'p25', 'p75',
              'high_pct', 'med_pct', 'low_pct', 'success_rate', 'mean_latency',
              'token_total', 'token_cost', 'google_calls', 'google_cost', 'fixed_human_cost']

md_lines = ["| " + " | ".join(cols_order) + " |",
            "|" + "---|"*len(cols_order)]
for _, row in out_df.iterrows():
    cells = []
    for c in cols_order:
        val = row[c]
        if c == 'method_id':
            cells.append(str(val))
        else:
            cells.append(fmt(val))
    md_lines.append("| " + " | ".join(cells) + " |")

md_table = "\n".join(md_lines)
print(md_table)

# Save output
OUTPUT = Path(__file__).with_suffix('.md')
OUTPUT.write_text(md_table)
print(f"Saved {OUTPUT.relative_to(ROOT)}") 