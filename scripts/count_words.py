#!/usr/bin/env python3
"""Simple word counter script.

Usage:
    python scripts/count_words.py path/to/file.md --limit 250
    cat file.md | python scripts/count_words.py --limit 250

The script prints the total word count. If --limit is provided, it also prints
how many words are over/under the limit.

Words are separated by any whitespace. Punctuation is ignored for counting
purposes, matching common academic style guidelines.
"""
import argparse
import sys
import re
from pathlib import Path

def count_words(text: str) -> int:
    """Return number of words in *text* using a basic whitespace split."""
    # Remove Markdown/LaTeX commands braces for a slightly cleaner count.
    cleaned = re.sub(r"\\[a-zA-Z]+|\n", " ", text)  # strip simple LaTeX commands and newlines
    # Treat hyphenated expressions (foo-bar) as one word, similar to most word processors.
    words = re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", cleaned)
    return len(words)

def main() -> None:
    parser = argparse.ArgumentParser(description="Count words in a text file or stdin.")
    parser.add_argument("file", nargs="?", help="Path to the text file. If omitted, read from stdin.")
    parser.add_argument("--limit", "-l", type=int, default=None, help="Target word limit to compare against.")
    parser.add_argument("--abstract", "-a", action="store_true", help="Count only the '# Abstract' section of a Markdown file.")
    args = parser.parse_args()

    if args.file:
        text_path = Path(args.file)
        if not text_path.exists():
            print(f"Error: {text_path} does not exist.", file=sys.stderr)
            sys.exit(1)
        text = text_path.read_text(encoding="utf-8")
    else:
        # Read from stdin
        text = sys.stdin.read()

    if args.abstract:
        # Extract the Abstract section from Markdown.
        lines = text.splitlines()
        start_idx = None
        for i, line in enumerate(lines):
            if re.match(r"\s*#+\s*Abstract\b", line, re.IGNORECASE):
                start_idx = i + 1  # Skip the header line itself
                break

        if start_idx is None:
            print("Warning: '# Abstract' header not found – counting entire document.")
        else:
            end_idx = len(lines)
            for j in range(start_idx, len(lines)):
                if re.match(r"\s*#+\s+", lines[j]) and not re.match(r"\s*#+\s*Abstract\b", lines[j], re.IGNORECASE):
                    end_idx = j
                    break
            text = "\n".join(lines[start_idx:end_idx])

    total_words = count_words(text)
    print(f"Word count: {total_words}")

    if args.limit is not None:
        diff = total_words - args.limit
        if diff == 0:
            print("Exactly at the limit! ✅")
        elif diff > 0:
            print(f"Over the limit by {diff} word{'s' if diff != 1 else ''}.")
        else:
            print(f"Under the limit by {-diff} word{'s' if diff != -1 else ''}.")

if __name__ == "__main__":
    main() 