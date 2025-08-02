import pandas as pd
import re
from pathlib import Path
import matplotlib.pyplot as plt
import sys
sys.path.append(str(Path(__file__).parent))
import plot_style  # noqa: F401

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "analysis" / "tool_usage" / "tool_usage_stats.md"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(exist_ok=True, parents=True)

rows = []
pat = re.compile(r"\|\s*(T-[0-9]+)\s*\|\s*(\d+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*:\s*([0-9.]+)\s*\|\s*([0-9.]+)%")
with MD.open() as fh:
    for line in fh:
        m = pat.match(line)
        if m:
            method, entries, mean_calls, geo_str, cent_str, first = m.groups()
            mean_calls = float(mean_calls)
            geo_ratio = float(geo_str)
            cent_ratio = float(cent_str)
            geo_calls = mean_calls * geo_ratio / (geo_ratio + cent_ratio)
            cent_calls = mean_calls * cent_ratio / (geo_ratio + cent_ratio)
            rows.append({'Method': method, 'Geocode': geo_calls, 'Centroid': cent_calls})

df = pd.DataFrame(rows)
if df.empty:
    quit()

df.set_index('Method', inplace=True)

df[['Geocode', 'Centroid']].plot(kind='barh', stacked=True, color=['#1f77b4', '#ff7f0e'], figsize=(6,3))
plt.xlabel('Average tool calls per entry')
plt.title('Tool-call mix by method')
plt.tight_layout()

png = OUT_DIR / 'tool_calls_stacked.png'
pdf_path = OUT_DIR / 'tool_calls_stacked.pdf'
plt.savefig(png, dpi=300)
plt.savefig(pdf_path)
print(f'Saved tool usage stacked bar to {png}') 