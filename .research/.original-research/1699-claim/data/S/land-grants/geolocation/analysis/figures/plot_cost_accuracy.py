import pandas as pd
import re
from pathlib import Path
import matplotlib.pyplot as plt
import sys, importlib, os, pathlib
sys.path.append(str(Path(__file__).parent))
import plot_style  # noqa: F401

ROOT = Path(__file__).resolve().parents[2]
COST_MD = ROOT / "analysis" / "cost_analysis" / "cost_stats.md"
ACC_MD = ROOT / "analysis" / "accuracy_usage" / "accuracy_stats.md"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(exist_ok=True, parents=True)

# parse cost table
cost_rows = []
pat_cost = re.compile(r"\|\s*([A-Z0-9-]+)\s*\|\s*[^|]*\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+[\d,]*\s*\|\s*\d+[\d,]*\s*\|\s*\$([0-9.]+)\s*\|\s*\$([0-9.]+)\s*\|\s*\$([0-9.]+)")
with COST_MD.open() as fh:
    for line in fh:
        m = pat_cost.match(line)
        if m:
            method, total_cost, cost_per_loc, cost_per_1k = m.groups()
            cost_rows.append({
                'Method': method,
                'Cost_per_1k': float(cost_per_1k.replace(',', ''))
            })
cost_df = pd.DataFrame(cost_rows)

# parse accuracy ≤10 km column
acc_rows = []
pat_acc = re.compile(r"\|\s*([A-Z0-9-]+)\s*\|\s*\d+\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*([0-9.]+)%")
with ACC_MD.open() as fh:
    for line in fh:
        m = pat_acc.match(line)
        if m:
            method, hit10 = m.groups()
            acc_rows.append({'Method': method, 'Hit10': float(hit10)})
acc_df = pd.DataFrame(acc_rows)

merge = pd.merge(cost_df, acc_df, on='Method', how='inner')

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(merge['Cost_per_1k'], merge['Hit10'], color='forestgreen')
for _, row in merge.iterrows():
    ax.text(row['Cost_per_1k'], row['Hit10'], row['Method'], fontsize=8, ha='right', va='bottom')
ax.set_xscale('log')
ax.set_xlabel('Cost per 1k located grants (USD, log scale)')
ax.set_ylabel('Hit-rate ≤ 10 km (%)')
ax.set_title('Dollar-for-accuracy frontier')
ax.grid(True, which='major', ls='--', alpha=0.3)
plt.tight_layout()

png_path = OUT_DIR / 'cost_accuracy_scatter.png'
pdf_path = OUT_DIR / 'cost_accuracy_scatter.pdf'
plt.savefig(png_path, dpi=300)
plt.savefig(pdf_path)
print(f'Saved cost-accuracy scatter to {png_path}') 