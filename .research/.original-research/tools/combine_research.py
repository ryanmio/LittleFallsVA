#!/usr/bin/env python3
"""
Combine all research files into a single JSON or markdown file.
This script recursively scans the .research directory and combines all text files,
excluding:
- /tools/ directory
- Falls Church History Room/General Indexes directory
- target-research-list.md

Usage:
    python combine_research.py --format [json|markdown] --output filename
"""

import os
import json
import argparse
import glob
from pathlib import Path
from datetime import datetime

def get_file_contents(file_path):
    """Read and return the contents of a file."""
    try:
        # Try to detect if file is binary
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # Binary file detection
                return f"[Skipped binary file: {file_path}]"
            
        # If not binary, read as text
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return f"[Skipped file with unsupported encoding: {file_path}]"
    except Exception as e:
        return f"[Error reading file {file_path}: {str(e)}]"

def is_text_file(file_path):
    """Check if a file is likely a text file by extension."""
    text_extensions = [
        '.md', '.txt', '.text', '.json', '.csv',
        '.py', '.js', '.html', '.css', '.sh',
        '.yaml', '.yml', '.xml', '.rst', '.ini',
        '.conf', '.cfg'
    ]
    return file_path.suffix.lower() in text_extensions

def should_exclude_file(file_path):
    """Check if a file should be excluded from processing."""
    path_str = str(file_path)
    
    # Exclude target-research-list.md
    if file_path.name == 'target-research-list.md':
        return True
    
    # Exclude tools directory
    if '/tools/' in path_str:
        return True
        
    # Exclude General Indexes
    if 'Falls Church History Room/General Indexes' in path_str:
        return True
        
    return False

def combine_to_json(base_dir):
    """Combine all research files into a JSON structure."""
    result = {}
    base_path = Path(base_dir)
    
    # Get all files recursively in the .research directory
    for file_path in base_path.glob('**/*'):
        # Skip directories and excluded files
        if file_path.is_dir() or should_exclude_file(file_path):
            continue
            
        # Skip binary files
        if not is_text_file(file_path) and not file_path.suffix == '':
            continue
            
        # Get relative path from base_dir
        rel_path = str(file_path.relative_to(base_path))
        
        # Add file contents to result
        try:
            result[rel_path] = get_file_contents(file_path)
        except Exception as e:
            result[rel_path] = f"[Error: {str(e)}]"
    
    return result

def combine_to_markdown(base_dir):
    """Combine all research files into a single markdown document."""
    result = []
    base_path = Path(base_dir)
    
    # Add header with generation time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result.append(f"# Combined Research\nGenerated on: {current_time}\n\n")
    
    # Get all files recursively in the .research directory
    files = sorted(base_path.glob('**/*'))  # Sort files for consistent output
    for file_path in files:
        # Skip directories and excluded files
        if file_path.is_dir() or should_exclude_file(file_path):
            continue
            
        # Skip non-text files
        if not is_text_file(file_path):
            continue
            
        # Get relative path from base_dir
        rel_path = str(file_path.relative_to(base_path))
        
        # Add file header and contents to result
        result.append(f"\n## {rel_path}\n")
        result.append(f"```{file_path.suffix[1:] if file_path.suffix else 'text'}")
        content = get_file_contents(file_path)
        result.append(content)
        result.append("```\n")
    
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description='Combine research files into a single file.')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown',
                        help='Output format (json or markdown)')
    parser.add_argument('--output', default='combined_research', 
                        help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    # Add current date to filename
    current_date = datetime.now().strftime('%Y-%m-%d')
    output_base = f"{args.output}_{current_date}"
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')
    
    if args.format == 'json':
        output_file = f"{output_base}.json"
        result = combine_to_json(base_dir)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    else:
        output_file = f"{output_base}.md"
        result = combine_to_markdown(base_dir)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    
    print(f"Combined research saved to {output_file}")

if __name__ == "__main__":
    main() 