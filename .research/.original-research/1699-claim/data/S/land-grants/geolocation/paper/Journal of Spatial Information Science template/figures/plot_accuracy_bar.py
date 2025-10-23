import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import importlib, sys, os
sys.path.append(str(Path(__file__).parent))
import plot_style  # noqa: F401  (applies rcParams)

ROOT = Path(__file__).resolve().parents[2]  # reach .../analysis
MARKDOWN = ROOT / "analysis" / "accuracy_extended" / "extended_accuracy_stats.md"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(exist_ok=True, parents=True)

# -- Parse markdown table -------------------------------------------------
rows = []
pattern = re.compile(r"\|\s*([^|]+)\s*\|\s*(\d+)\s*\|\s*([0-9.]+)\s*\|\s*\[([0-9.]+),\s*([0-9.]+)\]\s*\|")

with MARKDOWN.open() as fh:
    for line in fh:
        m = pattern.match(line)
        if m:
            method, n, mean, lo, hi = m.groups()
            if method.strip() == 'Method':
                continue
            rows.append({
                'Method': method.strip(),
                'Mean': float(mean),
                'CI_lo': float(lo),
                'CI_hi': float(hi)
            })

if not rows:
    raise RuntimeError("Failed to parse extended_accuracy_stats.md for mean error table")

df = pd.DataFrame(rows)

# Sort by mean ascending for better visual ordering
df = df.sort_values('Mean', ascending=True)

# -- Plot ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7,4))

# Colors (print-friendly): 35% gray fill, black edges/error bars; highlight best in Okabe–Ito green
fill_gray = '#A6A6A6'
edge_color = '#000000'
highlight_color = '#009E73'

# Determine best method (lowest mean)
best_idx = df['Mean'].idxmin()

# Draw bars individually to control colors and edges
for i, (method, mean, lo, hi) in enumerate(zip(df['Method'], df['Mean'], df['CI_lo'], df['CI_hi'])):
    color = highlight_color if df.index[i] == best_idx else fill_gray
    bar = ax.barh([method], [mean], color=color, edgecolor=edge_color, linewidth=0.8)
    # Error bars in black
    ax.errorbar(x=mean, y=[method], xerr=[[mean - lo], [hi - mean]], fmt='none', ecolor=edge_color, elinewidth=0.8, capsize=3)

ax.set_xlabel('Mean error (km) ± 95% CI')
# No in-figure title per print guidance
ax.invert_yaxis()  # best at top

# Faint gridlines already set via plot_style; ensure subtle
ax.grid(True, axis='x')
ax.grid(False, axis='y')

plt.tight_layout()

png_path = OUT_DIR / 'accuracy_bar.png'
pdf_path = OUT_DIR / 'accuracy_bar.pdf'
fig.savefig(png_path, dpi=300)
fig.savefig(pdf_path)
print(f'Saved accuracy bar chart to {png_path}') 