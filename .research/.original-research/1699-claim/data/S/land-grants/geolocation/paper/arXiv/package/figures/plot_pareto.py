import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # geolocation/
PARETO_CSV = ROOT / "analysis" / "accuracy_extended" / "pareto_points.csv"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(exist_ok=True, parents=True)

# Read data
pdf = pd.read_csv(PARETO_CSV)

plt.rcParams.update({
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'font.size': 10,
    'axes.linewidth': 0.8,
})

sns.set_palette('colorblind')

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(pdf['cost_per_1k'], pdf['mean_error_km'], color='steelblue', s=30, linewidths=0.8, edgecolor='k')

# Map raw model identifiers to display labels
LABEL_MAP = {
    'chatgpt-4o-latest': 'gpt-4o-2024-08-06',
    'human-gis': 'professional GIS'
}

for _, row in pdf.iterrows():
    label = LABEL_MAP.get(row['model'], row['model'])
    x = row['cost_per_1k']
    y = row['mean_error_km']
    if label == 'professional GIS':
        ax.text(x*0.7, y, label, fontsize=8, ha='right', va='bottom')
    else:
        ax.text(x, y, label, fontsize=8, ha='left', va='bottom')

ax.set_xscale('log')
ax.set_xlabel('Cost per 1k located (USD, log scale)')
ax.set_ylabel('Mean error (km)')
ax.set_title('Pareto trade-off: cost vs accuracy')
ax.grid(True, which='major', ls='--', alpha=0.3)
ax.minorticks_off()

plt.tight_layout()
plt.savefig(OUT_DIR / 'pareto_tradeoff.png', dpi=300)
plt.savefig(OUT_DIR / 'pareto_tradeoff.pdf')
print('Figure saved to figures folder') 