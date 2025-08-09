#!/usr/bin/env python3
"""
create_flow_diagrams.py - Generate visual flow diagrams showing the reasoning
process for one-shot vs tool-chain methods on the same test cases.

This script takes the reasoning traces from JSONL files and creates Graphviz
visualizations highlighting the different reasoning paths.
"""

import json
import os
from pathlib import Path
import sys

try:
    import graphviz
except ImportError:
    print("Please install graphviz: pip install graphviz")
    sys.exit(1)

# Create output directory for diagrams
OUTPUT_DIR = Path(__file__).parent

def load_traces(jsonl_path, subject_ids=None):
    """Load reasoning traces from JSONL file, optionally filtering by subject_id."""
    traces = []
    with open(jsonl_path) as f:
        for line in f:
            trace = json.loads(line)
            if subject_ids is None or trace["subject_id"] in subject_ids:
                traces.append(trace)
    return traces

def truncate_text(text, max_length=80):
    """Truncate text to a maximum length for display."""
    if text and len(text) > max_length:
        return text[:max_length] + "..."
    return text

def wrap_text(text, max_width=60):
    """Break long lines of text for better readability in graphviz nodes."""
    if not text or len(text) <= max_width:
        return text
        
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Check if adding this word would exceed max_width
        if current_length + len(word) + (1 if current_length > 0 else 0) > max_width:
            # Start a new line
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            # Add to current line
            current_line.append(word)
            current_length += len(word) + (1 if current_length > 0 else 0)
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def format_tool_args(args_dict):
    """Format tool arguments in a clean, readable way."""
    if not args_dict:
        return "None"
    
    # Handle the common case of 'query' and 'strategy' arguments
    if isinstance(args_dict, dict) and 'query' in args_dict:
        parts = []
        if 'query' in args_dict:
            parts.append(f"Query: '{args_dict['query']}'")
        if 'strategy' in args_dict:
            parts.append(f"Strategy: '{args_dict['strategy']}'")
        return '\n'.join(parts)
    
    # For other cases, just clean up the dict representation
    return str(args_dict).replace("{", "").replace("}", "").replace("'", "")

def format_tool_result(result_dict):
    """Format tool result in a clean, readable way."""
    if not result_dict:
        return "None"
    
    # For geocode results, create a more readable format
    if isinstance(result_dict, dict) and 'lat' in result_dict and 'lng' in result_dict:
        parts = []
        if 'lat' in result_dict and 'lng' in result_dict:
            parts.append(f"Coordinates: {result_dict['lat']}, {result_dict['lng']}")
        if 'formatted_address' in result_dict:
            parts.append(f"Address: {result_dict['formatted_address']}")
        if 'query_used' in result_dict:
            parts.append(f"Query used: {result_dict['query_used']}")
        return '\n'.join(parts)
    
    # For other cases, just clean up the dict representation
    return str(result_dict).replace("{", "").replace("}", "").replace("'", "")

def create_reasoning_diagram(trace, output_path):
    """Create a flowchart visualization of the reasoning process."""
    # Configure graph
    dot = graphviz.Digraph(
        comment=f'Reasoning flow for {trace["subject_id"]} using {trace["method_id"]}',
        format='png'
    )
    dot.attr('graph', rankdir='TB', ranksep='0.8', nodesep='0.6')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', margin='0.4,0.3')
    dot.attr('edge', fontname='Arial', fontsize='10')
    
    # Add input node (the abstract text or just subject ID if abstract is missing)
    if "abstract" in trace:
        # Still truncate the abstract to keep the graph readable
        abstract_short = truncate_text(trace["abstract"], 100)
        input_text = f'Input: {trace["subject_id"]}\n{abstract_short}'
    else:
        input_text = f'Input: {trace["subject_id"]}'
    
    dot.node('input', input_text, fillcolor='lightblue', style='filled')
    
    # Add method info node
    method_info = f'Method: {trace["method_id"]}\nPipeline: {trace["pipeline"]}'
    dot.node('method', method_info, fillcolor='lightgrey', style='filled')
    dot.edge('input', 'method')
    
    prev_node = 'method'
    
    # Process reasoning steps and tool calls
    if trace["pipeline"] == "tool_chain":
        # Tool chain has alternating reasoning and tool calls
        reasoning_steps = trace["reasoning"]
        tool_calls = trace["tool_trace"]
        
        # Create nodes for each reasoning step and tool call
        total_steps = max(len(reasoning_steps), len(tool_calls))
        
        for i in range(total_steps):
            # Add reasoning step if available
            if i < len(reasoning_steps):
                # Use full reasoning text without truncation, but wrap long lines
                r_text = wrap_text(reasoning_steps[i], max_width=80)
                reasoning_id = f'reasoning_{i}'
                dot.node(reasoning_id, f'Reasoning step {i+1}:\n{r_text}', 
                        fillcolor='#E8F8E8', style='filled')
                dot.edge(prev_node, reasoning_id)
                prev_node = reasoning_id
            
            # Add tool call if available
            if i < len(tool_calls):
                tool = tool_calls[i]
                tool_id = f'tool_{i}'
                
                # Format tool calls in a cleaner way
                tool_name = tool["tool"]
                formatted_args = format_tool_args(tool["args"])
                formatted_result = format_tool_result(tool["result"])
                
                tool_text = f'Tool: {tool_name}\n\n{formatted_args}\n\n{formatted_result}'
                dot.node(tool_id, tool_text, fillcolor='#FFE8E8', style='filled')
                dot.edge(prev_node, tool_id)
                prev_node = tool_id
    else:
        # One-shot just has reasoning steps
        for i, r in enumerate(trace["reasoning"]):
            # Use full reasoning text without truncation, but wrap long lines
            r_text = wrap_text(r, max_width=80)
            reasoning_id = f'reasoning_{i}'
            dot.node(reasoning_id, f'Reasoning step {i+1}:\n{r_text}', 
                    fillcolor='#E8F8E8', style='filled')
            dot.edge(prev_node, reasoning_id)
            prev_node = reasoning_id
    
    # Add prediction node
    prediction = trace["prediction"]
    dot.node('prediction', f'Output:\n{prediction}', fillcolor='#E8F8FF', style='filled')
    dot.edge(prev_node, 'prediction')
    
    # Save diagram
    try:
        dot.render(output_path, cleanup=True)
        print(f"Created diagram: {output_path}.png")
        return True
    except Exception as e:
        print(f"Error creating diagram: {e}")
        return False

def create_side_by_side_html(traces, output_path):
    """Create HTML file with side-by-side comparison of one-shot vs tool-chain."""
    # Group traces by subject_id
    by_subject = {}
    for trace in traces:
        sid = trace["subject_id"]
        if sid not in by_subject:
            by_subject[sid] = {}
        by_subject[sid][trace["pipeline"]] = trace
    
    # Create HTML for each subject
    html_parts = []
    
    for sid, methods in by_subject.items():
        if "one_shot" not in methods or "tool_chain" not in methods:
            print(f"Skipping {sid} - missing one of the methods")
            continue
            
        one_shot = methods["one_shot"]
        tool_chain = methods["tool_chain"]
        
        # Add abstract if available
        abstract_text = ""
        if "abstract" in one_shot:
            abstract_text = f'<div class="abstract"><strong>Abstract:</strong> {one_shot["abstract"]}</div>'
        
        html_parts.append(f"""
        <h2>Reasoning Comparison for {sid}</h2>
        {abstract_text}
        <table>
            <tr>
                <th>One-Shot ({one_shot["method_id"]})</th>
                <th>Tool-Chain ({tool_chain["method_id"]})</th>
            </tr>
        """)
        
        # Determine maximum number of rows needed
        one_shot_steps = len(one_shot["reasoning"])
        tool_chain_steps = len(tool_chain["reasoning"]) + len(tool_chain["tool_trace"])
        max_steps = max(one_shot_steps, tool_chain_steps)
        
        # Process one-shot reasoning
        one_shot_rows = []
        for i, r in enumerate(one_shot["reasoning"]):
            # Use full reasoning text with added styling for readability
            r_html = r.replace('\n', '<br>')
            one_shot_rows.append(f'<div class="reasoning-step"><strong>Step {i+1}:</strong><p>{r_html}</p></div>')
        
        # Process tool-chain (interleaving reasoning and tool calls)
        tool_chain_rows = []
        r_idx = t_idx = 0
        
        # Alternate between reasoning and tool calls
        while r_idx < len(tool_chain["reasoning"]) or t_idx < len(tool_chain["tool_trace"]):
            # Add reasoning step if available
            if r_idx < len(tool_chain["reasoning"]):
                # Use full reasoning text with added styling for readability
                r_html = tool_chain["reasoning"][r_idx].replace('\n', '<br>')
                tool_chain_rows.append(
                    f'<div class="reasoning-step"><strong>Reasoning {r_idx+1}:</strong><p>{r_html}</p></div>'
                )
                r_idx += 1
            
            # Add tool call if available
            if t_idx < len(tool_chain["tool_trace"]):
                tool = tool_chain["tool_trace"][t_idx]
                args_str = str(tool["args"]).replace('"', '&quot;')
                result_str = str(tool["result"]).replace('"', '&quot;')
                tool_chain_rows.append(
                    f'<div class="tool-call"><strong>Tool:</strong> {tool["tool"]}<br>'
                    f'<strong>Args:</strong> <pre>{args_str}</pre><br>'
                    f'<strong>Result:</strong> <pre>{result_str}</pre></div>'
                )
                t_idx += 1
        
        # Create table rows
        for i in range(max(len(one_shot_rows), len(tool_chain_rows))):
            html_parts.append("<tr>")
            
            # One-shot column
            html_parts.append("<td>")
            if i < len(one_shot_rows):
                html_parts.append(one_shot_rows[i])
            html_parts.append("</td>")
            
            # Tool-chain column
            html_parts.append("<td>")
            if i < len(tool_chain_rows):
                html_parts.append(tool_chain_rows[i])
            html_parts.append("</td>")
            
            html_parts.append("</tr>")
        
        # Add predictions
        html_parts.append(f"""
        <tr class="predictions">
            <td><strong>Prediction:</strong> {one_shot["prediction"]}</td>
            <td><strong>Prediction:</strong> {tool_chain["prediction"]}</td>
        </tr>
        </table>
        <hr>
        """)
    
    # Combine all parts into a complete HTML document
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Reasoning Comparison: One-Shot vs Tool-Chain</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; vertical-align: top; }}
            th {{ background-color: #f2f2f2; text-align: left; }}
            .abstract {{ margin-bottom: 15px; background-color: #f8f8f8; padding: 10px; border-left: 4px solid #ccc; }}
            .reasoning-step {{ background-color: #E8F8E8; padding: 8px; margin-bottom: 8px; }}
            .reasoning-step p {{ margin: 6px 0; line-height: 1.4; white-space: pre-wrap; }}
            .tool-call {{ background-color: #FFE8E8; padding: 8px; margin-bottom: 8px; }}
            .tool-call pre {{ margin: 5px 0; overflow-x: auto; background-color: #fff; padding: 5px; border: 1px solid #eee; }}
            .predictions {{ background-color: #E8F8FF; }}
            hr {{ margin: 30px 0; }}
        </style>
    </head>
    <body>
        <h1>Reasoning Comparison: One-Shot vs Tool-Chain</h1>
        {''.join(html_parts)}
    </body>
    </html>
    """
    
    # Write HTML to file
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Created HTML comparison: {output_path}")

def create_ascii_diagram(trace, output_path):
    """Create a simple ASCII flowchart of the reasoning process."""
    with open(output_path, 'w') as f:
        # Write header
        f.write(f"Reasoning flow for {trace['subject_id']} using {trace['method_id']}\n")
        f.write("=" * 80 + "\n\n")
        
        # Write input
        if "abstract" in trace:
            f.write(f"INPUT: {trace['abstract']}\n")
        else:
            f.write(f"INPUT: {trace['subject_id']}\n")
        f.write("|\n|\n↓\n\n")
        
        # Write method info
        f.write(f"METHOD: {trace['method_id']} ({trace['pipeline']})\n")
        f.write("|\n|\n↓\n\n")
        
        # Write reasoning steps and tool calls
        if trace["pipeline"] == "tool_chain":
            # Tool chain has alternating reasoning and tool calls
            reasoning_steps = trace["reasoning"]
            tool_calls = trace["tool_trace"]
            
            # Determine total steps
            total_steps = max(len(reasoning_steps), len(tool_calls))
            
            for i in range(total_steps):
                # Add reasoning step if available
                if i < len(reasoning_steps):
                    f.write(f"REASONING STEP {i+1}:\n")
                    f.write("-" * 80 + "\n")
                    f.write(reasoning_steps[i] + "\n")
                    f.write("|\n|\n↓\n\n")
                
                # Add tool call if available
                if i < len(tool_calls):
                    tool = tool_calls[i]
                    f.write(f"TOOL CALL {i+1}: {tool['tool']}\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"Args: {str(tool['args'])}\n")
                    f.write(f"Result: {str(tool['result'])}\n")
                    f.write("|\n|\n↓\n\n")
        else:
            # One-shot just has reasoning steps
            for i, r in enumerate(trace["reasoning"]):
                f.write(f"REASONING STEP {i+1}:\n")
                f.write("-" * 80 + "\n")
                f.write(r + "\n")
                f.write("|\n|\n↓\n\n")
        
        # Write prediction
        f.write("OUTPUT:\n")
        f.write("-" * 80 + "\n")
        f.write(trace["prediction"] + "\n")
    
    print(f"Created ASCII diagram: {output_path}")

def create_text_comparison(traces, output_path):
    """Create a text-based, publication-ready comparison of reasoning processes."""
    # Group traces by subject_id
    by_subject = {}
    for trace in traces:
        sid = trace["subject_id"]
        if sid not in by_subject:
            by_subject[sid] = {}
        by_subject[sid][trace["pipeline"]] = trace
    
    with open(output_path, 'w') as f:
        f.write("# Reasoning Process Comparison: One-Shot vs Tool-Chain\n\n")
        
        # Process each subject
        for sid, methods in by_subject.items():
            if "one_shot" not in methods or "tool_chain" not in methods:
                print(f"Skipping {sid} - missing one of the methods")
                continue
                
            one_shot = methods["one_shot"]
            tool_chain = methods["tool_chain"]
            
            # Write subject header and prediction
            f.write(f"## {sid}\n\n")
            
            # Write abstract if available
            if "abstract" in one_shot:
                f.write(f"**Abstract:** {one_shot['abstract']}\n\n")
            
            # Get final predictions
            os_prediction = one_shot.get("prediction", "No prediction")
            tc_prediction = tool_chain.get("prediction", "No prediction")
            
            f.write("### One-Shot Approach\n")
            f.write(f"**Method:** {one_shot['method_id']}\n\n")
            f.write("**Reasoning Process:**\n\n")
            
            # Write one-shot reasoning
            for i, r in enumerate(one_shot["reasoning"]):
                f.write(f"{i+1}. {r}\n\n")
            
            f.write(f"**Final Prediction:** {os_prediction}\n\n")
            
            f.write("### Tool-Chain Approach\n")
            f.write(f"**Method:** {tool_chain['method_id']}\n\n")
            f.write("**Reasoning Process with Tool Calls:**\n\n")
            
            # Interleave reasoning and tool calls
            r_idx = t_idx = 0
            steps = []
            
            # Create an interleaved list of steps
            while r_idx < len(tool_chain["reasoning"]) or t_idx < len(tool_chain["tool_trace"]):
                if r_idx < len(tool_chain["reasoning"]):
                    steps.append(("reasoning", r_idx, tool_chain["reasoning"][r_idx]))
                    r_idx += 1
                
                if t_idx < len(tool_chain["tool_trace"]):
                    steps.append(("tool", t_idx, tool_chain["tool_trace"][t_idx]))
                    t_idx += 1
            
            # Write interleaved steps with step numbers
            for i, (step_type, idx, content) in enumerate(steps):
                if step_type == "reasoning":
                    f.write(f"{i+1}. {content}\n\n")
                else:
                    tool_name = content["tool"]
                    args = content["args"]
                    result = content["result"]
                    
                    f.write(f"{i+1}. **Tool Call:** {tool_name}\n")
                    f.write(f"   - Arguments: {args}\n")
                    f.write(f"   - Result: {result}\n\n")
            
            f.write(f"**Final Prediction:** {tc_prediction}\n\n")
            
            # Add separator between subjects
            f.write("-" * 80 + "\n\n")
    
    print(f"Created text comparison: {output_path}")

def main():
    # Process command line arguments
    if len(sys.argv) < 2:
        print("Usage: python create_flow_diagrams.py <jsonl_file> [subject_id1,subject_id2,...]")
        sys.exit(1)
    
    jsonl_path = sys.argv[1]
    subject_ids = None
    if len(sys.argv) > 2:
        subject_ids = sys.argv[2].split(',')
    
    # Load traces
    try:
        traces = load_traces(jsonl_path, subject_ids)
    except Exception as e:
        print(f"Error loading traces: {e}")
        sys.exit(1)
    
    if not traces:
        print("No matching traces found")
        sys.exit(1)
    
    print(f"Processing {len(traces)} traces...")
    
    # Create various visualization types
    for trace in traces:
        # Create Graphviz diagram
        output_path = OUTPUT_DIR / f"{trace['subject_id']}_{trace['method_id']}"
        create_reasoning_diagram(trace, str(output_path))
        
        # Create ASCII diagram
        ascii_path = OUTPUT_DIR / f"{trace['subject_id']}_{trace['method_id']}_ascii.txt"
        create_ascii_diagram(trace, ascii_path)
    
    # Create HTML side-by-side comparison
    html_path = OUTPUT_DIR / "reasoning_comparison.html"
    create_side_by_side_html(traces, html_path)
    
    # Create text-based comparison for paper
    text_path = OUTPUT_DIR / "reasoning_comparison_for_paper.md"
    create_text_comparison(traces, text_path)

if __name__ == "__main__":
    main() 