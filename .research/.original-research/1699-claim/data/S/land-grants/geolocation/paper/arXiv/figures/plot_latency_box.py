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
# numeric
pdf['latency_s'] = pd.to_numeric(pdf['latency_s'], errors='coerce')
pdf = pdf.dropna(subset=['latency_s'])

order = pdf.groupby('method_id')['latency_s'].median().sort_values().index.tolist()

plt.figure(figsize=(7,4))
sns.boxplot(data=pdf, x='latency_s', y='method_id', order=order, orient='h', showfliers=False)
plt.xscale('log')
plt.xlabel('Latency (seconds, log scale)')
plt.ylabel('Method')
plt.title('Distribution of per-grant latency by method')
plt.grid(axis='x', which='both', ls='--', alpha=0.3)
plt.tight_layout()

png = OUT_DIR / 'latency_boxplot.png'
pdf_path = OUT_DIR / 'latency_boxplot.pdf'
plt.savefig(png, dpi=300)
plt.savefig(pdf_path)
print(f'Saved latency boxplot to {png}') 