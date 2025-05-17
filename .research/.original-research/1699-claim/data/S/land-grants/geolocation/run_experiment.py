#!/usr/bin/env python3
"""run_experiment.py – driver to evaluate geolocation Methods on a chosen Evaluation Set.

Usage:
    python run_experiment.py --evalset validation-dev-A.csv --dry-run

Flags:
    --evalset      Relative CSV filename in the geolocation directory.
    --methods-file Path to YAML of methods (default methods.yaml).
    --prompts-file Path to YAML of prompts (default prompts.yaml).
    --dry-run      If set, skip actual OpenAI calls and emit mock predictions.
    --seed         Random seed for reproducibility (default 123).
    --verbose      Print detailed progress & debugging info.
    --max-rows     Process at most N rows from the evaluation set (for quick smoke tests).

Outputs:
    • results_<evalset>_<timestamp>.csv       – row-level results for all methods
    • runs/<method>/<timestamp>.jsonl         – per-call log (even in dry-run)
"""
import argparse
import csv
import json
import os
import re
import random
import time
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI
import requests

# Constants
GEODIR = Path(__file__).resolve().parent
RUNS_DIR = GEODIR / "runs"
MOCKDATA_PREFIX = "99" # Clearly non-Virginia coordinates (99°N, 99°W)

# Google API key (for tool_chain)
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Tool specification for the OpenAI Responses API
GEOCODE_TOOL_SPEC = {
    "type": "function",
    "name": "geocode_place",
    "description": (
        "Resolve a colonial-era Virginia place description to coordinates. "
        "Returns JSON with lat, lng, formatted_address and metadata."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Geocoding query, e.g. 'Blackwater River, Isle of Wight County, Virginia'",
            },
            "strategy": {
                "type": "string",
                "enum": [
                    "natural_feature",
                    "restricted_va",
                    "standard_va",
                    "county_fallback",
                ],
                "description": "Which lookup strategy to attempt first.",
            },
        },
        "required": ["query"],
    },
}

# New utility tool for geometric averaging
CENTROID_TOOL_SPEC = {
    "type": "function",
    "name": "compute_centroid",
    "description": "Return the centroid (average lat/lng) of two or more coordinate points.",
    "parameters": {
        "type": "object",
        "properties": {
            "points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number"},
                        "lng": {"type": "number"},
                    },
                    "required": ["lat", "lng"],
                },
                "minItems": 2,
                "description": "List of coordinate objects to average",
            }
        },
        "required": ["points"],
    },
}

# Load pricing config
PRICING_PATH = GEODIR / "pricing.yaml"
PRICING_DATA = {}
if PRICING_PATH.exists():
    with open(PRICING_PATH, "r", encoding="utf-8") as _pf:
        for entry in yaml.safe_load(_pf):
            PRICING_DATA[entry["model"]] = entry

# ---------------------------------------------------------------------
# Pricing lookup helper
# ---------------------------------------------------------------------

def get_pricing_for_model(model_name: str):
    """Return the pricing entry whose model prefix matches the provided model_name.
    Falls back to None if no entry is found."""
    if model_name in PRICING_DATA:
        return PRICING_DATA[model_name]
    # Try prefix matches (e.g., 'gpt-4.1-2025-04-14' matches 'gpt-4.1')
    for key, entry in PRICING_DATA.items():
        if model_name.startswith(key):
            return entry
    return None

# Load environment
load_dotenv()

# ---------------------------------------------------------------------
# Helper loading functions
# ---------------------------------------------------------------------

def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_evalset(path: Path):
    """Return (rows_to_evaluate, total_rows_in_file). Rows are automatically filtered to
    those with `has_ground_truth == 1` when that column is present so that metrics
    are only computed on verified coordinates. The total row count is returned so
    callers can report how many were filtered out."""

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total_rows = len(rows)

    # Only process rows with ground truth if specified
    has_gt_col = "has_ground_truth" in (reader.fieldnames or []) if rows else False
    if has_gt_col:
        filtered_rows = [r for r in rows if r.get("has_ground_truth") == "1"]
        print(f"Filtering: {len(filtered_rows)}/{total_rows} rows have ground truth")
        return filtered_rows, total_rows

    return rows, total_rows

# ---------------------------------------------------------------------
# Geospatial utilities
# ---------------------------------------------------------------------

def dms_to_decimal(dms_str):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
    # Extract deg, min, sec, and direction using regex
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

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/long points in km (Haversine formula)."""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

# ---------------------------------------------------------------------
# Ground-truth parsing helper
# ---------------------------------------------------------------------

def _parse_ground_truth(gt):
    """Return (lat, lon) floats or (None, None) if unparseable.

    Accepts:
    • "lat,lon"  (comma with/without space)
    • "lat lon"  (space-separated decimal)
    • DMS pairs like '36°43'30.2"N 77°00'12.5"W'
    """

    if gt is None:
        return None, None

    # Already numeric tuple/list
    if isinstance(gt, (list, tuple)) and len(gt) == 2:
        try:
            return float(gt[0]), float(gt[1])
        except Exception:
            return None, None

    if not isinstance(gt, str):
        return None, None

    gt = gt.strip()
    if not gt:
        return None, None

    # 1. Decimal with comma (allow optional space)
    m = re.match(r"\s*([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)\s*", gt)
    if m:
        return float(m.group(1)), float(m.group(2))

    # 2. Two decimals separated by whitespace
    parts = gt.split()
    if len(parts) == 2:
        try:
            return float(parts[0]), float(parts[1])
        except Exception:
            pass

    # 3. DMS pattern – reuse extract_coords_from_text which can parse DMS pairs
    lat, lon = extract_coords_from_text(gt)
    return lat, lon

def calculate_error(pred_text, ground_truth):
    """Calculate error distance from predicted coordinates to ground truth lat/long."""
    try:
        # Robustly parse ground-truth string/tuple
        lat_gt, lon_gt = _parse_ground_truth(ground_truth)
        if lat_gt is None or lon_gt is None:
            return None

        lat_pred, lon_pred = extract_coords_from_text(pred_text)
        if lat_pred is None or lon_pred is None:
            return None

        return haversine(lat_gt, lon_gt, lat_pred, lon_pred)
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return None

# ---------------------------------------------------------------------
# Coordinate extraction helper
# ---------------------------------------------------------------------

def extract_coords_from_text(text: str):
    """Try to extract (lat, lon) in decimal from arbitrary text containing coordinates."""
    # 1. Decimal pair with comma
    m = re.search(r"([-+]?\d+\.\d+)\s*,\s*([-+]?\d+\.\d+)", text)
    if m:
        return float(m.group(1)), float(m.group(2))

    # 2. Decimal with N/S and E/W (degree symbol optional)
    lat_dir_match = re.search(r"([-+]?\d+\.\d+)\s*°?\s*([NnSs])", text)
    lon_dir_match = re.search(r"([-+]?\d+\.\d+)\s*°?\s*([EeWw])", text)
    if lat_dir_match and lon_dir_match:
        lat = float(lat_dir_match.group(1))
        lon = float(lon_dir_match.group(1))
        if lat_dir_match.group(2).upper() == "S":
            lat = -lat
        if lon_dir_match.group(2).upper() == "W":
            lon = -lon
        return lat, lon

    # 3. DMS strings
    dms_pattern = r"(\d{1,3}°\s*\d{1,2}'\s*\d+(?:\.\d+)?\"\s*[NSEWnsew])"
    dms_matches = re.findall(dms_pattern, text)
    if len(dms_matches) >= 2:
        lat = dms_to_decimal(dms_matches[0].replace(" ", ""))
        lon = dms_to_decimal(dms_matches[1].replace(" ", ""))
        return lat, lon

    # 4. Two space-separated tokens fallback
    parts = text.strip().split()
    if len(parts) == 2:
        lat = dms_to_decimal(parts[0])
        lon = dms_to_decimal(parts[1])
        return lat, lon

    return None, None

# ---------------------------------------------------------------------
# Output parsing helpers (define early so later functions can reference)
# ---------------------------------------------------------------------

def extract_output_text(output_item):
    """Return a string representation of a Responses output item.
    Handles assistant message items that may contain text or JSON."""
    if output_item is None:
        return ""

    # Detect SDK object vs dict
    typ = getattr(output_item, "type", None) or (output_item.get("type") if isinstance(output_item, dict) else None)

    # If this is the message wrapper produced by Responses API
    if typ == "message":
        content = getattr(output_item, "content", None) or output_item.get("content", [])
        if content and isinstance(content, list):
            first = content[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict):
                return first.get("text", str(first))
        return str(content)

    # Direct text or text object
    if typ == "text":
        return getattr(output_item, "text", None) or output_item.get("text", "")

    # JSON result (rare for final answers, but good to cover)
    if typ == "json_object":
        j = getattr(output_item, "json", None) or output_item.get("json", {})
        return json.dumps(j)

    # Fallback generic stringification
    return str(output_item)

# ---------------------------------------------------------------------
# Google Geocoding helpers (used by the tool)
# ---------------------------------------------------------------------

def verify_result_is_in_virginia(result: dict) -> bool:
    """Return True if geocoder result is inside Virginia."""
    if not result or "address_components" not in result:
        return False

    for comp in result["address_components"]:
        if "administrative_area_level_1" in comp.get("types", []) and (
            comp.get("short_name") == "VA" or comp.get("long_name") == "Virginia"
        ):
            return True

    # Fallback check in formatted address
    if "formatted_address" in result and (
        "Virginia" in result["formatted_address"] or ", VA" in result["formatted_address"]
    ):
        return True

    return False


def _google_geocode(query: str, **params):
    if not GOOGLE_API_KEY:
        return None
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    full_params = {
        "address": query,
        "region": "us",
        "components": "administrative_area:VA|country:US",
        "key": GOOGLE_API_KEY,
    }
    full_params.update(params)
    try:
        resp = requests.get(url, params=full_params, timeout=10)
        data = resp.json()
        if data.get("status") == "OK" and data.get("results"):
            return data["results"]
    except Exception:
        pass
    return None


def geocode_place(query: str, strategy: str | None = None):
    """Implements the four-strategy geocoder described in the TS prototype."""
    strategy = strategy or "natural_feature"

    # Build variant queries per strategy
    variants = []
    county_part = ""
    if "," in query:
        # crude: assume last "," separated token before 'Virginia' is county part
        county_part = query.split(",")[-2].strip() if "Virginia" in query else ""

    if strategy == "natural_feature":
        variants = [
            f"{query} point, Virginia",
            query,
            f"{query} water feature, Virginia",
        ]
    elif strategy == "restricted_va":
        variants = [query]
    elif strategy == "standard_va":
        variants = [query]
    elif strategy == "county_fallback":
        c = f"{county_part}, Virginia" if county_part else query
        variants = [c]
    else:
        variants = [query]

    for q in variants:
        res = _google_geocode(q)
        if not res:
            continue
        candidate = res[0]
        if not verify_result_is_in_virginia(candidate):
            continue
        loc = candidate["geometry"]["location"]
        return {
            "lat": loc["lat"],
            "lng": loc["lng"],
            "formatted_address": candidate.get("formatted_address"),
            "strategy": strategy,
            "query_used": q,
        }

    return {"error": f"No result for '{query}' via {strategy}"}

# ---------------------------------------------------------------------
# Centroid utility for tool calls
# ---------------------------------------------------------------------

def compute_centroid(points: list):
    """Return the geographic centroid (on a sphere) of ≥2 lat/lng points.

    Algorithm:
    1. Convert each (lat, lng) to 3-D Cartesian coordinates on the unit sphere.
    2. Average the x, y, z components.
    3. Project the mean vector back to latitude/longitude.

    This avoids the bias that a simple arithmetic mean of lat/lng exhibits near
    the ±180° meridian or for points far apart.
    """

    import math

    try:
        if not isinstance(points, list) or len(points) < 2:
            return {"error": "Need at least two points"}

        # Convert to radians and then to Cartesian coordinates.
        x = y = z = 0.0
        for p in points:
            lat_rad = math.radians(p["lat"])
            lng_rad = math.radians(p["lng"])
            x += math.cos(lat_rad) * math.cos(lng_rad)
            y += math.cos(lat_rad) * math.sin(lng_rad)
            z += math.sin(lat_rad)

        # Average the coordinates.
        total = len(points)
        x /= total
        y /= total
        z /= total

        # Convert the averaged vector back to lat/lng.
        lng_centroid = math.degrees(math.atan2(y, x))
        hyp = math.sqrt(x * x + y * y)
        lat_centroid = math.degrees(math.atan2(z, hyp))

        return {"lat": lat_centroid, "lng": lng_centroid}
    except Exception as e:
        return {"error": str(e)}

# ---------------------------------------------------------------------
# Tool-chain controller
# ---------------------------------------------------------------------

def _scrub_msg(msg: dict):
    """Remove keys the Responses API rejects (status, etc.)."""
    if isinstance(msg, dict) and "status" in msg:
        msg.pop("status", None)
    return msg

def run_tool_chain(client: OpenAI, method: dict, prompt_obj: dict, entry_text: str):
    """Drive the assistant with tool support until it returns final coordinates."""

    params = method.get("params", {}).copy()
    params.setdefault("store", True)
    if "reasoning_effort" in params:
        params["reasoning"] = {"effort": params.pop("reasoning_effort")}

    # Computer vision (computer-*) models require truncation=auto
    if method["model"].startswith("computer-") or "computer-" in method["model"]:
        params.setdefault("truncation", "auto")

    # Remove the 'tools' key if it exists to avoid parameter collision
    params.pop("tools", None)

    # Build initial conversation messages
    messages = [
        {"role": "user", "content": entry_text},
    ]

    tools = [GEOCODE_TOOL_SPEC, CENTROID_TOOL_SPEC]

    total_usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    # Collect a lightweight trace of tool interactions for debugging/logging
    tool_trace: list[dict] = []
    start_time = time.time()

    # Safety cap to avoid infinite loops
    for _ in range(10):
        response = client.responses.create(
            model=method["model"],
            input=messages,
            instructions=prompt_obj["text"].strip(),
            tools=tools,
            **params
        )

        # Aggregate token usage if provided
        if hasattr(response, "usage") and response.usage:
            u = response.usage.model_dump()
            for k in ("input_tokens", "output_tokens", "total_tokens"):
                total_usage[k] = total_usage.get(k, 0) + u.get(k, 0)

        # Examine all output items – ignore reasoning, handle first function_call, else first answer message
        func_item = None
        answer_item = None
        reasoning_item = None
        for itm in response.output:
            typ_ = getattr(itm, "type", None) or (itm.get("type") if isinstance(itm, dict) else None)
            if typ_ == "function_call" and func_item is None:
                func_item = itm
            elif typ_ == "reasoning" and reasoning_item is None:
                reasoning_item = itm
            elif typ_ in {"message", "text", "json_object"} and answer_item is None:
                answer_item = itm

        if func_item is not None:
            tool_call = func_item
            name = tool_call["name"] if isinstance(tool_call, dict) else tool_call.name
            args_json = tool_call["arguments"] if isinstance(tool_call, dict) else tool_call.arguments
            try:
                args = json.loads(args_json) if isinstance(args_json, str) else args_json
            except Exception:
                args = {}

            if name == "geocode_place":
                result = geocode_place(**args)
            elif name == "compute_centroid":
                result = compute_centroid(**args)
            else:
                result = {"error": f"Unknown tool {name}"}

            # Record this interaction for the trace (JSON-serialisable)
            tool_trace.append({
                "tool_name": name,
                "arguments": args,
                "result": result,
            })

            # Extract id (must start with 'fc_') and call_id
            fc_id = None
            call_id = None

            if isinstance(tool_call, dict):
                fc_id = tool_call.get("id")
                call_id = tool_call.get("call_id")
            else:
                fc_id = getattr(tool_call, "id", None)
                call_id = getattr(tool_call, "call_id", None)

            if not fc_id:
                fc_id = f"fc_{int(time.time()*1000)}"
            if not call_id:
                call_id = f"call_{int(time.time()*1000)}"

            # Assistant's function_call message must stay in history so model sees its own call.
            if hasattr(tool_call, "model_dump"):
                call_msg = tool_call.model_dump()
            else:
                call_msg = json.loads(json.dumps(tool_call)) if not isinstance(tool_call, dict) else tool_call
            call_msg = _scrub_msg(call_msg)

            # Tool result item that the model will read next turn
            fc_output_item = {
                "type": "function_call_output",
                "call_id": call_id,
                "output": json.dumps(result),
            }

            # Preserve the reasoning item first if it exists (required by o4-mini)
            if reasoning_item is not None:
                if hasattr(reasoning_item, "model_dump"):
                    rmsg = reasoning_item.model_dump()
                else:
                    rmsg = json.loads(json.dumps(reasoning_item)) if not isinstance(reasoning_item, dict) else reasoning_item
                messages.append(_scrub_msg(rmsg))

            messages.extend([call_msg, fc_output_item])
            continue  # Let the model read tool result

        # Otherwise assume assistant has returned final answer text (skip reasoning-only outputs)
        if answer_item is None:
            # No usable answer – treat as unresolved
            break
        content = extract_output_text(answer_item)
        safe_resp = response.model_dump()
        return {
            "id": response.id,
            "model": response.model,
            "response": safe_resp,
            "usage": safe_resp.get("usage", {}),
            "latency_s": time.time() - start_time,
            "mock": False,
            "created_at": int(time.time()),
            "tool_trace": tool_trace,
        }, content, total_usage, time.time() - start_time

    # If loop ends without resolution
    return {
        "error": "Tool chain exceeded max turns",
        "model": method["model"],
        "usage": total_usage,
        "latency_s": time.time() - start_time,
        "mock": False,
        "created_at": int(time.time()),
        "tool_trace": tool_trace,
    }, "ERROR: tool chain unresolved", total_usage, time.time() - start_time

# ---------------------------------------------------------------------
# OpenAI client initialization
# ---------------------------------------------------------------------

def init_openai_client():
    """Initialize the OpenAI client from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY not found in environment. Set this for real runs.")
        return None
    return OpenAI(api_key=api_key)

# ---------------------------------------------------------------------
# Mock/dry-run utilities
# ---------------------------------------------------------------------

def mock_predict(one_shot=True, row_index=0, method_id="MOCK"):
    """Return a fake DMS coordinate string (clearly marked as fake)."""
    # Use MOCKDATA_PREFIX to ensure these are never confused with real predictions
    lat_deg = f"{MOCKDATA_PREFIX}"
    lon_deg = f"{MOCKDATA_PREFIX}"
    
    # Add minor variations based on row/method to simulate different results
    min_lat = (row_index * 7) % 60  
    sec_lat = float(f"{(hash(method_id) % 100):02d}.{(row_index % 100):05d}")
    min_lon = (row_index * 13) % 60
    sec_lon = float(f"{(hash(method_id) % 100):02d}.{(row_index % 100):05d}")
    
    # Format as DMS for one_shot
    if one_shot:
        return f"{lat_deg}°{min_lat:02d}'{sec_lat:.5f}\"N {lon_deg}°{min_lon:02d}'{sec_lon:.5f}\"W"
    
    # Format as decimal for tool_chain
    lat_dec = float(lat_deg) + (min_lat/60) + (sec_lat/3600)
    lon_dec = -1 * (float(lon_deg) + (min_lon/60) + (sec_lon/3600))  # West is negative
    return f"{lat_dec:.6f}, {lon_dec:.6f}"

def mock_usage(method_id, row_index, pipeline):
    """Generate mock token usage based on method and row."""
    # Create deterministic but varying mock usage
    base_input = 150 + (hash(method_id) % 100)
    base_output = 30 + (hash(method_id) % 20)
    reasoning = 0
    if pipeline == "tool_chain":
        base_input += 100
        base_output += 50
        reasoning = 80
        
    # Add jitter
    input_tokens = base_input + (row_index % 50)
    output_tokens = base_output + (row_index % 15)
    reasoning_tokens = reasoning + (row_index % 20) if reasoning else 0
    
    total = input_tokens + output_tokens
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "output_tokens_details": {"reasoning_tokens": reasoning_tokens},
        "total_tokens": total
    }

def mock_response(method, prompt, entry_text, row_index):
    """Generate a detailed mock response object like a real API call would return."""
    pipeline = method["pipeline"]
    method_id = method["id"]
    
    # Generate mock prediction and usage
    pred_text = mock_predict(one_shot=(pipeline == "one_shot"), row_index=row_index, method_id=method_id)
    usage = mock_usage(method_id, row_index, pipeline)
    
    # Build a simulated response with key attributes matching the real API
    return {
        "id": f"mock_resp_{int(time.time())}_{method_id}_{row_index}",
        "model": method["model"],
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": pred_text}]
            }
        ],
        "usage": usage,
        "reasoning": {"effort": method.get("params", {}).get("reasoning_effort")},
        "mock": True,
        "created_at": int(time.time())
    }

# ---------------------------------------------------------------------
# OpenAI API interaction
# ---------------------------------------------------------------------

def call_openai_responses(client, method, prompt, entry_text):
    """Make a real call to OpenAI's Responses API."""
    if client is None:
        raise ValueError("OpenAI client is not initialized. Check API key.")
    
    start_time = time.time()
    
    # Extract parameters that are explicitly defined in our method config
    # Convert our YAML params to API parameters
    params = method.get("params", {}).copy()
    params.setdefault("store", True)
    
    # Handle reasoning field (API expects object with effort)
    if "reasoning_effort" in params:
        params["reasoning"] = {"effort": params.pop("reasoning_effort")}
        
    # Add required text format parameter
    params["text"] = {"format": {"type": "text"}}
    
    try:
        response = client.responses.create(
            model=method["model"],
            input=[{"role": "user", "content": entry_text}],
            instructions=prompt["text"].strip(),
            **params
        )
        
        # Extract prediction text: skip reasoning-type items
        pred_text = "ERROR: No output text"
        if hasattr(response, "output") and response.output:
            for itm in response.output:
                itype = getattr(itm, "type", None) or (itm.get("type") if isinstance(itm, dict) else None)
                if itype in {"message", "text", "json_object"}:
                    pred_text = extract_output_text(itm)
                    if pred_text:
                        break
        
        # Use SDK's model_dump so everything is JSON-serialisable for our logs
        safe_resp = response.model_dump()

        return {
            "id": response.id,
            "model": response.model,
            "response": safe_resp,
            "usage": safe_resp.get("usage", {}),
            "latency_s": time.time() - start_time,
            "mock": False,
            "created_at": int(time.time()),
        }, pred_text
        
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {
            "error": str(e),
            "model": method["model"],
            "usage": {},
            "latency_s": time.time() - start_time,
            "mock": False,
            "created_at": int(time.time())
        }, f"ERROR: {e}"

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

def log_run(run_dir: Path, log_entry: dict):
    """Append a JSON entry describing one API (or mock) call."""
    log_file = run_dir / "calls.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    return log_file

# ---------------------------------------------------------------------
# Main experiment logic
# ---------------------------------------------------------------------

def run_experiment(args):
    random.seed(args.seed)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Build run_id from evalset filename but replace problematic chars (spaces, slashes) with "-"
    stem_safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", Path(args.evalset).stem).strip("-")
    run_id = f"{stem_safe}_{timestamp}"

    # Create a dedicated directory for this run
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"Artifacts will be stored in {run_dir}\n")

    # Resolve paths
    methods_path = GEODIR / args.methods_file
    prompts_path = GEODIR / args.prompts_file
    evalset_path = GEODIR / args.evalset

    methods = load_yaml(methods_path)
    prompts = load_yaml(prompts_path)
    # Load evaluation set and keep track of original size for provenance logging
    eval_rows, total_rows_in_file = load_evalset(evalset_path)

    if args.max_rows is not None:
        eval_rows = eval_rows[:args.max_rows]
        print(f"Truncating eval set to first {args.max_rows} rows (for max-rows flag)")

    print(f"Loaded {len(methods)} methods, {len(eval_rows)} eval rows, dry_run={args.dry_run}")

    # Map pipeline -> prompt (take latest version per pipeline)
    prompt_by_pipeline = {}
    for p in prompts:
        # assume unique id per entry; choose by pipeline first occurrence (latest at top) if duplicates
        prompt_by_pipeline[p["pipeline"]] = p

    # Initialize OpenAI client for real runs
    client = None if args.dry_run else init_openai_client()

    # Prepare containers for results and aggregates
    results_rows: list[dict] = []
    total_input_tokens = 0
    total_output_tokens = 0
    total_token_cost_usd = 0.0  # excludes fixed human cost
    # Per-method aggregation (errors, tokens)
    method_stats = {}

    # Start time for overall run
    start_time = time.time()
    
    print(f"Starting run with {len(eval_rows)} entries across {sum(1 for m in methods if m.get('enabled', True))} enabled methods")
    print(f"{'=' * 70}")

    for row_idx, entry in enumerate(eval_rows, 1):
        raw_entry = entry["raw_entry"]
        
        # Extract ground truth coordinates if present for error calculation
        ground_truth = entry.get("latitude/longitude", "")
        
        for m in methods:
            if not m.get("enabled", True):
                continue
                
            method_id = m["id"]
            pipeline = m["pipeline"]
            model = m["model"]
            params = m.get("params", {})
            params.setdefault("store", True)

            # --------------------------------------------------------------
            # STATIC PIPELINE (human baseline or other pre-computed guesses)
            # --------------------------------------------------------------
            # We treat a pipeline value of "static" as meaning the prediction
            # already exists in the evaluation CSV (e.g. columns
            # `h1_latitude` / `h1_longitude`).  No model call is made – we
            # just read the values, assemble a coordinate string, and record
            # zero token usage.
            if pipeline == "static":
                print(f"Entry {row_idx}/{len(eval_rows)} | Method {method_id} ({model}) | STATIC | ", end="", flush=True)
                lat_val = (entry.get("h1_latitude") or "").strip()
                lon_val = (entry.get("h1_longitude") or "").strip()

                if lat_val and lon_val:
                    pred_text = f"{lat_val}, {lon_val}"
                else:
                    # Leave blank – counts as unsuccessful prediction
                    pred_text = ""

                usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
                latency = 0.0  # Could be refined to billed_hours / N if desired

                # Minimal request / response placeholders for logging parity
                request = {
                    "model": model,
                    "pipeline": pipeline,
                    "params": params,
                    "prompt_id": "static",
                    "prompt_version": "1",
                    "entry_text": raw_entry[:100] + ("..." if len(raw_entry) > 100 else "")
                }
                response_obj = {"static": True, "prediction_present": bool(pred_text)}

                # Log the pseudo-call for provenance
                log_run(run_dir, {
                    "row_index": row_idx,
                    "method_id": method_id,
                    "request": request,
                    "response": response_obj,
                })

                # Prompt object stub so later code that expects ids works
                prompt_obj = {"id": "static", "version": "1"}

                # Calculate error distance if ground-truth present
                error_km = None
                if ground_truth and pred_text:
                    error_km = calculate_error(pred_text, ground_truth)

                # Record results row immediately (static pipeline bypasses rest)
                result_row = {
                    "row_index": row_idx,
                    "method_id": method_id,
                    "model": model,
                    "pipeline": pipeline,
                    "prompt_id": prompt_obj["id"],
                    "prompt_version": prompt_obj["version"],
                    "prediction": pred_text,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "reasoning_tokens": 0,
                    "total_tokens": 0,
                    "latency_s": latency,
                    "error_km": error_km if error_km is not None else "",
                    "is_mock": "1" if args.dry_run else "0"
                }
                results_rows.append(result_row)

                # Console summary
                print(f"Pred: {pred_text[:30]}{'...' if len(pred_text) > 30 else ''} | ", end="")
                if error_km is not None:
                    print(f"Error: {error_km:.2f} km | ", end="")
                print("Tokens: 0 | Latency: 0.00s")

                # Update stats
                stats = method_stats.setdefault(method_id, {
                    "calls": 0,
                    "error_kms": [],
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0.0,
                })
                stats["calls"] += 1
                if error_km is not None:
                    stats["error_kms"].append(error_km)

                # Fixed cost added once (handled later if not yet set)
                if not args.dry_run:
                    fixed = params.get("fixed_cost_usd", 0.0)
                    # Record the fixed human cost in per-method stats but **do not** add it
                    # to total_token_cost_usd (API spend tracker)
                    if stats["cost_usd"] == 0.0:
                        stats["cost_usd"] = fixed

                # Continue to next method
                continue

            else:
                prompt_obj = prompt_by_pipeline.get(pipeline)
                if prompt_obj is None:
                    print(f"[WARN] No prompt defined for pipeline {pipeline}, skipping {method_id}")
                    continue
                
                print(f"Entry {row_idx}/{len(eval_rows)} | Method {method_id} ({model}) | ", end="", flush=True)

                # Prepare request details for logging
                request = {
                    "model": model,
                    "pipeline": pipeline,
                    "params": params,
                    "prompt_id": prompt_obj["id"],
                    "prompt_version": prompt_obj["version"],
                    "entry_text": raw_entry[:100] + ("..." if len(raw_entry) > 100 else "")
                }

                # In dry-run, generate mock prediction
                if args.dry_run:
                    print("MOCK mode | ", end="", flush=True)
                    
                    # Simulate latency for more realistic testing
                    mock_latency = 0.5 + random.random() * 2
                    if args.verbose:
                        print(f"Simulating {mock_latency:.1f}s latency | ", end="", flush=True)
                    time.sleep(mock_latency)
                    
                    response_obj = mock_response(m, prompt_obj, raw_entry, row_idx)
                    pred_text = response_obj["output"][0]["content"][0]["text"]
                    usage = response_obj["usage"]
                    latency = mock_latency
                    
                    # Log the mock call
                    log_entry = {
                        "row_index": row_idx,
                        "method_id": method_id,
                        "request": request,
                        "response": response_obj,
                    }
                    log_run(run_dir, log_entry)
                    
                else:
                    # Make a real call to OpenAI
                    print("REAL API call | ", end="", flush=True)
                    try:
                        if pipeline == "tool_chain":
                            response_obj, pred_text, usage, latency = run_tool_chain(client, m, prompt_obj, raw_entry)
                        else:
                            response_obj, pred_text = call_openai_responses(client, m, prompt_obj, raw_entry)
                            usage = response_obj.get("usage", {})
                            latency = response_obj.get("latency_s", 0.0)
                        
                        # Log the call
                        log_entry = {
                            "row_index": row_idx,
                            "method_id": method_id,
                            "request": request,
                            "response": response_obj,
                        }
                        log_run(run_dir, log_entry)
                        
                        # Add delay to avoid rate limits
                        time.sleep(max(0, 0.5 - latency))
                        
                    except Exception as e:
                        print(f"ERROR: {e}")
                        pred_text = f"ERROR: {e}"
                        usage = {}
                        latency = 0.0
                
                # Calculate error if ground truth is available
                error_km = None
                if ground_truth and pred_text and not pred_text.startswith("ERROR:"):
                    error_km = calculate_error(pred_text, ground_truth)
                
                # Record results
                result_row = {
                    "row_index": row_idx,
                    "method_id": method_id,
                    "model": model,
                    "pipeline": pipeline,
                    "prompt_id": prompt_obj["id"],
                    "prompt_version": prompt_obj["version"],
                    "prediction": pred_text,
                    "input_tokens": usage.get("input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                    "reasoning_tokens": usage.get("output_tokens_details", {}).get("reasoning_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                    "latency_s": latency,
                    "error_km": error_km if error_km is not None else "",
                    "is_mock": "1" if args.dry_run else "0"
                }
                results_rows.append(result_row)
                
                # Print brief result summary
                print(f"Pred: {pred_text[:30]}{'...' if len(pred_text) > 30 else ''} | ", end="")
                if error_km is not None:
                    print(f"Error: {error_km:.2f} km | ", end="")
                print(f"Tokens: {usage.get('total_tokens', 0)} | Latency: {latency:.2f}s")

                # Aggregate real token usage
                if not args.dry_run:
                    total_input_tokens += usage.get("input_tokens", 0)
                    total_output_tokens += usage.get("output_tokens", 0)

                # Update per-method stats (always, even dry-run so we get counts)
                stats = method_stats.setdefault(method_id, {
                    "calls": 0,
                    "error_kms": [],
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0.0,
                })
                stats["calls"] += 1
                if error_km is not None:
                    stats["error_kms"].append(error_km)
                stats["input_tokens"] += usage.get("input_tokens", 0)
                stats["output_tokens"] += usage.get("output_tokens", 0)

                if not args.dry_run:
                    pricing = get_pricing_for_model(model)
                    if pricing:
                        inp_rate = pricing["input_per_m"] / 1_000_000
                        out_rate = pricing["output_per_m"] / 1_000_000
                        call_cost = usage.get("input_tokens", 0)*inp_rate + usage.get("output_tokens", 0)*out_rate
                    else:
                        call_cost = 0.0
                    total_token_cost_usd += call_cost
                    stats["cost_usd"] = stats.get("cost_usd", 0.0) + call_cost

    # Save combined results CSV
    run_duration = time.time() - start_time
    out_file = run_dir / f"results_{Path(args.evalset).stem}.csv"

    if results_rows:
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(results_rows[0].keys()))
            writer.writeheader()
            writer.writerows(results_rows)
        print(f"{'=' * 70}")
        print(f"Saved results → {out_file} ({len(results_rows)} rows)")
        print(f"Run completed in {run_duration:.2f}s")
        
        # -----------------------------------------------------------------
        # Build top-level provenance / metadata section
        # -----------------------------------------------------------------

        # Reconstruct CLI flags for logging (skip flags with default/false values)
        cli_flags_parts = []
        for k, v in vars(args).items():
            if isinstance(v, bool):
                if v:
                    cli_flags_parts.append(f"--{k}")
            elif v is not None:
                cli_flags_parts.append(f"--{k}={v}")
        cli_flags_str = " ".join(cli_flags_parts)

        # Path provenance
        provenance_lines = [
            f"**Working directory:** `{os.getcwd()}`",
            f"**Methods file:** `{methods_path}`",
            f"**Prompts file:** `{prompts_path}`",
            f"**Results directory:** `{run_dir}`",
            f"**Rows in evaluation file:** {total_rows_in_file}",
        ]

        if total_rows_in_file != len(eval_rows):
            provenance_lines.append(f"**Rows with ground truth evaluated:** {len(eval_rows)} (filtered)")

        report_md = [
            "# Geolocation Experiment – Run Report",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**CLI command flags:** `{cli_flags_str}`",
            f"**Evaluation set:** {args.evalset}",
            f"**Dry-run:** {'Yes' if args.dry_run else 'No'}",
            f"**Rows evaluated:** {len(eval_rows)}",
            f"**Methods executed:** {sum(1 for m in methods if m.get('enabled', True))}",
            f"**Runtime:** {run_duration:.2f} s",
            f"**Total tokens:** {total_input_tokens + total_output_tokens if not args.dry_run else 0}",
            f"**Estimated token cost:** ${total_token_cost_usd if not args.dry_run else 0.0:.4f}",
            f"**Results CSV:** `{out_file.relative_to(run_dir)}`",
            "",
        ] + provenance_lines + [
            "",
            "## Methods",
            "| ID | Model | Pipeline | Params |",
            "|---|---|---|---|",
        ]

        method_table_rows = []
        for m in [m for m in methods if m.get("enabled", True)]:
            param_str = ", ".join(f"{k}={v}" for k, v in m.get("params", {}).items())
            method_table_rows.append(f"| {m['id']} | {m['model']} | {m['pipeline']} | {param_str} |")

        prompt_table_rows = []
        seen_prompt_ids = set()
        for pipeline, pobj in prompt_by_pipeline.items():
            if pobj["id"] not in seen_prompt_ids:
                prompt_table_rows.append(f"| {pipeline} | {pobj['id']} | {pobj['version']} |")
                seen_prompt_ids.add(pobj["id"])

        report_md += method_table_rows + [
            "",
            "## Prompts",
            "| Pipeline | Prompt ID | Version |",
            "|---|---|---|",
        ] + prompt_table_rows

        # -----------------------------------------------------------------
        # Per-method summary table
        # -----------------------------------------------------------------
        summary_rows = ["", "## Method-level Summary", "| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |", "|---|---|---|---|---|"]

        cost_table = {
            # Example simple pricing ($/1k tokens); adjust as needed
            "default": 0.002,
        }

        for mid, st in method_stats.items():
            tok = st["input_tokens"] + st["output_tokens"]
            avg_err = sum(st["error_kms"])/len(st["error_kms"]) if st["error_kms"] else "—"
            if args.dry_run:
                cost_str = "0.0000"
            else:
                cost_str = f"{st['cost_usd']:.4f}"
            summary_rows.append(f"| {mid} | {st['calls']} | {avg_err if isinstance(avg_err,str) else f'{avg_err:.2f}'} | {tok} | {cost_str} |")

        report_md += summary_rows

        # Error summary if available
        error_values = [float(r["error_km"]) for r in results_rows if r["error_km"]]
        if error_values:
            avg_err = sum(error_values) / len(error_values)
            high = sum(1 for e in error_values if e < 1)
            medium = sum(1 for e in error_values if 1 <= e < 10)
            low = sum(1 for e in error_values if e >= 10)
            report_md += [
                "",
                "## Accuracy Summary",
                f"Average Haversine error: **{avg_err:.2f} km**",
                f"High (<1 km): {high} Medium (1–10 km): {medium} Low (>10 km): {low}",
            ]

        report_path = run_dir / "report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_md))
        print(f"Report saved → {report_path}")

        # Also echo error bands in console (already in report)
        if error_values:
            avg_err = sum(error_values) / len(error_values)
            high = sum(1 for e in error_values if e < 1)
            medium = sum(1 for e in error_values if 1 <= e < 10)
            low = sum(1 for e in error_values if e >= 10)
            print(f"Average error: {avg_err:.2f} km | Bands: {high}/{medium}/{low} (H/M/L)")
    else:
        print("No results generated")


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Run geolocation experiment methods on an evaluation set")
    parser.add_argument("--evalset", required=True, help="CSV filename (e.g., validation-dev-A.csv)")
    parser.add_argument("--methods-file", default="methods.yaml")
    parser.add_argument("--prompts-file", default="prompts.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Skip real OpenAI calls, produce mock outputs")
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--verbose", action="store_true", help="Print detailed progress info")
    parser.add_argument("--max-rows", type=int, default=None, help="Limit number of rows processed")
    return parser.parse_args()


if __name__ == "__main__":
    run_experiment(parse_args()) 