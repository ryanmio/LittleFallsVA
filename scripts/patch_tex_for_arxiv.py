#!/usr/bin/env python3
r"""patch_tex_for_arxiv.py

Make a copy of a .tex file with XeTeX/LuaTeX-only packages removed so
arXiv doesn't think a Unicode engine is required.

Specifically strips lines containing:
  * \usepackage{unicode-math}
  * fontspec
  * defaultfontfeatures

Usage
-----
$ python scripts/patch_tex_for_arxiv.py path/to/main.tex

Creates path/to/main_arxiv.tex (unless -o is given).
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

PATTERNS = [
    re.compile(r"unicode-math"),
    re.compile(r"fontspec"),
    re.compile(r"defaultfontfeatures"),
    re.compile(r"\\else % if luatex or xetex"),
    re.compile(r"% xetex/luatex font selection"),
]

REPLACEMENTS = [
    # Replace passthrough lstinline with texttt
    (re.compile(r"\\passthrough\{\\lstinline!([^!]+)!\}"), r"\\texttt{\1}"),
    # Replace longtable with tabular in twocolumn
    (re.compile(r"\\begin\{longtable\}"), r"\\begin{tabular}"),
    (re.compile(r"\\end\{longtable\}"), r"\\end{tabular}"),
    # Remove longtable-specific commands
    (re.compile(r"\\tabularnewline"), r"\\\\"),
    (re.compile(r"\\endfirsthead.*"), r""),
    (re.compile(r"\\endhead.*"), r""),
    (re.compile(r"\\endlastfoot.*"), r""),
    # Fix caption issues - remove captions from tabular
    (re.compile(r"\\caption\{[^}]+\}\\\\"), r""),
    (re.compile(r"\\caption\{\\label\{[^}]+\}[^}]+\}\\\\"), r""),
    # Remove problematic Unicode options
    (re.compile(r"\\PassOptionsToPackage\{unicode\}\{hyperref\}"), r"% Unicode option removed"),
    # Replace degree symbols with LaTeX commands
    (re.compile("°"), r"\\textdegree{}"),
    # Replace smart quotes
    (re.compile("'"), r"'"),
    (re.compile("'"), r"'"),
    # Remove noalign commands that cause issues
    (re.compile(r"\\toprule\\noalign\{\}"), r"\\toprule"),
    (re.compile(r"\\midrule\\noalign\{\}"), r"\\midrule"),
    (re.compile(r"\\bottomrule\\noalign\{\}"), r"\\bottomrule"),
]


def should_strip(line: str) -> bool:
    return any(p.search(line) for p in PATTERNS)


def apply_replacements(line: str) -> str:
    """Apply regex replacements to fix arXiv compatibility issues."""
    for pattern, replacement in REPLACEMENTS:
        line = pattern.sub(replacement, line)
    return line


def patch_file(src: pathlib.Path, dest: pathlib.Path) -> None:
    content = src.read_text(encoding="utf-8")
    
    # First apply line-by-line replacements
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        if should_strip(line):
            # Comment stripped line so numbering preserved for debugging
            processed_lines.append(f"%% arXiv patch removed: {line}")
        else:
            # Apply replacements to fix compatibility issues
            line = apply_replacements(line)
            processed_lines.append(line)
    
    content = '\n'.join(processed_lines)
    
    # Now handle table structures - convert problematic tabular to proper table floats
    # Pattern: \begin{tabular}...\caption{...}...content...\end{tabular}
    import re
    
    def fix_table(match):
        table_content = match.group(0)
        # Extract caption if present
        caption_match = re.search(r'\\caption\{([^}]+)\}', table_content)
        caption = caption_match.group(1) if caption_match else ""
        
        # Remove caption from tabular content
        table_content = re.sub(r'\\caption\{[^}]+\}\\\\', '', table_content)
        
        # Wrap in table float
        if caption:
            return f"\\begin{{table}}[ht]\n\\centering\n{table_content}\n\\caption{{{caption}}}\n\\end{{table}}"
        else:
            return table_content
    
    # Fix tables with captions - more comprehensive approach
    # First fix the table environment that already has \begin{table}
    content = re.sub(
        r'(\\begin\{table\}\[ht\]\n\\centering\n\\begin\{tabular\}[^}]*\}).*?(\\caption\{[^}]+\}\\\\)(.*?)(\\end\{tabular\}\n\\caption\{[^}]+\}\n\\end\{table\})',
        lambda m: f"{m.group(1)}\n{m.group(3)}\n\\end{{tabular}}\n{m.group(2).replace('\\\\', '')}\n\\end{{table}}",
        content,
        flags=re.DOTALL
    )
    
    # Clean up any remaining duplicate headers and footers in tables
    content = re.sub(r'\\toprule\nID & Model \\\\\n\\midrule\n\n\\toprule\nID & Model \\\\\n\\midrule\n\n\\bottomrule\n\n', r'\\toprule\nID & Model \\\\\n\\midrule\n', content)
    
    # Fix any remaining standalone tabular with captions
    content = re.sub(
        r'\\begin\{tabular\}[^}]*\}.*?\\caption\{[^}]+\}.*?\\end\{tabular\}',
        fix_table,
        content,
        flags=re.DOTALL
    )
    
    dest.write_text(content, encoding="utf-8")
    print(f"Created cleaned TeX: {dest}")


def parse_args(argv: list[str] | None = None):
    ap = argparse.ArgumentParser(description="Remove unicode-math / fontspec lines from TeX file.")
    ap.add_argument("tex_file", type=pathlib.Path, help="Original .tex file")
    ap.add_argument("-o", "--output", type=pathlib.Path,
                    help="Output .tex file (default: <stem>_arxiv.tex)")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None):
    args = parse_args(argv)
    if not args.tex_file.exists():
        sys.exit(f"File {args.tex_file} not found")
    output = args.output or args.tex_file.with_stem(args.tex_file.stem + "_arxiv")
    patch_file(args.tex_file, output)


if __name__ == "__main__":
    main() 