#!/usr/bin/env python3
"""reasoning_extract.py - Extract reasoning content from JSONL files

This script reads the JSONL files produced by run_reasoning_capture.py and
formats the reasoning blocks into Markdown for side-by-side comparison in
the paper.

Usage:
    python reasoning_extract.py [--jsonl PATH] [--subject-id SID]

Example:
    python reasoning_extract.py --subject-id test_entry_04
"""
import argparse
import glob
import json
import os
from pathlib import Path
import re


def strip_pydantic_wrapper(text):
    """Remove ResponseReasoningItem wrapper if present."""
    match = re.search(r'ResponseReasoningItem\([^)]*text=\'([^\']*)', text)
    if match:
        return match.group(1)
    return text


def extract_reasoning(jsonl_path, subject_id=None):
    """Extract reasoning blocks from JSONL file."""
    with open(jsonl_path, 'r') as f:
        entries = [json.loads(line) for line in f]
    
    if subject_id:
        entries = [e for e in entries if e.get('subject_id') == subject_id]
    
    result = {}
    for entry in entries:
        sid = entry.get('subject_id')
        mid = entry.get('method_id')
        pipeline = entry.get('pipeline')
        
        reasoning_blocks = entry.get('reasoning', [])
        tool_trace = entry.get('tool_trace', [])
        prediction = entry.get('prediction', '')
        
        # Process reasoning blocks
        clean_blocks = []
        for block in reasoning_blocks:
            if isinstance(block, str):
                if block == "MOCK reasoning block":
                    continue  # Skip mock blocks
                clean_blocks.append(strip_pydantic_wrapper(block))
        
        if sid not in result:
            result[sid] = {}
        
        result[sid][mid] = {
            'pipeline': pipeline,
            'reasoning': clean_blocks,
            'tool_trace': tool_trace,
            'prediction': prediction
        }
    
    return result


def format_markdown(results):
    """Generate a simple markdown listing reasoning per method and tool calls."""
    markdown = []
    
    for sid, methods in results.items():
        markdown.append(f"# {sid}\n")
        for mid, data in methods.items():
            markdown.append(f"## {mid} ({data['pipeline']})\n")
            if data['reasoning']:
                markdown.append("### Reasoning Summary")
                for line in data['reasoning']:
                    markdown.append(f"- {line}")
            if data['tool_trace']:
                markdown.append("### Tool Trace")
                for tool in data['tool_trace']:
                    markdown.append(f"* **{tool['tool']}** args={tool['args']} result={tool['result']}")
            markdown.append(f"### Prediction\n`{data['prediction']}`\n")
        markdown.append("\n---\n")
    
    return "\n".join(markdown)


def main():
    parser = argparse.ArgumentParser(description="Extract reasoning from JSONL files")
    parser.add_argument("--jsonl", help="Path to reasoning JSONL file")
    parser.add_argument("--subject-id", help="Filter by subject ID")
    args = parser.parse_args()
    
    # Find latest JSONL file if not specified
    jsonl_path = args.jsonl
    if not jsonl_path:
        base_dir = Path(__file__).resolve().parent
        patterns = [
            str(base_dir / "reasoning_runs" / "reasoning_*" / "reasoning_traces.jsonl"),
        ]
        
        all_files = []
        for pattern in patterns:
            all_files.extend(glob.glob(pattern))
        
        if not all_files:
            print("No reasoning trace files found.")
            return
        
        # Sort by modification time to get the latest
        jsonl_path = sorted(all_files, key=os.path.getmtime)[-1]
        print(f"Using latest file: {jsonl_path}")
    
    results = extract_reasoning(jsonl_path, args.subject_id)
    markdown = format_markdown(results)
    
    # Save to file
    output_file = Path(jsonl_path).parent / "reasoning_comparison.md"
    with open(output_file, "w") as f:
        f.write(markdown)
    
    print(f"Wrote comparison to {output_file}")
    print("\nPreview of markdown:")
    print("=" * 40)
    print(markdown[:1000] + "..." if len(markdown) > 1000 else markdown)


if __name__ == "__main__":
    main() 