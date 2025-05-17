#!/usr/bin/env python3
"""
Patent Buffer Analysis Script

This script processes historical land patent data to determine:
1. Which patents intersect with a 2-mile buffer around Big Chimneys
2. Statistical measures for the R factor in our Bayesian analysis

Usage:
    python compute_R_patent_stats.py

Requirements:
    - geopandas
    - pandas
    - shapely
    - scipy
    - matplotlib
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scipy.stats import beta
import os
import yaml
from pathlib import Path

# Set paths
BASE_DIR = Path(__file__).parent.parent
COORDINATES_FILE = BASE_DIR / "data" / "coordinates" / "big_chimneys.geojson"
PATENTS_FILE = BASE_DIR / "data" / "R" / "patents_raw.shp"  # This will be your input shapefile
OUTPUT_CSV = BASE_DIR / "data" / "R" / "patents_2mi_buffer_1650-1739.csv"
OUTPUT_MAP = BASE_DIR / "figures" / "R_patent_buffer_map.pdf"
MARKDOWN_FILE = BASE_DIR / "data" / "R" / "patents_2mi_buffer_1650-1739.md"

# Create figures directory if it doesn't exist
os.makedirs(BASE_DIR / "figures", exist_ok=True)

def main():
    """Main processing function"""
    print("Starting patent buffer analysis...")
    
    # 1. Read Big Chimneys location
    try:
        big_chimneys = gpd.read_file(COORDINATES_FILE)
        big_chimneys_point = big_chimneys.geometry.iloc[0]
        print(f"Big Chimneys location loaded: {big_chimneys_point.y}, {big_chimneys_point.x}")
    except FileNotFoundError:
        print(f"Coordinates file not found at {COORDINATES_FILE}")
        # Fallback to hardcoded coordinates
        big_chimneys_point = Point(-77.174817, 38.882378)
        print(f"Using hardcoded coordinates: 38.882378, -77.174817")
    
    # 2. Create a 2-mile (3.22 km) buffer
    # Convert to a projected CRS for accurate buffer calculation
    point_gdf = gpd.GeoDataFrame(geometry=[big_chimneys_point], crs="EPSG:4326")
    point_projected = point_gdf.to_crs("EPSG:3857")  # Web Mercator
    buffer_projected = point_projected.buffer(3218.7)  # 2 miles in meters
    buffer_gdf = gpd.GeoDataFrame(geometry=buffer_projected, crs="EPSG:3857")
    buffer_wgs84 = buffer_gdf.to_crs("EPSG:4326")  # Convert back to WGS84
    buffer = buffer_wgs84.geometry.iloc[0]
    
    print("2-mile buffer created")
    
    # 3. Read patent data (if available)
    patents_exist = os.path.exists(PATENTS_FILE)
    if patents_exist:
        patents = gpd.read_file(PATENTS_FILE)
        print(f"Loaded {len(patents)} patents from shapefile")
        
        # 4. Filter patents by buffer intersection
        patents['intersects_buffer'] = patents.geometry.intersects(buffer)
        patents_in_buffer = patents[patents.intersects_buffer]
        print(f"Found {len(patents_in_buffer)} patents intersecting the buffer")
        
        # 5. Calculate centroids
        patents_in_buffer['centroid_lat'] = patents_in_buffer.geometry.centroid.y
        patents_in_buffer['centroid_lon'] = patents_in_buffer.geometry.centroid.x
        
        # 6. Add decade classification
        patents_in_buffer['decade'] = (patents_in_buffer['year'] // 10) * 10
        
        # 7. Export to CSV
        output_columns = ['patent_id', 'grantee', 'year', 'acreage', 
                         'centroid_lat', 'centroid_lon', 'intersects_buffer']
        if all(col in patents_in_buffer.columns for col in output_columns):
            patents_in_buffer[output_columns].to_csv(OUTPUT_CSV, index=False)
            print(f"Exported filtered patents to {OUTPUT_CSV}")
        else:
            missing_cols = [col for col in output_columns if col not in patents_in_buffer.columns]
            print(f"Warning: Missing columns in patent data: {missing_cols}")
            # Export with available columns
            patents_in_buffer.to_csv(OUTPUT_CSV, index=False)
            print(f"Exported filtered patents to {OUTPUT_CSV} with available columns")
        
        # 8. Calculate decade statistics
        decades = range(1650, 1740, 10)
        decade_counts = patents_in_buffer['decade'].value_counts().reindex(decades, fill_value=0)
        
        # Count decades with at least one patent
        k = (decade_counts > 0).sum()
        n = 9  # Number of decades 1650-1739
        
        alpha0, beta0 = 1, 1
        alpha = alpha0 + k
        beta_ = beta0 + n - k
        mean = alpha / (alpha + beta_)
        ci_lower, ci_upper = beta.ppf([0.025, 0.975], alpha, beta_)
        
        print(f"Statistical results:")
        print(f"  k={k} (decades with patents), n={n} (total decades)")
        print(f"  alpha={alpha}, beta={beta_}")
        print(f"  mean={mean:.4f}, 95% CI=[{ci_lower:.4f}, {ci_upper:.4f}]")
        
        # 9. Create map visualization
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Plot buffer
        buffer_gdf.to_crs("EPSG:4326").plot(ax=ax, color='none', edgecolor='blue', 
                                           alpha=0.5, linewidth=2, label='2-mile buffer')
        
        # Plot Big Chimneys point
        point_gdf.plot(ax=ax, color='red', marker='*', markersize=100, label='Big Chimneys')
        
        # Define colors for different decades
        decade_colors = {
            1650: 'purple', 1660: 'purple', 1670: 'purple', 1680: 'purple', 1690: 'purple',
            1700: 'green', 1710: 'green', 
            1720: 'orange', 1730: 'orange'
        }
        
        # Group patents by decade for plotting
        for decade, color in decade_colors.items():
            mask = patents_in_buffer['decade'] == decade
            if mask.any():
                patents_in_buffer[mask].plot(ax=ax, color=color, alpha=0.5, 
                                           label=f'{decade}s patents')
        
        # Add labels and legend
        ax.set_title('Land Patents Within 2-Mile Buffer of Big Chimneys', fontsize=14)
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        
        # Save figure
        plt.savefig(OUTPUT_MAP, dpi=300, bbox_inches='tight')
        print(f"Map saved to {OUTPUT_MAP}")
        
        # 10. Update markdown file with results
        update_markdown(MARKDOWN_FILE, k, n, alpha, beta_, mean, ci_lower, ci_upper)
        
    else:
        print(f"Patent shapefile not found at {PATENTS_FILE}")
        print("Please create a shapefile of patents before running this analysis.")
        print("Buffer statistics and visualization cannot be computed.")
        
        # Create a simple visualization with just the buffer and point
        fig, ax = plt.subplots(figsize=(10, 10))
        buffer_wgs84.plot(ax=ax, color='none', edgecolor='blue', 
                         alpha=0.5, linewidth=2, label='2-mile buffer')
        point_gdf.plot(ax=ax, color='red', marker='*', markersize=100, label='Big Chimneys')
        ax.set_title('2-Mile Buffer Around Big Chimneys', fontsize=14)
        ax.legend(loc='upper left', fontsize=10)
        plt.savefig(OUTPUT_MAP, dpi=300, bbox_inches='tight')
        print(f"Buffer map saved to {OUTPUT_MAP}")
    
    print("Analysis complete!")

def update_markdown(file_path, k, n, alpha, beta_, mean, ci_lower, ci_upper):
    """Update the YAML frontmatter in the markdown file with calculated statistics"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse YAML frontmatter
        if content.startswith('---'):
            _, frontmatter, body = content.split('---', 2)
            metadata = yaml.safe_load(frontmatter)
            
            # Update with new values
            metadata['k'] = int(k)
            metadata['n'] = int(n)
            metadata['alpha'] = float(alpha)
            metadata['beta'] = float(beta_)
            metadata['mean'] = float(mean)
            metadata['ci_lower'] = float(ci_lower)
            metadata['ci_upper'] = float(ci_upper)
            
            # Write back to file
            updated_frontmatter = yaml.dump(metadata, sort_keys=False)
            updated_content = f"---\n{updated_frontmatter}---{body}"
            
            with open(file_path, 'w') as f:
                f.write(updated_content)
            
            print(f"Updated markdown file with calculated statistics: {file_path}")
        else:
            print(f"Warning: {file_path} does not have valid YAML frontmatter")
            
    except Exception as e:
        print(f"Error updating markdown file: {e}")

if __name__ == "__main__":
    main() 