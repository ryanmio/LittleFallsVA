#!/usr/bin/env python3
"""ocr_and_extract_gray_nn.py

OCR, clean, and extract raw land-grant entries from Gray's Northern Neck volume
(parts: nn_gray_pt1.pdf, nn_gray_pt2.pdf, nn_gray_pt3.pdf).

Special handling:
- Skip first 8 pages of pt1 (front matter)
- Only keep pages 1–27 of pt3 (exclude index)

Emits:
- <volume>_ocr.txt, <volume>_clean.txt in OCR-output/
- grant_blobs_<volume>.csv in OCR-output/
"""

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from pypdf import PdfReader, PdfWriter

try:
    from tqdm import tqdm  # type: ignore
    TQDM = tqdm
except Exception:  # pragma: no cover
    def _tqdm(it, **kw):
        return it
    TQDM = _tqdm  # type: ignore

# Defaults for Gray volume
BASE_DIR = Path("/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/gray-northern-neck")
DEFAULT_INPUT_DIR = BASE_DIR / "pdf-scans"
DEFAULT_OUTPUT_DIR = BASE_DIR / "OCR-output"
DEFAULT_VOLUME_NAME = "gray_nn"
DEFAULT_PSM = 3
DEFAULT_OEM = 3
DEFAULT_PROCESSING_ORDER = [
    "nn_gray_pt1.pdf",
    "nn_gray_pt2.pdf",
    "nn_gray_pt3.pdf",
]

# Per-file page ranges to include (1-based, inclusive). None means all pages.
PAGE_INCLUDES = {
    "nn_gray_pt1.pdf": (9, None),  # skip first 8 pages
    "nn_gray_pt2.pdf": (1, None),
    "nn_gray_pt3.pdf": (1, 27),    # only first 27 pages
}

OCR_ARGS_BASE = [
    "ocrmypdf",
    "--rotate-pages",
    "--deskew",
    "--tesseract-oem", str(DEFAULT_OEM),
    "--tesseract-pagesegmode", str(DEFAULT_PSM),
    "--language", "eng",
    "--tesseract-config", "preserve_interword_spaces=1",
    "-v", "1",
    "--output-type", "none",
]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def run_cmd(cmd: List[str]) -> None:
    logger.info("RUN: %s", " ".join(cmd))
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}")


def write_subset_pdf(src_pdf: Path, dest_pdf: Path, include: Tuple[int | None, int | None]) -> None:
    """Write a subset of pages from src_pdf to dest_pdf based on 1-based inclusive include."""
    reader = PdfReader(str(src_pdf))
    total = len(reader.pages)
    start, end = include
    if start is None:
        start = 1
    if end is None:
        end = total
    # Clamp bounds
    start = max(1, start)
    end = min(total, end)
    writer = PdfWriter()
    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])
    dest_pdf.parent.mkdir(parents=True, exist_ok=True)
    with dest_pdf.open("wb") as fp:
        writer.write(fp)


def ocr_with_page_filter(pdf_path: Path, output_dir: Path, include: Tuple[int | None, int | None]) -> Path:
    sidecar_txt = output_dir / f"{pdf_path.stem}_ocr.txt"
    if sidecar_txt.exists():
        logger.info("[skip] %s already OCR'd", pdf_path.name)
        return sidecar_txt

    # Create a subset PDF and OCR that file for reliability across ocrmypdf versions
    subset_pdf = output_dir / f"{pdf_path.stem}_subset.pdf"
    logger.info("Creating subset for %s", pdf_path.name)
    write_subset_pdf(pdf_path, subset_pdf, include)

    args = OCR_ARGS_BASE[:] + ["--sidecar", str(sidecar_txt), str(subset_pdf), "-"]
    logger.info("OCRing %s subset for text only", pdf_path.name)
    run_cmd(args)
    return sidecar_txt


def concat_files(text_paths: List[Path], dest: Path) -> None:
    logger.info("Concatenating %d text files → %s", len(text_paths), dest)
    with dest.open("w", encoding="utf-8") as out_fp:
        for idx, p in enumerate(text_paths):
            out_fp.write(p.read_text(encoding="utf-8"))
            if idx != len(text_paths) - 1:
                out_fp.write("\f\n")


def clean_text(raw_text: str) -> str:
    pages = raw_text.split("\f")
    cleaned_pages: List[str] = []
    header_pat = re.compile(r"^\s*Page\s*\d+\.?$|^\s*\d+\s*$", re.M)
    for page in pages:
        lines = page.splitlines()
        if len(lines) >= 2:
            lines = lines[2:]
        lines = [ln for ln in lines if not header_pat.match(ln)]
        cleaned_pages.append("\n".join(lines))
    cleaned_text = "\f".join(cleaned_pages)
    cleaned_text = re.sub(r"-\n\s*", "", cleaned_text)
    return cleaned_text


def extract_grant_blobs(clean_text_str: str) -> List[str]:
    paras = re.split(r"\n\s*\n", clean_text_str)
    blobs: List[str] = []
    # Gray may use long narrative; still key off months + year or county cues
    month_pat = r"Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec|Octo\."
    year_pat = r"16\d{2}|17\d{2}"
    cue = re.compile(rf"(?:\b{month_pat}\b[^\n]{{0,120}}\b{year_pat}\b)|\b(?:Co\.|Cnty|County|City|Citty)\b", re.IGNORECASE)
    for para in paras:
        p = para.strip()
        if len(p) < 50:
            continue
        if cue.search(p):
            blobs.append(p)
    return blobs


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
        include = PAGE_INCLUDES.get(pdf_path.name, (1, None))
        sidecar = ocr_with_page_filter(pdf_path, output_dir, include)
        sidecars.append(sidecar)

    volume_txt = output_dir / f"{volume_name}_ocr.txt"
    concat_files(sidecars, volume_txt)

    raw_text = volume_txt.read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)
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
    p = argparse.ArgumentParser(description="OCR & grant-entry extractor for Gray Northern Neck volume")
    p.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    p.add_argument("--volume-name", type=str, default=DEFAULT_VOLUME_NAME)
    p.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    logging.getLogger().setLevel(args.log_level)
    try:
        out = process_volume(args.input_dir, args.output_dir, args.volume_name)
        print(out)
    except Exception as exc:
        logger.error("Processing failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
