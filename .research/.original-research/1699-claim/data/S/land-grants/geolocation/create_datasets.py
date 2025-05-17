#!/usr/bin/env python3
"""
Dataset preparation for Virginia land grants geolocation experiment
- Splits source dataset into dev/test
- Creates validation files by sampling from each split
- Adds has_ground_truth flag (default=0)
"""

import csv
import os
import random
from pathlib import Path

# Constants
RANDOM_SEED = 42
DEV_RATIO = 0.2  # 20% dev split
OUTPUT_DIR = Path(__file__).resolve().parent
SOURCE_DATASET = Path("/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/combined/books9-14.csv")

# Validation sample sizes (rows to be manually geolocated)
DEV_SAMPLE_SIZE_A = 20
DEV_SAMPLE_SIZE_B = 20
TEST_SAMPLE_SIZE = 125

def read_source_dataset(filepath):
    """Read the source dataset CSV"""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def split_dataset(data, dev_ratio=DEV_RATIO, seed=RANDOM_SEED):
    """Split dataset into dev and test sets"""
    random.seed(seed)
    # Shuffle a copy of the data indices
    indices = list(range(len(data)))
    random.shuffle(indices)
    
    # Calculate split point
    dev_size = int(len(data) * dev_ratio)
    
    # Create sets for O(1) lookup
    dev_indices = set(indices[:dev_size])
    
    # Create new dataset with split column
    split_data = []
    for i, row in enumerate(data):
        new_row = row.copy()
        new_row['set'] = 'dev' if i in dev_indices else 'test'
        split_data.append(new_row)
    
    return split_data

def save_split_dataset(data, output_path):
    """Save the split dataset"""
    if not data:
        return
    
    fieldnames = list(data[0].keys())
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Saved split dataset to {output_path}")

def create_validation_samples(split_data, seed=RANDOM_SEED):
    """Return dev_sample_a, dev_sample_b, test_sample list of rows."""
    random.seed(seed)
    # Separate dev and test rows
    dev_rows = [r for r in split_data if r["set"] == "dev"]
    test_rows = [r for r in split_data if r["set"] == "test"]

    # Sample dev A
    dev_a = random.sample(dev_rows, min(DEV_SAMPLE_SIZE_A, len(dev_rows)))
    # Sample dev B without overlap
    remaining_dev = [r for r in dev_rows if r not in dev_a]
    dev_b = random.sample(remaining_dev, min(DEV_SAMPLE_SIZE_B, len(remaining_dev)))
    # Sample test validation set
    test_sample = random.sample(test_rows, min(TEST_SAMPLE_SIZE, len(test_rows)))

    for row in dev_a + dev_b + test_sample:
        row["has_ground_truth"] = "0"
        row["latitude/longitude"] = ""

    return dev_a, dev_b, test_sample

def save_validation_samples(dev_a, dev_b, test_sample, output_dir=OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = [
        (output_dir / "validation-dev-A.csv", dev_a),
        (output_dir / "validation-dev-B.csv", dev_b),
        (output_dir / "validation-test.csv", test_sample),
    ]
    for path, rows in files:
        if not rows:
            continue
        fieldnames = list(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved {len(rows)} rows → {path}")

def main():
    print(f"Reading source dataset from {SOURCE_DATASET}")
    data = read_source_dataset(SOURCE_DATASET)
    print(f"Read {len(data)} records")
    
    print(f"Splitting dataset (dev ratio: {DEV_RATIO}, seed: {RANDOM_SEED})")
    split_data = split_dataset(data)
    
    split_path = OUTPUT_DIR / "split_books9-14.csv"
    save_split_dataset(split_data, split_path)
    
    print("Creating validation samples (devA: {DEV_SAMPLE_SIZE_A}, devB: {DEV_SAMPLE_SIZE_B}, test: {TEST_SAMPLE_SIZE})")
    dev_a, dev_b, test_sample = create_validation_samples(split_data)
    save_validation_samples(dev_a, dev_b, test_sample)
    
    print("Dataset preparation complete")

if __name__ == "__main__":
    main() 