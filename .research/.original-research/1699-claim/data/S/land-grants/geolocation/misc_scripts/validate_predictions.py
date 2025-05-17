# This was a test script used to validate the original idea, and we have since transitioned to using run_experiment.py

import csv
import os
import re
import time
from math import radians, cos, sin, asin, sqrt
from dotenv import load_dotenv
from openai import OpenAI
from time import perf_counter  # high-resolution timer
from pathlib import Path

# --- Pricing constants for o4-mini (USD per token) ---
USD_PER_INPUT_TOKEN = 1.10 / 1_000_000    # $1.10 per 1M input tokens
USD_PER_OUTPUT_TOKEN = 4.40 / 1_000_000   # $4.40 per 1M output tokens

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Remove printing full key; confirm key loaded
print("OpenAI key loaded" if api_key else "No OpenAI key found – please set OPENAI_API_KEY in .env")

# Determine directory of this script for consistent I/O
SCRIPT_DIR = Path(__file__).resolve().parent

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees"""
    # Extract degrees, minutes, seconds, and direction
    match = re.match(r'(\d+)°(\d+)\'(\d+\.\d+)"([NSEW])', dms_str)
    if not match:
        return None
    
    degrees, minutes, seconds, direction = match.groups()
    
    # Convert to decimal degrees
    decimal = float(degrees) + float(minutes)/60 + float(seconds)/3600
    
    # If direction is South or West, make the coordinate negative
    if direction in ['S', 'W']:
        decimal = -decimal
        
    return decimal

def get_prediction(entry_text):
    """Call the model, return (pred_text, usage_dict, elapsed_seconds) or (None, None, elapsed)."""
    start = perf_counter()
    try:
        completion = client.chat.completions.create(
            model="o4-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Geolocate this colonial Virginia land grant to precise latitude and longitude "
                        "coordinates. Output only the coordinates in this exact format: "
                        "[DD]°[MM]'[SS].[SSSSS]\"N [DDD]°[MM]'[SS].[SSSSS]\"W"
                    ),
                },
                {"role": "user", "content": entry_text},
            ],
        )
        elapsed = perf_counter() - start
        usage = completion.usage  # contains prompt_tokens, completion_tokens, total_tokens
        text_out = completion.choices[0].message.content.strip()
        return text_out, usage, elapsed
    except Exception as e:
        elapsed = perf_counter() - start
        print(f"Error getting prediction: {e}")
        return None, None, elapsed

def process_validation_data(csv_path, max_entries=10):
    results = []
    totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "cost_usd": 0.0, "time_seconds": 0.0}

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= max_entries:
                break

            print(f"Processing entry {i + 1} ...")
            entry_text = row["raw_entry"]
            prediction, usage, elapsed = get_prediction(entry_text)

            if prediction is None:
                print("First prediction failed; aborting remaining calls to save tokens.")
                break

            if not prediction or "°" not in prediction:
                print(f"Skipping invalid prediction: {prediction}")
                continue

            try:
                actual_lat, actual_lon = map(float, row["latitude/longitude"].split(", "))
                lat_dms, lon_dms = prediction.split(" ")
                pred_lat = dms_to_decimal(lat_dms)
                pred_lon = dms_to_decimal(lon_dms)
                if pred_lat is None or pred_lon is None:
                    print(f"Could not parse DMS from prediction: {prediction}")
                    continue
                distance_km = haversine(actual_lat, actual_lon, pred_lat, pred_lon)

                # cost calculation
                if usage:
                    prompt_tokens = usage.prompt_tokens or 0
                    completion_tokens = usage.completion_tokens or 0
                    total_tokens = usage.total_tokens or (prompt_tokens + completion_tokens)
                    cost = prompt_tokens * USD_PER_INPUT_TOKEN + completion_tokens * USD_PER_OUTPUT_TOKEN
                else:
                    prompt_tokens = completion_tokens = total_tokens = 0
                    cost = 0.0

                # accumulate totals
                totals["prompt_tokens"] += prompt_tokens
                totals["completion_tokens"] += completion_tokens
                totals["total_tokens"] += total_tokens
                totals["cost_usd"] += cost
                totals["time_seconds"] += elapsed

                results.append(
                    {
                        "entry": entry_text,
                        "actual_coords": f"{actual_lat}, {actual_lon}",
                        "predicted_coords": f"{pred_lat}, {pred_lon}",
                        "predicted_dms": prediction,
                        "distance_km": distance_km,
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens,
                        "cost_usd": round(cost, 6),
                        "time_seconds": round(elapsed, 3),
                    }
                )

                print(f"Predicted: {prediction}")
                print(f"Distance: {distance_km:.2f} km | Cost: ${cost:.4f} | Time: {elapsed:.2f}s")
                print("-" * 60)

            except Exception as e:
                print(f"Error processing row {i + 1}: {e}")

            time.sleep(1)

    return results, totals

def save_results(results, totals, output_path=None):
    if output_path is None:
        output_path = SCRIPT_DIR / "validation_results.csv"
    else:
        output_path = Path(output_path)
    fieldnames = [
        "entry",
        "actual_coords",
        "predicted_coords",
        "predicted_dms",
        "distance_km",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "cost_usd",
        "time_seconds",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # summary
    avg_distance = (
        sum(r["distance_km"] for r in results) / len(results) if results else 0
    )
    avg_cost = totals["cost_usd"] / len(results) if results else 0
    avg_time = totals["time_seconds"] / len(results) if results else 0

    print(f"Results saved to {output_path}")
    print(f"Total tokens: {totals['total_tokens']}")
    print(f"Total cost: ${totals['cost_usd']:.4f}")
    print(f"Average cost per call: ${avg_cost:.4f}")
    print(f"Average distance error: {avg_distance:.2f} km")
    print(f"Average latency per call: {avg_time:.2f}s")

def main():
    csv_path = "validation.csv"
    if not os.path.exists(csv_path):
        csv_path = ".research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/combined/validation.csv"
        if not os.path.exists(csv_path):
            print(f"Validation file not found at {csv_path}")
            return

    results, totals = process_validation_data(csv_path)
    save_results(results, totals)

if __name__ == "__main__":
    main() 