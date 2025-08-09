#!/usr/bin/env python3
"""run_reasoning_capture.py – lightweight driver to capture chain-of-thought
reasoning for a small number of rows and methods.

Differences vs. run_experiment.py
--------------------------------
• Focuses on *reasoning output* rather than error metrics.
• Allows explicit row selection via `--subject-ids` (comma-separated) so that we
  can target interesting examples for the paper (e.g. "test_entry_04").
• Stores a compact JSONL of the conversation trace with keys:
    subject_id, method_id, pipeline, reasoning (list[str]), tool_trace (list),
    prediction (str), latency_s (float).
• Supports both real and dry-run execution.  In dry-run we re-use the mock
  machinery from run_experiment so that the flow can be tested without API
  calls.

Example usage
-------------
python run_reasoning_capture.py \
    --evalset "validation - TEST-FULL-H1-final.csv" \
    --methods-file methods-thinking-capture.yaml \
    --subject-ids test_entry_04 \
    --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import time
from datetime import datetime
from pathlib import Path

from openai import OpenAI

# We re-use a subset of utilities from the original driver.
# The file is in the same directory, so a relative import works.
import run_experiment as _exp  # type: ignore

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_evalset_rows(path: Path, subject_ids: set[str]) -> list[dict]:
    """Return the subset of CSV rows whose `subject_id` appears in subject_ids."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r.get("subject_id") in subject_ids]
    if not rows:
        raise ValueError(
            f"No rows found for the supplied subject_ids in {path}: {', '.join(subject_ids)}"
        )
    return rows


def extract_reasoning_texts(output_items) -> list[str]:
    """Extract any `reasoning` blocks emitted by the Responses API."""
    reasoning_texts: list[str] = []
    for itm in output_items:
        typ = getattr(itm, "type", None) if hasattr(itm, "type") else itm.get("type", "")
        if typ != "reasoning":
            continue

        # Prefer the summarizer output if present
        summaries = None
        if hasattr(itm, "summary"):
            summaries = itm.summary  # list of objects with 'text'
        elif isinstance(itm, dict) and "summary" in itm:
            summaries = itm["summary"]

        if summaries:
            for s in summaries:
                if isinstance(s, dict):
                    reasoning_texts.append(s.get("text", ""))
                else:
                    # Pydantic model: use .text when available or str()
                    reasoning_texts.append(getattr(s, "text", str(s)))
        else:
            # Fallback to .text or generic string if no summary
            if hasattr(itm, "text"):
                reasoning_texts.append(itm.text)
            elif isinstance(itm, dict):
                reasoning_texts.append(itm.get("text", ""))
            else:
                reasoning_texts.append(str(itm))
    return reasoning_texts


# ---------------------------------------------------------------------------
# One-shot pipeline wrapper (captures reasoning output)
# ---------------------------------------------------------------------------


def run_one_shot_capture(client: OpenAI, method: dict, prompt_obj: dict, entry_text: str):
    params = method.get("params", {}).copy()
    params.setdefault("store", True)

    # Handle reasoning directive; adapt from original driver
    if "reasoning_effort" in params:
        params["reasoning"] = {
            "effort": params.pop("reasoning_effort"),
            "summary": "detailed",
        }

    # Ensure we request plain text format for the answer
    params["text"] = {"format": {"type": "text"}}

    start = time.time()
    response = client.responses.create(
        model=method["model"],
        input=[{"role": "user", "content": entry_text}],
        instructions=prompt_obj["text"].strip(),
        **params,
    )
    latency = time.time() - start

    # Extract reasoning blocks and final answer
    reasoning_blocks = extract_reasoning_texts(response.output)

    final_answer = ""
    for itm in response.output:
        typ = getattr(itm, "type", None) if hasattr(itm, "type") else itm.get("type")
        if typ in {"message", "text", "json_object"}:
            final_answer = _exp.extract_output_text(itm)  # re-use util
            if final_answer:
                break

    usage = response.model_dump().get("usage", {})

    return {
        "reasoning": reasoning_blocks,
        "prediction": final_answer,
        "tool_trace": [],
        "usage": usage,
        "latency_s": latency,
        "raw_response": response.model_dump(),
    }


# ---------------------------------------------------------------------------
# Tool-chain pipeline (captures stepwise reasoning + tool calls)
# ---------------------------------------------------------------------------


def run_tool_chain_capture(client: OpenAI, method: dict, prompt_obj: dict, entry_text: str):
    params = method.get("params", {}).copy()
    params.setdefault("store", True)
    if "reasoning_effort" in params:
        params["reasoning"] = {
            "effort": params.pop("reasoning_effort"),
            "summary": "detailed",
        }

    messages = [{"role": "user", "content": entry_text}]
    tools = [_exp.GEOCODE_TOOL_SPEC, _exp.CENTROID_TOOL_SPEC]

    total_usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    reasoning_blocks: list[str] = []
    tool_trace: list[dict] = []

    start_time = time.time()

    for _ in range(12):  # generous cap
        response = client.responses.create(
            model=method["model"],
            input=messages,
            instructions=prompt_obj["text"].strip(),
            tools=tools,
            **params,
        )

        # accumulate token usage
        if response.usage:
            u = response.usage.model_dump()
            for k in ("input_tokens", "output_tokens", "total_tokens"):
                total_usage[k] = total_usage.get(k, 0) + u.get(k, 0)

        # Harvest reasoning blocks from this round
        reasoning_blocks.extend(extract_reasoning_texts(response.output))

        # Detect first function call vs final answer
        func_item = None
        answer_item = None
        for itm in response.output:
            typ = getattr(itm, "type", None) if hasattr(itm, "type") else itm.get("type")
            if typ == "function_call" and func_item is None:
                func_item = itm
            elif typ in {"message", "text", "json_object"} and answer_item is None:
                answer_item = itm

        if func_item is not None:
            # Execute the tool locally (same logic as run_experiment)
            name = func_item.get("name") if isinstance(func_item, dict) else func_item.name
            args_json = func_item.get("arguments") if isinstance(func_item, dict) else func_item.arguments
            try:
                args = json.loads(args_json) if isinstance(args_json, str) else args_json
            except Exception:
                args = {}

            if name == "geocode_place":
                result = _exp.geocode_place(**args)
            elif name == "compute_centroid":
                result = _exp.compute_centroid(**args)
            else:
                result = {"error": f"Unknown tool {name}"}

            # Append to trace
            tool_trace.append({"tool": name, "args": args, "result": result})

            # Build messages that the model will read next
            # The Responses API requires the assistant's function_call message to be
            # preceded by a `reasoning` item.  Preserve the original reasoning if
            # present, otherwise inject an empty placeholder to satisfy schema.
            reasoning_item = None
            for itm in response.output:
                t = getattr(itm, "type", None) if hasattr(itm, "type") else itm.get("type", "")
                if t == "reasoning":
                    reasoning_item = itm
                    break

            if reasoning_item is None:
                reasoning_item = {
                    "type": "reasoning",
                    "text": "",
                }

            call_msg = func_item.model_dump() if hasattr(func_item, "model_dump") else func_item
            messages.append(reasoning_item)
            messages.append(call_msg)
            messages.append({
                "type": "function_call_output",
                "call_id": func_item.get("call_id") if isinstance(func_item, dict) else func_item.call_id,
                "output": json.dumps(result),
            })
            continue  # next round

        # Otherwise, treat as final answer
        final_answer = _exp.extract_output_text(answer_item) if answer_item else ""
        return {
            "reasoning": reasoning_blocks,
            "prediction": final_answer,
            "tool_trace": tool_trace,
            "usage": total_usage,
            "latency_s": time.time() - start_time,
            "raw_response": response.model_dump(),
        }

    # fell through loop without final answer
    return {
        "reasoning": reasoning_blocks,
        "prediction": "ERROR: exceeded max turns",
        "tool_trace": tool_trace,
        "usage": total_usage,
        "latency_s": time.time() - start_time,
        "raw_response": {},
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description="Capture reasoning traces for selected rows.")
    ap.add_argument("--evalset", required=True, help="CSV evaluation set filename")
    ap.add_argument("--methods-file", required=True, help="YAML of methods to run")
    ap.add_argument("--prompts-file", default="prompts.yaml", help="YAML of prompts")
    ap.add_argument("--subject-ids", required=True, help="Comma-separated list of subject_id values to evaluate")
    ap.add_argument("--dry-run", action="store_true", help="Use mock outputs instead of real API calls")
    ap.add_argument("--seed", type=int, default=123)
    args = ap.parse_args()

    random.seed(args.seed)

    wd = Path(__file__).resolve().parent
    evalset_path = wd / args.evalset
    methods_path = wd / args.methods_file
    prompts_path = wd / args.prompts_file

    subject_ids = {sid.strip() for sid in args.subject_ids.split(',') if sid.strip()}
    rows = load_evalset_rows(evalset_path, subject_ids)

    methods = _exp.load_yaml(methods_path)
    prompts = _exp.load_yaml(prompts_path)
    prompt_by_pipeline = {p["pipeline"]: p for p in prompts}

    # output directory
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = wd / "reasoning_runs" / f"reasoning_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    client = None if args.dry_run else _exp.init_openai_client()

    jsonl_path = out_dir / "reasoning_traces.jsonl"

    with open(jsonl_path, "w", encoding="utf-8") as log_f:
        for row in rows:
            subj = row.get("subject_id")
            entry_text = row["raw_entry"]
            for m in methods:
                if not m.get("enabled", True):
                    continue
                method_id = m["id"]
                pipeline = m["pipeline"]
                prompt_obj = prompt_by_pipeline[pipeline]

                if args.dry_run:
                    # leverage existing mock_response util
                    mock_resp = _exp.mock_response(m, prompt_obj, entry_text, 0)
                    reasoning = ["MOCK reasoning block"]
                    prediction = mock_resp["output"][0]["content"][0]["text"]
                    tool_trace = []
                    usage = mock_resp["usage"]
                    latency = 0.0
                else:
                    if pipeline == "one_shot":
                        res = run_one_shot_capture(client, m, prompt_obj, entry_text)
                    else:
                        res = run_tool_chain_capture(client, m, prompt_obj, entry_text)
                    reasoning = res["reasoning"]
                    prediction = res["prediction"]
                    tool_trace = res["tool_trace"]
                    usage = res["usage"]
                    latency = res["latency_s"]

                record = {
                    "subject_id": subj,
                    "method_id": method_id,
                    "model": m["model"],
                    "pipeline": pipeline,
                    "reasoning": reasoning,
                    "tool_trace": tool_trace,
                    "prediction": prediction,
                    "usage": usage,
                    "latency_s": latency,
                }
                log_f.write(json.dumps(record) + "\n")
                print(f"{subj} | {method_id} done – reasoning lines: {len(reasoning)}")

    print(f"\nWrote reasoning traces → {jsonl_path}\n")


if __name__ == "__main__":
    main() 