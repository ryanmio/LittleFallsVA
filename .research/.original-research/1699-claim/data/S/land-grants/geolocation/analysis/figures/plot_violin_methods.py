import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "analysis" / "full_results.csv"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load and filter
pdf = pd.read_csv(CSV_PATH)
loc = pdf[pdf['is_locatable'].astype(str).isin(['1', 'True', 'true'])].copy()
loc['error_km'] = pd.to_numeric(loc['error_km'], errors='coerce')
loc = loc.dropna(subset=['error_km'])
# Keep only methods with >= 20 located to avoid tiny violins
counts = loc['method_id'].value_counts()
keep_methods = counts[counts >= 20].index.tolist()
loc = loc[loc['method_id'].isin(keep_methods)]

plt.figure(figsize=(10, 4))
sns.violinplot(data=loc, x='method_id', y='error_km', inner='quartile', palette='muted', cut=0)
plt.ylabel('Error (km)')
plt.xlabel('Method')
plt.title('Error distribution per method')
plt.tight_layout()
plt.savefig(OUT_DIR / 'error_violin_methods.png', dpi=300)
plt.savefig(OUT_DIR / 'error_violin_methods.pdf')
print('Violin plot saved.') 