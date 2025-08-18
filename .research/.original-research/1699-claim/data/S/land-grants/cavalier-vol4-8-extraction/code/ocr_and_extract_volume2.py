#!/usr/bin/env python3
"""ocr_and_extract_volume2.py

Batch-OCR, clean, and extract raw land-grant entries from Cavaliers & Pioneers, Volume 2.

The script completes four phases:

1. OCR – Iterate through every PDF in the *input* directory and run OCRmyPDF
   using the same flags adopted for Volume 3. Each scanned PDF will emit two
   artefacts next to the *output* directory:

   ├─ <stem>_ocr.pdf  – searchable PDF/A
   └─ <stem>_ocr.txt  – plain-text side-car produced by `--sidecar`

2. Merge – Concatenate all OCR side-cars (retaining form-feeds) and merge the
   searchable PDFs into a single file called ``volume2_ocr.(pdf|txt)`` so that
   downstream parcels have a single canonical source.

3. Clean – Strip page headers & footer cruft, de-hyphenate line-breaks, and
   write the cleaned corpus to ``volume2_clean.txt``.

4. Extract – Apply a coarse regex that isolates *grant blobs* (one row per
   original entry) and emit them to ``grant_blobs_volume2.csv`` with exactly one
   column called ``raw_entry``.

CLI Usage
---------
Minimal invocation (will use default constants defined below)::

    python ocr_and_extract_volume2.py

Optional overrides::

    python ocr_and_extract_volume2.py \
        --input-dir  /path/to/pdf_scans \
        --output-dir /path/to/OCR-output \
        --volume-name volume2

Dependencies (see requirements.txt)
-----------------------------------
* OCRmyPDF ≥ 15
* pandas
* pypdf (the modern fork of PyPDF2)
* tqdm (nice but optional progress-bar)

Make sure `tesseract` with language packs ``eng`` and ``lat`` is available in
$PATH.
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

import pandas as pd
from pypdf import PdfMerger

try:
    from tqdm import tqdm  # type: ignore

    TQDM = tqdm
except ImportError:  # pragma: no cover – `tqdm` is optional
    def _tqdm(iterable, **kwargs):  # type: ignore
        return iterable

    TQDM = _tqdm  # type: ignore

# -----------------------------------------------------------------------------
# Configurable constants – adjust here or via CLI arguments
# -----------------------------------------------------------------------------
DEFAULT_INPUT_DIR = Path(
    "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol4-8-extraction/pdf-scans"
)
DEFAULT_OUTPUT_DIR = Path(
    "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol4-8-extraction/OCR-output"
)
DEFAULT_VOLUME_NAME = "vol4_8"
DEFAULT_PSM = 3
DEFAULT_OEM = 3
DEFAULT_PROCESSING_ORDER = [
    # Update this order after you place PDFs into pdf-scans/
]

# OCRmyPDF parameters mirroring the Volume 3 pipeline
OCR_ARGS = [
    "ocrmypdf",
    "--rotate-pages",
    "--deskew",
    "--tesseract-oem",
    str(DEFAULT_OEM),
    "--tesseract-pagesegmode", 
    str(DEFAULT_PSM),
    "--language",
    "eng",
    "--tesseract-config",
    "preserve_interword_spaces=1",
    "-v",
    "1",
    "--output-type",
    "none",
]
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def run_cmd(cmd: List[str]) -> None:
    """Run *cmd* inheriting parent stdout/stderr so logs stream to run.log."""
    logger.info("RUN: %s", " ".join(cmd))
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {proc.returncode}: {' '.join(cmd)}")


def ocr_single_pdf(pdf_path: Path, output_dir: Path) -> tuple[Path, Path]:
    """OCR *pdf_path* → returns (ocr_pdf, sidecar_txt)."""
    # We still define output_pdf for compatibility, but it won't be created
    output_pdf = output_dir / f"{pdf_path.stem}_ocr.pdf"
    sidecar_txt = output_dir / f"{pdf_path.stem}_ocr.txt"

    if sidecar_txt.exists():
        logger.info("[skip] %s already OCR'd", pdf_path.name)
        return output_pdf, sidecar_txt

    # Use '-' as output target with --output-type none; ocrmypdf will not write a PDF
    cmd = OCR_ARGS + ["--sidecar", str(sidecar_txt), str(pdf_path), "-"]
    logger.info("OCRing %s for text extraction only", pdf_path.name)
    run_cmd(cmd)
    logger.info("Finished OCR %s", pdf_path.name)
    return output_pdf, sidecar_txt


def concat_files(text_paths: List[Path], dest: Path) -> None:
    """Concatenate *text_paths* into *dest* separated by a single form-feed."""
    logger.info("Concatenating %d text files → %s", len(text_paths), dest)
    with dest.open("w", encoding="utf-8") as out_fp:
        for idx, p in enumerate(text_paths):
            out_fp.write(p.read_text(encoding="utf-8"))
            if idx != len(text_paths) - 1:
                out_fp.write("\f\n")  # ensure page break between source docs


def merge_pdfs(pdf_paths: List[Path], dest: Path) -> None:
    """Merge *pdf_paths* in order → *dest*."""
    logger.info("Merging %d searchable PDFs → %s", len(pdf_paths), dest)
    merger = PdfMerger()
    for p in pdf_paths:
        merger.append(str(p))
    merger.write(str(dest))
    merger.close()


def clean_text(raw_text: str) -> str:
    """Apply header stripping, hyphen de-merging, etc."""
    pages = raw_text.split("\f")
    cleaned_pages: List[str] = []
    header_pat = re.compile(r"^Patent Book|^\s*\d+\s*$", re.M)

    for page in pages:
        lines = page.splitlines()
        if len(lines) >= 2:
            lines = lines[2:]  # drop running header & following blank/page number line
        # Remove residual header/footer lines
        lines = [ln for ln in lines if not header_pat.match(ln)]
        cleaned_pages.append("\n".join(lines))

    cleaned_text = "\f".join(cleaned_pages)
    # Merge hyphenated line-breaks
    cleaned_text = re.sub(r"-\n\s*", "", cleaned_text)
    return cleaned_text


def extract_grant_blobs(clean_text_str: str) -> List[str]:
    pattern = re.compile(r"^[A-Z][A-Z\s\.\-]+?,.*?(?=\n[A-Z][A-Z\s\.\-]+?,|\Z)", re.S | re.M)
    matches = pattern.findall(clean_text_str)
    return [m.strip() for m in matches if m.strip()]


# -----------------------------------------------------------------------------
# Core routine
# -----------------------------------------------------------------------------

def process_volume(
    input_dir: Path, output_dir: Path, volume_name: str = DEFAULT_VOLUME_NAME
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {input_dir}")

    order_rank = {name: idx for idx, name in enumerate(DEFAULT_PROCESSING_ORDER)}
    pdf_files.sort(key=lambda p: (order_rank.get(p.name, len(order_rank)), p.name))
    logger.info("Processing order: %s", ", ".join(p.name for p in pdf_files))

    sidecars: List[Path] = []

    for pdf_path in TQDM(pdf_files, desc="OCR PDFs"):
        _, sidecar = ocr_single_pdf(pdf_path, output_dir)
        sidecars.append(sidecar)

    # Merge outputs
    volume_txt = output_dir / f"{volume_name}_ocr.txt"

    concat_files(sidecars, volume_txt)
    
    # No more PDF merging
    logger.info("Skipped PDF generation to focus on text extraction")

    # Clean text
    raw_text = volume_txt.read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)
    clean_txt_path = output_dir / f"{volume_name}_clean.txt"
    clean_txt_path.write_text(cleaned_text, encoding="utf-8")
    logger.info("Wrote cleaned text → %s", clean_txt_path)

    # Extract grant blobs
    blobs = extract_grant_blobs(cleaned_text)
    df = pd.DataFrame({"raw_entry": blobs})
    csv_path = output_dir / f"grant_blobs_{volume_name}.csv"
    df.to_csv(csv_path, index=False)
    logger.info("CSV with %d grant entries written → %s", len(blobs), csv_path)

    return csv_path


# -----------------------------------------------------------------------------
# Entry-point
# -----------------------------------------------------------------------------

def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OCR & grant-entry extractor for Cavaliers & Pioneers (Volume workspace)")
    p.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR, help="Directory containing input PDFs")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for OCR artefacts")
    p.add_argument("--volume-name", type=str, default=DEFAULT_VOLUME_NAME, help="Stem used for merged artefacts")
    p.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    logging.getLogger().setLevel(args.log_level)

    try:
        csv_path = process_volume(args.input_dir, args.output_dir, args.volume_name)
        print(csv_path)
    except Exception as exc:
        logger.error("Processing failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main() 