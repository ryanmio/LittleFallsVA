#!/usr/bin/env python3
"""ocr_and_extract_northerneck1.py

Batch-OCR (if needed), clean, and extract raw land-grant entries from
Cavaliers & Pioneers – Supplement: Northern Neck Grants No. 1 (1690–1692).

Phases:
  1. OCR – Iterate all PDFs in input dir and run OCRmyPDF with text sidecars
  2. Merge – Concatenate all sidecars into "<volume>_ocr.txt"
  3. Clean – Strip headers/footers, de-hyphenate → "<volume>_clean.txt"
  4. Extract – Coarse regex to isolate grant blobs → "grant_blobs_<volume>.csv"

CLI:
  python ocr_and_extract_northerneck1.py \
    --input-dir  /path/to/pdf-scans \
    --output-dir /path/to/OCR-output \
    --volume-name nn1

Requires:
  - ocrmypdf >= 15
  - pandas
  - pypdf
  - tqdm (optional)
  - tesseract with 'eng' (and optionally 'lat')
"""

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import List

import pandas as pd

try:
    from tqdm import tqdm  # type: ignore

    TQDM = tqdm
except ImportError:  # pragma: no cover – `tqdm` is optional
    def _tqdm(iterable, **kwargs):  # type: ignore
        return iterable

    TQDM = _tqdm  # type: ignore

# -----------------------------------------------------------------------------
# Configurable constants – NN1 defaults
# -----------------------------------------------------------------------------
DEFAULT_INPUT_DIR = Path(
    "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/pdf-scans"
)
DEFAULT_OUTPUT_DIR = Path(
    "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-output"
)
DEFAULT_VOLUME_NAME = "nn1"
DEFAULT_PSM = 3
DEFAULT_OEM = 3
DEFAULT_PROCESSING_ORDER = [
    "nn_supp.pdf",
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
# Helpers
# -----------------------------------------------------------------------------

def run_cmd(cmd: List[str]) -> None:
    logger.info("RUN: %s", " ".join(cmd))
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {proc.returncode}: {' '.join(cmd)}"
        )


def ocr_single_pdf(pdf_path: Path, output_dir: Path) -> Path:
    """OCR pdf_path → returns sidecar_txt path (no PDF produced)."""
    sidecar_txt = output_dir / f"{pdf_path.stem}_ocr.txt"
    if sidecar_txt.exists():
        logger.info("[skip] %s already OCR'd", pdf_path.name)
        return sidecar_txt

    cmd = OCR_ARGS + ["--sidecar", str(sidecar_txt), str(pdf_path), "-"]
    logger.info("OCRing %s for text extraction only", pdf_path.name)
    run_cmd(cmd)
    logger.info("Finished OCR %s", pdf_path.name)
    return sidecar_txt


def concat_files(text_paths: List[Path], dest: Path) -> None:
    logger.info("Concatenating %d text files → %s", len(text_paths), dest)
    with dest.open("w", encoding="utf-8") as out_fp:
        for idx, p in enumerate(text_paths):
            out_fp.write(p.read_text(encoding="utf-8"))
            if idx != len(text_paths) - 1:
                out_fp.write("\f\n")  # page break between source docs


def clean_text(raw_text: str) -> str:
    pages = raw_text.split("\f")
    cleaned_pages: List[str] = []
    header_pat = re.compile(r"^CAVALIERS AND PIONEERS|^Abstracts of|^SUPPLEMENT$|^\s*Page\s*\d+\.?$|^\s*\d+\s*$", re.M)

    for page in pages:
        lines = page.splitlines()
        if len(lines) >= 2:
            lines = lines[2:]  # drop running header & next line/page number
        lines = [ln for ln in lines if not header_pat.match(ln)]
        cleaned_pages.append("\n".join(lines))

    cleaned_text = "\f".join(cleaned_pages)
    cleaned_text = re.sub(r"-\n\s*", "", cleaned_text)
    return cleaned_text


def find_abstracts_start_nn1(text: str) -> int:
    """Locate the start of the Northern Neck abstracts section."""
    m = re.search(r"NORTHERN\s+NECK\s+BOOK\b.*", text, re.IGNORECASE)
    if m:
        return m.start()
    m2 = re.search(r"The following is an abstract of one-half of", text, re.IGNORECASE)
    if m2:
        return m2.start()
    return 0


def extract_grant_blobs(clean_text_str: str) -> List[str]:
    # Use paragraphs that contain a month token and a 1690–1692 year
    paras = re.split(r"\n\s*\n", clean_text_str)
    blobs: List[str] = []
    month_pat = r"Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec|Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.|Octo\."
    year_pat = r"169[0-2]"
    pat = re.compile(rf"\b(?:{month_pat})\b[^\n]{{0,120}}\b{year_pat}\b", re.IGNORECASE)
    for para in paras:
        p = para.strip()
        if len(p) < 50:
            continue
        if pat.search(p):
            blobs.append(p)
    return blobs


# -----------------------------------------------------------------------------
# Core
# -----------------------------------------------------------------------------

def process_volume(input_dir: Path, output_dir: Path, volume_name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {input_dir}")

    order_rank = {name: idx for idx, name in enumerate(DEFAULT_PROCESSING_ORDER)}
    pdf_files.sort(key=lambda p: (order_rank.get(p.name, len(order_rank)), p.name))
    logger.info("Processing order: %s", ", ".join(p.name for p in pdf_files))

    sidecars: List[Path] = []
    for pdf_path in TQDM(pdf_files, desc="OCR PDFs"):
        sidecar = ocr_single_pdf(pdf_path, output_dir)
        sidecars.append(sidecar)

    volume_txt = output_dir / f"{volume_name}_ocr.txt"
    concat_files(sidecars, volume_txt)

    raw_text = volume_txt.read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)

    # Trim to the abstracts section to avoid preface/index noise
    start_idx = find_abstracts_start_nn1(cleaned_text)
    if start_idx > 0:
        cleaned_text = cleaned_text[start_idx:]

    clean_txt_path = output_dir / f"{volume_name}_clean.txt"
    clean_txt_path.write_text(cleaned_text, encoding="utf-8")
    logger.info("Wrote cleaned text → %s", clean_txt_path)

    blobs = extract_grant_blobs(cleaned_text)
    df = pd.DataFrame({"raw_entry": blobs})
    csv_path = output_dir / f"grant_blobs_{volume_name}.csv"
    df.to_csv(csv_path, index=False)
    logger.info("CSV with %d grant entries written → %s", len(blobs), csv_path)

    return csv_path


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OCR & grant-entry extractor for C&P Northern Neck Supplement")
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
