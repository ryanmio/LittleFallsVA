import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import statistics as stats

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "analysis" / "full_results.csv"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
pdf = pd.read_csv(CSV_PATH)
# filter locatable
pdf = pdf[pdf['is_locatable'].astype(str).isin(['1', 'True', 'true'])]

# Ensure numeric error and latency
pdf['error_km'] = pd.to_numeric(pdf['error_km'], errors='coerce')
pdf['latency_s'] = pd.to_numeric(pdf['latency_s'], errors='coerce')

agg = (
    pdf.groupby('model')
    .agg(mean_error_km=('error_km', 'mean'), mean_latency_s=('latency_s', 'mean'))
    .dropna()
    .reset_index()
)
agg['hours_per_1k'] = agg['mean_latency_s'] * 1000 / 3600

# save csv for transparency
agg.to_csv(OUT_DIR / 'pareto_latency_points.csv', index=False)

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(agg['hours_per_1k'], agg['mean_error_km'], color='darkorange')

# label mapping
LABEL_MAP = {
    'chatgpt-4o-latest': 'gpt-4o-2024-08-06',
    'human-gis': 'professional GIS'
}

for _, row in agg.iterrows():
    label = LABEL_MAP.get(row['model'], row['model'])
    x = row['hours_per_1k']
    y = row['mean_error_km']
    if label == 'professional GIS':
        ax.text(x*0.7, y, label, fontsize=8, ha='right', va='bottom')
    else:
        ax.text(x, y, label, fontsize=8, ha='left', va='bottom')

ax.set_xscale('log')
ax.set_xlabel('Wall-clock hours per 1k located (log scale)')
ax.set_ylabel('Mean error (km)')
ax.set_title('Pareto trade-off: latency vs accuracy')
ax.grid(True, which='major', ls='--', alpha=0.3)
ax.minorticks_off()

plt.tight_layout()
plt.savefig(OUT_DIR / 'pareto_latency_tradeoff.png', dpi=300)
plt.savefig(OUT_DIR / 'pareto_latency_tradeoff.pdf')
print('Latency Pareto figure saved.') 