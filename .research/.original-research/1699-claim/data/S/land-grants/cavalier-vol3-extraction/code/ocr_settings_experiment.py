#!/usr/bin/env python3
"""ocr_settings_experiment.py

Run multiple OCRmyPDF passes on a *sample* of pages from a single PDF to
benchmark various OEM/PSM settings.

Example
-------
python ocr_settings_experiment.py \
    --input-pdf "book10.pdf" \
    --pages 5 \
    --oem-list 3,1 \
    --psm-list 6,4,3 \
    --output-dir ./OCR-experiments

The script will produce:
    OCR-experiments/
        oem3_psm6.pdf
        oem3_psm6.txt
        oem3_psm4.pdf
        ...
    summary_stats.csv   # statistics comparing textual output across settings

Metrics captured
----------------
* characters – total character count of OCR sidecar
* words       – whitespace-separated word count
* unique_words– unique word count (case-insensitive)
* lines       – number of non-empty lines

You can sort the CSV or open it in a spreadsheet to choose the best combo.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from itertools import product
from pathlib import Path
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def run_cmd(cmd: List[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        logger.error(proc.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")


def ocr_sample(
    input_pdf: Path,
    out_pdf: Path,
    sidecar: Path,
    pages: int,
    oem: int,
    psm: int,
) -> None:
    cmd = [
        "ocrmypdf",
        "--pages",
        f"1-{pages}",
        "--rotate-pages",
        "--deskew",
        "--force-ocr",
        "--tesseract-oem",
        str(oem),
        "--tesseract-pagesegmode",
        str(psm),
        "--language",
        "eng",
        "--tesseract-config",
        "preserve_interword_spaces=1",
        "--sidecar",
        str(sidecar),
        str(input_pdf),
        str(out_pdf),
    ]
    logger.info("OCR (%s) → %s", sidecar.stem, out_pdf.name)
    run_cmd(cmd)


def compute_stats(text: str) -> dict[str, int]:
    words = [w for w in text.split() if w]
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return {
        "characters": len(text),
        "words": len(words),
        "unique_words": len(set(w.lower() for w in words)),
        "lines": len(lines),
    }


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="OCR parameter benchmarking tool")
    parser.add_argument("--input-pdf", type=Path, required=True, help="Path to a single input PDF")
    parser.add_argument("--pages", type=int, default=5, help="Number of initial pages to OCR for testing")
    parser.add_argument("--oem-list", type=str, default="3", help="Comma-separated OEM values (e.g., '3,1')")
    parser.add_argument("--psm-list", type=str, default="6", help="Comma-separated PSM values (e.g., '6,4,3')")
    parser.add_argument("--output-dir", type=Path, default=Path("./OCR-experiments"))
    args = parser.parse_args(argv)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    oem_vals = [int(x) for x in args.oem_list.split(",") if x.strip()]
    psm_vals = [int(x) for x in args.psm_list.split(",") if x.strip()]

    results: list[dict[str, int | str]] = []

    for oem, psm in product(oem_vals, psm_vals):
        label = f"oem{oem}_psm{psm}"
        out_pdf = args.output_dir / f"{label}.pdf"
        sidecar = args.output_dir / f"{label}.txt"

        if not sidecar.exists():
            ocr_sample(args.input_pdf, out_pdf, sidecar, args.pages, oem, psm)
        else:
            logger.info("[skip] %s exists", sidecar.name)

        text = sidecar.read_text(encoding="utf-8", errors="ignore")
        stats = compute_stats(text)
        stats.update({"label": label, "oem": oem, "psm": psm})
        results.append(stats)

    df = pd.DataFrame(results)
    csv_path = args.output_dir / "summary_stats.csv"
    df.sort_values(["characters"], ascending=False).to_csv(csv_path, index=False)
    logger.info("Summary stats written → %s", csv_path)
    print(csv_path)


if __name__ == "__main__":
    main() 