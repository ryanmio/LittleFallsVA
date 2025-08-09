import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import sys, importlib
sys.path.append(str(Path(__file__).parent))
import plot_style  # noqa: F401

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "analysis" / "full_results.csv"
OUT_DIR = Path(__file__).parent

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load
pdf = pd.read_csv(CSV_PATH)
# Filter to only include locatable entries with error values
pdf = pdf[pdf['is_locatable'] == 1]
pdf['error_km'] = pd.to_numeric(pdf['error_km'], errors='coerce')
pdf = pdf.dropna(subset=['error_km'])

# Order methods by median error (ascending)
order = pdf.groupby('method_id')['error_km'].median().sort_values().index.tolist()

plt.figure(figsize=(7,4))
sns.boxplot(data=pdf, x='error_km', y='method_id', order=order, orient='h', showfliers=True)
plt.xlabel('Error (kilometers)')
plt.ylabel('Method')
plt.title('Distribution of geolocation error by method')
plt.grid(axis='x', ls='--', alpha=0.3)
plt.tight_layout()

png = OUT_DIR / 'error_boxplot.png'
pdf_path = OUT_DIR / 'error_boxplot.pdf'
plt.savefig(png, dpi=300)
plt.savefig(pdf_path)
print(f'Saved error boxplot to {png}') 