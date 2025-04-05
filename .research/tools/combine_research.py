#!/usr/bin/env python3
"""
Combine all research files into a single JSON or markdown file.
This script recursively scans the .research directory and combines all text files,
excluding the .original-research directory and target-research-list.md.

Usage:
    python combine_research.py --format [json|markdown] --output filename
"""

import os
import json
import argparse
import glob
from pathlib import Path

def get_file_contents(file_path):
    """Read and return the contents of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file {file_path}: {str(e)}]"

def is_text_file(file_path):
    """Check if a file is likely a text file by extension."""
    text_extensions = [
        '.md', '.txt', '.text', '.json', '.csv', '.html', '.xml', 
        '.js', '.py', '.css', '.sh', '.bat', '.ps1'
    ]
    return file_path.suffix.lower() in text_extensions

def should_exclude_file(file_path):
    """Check if a file should be excluded from processing."""
    # Exclude .original-research directory
    if '.original-research' in str(file_path):
        return True
        
    # Exclude target-research-list.md
    if file_path.name == 'target-research-list.md':
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
        
        # Add file header and contents to result
        result.append(f"# FILE: {rel_path}\n\n```{file_path.suffix[1:] if file_path.suffix else 'text'}")
        try:
            result.append(get_file_contents(file_path))
        except Exception as e:
            result.append(f"[Error: {str(e)}]")
        result.append("```\n\n")
    
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description='Combine research files into a single file.')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown',
                        help='Output format (json or markdown)')
    parser.add_argument('--output', default='combined_research', 
                        help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')
    
    if args.format == 'json':
        output_file = f"{args.output}.json"
        result = combine_to_json(base_dir)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    else:
        output_file = f"{args.output}.md"
        result = combine_to_markdown(base_dir)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    
    print(f"Combined research saved to {output_file}")

if __name__ == "__main__":
    main() 