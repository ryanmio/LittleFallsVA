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
ax.barh(df['Method'], df['Mean'], xerr=[df['Mean']-df['CI_lo'], df['CI_hi']-df['Mean']], color='steelblue', alpha=0.8)
ax.set_xlabel('Mean error (km) ± 95% CI')
ax.set_title('Coordinate accuracy by method')
ax.invert_yaxis()  # best at top
plt.tight_layout()

png_path = OUT_DIR / 'accuracy_bar.png'
pdf_path = OUT_DIR / 'accuracy_bar.pdf'
fig.savefig(png_path, dpi=300)
fig.savefig(pdf_path)
print(f'Saved accuracy bar chart to {png_path}') 