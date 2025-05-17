#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Falls Church 1699 Settlement Claim - Improved Bayesian Analysis
with proper handling of evidence, constraints, and sensitivity
"""

import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import os
import SALib
from SALib.sample import saltelli
from SALib.analyze import sobol
import warnings

# Print versions for reproducibility
print(f"PyMC version: {pm.__version__}")
print(f"ArviZ version: {az.__version__}")
print(f"SALib version: {SALib.__version__}")

# Set random seeds for reproducibility
np.random.seed(42)
SALTELLI_SEED = 42

# Create output directory for figures if it doesn't exist
if not os.path.exists('figures'):
    os.makedirs('figures')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

print("Running improved Falls Church 1699 Bayesian Analysis...")

# --------------------------------------------------
# MODEL 1: Basic model with independent priors
# --------------------------------------------------
def run_basic_model():
    print("\nRunning basic model with independent priors...")
    with pm.Model() as model_basic:
        # Define prior distributions
        R = pm.Beta('R', alpha=7, beta=3)         # Region habitable
        S = pm.Beta('S', alpha=6, beta=4)         # Structure built
        D = pm.Beta('D', alpha=2.5, beta=7.5)     # Had brick chimney
        
        # Beta-Binomial update for V based on 19th century testimony
        V_prior = pm.Beta('V_prior', alpha=1, beta=9)  # Prior belief about inscribed brick
        # Treat 19th century testimony as a Bernoulli trial with observed success
        brick_obs = pm.Binomial('brick_obs', n=1, p=V_prior, observed=1)
        V = pm.Deterministic('V', V_prior)  # For clarity in output
        
        A = pm.Beta('A', alpha=4, beta=6)         # 1699 accurate
        
        # Define the joint probability using chain rule
        P = pm.Deterministic('P', R * S * D * V * A)
        
        # Sample from the posterior
        trace_basic = pm.sample(4000, tune=2000, random_seed=42)
        
        # Store summary statistics
        summary_basic = az.summary(trace_basic, var_names=['R', 'S', 'D', 'V', 'A', 'P'])
        
    return model_basic, trace_basic, summary_basic

# --------------------------------------------------
# MODEL 2: Model with logical constraint where S=0 whenever R<0.1
# --------------------------------------------------
def run_constrained_model():
    print("\nRunning model with logical constraint (S=0 when R<0.1)...")
    with pm.Model() as model_constrained:
        # Define prior distributions
        R = pm.Beta('R', alpha=7, beta=3)         # Region habitable
        
        # S is now logically constrained by R
        S_raw = pm.Beta('S_raw', alpha=6, beta=4)  # Raw prior for S
        S = pm.Deterministic('S', pm.math.switch(R < 0.1, 0, S_raw))  # S=0 when R<0.1
        
        D = pm.Beta('D', alpha=2.5, beta=7.5)     # Had brick chimney
        
        # Beta-Binomial update for V
        V_prior = pm.Beta('V_prior', alpha=1, beta=9)
        brick_obs = pm.Binomial('brick_obs', n=1, p=V_prior, observed=1)
        V = pm.Deterministic('V', V_prior)
        
        A = pm.Beta('A', alpha=4, beta=6)         # 1699 accurate
        
        # Define the joint probability using chain rule
        P = pm.Deterministic('P', R * S * D * V * A)
        
        # Sample from the posterior
        trace_constrained = pm.sample(4000, tune=2000, random_seed=42)
        
        # Store summary statistics
        summary_constrained = az.summary(trace_constrained, var_names=['R', 'S', 'D', 'V', 'A', 'P'])
        
    return model_constrained, trace_constrained, summary_constrained

# --------------------------------------------------
# Calculate first-order Sobol indices with bootstrap confidence intervals
# --------------------------------------------------
def calculate_sobol_indices(trace, param='P', num_samples=10000):
    print(f"\nCalculating Sobol indices for {param} using SALib (Saltelli sampler, {num_samples} samples)...")
    
    # Extract posterior samples
    p_samples = trace.posterior[param].values.flatten()
    
    # Define parameter bounds for SALib
    problem = {
        'num_vars': 5,
        'names': ['R', 'S', 'D', 'V', 'A'],
        'bounds': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
    }
    
    # Generate samples using Saltelli's method
    param_values = saltelli.sample(problem, num_samples, calc_second_order=False, seed=SALTELLI_SEED)
    
    # Generate model output (P = R*S*D*V*A) for each sample
    Y = param_values[:, 0] * param_values[:, 1] * param_values[:, 2] * param_values[:, 3] * param_values[:, 4]
    
    # Perform Sobol sensitivity analysis
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Si = sobol.analyze(problem, Y, print_to_console=False, calc_second_order=False)
    
    # Calculate bootstrap confidence intervals for Sobol indices
    num_bootstrap = 1000
    S1_bootstrap = np.zeros((num_bootstrap, 5))
    
    for i in range(num_bootstrap):
        # Bootstrap resampling
        idx = np.random.choice(len(Y), len(Y), replace=True)
        Y_boot = Y[idx]
        
        # Calculate Sobol indices for the bootstrap sample
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Si_boot = sobol.analyze(problem, Y_boot, print_to_console=False, calc_second_order=False)
        
        S1_bootstrap[i, :] = Si_boot['S1']
    
    # Calculate confidence intervals
    S1_ci_lower = np.percentile(S1_bootstrap, 2.5, axis=0)
    S1_ci_upper = np.percentile(S1_bootstrap, 97.5, axis=0)
    
    # Compile results
    sobol_results = {
        'Variable': problem['names'],
        'S1': Si['S1'] * 100,  # Convert to percentage
        'S1_CI_lower': S1_ci_lower * 100,
        'S1_CI_upper': S1_ci_upper * 100
    }
    
    # Create DataFrame for easier manipulation
    sobol_df = pd.DataFrame(sobol_results)
    
    return sobol_df

# --------------------------------------------------
# Create figures
# --------------------------------------------------
def create_figures(trace_basic, sobol_df):
    print("\nCreating figures...")
    
    # Figure 1: Posterior density plot
    plt.figure(figsize=(10, 6))
    az.plot_posterior(trace_basic, var_names=['P'], hdi_prob=0.95, 
                     point_estimate='mean', ref_val=0, kind='kde')
    plt.title("Posterior Distribution of Settlement Probability P(E)", fontsize=16)
    plt.xlabel("Probability", fontsize=14)
    plt.ylabel("Density", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/posterior_density.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/posterior_density.png', dpi=300, bbox_inches='tight')
    
    # Figure 2: Sobol indices tornado plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort factors by importance
    sobol_df = sobol_df.sort_values(by='S1', ascending=False)
    
    # Prepare data for plotting
    factors = [f"{f} ({name})" for f, name in 
              zip(sobol_df['Variable'], 
                  ["Region", "Structure", "Chimney", "Inscription", "Accuracy"])]
    values = sobol_df['S1'].values
    lower_ci = sobol_df['S1_CI_lower'].values
    upper_ci = sobol_df['S1_CI_upper'].values
    
    # Create horizontal bar plot
    bars = ax.barh(factors, values, color='steelblue')
    
    # Add confidence intervals
    for i in range(len(factors)):
        ax.plot([lower_ci[i], upper_ci[i]], [i, i], color='black', linewidth=2)
        ax.plot([lower_ci[i]], [i], color='black', marker='|', markersize=10)
        ax.plot([upper_ci[i]], [i], color='black', marker='|', markersize=10)
    
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
    
    plt.tight_layout()
    plt.savefig('figures/sobol_indices.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/sobol_indices.png', dpi=300, bbox_inches='tight')
    
    print("Figures saved.")

# --------------------------------------------------
# Export results to CSV for reproducibility
# --------------------------------------------------
def export_results(summary_basic, summary_constrained, sobol_df):
    print("\nExporting results to CSV...")
    
    # Extract statistics from basic model
    p_mean = summary_basic.loc['P', 'mean']
    p_median = summary_basic.loc['P', '50%']
    p_lower = summary_basic.loc['P', 'hdi_2.5%']
    p_upper = summary_basic.loc['P', 'hdi_97.5%']
    
    # Extract statistics from constrained model
    p_constrained_mean = summary_constrained.loc['P', 'mean']
    
    # Create results DataFrame
    results = {
        'Statistic': [
            'Mean', 'Median', '2.5% CI', '97.5% CI',
            'Constrained Model Mean',
            'R Sobol Index', 'S Sobol Index', 'D Sobol Index', 'V Sobol Index', 'A Sobol Index',
            'R Sobol Lower', 'S Sobol Lower', 'D Sobol Lower', 'V Sobol Lower', 'A Sobol Lower',
            'R Sobol Upper', 'S Sobol Upper', 'D Sobol Upper', 'V Sobol Upper', 'A Sobol Upper'
        ],
        'Value': [
            p_mean, p_median, p_lower, p_upper,
            p_constrained_mean
        ]
    }
    
    # Add Sobol indices, ordering by the variable names in ['R', 'S', 'D', 'V', 'A']
    factor_order = ['R', 'S', 'D', 'V', 'A']
    sobol_ordered = sobol_df.set_index('Variable').loc[factor_order]
    
    # Add Sobol indices and CIs to results
    results['Value'].extend(sobol_ordered['S1'].values)
    results['Value'].extend(sobol_ordered['S1_CI_lower'].values)
    results['Value'].extend(sobol_ordered['S1_CI_upper'].values)
    
    # Save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv('falls_church_results.csv', index=False)
    
    # Save model comparison for Appendix C
    model_comparison = pd.DataFrame({
        'Model': ['Basic Model', 'Constrained Model (S=0 when R<0.1)'],
        'Posterior Mean P(E)': [p_mean, p_constrained_mean],
        'Difference': [0, p_constrained_mean - p_mean]
    })
    model_comparison.to_csv('model_comparison.csv', index=False)
    
    print("Results saved to CSV.")
    print(f"Basic model posterior mean: {p_mean:.6f}")
    print(f"Constrained model posterior mean: {p_constrained_mean:.6f}")
    print(f"Difference: {p_constrained_mean - p_mean:.6f}")
    
    return results_df, model_comparison

# --------------------------------------------------
# Main function to run the full analysis
# --------------------------------------------------
def main():
    # Run the basic model with independent priors
    model_basic, trace_basic, summary_basic = run_basic_model()
    
    # Run the constrained model
    model_constrained, trace_constrained, summary_constrained = run_constrained_model()
    
    # Calculate Sobol indices for sensitivity analysis
    sobol_df = calculate_sobol_indices(trace_basic, param='P', num_samples=10000)
    
    # Create figures
    create_figures(trace_basic, sobol_df)
    
    # Export results
    results_df, model_comparison = export_results(summary_basic, summary_constrained, sobol_df)
    
    print("\nAnalysis complete!")
    print(f"Posterior mean P(E): {summary_basic.loc['P', 'mean']:.6f}")
    print(f"Posterior median P(E): {summary_basic.loc['P', '50%']:.6f}")
    print(f"95% credible interval: [{summary_basic.loc['P', 'hdi_2.5%']:.6f}, {summary_basic.loc['P', 'hdi_97.5%']:.6f}]")
    
    # Print Sobol indices
    print("\nSobol indices (% of variance explained):")
    for idx, row in sobol_df.iterrows():
        print(f"{row['Variable']}: {row['S1']:.1f}% (95% CI: {row['S1_CI_lower']:.1f}% - {row['S1_CI_upper']:.1f}%)")
    
    return model_basic, trace_basic, model_constrained, trace_constrained, sobol_df

if __name__ == "__main__":
    main() 