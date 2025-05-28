import csv

# Read H-2 results and analyze the outliers
with open('full_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    h2_results = [row for row in reader if row['method_category'] == 'H-2']

# Find the outliers
outliers = []
for row in h2_results:
    error = float(row['error_km'])
    if error > 300:  # Define outliers as >300km error
        outliers.append({
            'grant_id': row['grant_id'],
            'prediction': row['prediction'],
            'error_km': error
        })

print('Stanford NER (H-2) Outlier Analysis:')
print('=====================================')
print(f'Total H-2 predictions: {len(h2_results)}')
print(f'Outliers (>300km error): {len(outliers)}')
print()

for outlier in outliers:
    print(f'Grant #{outlier["grant_id"]}: {outlier["prediction"]} (Error: {outlier["error_km"]:.1f} km)')

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