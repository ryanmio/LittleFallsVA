#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Falls Church 1699 Settlement Claim - Bayesian Chain-Rule Analysis
"""

import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter
from SALib.analyze import sobol
from SALib.sample import saltelli

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

# Create output directory for figures if it doesn't exist
import os
if not os.path.exists('figures'):
    os.makedirs('figures')

print("Running Falls Church 1699 Bayesian Analysis...")

# Set random seed for reproducibility
np.random.seed(42)

# --------------------------------------------------
# Define and run the model
# --------------------------------------------------

with pm.Model() as model:
    # Define the five factors as Beta distributions with parameters from the paper
    R = pm.Beta('R', 7, 3)                # Region habitable
    S = pm.Beta('S', 6, 4)                # Structure built
    D = pm.Beta('D', 2.5, 7.5)            # Had brick chimney
    V = pm.Beta('V', 1, 9)                # Bore inscribed brick
    A = pm.Beta('A', 4, 6)                # 1699 accurate
    
    # Joint probability (chain rule)
    P = pm.Deterministic('P', R * S * D * V * A)
    
    # Sample from the posterior
    trace = pm.sample(4000, tune=2000, random_seed=42, return_inferencedata=True)

print("Sampling complete.")

# --------------------------------------------------
# Results Analysis
# --------------------------------------------------

# Extract posterior samples for calculation
samples = az.extract(trace, var_names=["R", "S", "D", "V", "A", "P"])
r_samples = samples.R.values
s_samples = samples.S.values
d_samples = samples.D.values
v_samples = samples.V.values
a_samples = samples.A.values
p_samples = samples.P.values

# Calculate summary statistics
p_mean = np.mean(p_samples)
p_median = np.median(p_samples)
p_95_interval = np.percentile(p_samples, [2.5, 97.5])

print(f"Posterior P(E) mean: {p_mean:.3f}")     # Result: 0.004
print(f"Posterior P(E) median: {p_median:.3f}") # Result: 0.002
print(f"95% credible interval: [{p_95_interval[0]:.3f}, {p_95_interval[1]:.3f}]") # Result: [0.000, 0.020]

# --------------------------------------------------
# Figure 1: Posterior density plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))
az.plot_posterior(trace, var_names=["P"], hdi_prob=0.95, 
                 point_estimate="mean", ax=ax)

# Customize the plot
ax.set_title("Posterior Distribution of Settlement Probability P(E)", fontsize=16)
ax.set_xlabel("Probability", fontsize=14)
ax.grid(True, alpha=0.3)

# Annotate with summary statistics
stats_text = (
    f"Mean: {p_mean:.3f}\n"
    f"Median: {p_median:.3f}\n"
    f"95% CI: [{p_95_interval[0]:.3f}, {p_95_interval[1]:.3f}]"
)
ax.text(0.65, 0.7, stats_text, transform=ax.transAxes, 
        bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

# Save the figure
plt.tight_layout()
plt.savefig('figures/posterior_density.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/posterior_density.png', dpi=300, bbox_inches='tight')
print("Figure 1 saved.")

# --------------------------------------------------
# Sensitivity Analysis (First-order Sobol indices)
# --------------------------------------------------

# SALib rigorous Sobol analysis
problem = {
    'num_vars': 5,
    'names': ['R', 'S', 'D', 'V', 'A'],
    'bounds': [[0, 1]] * 5
}

# Combine the independent posterior draws into a sample matrix
X = np.vstack([r_samples, s_samples, d_samples, v_samples, a_samples]).T  # shape (n_samples, 5)
Y = p_samples  # output

sobol_res = sobol.analyze(problem, Y, calc_second_order=False, print_to_console=False)

sobol_indices = {
    'R': sobol_res['S1'][0] * 100,
    'S': sobol_res['S1'][1] * 100,
    'D': sobol_res['S1'][2] * 100,
    'V': sobol_res['S1'][3] * 100,
    'A': sobol_res['S1'][4] * 100,
}

print("Sobol indices (% of variance explained, SALib rigorous):")
for factor, index in sobol_indices.items():
    print(f"{factor}: {index:.1f}%")

# --------------------------------------------------
# Figure 2: Tornado plot of Sobol indices
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))

# Sort factors by importance
sorted_factors = sorted(sobol_indices.items(), key=lambda x: x[1], reverse=True)
factors = [f"{f} ({name})" for f, name in 
           zip([item[0] for item in sorted_factors], 
               ["Region", "Structure", "Chimney", "Inscription", "Accuracy"])]
values = [item[1] for item in sorted_factors]

# Create horizontal bar plot
bars = ax.barh(factors, values, color='steelblue')

# Customize the plot
ax.set_title("Variance Contribution by Factor (First-Order Sobol Indices)", fontsize=16)
ax.set_xlabel("Percentage of Variance Explained", fontsize=14)
ax.xaxis.set_major_formatter(PercentFormatter())
ax.grid(True, alpha=0.3, axis='x')

# Add value labels to the bars
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
            f"{width:.1f}%", ha='left', va='center')

# Save the figure
plt.tight_layout()
plt.savefig('figures/sobol_indices.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figures/sobol_indices.png', dpi=300, bbox_inches='tight')
print("Figure 2 saved.")

# --------------------------------------------------
# Export results to CSV for reproducibility
# --------------------------------------------------

# Create a DataFrame with all results
results_df = pd.DataFrame({
    'Statistic': ['Mean', 'Median', '2.5% CI', '97.5% CI'] + 
                 [f"{f} Sobol Index" for f in "RSDVA"],
    'Value': [p_mean, p_median, p_95_interval[0], p_95_interval[1]] +
             [sobol_indices[f] for f in "RSDVA"]
})

# Save to CSV
results_df.to_csv('falls_church_results.csv', index=False)
print("Results saved to CSV.")

print("Analysis complete.") 