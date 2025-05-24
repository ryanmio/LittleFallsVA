"""Common Matplotlib style for academic figures.
Importing this module applies serif fonts, small sizes, and subtle grid lines.
"""
import matplotlib as mpl

mpl.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'axes.linewidth': 0.8,
    'grid.color': '#CCCCCC',
    'grid.linestyle': '--',
    'grid.linewidth': 0.4,
    'axes.grid': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'errorbar.capsize': 3,
}) 