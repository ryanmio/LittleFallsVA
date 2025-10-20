import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")
plt.rcParams.update({'pdf.fonttype':42,'ps.fonttype':42,'font.size':10,'axes.linewidth':0.8})
sns.set_palette('colorblind')

LABEL_MAP = {
    'chatgpt-4o-latest': 'gpt-4o-2024-08-06',
    'human-gis': 'Professional GIS',
}

ROOT = Path(__file__).resolve().parents[2]
ACC_DIR = ROOT / "analysis" / "accuracy_extended"
CDF_DIR = ACC_DIR / "cdf_models"
OVERALL_CSV = ACC_DIR / "cdf_overall.csv"
OUT_DIR = Path(__file__).parent / "cdf_graphs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- Overall CDF -----------------
overall = pd.read_csv(OVERALL_CSV)
fig, ax = plt.subplots(figsize=(5,3))
ax.plot(overall['threshold_km'], overall['cumulative_pct'], color='black', linewidth=1.3)
ax.set_xlim(0,100)
ax.set_xlabel('Distance threshold (km)')
ax.set_ylabel('% grants ≤ threshold')
ax.set_title('Overall cumulative accuracy')
plt.tight_layout()
fig.savefig(OUT_DIR / 'cdf_overall.png', dpi=300)
fig.savefig(OUT_DIR / 'cdf_overall.pdf')
plt.close(fig)

# ------------- Combined models ---------------
fig, ax = plt.subplots(figsize=(6,4))
colors = sns.color_palette('tab10')
for i, csv_path in enumerate(sorted(CDF_DIR.glob('cdf_*.csv'))):
    df = pd.read_csv(csv_path)
    model = csv_path.stem.replace('cdf_','')
    label = LABEL_MAP.get(model, model)
    ax.plot(df['threshold_km'], df['cumulative_pct'], label=label, color=colors[i%10], linewidth=1.3)
ax.set_xlim(0,100)
ax.set_xlabel('Distance threshold (km)')
ax.set_ylabel('% grants ≤ threshold')
ax.set_title('Cumulative accuracy by model')
ax.legend(fontsize=8, frameon=False)
plt.tight_layout()
fig.savefig(OUT_DIR / 'cdf_models_combined.png', dpi=300)
fig.savefig(OUT_DIR / 'cdf_models_combined.pdf')
plt.close(fig)

# ------------- Per-model individual plots -------------
for csv_path in CDF_DIR.glob('cdf_*.csv'):
    df = pd.read_csv(csv_path)
    model = csv_path.stem.replace('cdf_','')
    pretty = LABEL_MAP.get(model, model)
    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(df['threshold_km'], df['cumulative_pct'], color='steelblue', linewidth=1.3)
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    ax.set_xlabel('Distance threshold (km)')
    ax.set_ylabel('% grants ≤ threshold')
    ax.set_title(f'Cumulative accuracy – {pretty}')
    plt.tight_layout()
    fig.savefig(OUT_DIR / f'cdf_{model}.png', dpi=300)
    fig.savefig(OUT_DIR / f'cdf_{model}.pdf')
    plt.close(fig)

print('CDF figures saved to', OUT_DIR) 