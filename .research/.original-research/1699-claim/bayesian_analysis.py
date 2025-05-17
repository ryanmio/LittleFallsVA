#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Falls Church 1699 Settlement Claim - Improved Bayesian Analysis
with proper handling of evidence, constraints, and sensitivity
Using NumPy for implementation to avoid dependency issues
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import os

# Set random seed for reproducibility
np.random.seed(42)
SOBOL_SEED = 42

# Create output directory for figures if it doesn't exist
if not os.path.exists('figures'):
    os.makedirs('figures')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

print("Running improved Falls Church 1699 Bayesian Analysis...")

# --------------------------------------------------
# MODEL 1: Basic model with independent priors, but with Beta-Binomial update for V
# --------------------------------------------------
def run_basic_model(n_samples=4000):
    print("\nRunning basic model with Beta-Binomial update for V...")
    
    # Draw samples from prior distributions
    r_samples = np.random.beta(7, 3, n_samples)        # Region habitable
    s_samples = np.random.beta(6, 4, n_samples)        # Structure built
    d_samples = np.random.beta(2.5, 7.5, n_samples)    # Had brick chimney
    
    # For V, we apply Beta-Binomial update
    # Prior: Beta(1, 9)
    # Observation: One positive testimony (Bernoulli trial with success)
    # Posterior: Beta(1+1, 9+0) = Beta(2, 9)
    v_raw_samples = np.random.beta(2, 9, n_samples)        # Raw inscribed brick distribution
    
    # Logical constraint: V=0 whenever D=0 (can't have an inscribed brick without a chimney)
    v_samples = np.where(d_samples > 0, v_raw_samples, 0)  # Apply constraint
    
    a_samples = np.random.beta(4, 6, n_samples)        # 1699 accurate
    
    # Calculate joint probability (chain rule)
    p_samples = r_samples * s_samples * d_samples * v_samples * a_samples
    
    # Calculate summary statistics
    p_mean = np.mean(p_samples)
    p_median = np.median(p_samples)
    p_95_interval = np.percentile(p_samples, [2.5, 97.5])
    
    # Save all samples for later use
    samples = {
        'R': r_samples,
        'S': s_samples, 
        'D': d_samples,
        'V': v_samples,
        'A': a_samples,
        'P': p_samples
    }
    
    # Create a summary dictionary
    summary = {
        'mean': {'R': np.mean(r_samples), 'S': np.mean(s_samples), 
                'D': np.mean(d_samples), 'V': np.mean(v_samples), 
                'A': np.mean(a_samples), 'P': p_mean},
        'median': {'R': np.median(r_samples), 'S': np.median(s_samples), 
                  'D': np.median(d_samples), 'V': np.median(v_samples), 
                  'A': np.median(a_samples), 'P': p_median},
        '2.5%': {'R': np.percentile(r_samples, 2.5), 'S': np.percentile(s_samples, 2.5), 
                'D': np.percentile(d_samples, 2.5), 'V': np.percentile(v_samples, 2.5), 
                'A': np.percentile(a_samples, 2.5), 'P': p_95_interval[0]},
        '97.5%': {'R': np.percentile(r_samples, 97.5), 'S': np.percentile(s_samples, 97.5), 
                 'D': np.percentile(d_samples, 97.5), 'V': np.percentile(v_samples, 97.5), 
                 'A': np.percentile(a_samples, 97.5), 'P': p_95_interval[1]}
    }
    
    print(f"Posterior mean P(E): {p_mean:.6f}")
    print(f"Posterior median P(E): {p_median:.6f}")
    print(f"95% credible interval: [{p_95_interval[0]:.6f}, {p_95_interval[1]:.6f}]")
    
    return samples, summary

# --------------------------------------------------
# MODEL 2: Model with logical constraint where S=0 whenever R<0.1
# --------------------------------------------------
def run_constrained_model(n_samples=4000):
    print("\nRunning model with logical constraint (S=0 when R<0.1)...")
    
    # Draw samples from prior distributions
    r_samples = np.random.beta(7, 3, n_samples)        # Region habitable
    
    # Apply logical constraint: S=0 when R<0.1
    s_raw_samples = np.random.beta(6, 4, n_samples)    # Raw structure prior
    s_samples = np.where(r_samples < 0.1, 0, s_raw_samples)  # Apply constraint
    
    d_samples = np.random.beta(2.5, 7.5, n_samples)    # Had brick chimney
    
    # Beta-Binomial update for V (Beta(1,9) → Beta(2,9))
    v_raw_samples = np.random.beta(2, 9, n_samples)        # Raw inscribed brick distribution
    
    # Logical constraint: V=0 whenever D=0 (can't have an inscribed brick without a chimney)
    v_samples = np.where(d_samples > 0, v_raw_samples, 0)  # Apply constraint
    
    a_samples = np.random.beta(4, 6, n_samples)        # 1699 accurate
    
    # Calculate joint probability (chain rule)
    p_samples = r_samples * s_samples * d_samples * v_samples * a_samples
    
    # Calculate summary statistics
    p_mean = np.mean(p_samples)
    p_median = np.median(p_samples)
    p_95_interval = np.percentile(p_samples, [2.5, 97.5])
    
    # Save all samples for later use
    samples = {
        'R': r_samples,
        'S': s_samples, 
        'D': d_samples,
        'V': v_samples,
        'A': a_samples,
        'P': p_samples
    }
    
    # Create a summary dictionary
    summary = {
        'mean': {'R': np.mean(r_samples), 'S': np.mean(s_samples), 
                'D': np.mean(d_samples), 'V': np.mean(v_samples), 
                'A': np.mean(a_samples), 'P': p_mean},
        'median': {'R': np.median(r_samples), 'S': np.median(s_samples), 
                  'D': np.median(d_samples), 'V': np.median(v_samples), 
                  'A': np.median(a_samples), 'P': p_median},
        '2.5%': {'R': np.percentile(r_samples, 2.5), 'S': np.percentile(s_samples, 2.5), 
                'D': np.percentile(d_samples, 2.5), 'V': np.percentile(v_samples, 2.5), 
                'A': np.percentile(a_samples, 2.5), 'P': p_95_interval[0]},
        '97.5%': {'R': np.percentile(r_samples, 97.5), 'S': np.percentile(s_samples, 97.5), 
                 'D': np.percentile(d_samples, 97.5), 'V': np.percentile(v_samples, 97.5), 
                 'A': np.percentile(a_samples, 97.5), 'P': p_95_interval[1]}
    }
    
    print(f"Posterior mean P(E): {p_mean:.6f}")
    print(f"Posterior median P(E): {p_median:.6f}")
    print(f"95% credible interval: [{p_95_interval[0]:.6f}, {p_95_interval[1]:.6f}]")
    
    return samples, summary

# --------------------------------------------------
# Calculate first-order Sobol indices with bootstrap confidence intervals
# --------------------------------------------------
def calculate_sobol_indices(samples, param='P', num_samples=10000):
    print(f"\nCalculating Sobol indices for {param} using Saltelli's method ({num_samples} samples)...")
    
    # Implementation of the Saltelli method for first-order Sobol indices
    # (Simplified version without SALib dependency)
    
    np.random.seed(SOBOL_SEED)  # Set seed for reproducibility
    
    # Generate two independent sample matrices
    def generate_sample_matrix(size):
        return np.column_stack([
            np.random.beta(7, 3, size),      # R
            np.random.beta(6, 4, size),      # S
            np.random.beta(2.5, 7.5, size),  # D
            np.random.beta(2, 9, size),      # V (with Beta-Binomial update)
            np.random.beta(4, 6, size)       # A
        ])
    
    # Number of base samples (will result in N*(D+2) total evaluations)
    N = num_samples // 7  # Approximating Saltelli's recommended size
    
    # Generate sample matrices
    A = generate_sample_matrix(N)  # First sample matrix
    B = generate_sample_matrix(N)  # Second sample matrix
    
    # Function to evaluate the model
    def evaluate_model(params):
        # Extract individual parameters
        R = params[:, 0]
        S = params[:, 1]
        D = params[:, 2]
        V_raw = params[:, 3]
        A = params[:, 4]
        
        # Apply logical constraint: V=0 whenever D=0
        V = np.where(D > 0, V_raw, 0)
        
        # P = R * S * D * V * A
        return R * S * D * V * A
    
    # Evaluate f(A) and f(B)
    f_A = evaluate_model(A)
    f_B = evaluate_model(B)
    
    # Calculate total variance
    f_all = np.concatenate([f_A, f_B])
    V_Y = np.var(f_all, ddof=1)
    
    # Calculate first-order Sobol indices
    S1 = np.zeros(5)
    S1_bootstrap_samples = np.zeros((1000, 5))
    
    for i in range(5):
        # Create A_B matrix where only the i-th column is from B
        A_B = A.copy()
        A_B[:, i] = B[:, i]
        
        # Evaluate f(A_B)
        f_A_B = evaluate_model(A_B)
        
        # First-order index formula: S_i = Var_i / Var_total
        # where Var_i = Var_Y - E[(f(A) - f(A_B))²]/2
        S1[i] = (np.mean(f_B * f_A_B) - np.mean(f_A) * np.mean(f_B)) / V_Y
        
        # Bootstrap for confidence intervals
        for j in range(1000):
            # Bootstrap sampling with replacement
            idx = np.random.choice(N, N, replace=True)
            f_A_boot = f_A[idx]
            f_B_boot = f_B[idx]
            f_A_B_boot = f_A_B[idx]
            
            # Calculate S1 for this bootstrap sample
            V_Y_boot = (np.var(np.concatenate([f_A_boot, f_B_boot]), ddof=1))
            S1_bootstrap_samples[j, i] = (np.mean(f_B_boot * f_A_B_boot) - 
                                         np.mean(f_A_boot) * np.mean(f_B_boot)) / V_Y_boot
    
    # Calculate confidence intervals
    S1_ci_lower = np.percentile(S1_bootstrap_samples, 2.5, axis=0)
    S1_ci_upper = np.percentile(S1_bootstrap_samples, 97.5, axis=0)
    
    # Convert to percentages
    S1 = S1 * 100
    S1_ci_lower = S1_ci_lower * 100
    S1_ci_upper = S1_ci_upper * 100
    
    # Create DataFrame
    variables = ['R', 'S', 'D', 'V', 'A']
    sobol_df = pd.DataFrame({
        'Variable': variables,
        'S1': S1,
        'S1_CI_lower': S1_ci_lower,
        'S1_CI_upper': S1_ci_upper
    })
    
    # Print results
    print("\nSobol indices (% of variance explained, Saltelli method, seed 42):")
    for i, var in enumerate(variables):
        print(f"{var}: {S1[i]:.1f}% (95% CI: {S1_ci_lower[i]:.1f}% - {S1_ci_upper[i]:.1f}%)")
    
    return sobol_df

# --------------------------------------------------
# Create figures
# --------------------------------------------------
def create_figures(samples, sobol_df):
    print("\nCreating figures...")
    
    # Figure 1: Posterior density plot for P
    plt.figure(figsize=(10, 6))
    sns.kdeplot(samples['P'], fill=True, color='steelblue')
    
    # Add vertical lines for mean and median
    plt.axvline(np.mean(samples['P']), color='red', linestyle='--', 
                label=f'Mean: {np.mean(samples["P"]):.4f}')
    plt.axvline(np.median(samples['P']), color='green', linestyle='-.', 
                label=f'Median: {np.median(samples["P"]):.4f}')
    
    # Add shading for 95% CI
    ci = np.percentile(samples['P'], [2.5, 97.5])
    plt.axvspan(ci[0], ci[1], alpha=0.2, color='gray', 
                label=f'95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]')
    
    plt.title("Posterior Distribution of Settlement Probability P(E)", fontsize=16)
    plt.xlabel("Probability", fontsize=14)
    plt.ylabel("Density", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/posterior_density.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figures/posterior_density.png', dpi=300, bbox_inches='tight')
    
    # Figure 2: Sobol indices tornado plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort factors by importance
    sobol_df = sobol_df.sort_values(by='S1', ascending=False)
    
    # Correct mapping of variables to their meanings
    factor_meanings = {
        'R': "Region habitable",
        'S': "Structure built",
        'D': "Brick chimney",
        'V': "Inscribed brick",
        'A': "Date accuracy"
    }
    
    # Create properly labeled factors
    factors = [f"{row['Variable']} ({factor_meanings[row['Variable']]})" for _, row in sobol_df.iterrows()]
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
def export_results(basic_summary, constrained_summary, sobol_df):
    print("\nExporting results to CSV...")
    
    # Extract statistics
    p_mean = basic_summary['mean']['P']
    p_median = basic_summary['median']['P']
    p_lower = basic_summary['2.5%']['P']
    p_upper = basic_summary['97.5%']['P']
    
    p_constrained_mean = constrained_summary['mean']['P']
    
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
    # Run the basic model with Beta-Binomial update for V
    basic_samples, basic_summary = run_basic_model(n_samples=4000)
    
    # Run the constrained model
    constrained_samples, constrained_summary = run_constrained_model(n_samples=4000)
    
    # Calculate Sobol indices for sensitivity analysis (using basic model samples)
    sobol_df = calculate_sobol_indices(basic_samples, param='P', num_samples=10000)
    
    # Create figures
    create_figures(basic_samples, sobol_df)
    
    # Export results
    results_df, model_comparison = export_results(basic_summary, constrained_summary, sobol_df)
    
    print("\nAnalysis complete!")
    print(f"Posterior mean P(E): {basic_summary['mean']['P']:.6f}")
    print(f"Posterior median P(E): {basic_summary['median']['P']:.6f}")
    print(f"95% credible interval: [{basic_summary['2.5%']['P']:.6f}, {basic_summary['97.5%']['P']:.6f}]")
    
    return basic_samples, basic_summary, constrained_samples, constrained_summary, sobol_df

if __name__ == "__main__":
    main() 