#!/usr/bin/env python3
"""
prepare_arxiv_submission.py
---------------------------
Create a minimal tar.gz bundle of a LaTeX project for easy arXiv upload.

Example
-------
$ python scripts/prepare_arxiv_submission.py \
      .research/.original-research/1699-claim/data/S/land-grants/geolocation/paper/arXiv/main_two_column.tex

This will produce `arxiv_upload.tar.gz` alongside the main .tex file (or
at the location given with --output/-o).

The script keeps only the file types accepted by arXiv (source, style,
figures) and drops common LaTeX build artefacts (aux, log, synctex, ...).
"""
from __future__ import annotations

import argparse
import pathlib
import tarfile
import sys
from typing import Iterable

# File extensions that arXiv accepts / are usually required for compilation.
# Modify this list if your project needs additional formats (e.g., .eps).
ALLOWED_EXT = {
    ".tex",
    ".bib",
    ".bst",
    ".cls",
    ".sty",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",   # figure PDFs
    ".eps",
    ".ps",
    ".csv",
    ".tsv",
    ".txt",
    ".bbl",
}

# File name patterns or extensions that should be skipped (build artefacts)
SKIP_SUFFIX = {
    ".aux",
    ".log",
    ".fls",
    ".out",
    ".fdb_latexmk",
    ".synctex.gz",
    ".toc",
}

# Additional individual files to skip (e.g., compiled PDFs named main.pdf)
EXPLICIT_SKIP = set()  # Populated at runtime (the compiled PDF corresponding to the main .tex)


def iter_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    """Yield all regular files recursively under *root*."""
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def should_include(path: pathlib.Path) -> bool:
    """Return True if *path* should be part of the archive."""
    if path.name.startswith("."):
        # Skip hidden files (including .git/*)
        return False

    if path.suffix.lower() in SKIP_SUFFIX:
        return False

    if path in EXPLICIT_SKIP:
        return False

    # Skip map PNGs except for the two used in the paper
    if (path.suffix.lower() == ".png" and 
        "map" in path.name.lower() and 
        path.name not in ["grant_1_map.png", "grant_19_map.png"]):
        return False

    return path.suffix.lower() in ALLOWED_EXT


def build_archive(main_tex: pathlib.Path, output: pathlib.Path) -> None:
    root = main_tex.parent.resolve()
    if not output.is_absolute():
        output = root / output

    # Skip the compiled PDF with the same basename as the main .tex file
    compiled_pdf = main_tex.with_suffix(".pdf").resolve()
    EXPLICIT_SKIP.add(compiled_pdf)

    # Collect files
    files = [p for p in iter_files(root) if should_include(p)]
    if not files:
        print("[ERROR] No eligible files found. Check your filters.", file=sys.stderr)
        sys.exit(1)

    # Create tar.gz archive
    with tarfile.open(output, "w:gz") as tar:
        for f in files:
            tar.add(f, arcname=f.relative_to(root))

    print(f"Created archive: {output} (contains {len(files)} files)")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:  # type: ignore[type-arg]
    parser = argparse.ArgumentParser(description="Bundle LaTeX project for arXiv upload.")
    parser.add_argument("main_tex", type=pathlib.Path, help="Path to the main .tex file")
    parser.add_argument("-o", "--output", type=pathlib.Path, default=pathlib.Path("arxiv_upload.tar.gz"),
                        help="Name of the resulting archive (default: arxiv_upload.tar.gz)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if not args.main_tex.exists():
        print(f"[ERROR] {args.main_tex} does not exist", file=sys.stderr)
        sys.exit(1)
    if args.main_tex.suffix.lower() != ".tex":
        print("[ERROR] main_tex should be a .tex file", file=sys.stderr)
        sys.exit(1)

    build_archive(args.main_tex, args.output)


if __name__ == "__main__":
    main() 