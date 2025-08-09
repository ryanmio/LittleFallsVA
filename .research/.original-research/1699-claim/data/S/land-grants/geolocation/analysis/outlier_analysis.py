import csv
from pathlib import Path

# Path relative to this script (analysis directory)
CSV_PATH = Path(__file__).parent / 'full_results.csv'

# Filter rows for Stanford NER (method_id == 'H-2')
with CSV_PATH.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    h2_results = [row for row in reader if row.get('method_id') == 'H-2']

# Find outliers (error > 300 km)
outliers = []
for row in h2_results:
    try:
        error = float(row['error_km'])
    except (ValueError, KeyError):
        continue
    if error > 300:  # Outliers threshold
        outliers.append({
            'row_index': row.get('row_index'),
            'prediction': row.get('prediction', ''),
            'error_km': error
        })

print('Stanford NER (H-2) Outlier Analysis:')
print('=====================================')
print(f'Total H-2 predictions: {len(h2_results)}')
print(f'Outliers (>300km error): {len(outliers)}')
print()

for outlier in outliers:
    print(f'Row #{outlier["row_index"]}: {outlier["prediction"]} (Error: {outlier["error_km"]:.1f} km)')

# Check if outliers use the same coordinates
coords = [outlier['prediction'] for outlier in outliers]
unique_coords = set(coords)
print(f'\nUnique outlier coordinates: {len(unique_coords)}')
for coord in unique_coords:
    count = coords.count(coord)
    print(f'  {coord}: {count} occurrences')

# Calculate stats without outliers
non_outlier_errors = [float(row['error_km']) for row in h2_results if float(row['error_km']) <= 300]
if non_outlier_errors:
    import statistics
    print(f'\nStats without outliers (≤300km):')
    print(f'  Mean error: {statistics.mean(non_outlier_errors):.2f} km')
    print(f'  Median error: {statistics.median(non_outlier_errors):.2f} km')
    print(f'  Count: {len(non_outlier_errors)}/{len(h2_results)} predictions') 