import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "analysis" / "full_results_v2.csv"
if not CSV_PATH.exists():
    CSV_PATH = ROOT / "analysis" / "full_results.csv"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load and filter data
pdf = pd.read_csv(CSV_PATH)
loc = pdf[pdf['is_locatable'].astype(str).isin(['1', 'True', 'true'])].copy()
loc['error_km'] = pd.to_numeric(loc['error_km'], errors='coerce')
loc = loc.dropna(subset=['error_km'])

# Keep only E-1 + M- / T- series and baseline H-1
allowed = ['E-1', 'H-1']
allowed_prefixes = ('M-', 'T-')
loc = loc[loc['method_id'].apply(lambda m: m in allowed or any(m.startswith(p) for p in allowed_prefixes))]

# Require at least 20 rows per violin to avoid tiny shapes
counts = loc['method_id'].value_counts()
keep_methods = counts[counts >= 20].index.tolist()
loc = loc[loc['method_id'].isin(keep_methods)]

method_order = ['E-1',
                'M-1', 'M-2', 'M-3', 'M-4', 'M-5', 'M-6',
                'T-1', 'T-4',
                'H-1']
method_order = [m for m in method_order if m in keep_methods]

plt.figure(figsize=(10, 6))
sns.violinplot(data=loc, x='method_id', y='error_km', inner='quartile', palette='muted', cut=0, order=method_order)
plt.ylabel('Error (km)')
plt.xlabel('Method')
plt.title('Error distribution (Ensemble & M/T series)')
plt.tight_layout()
plt.savefig(OUT_DIR / 'error_violin_core_methods.png', dpi=300)
plt.savefig(OUT_DIR / 'error_violin_core_methods.pdf')
print('Core violin plot saved.') 