#!/usr/bin/env python3
"""process_single_pdf.py

Process a single PDF file at a time from the Cavaliers & Pioneers collection.
Performs OCR text extraction using Tesseract with configured parameters.

Usage:
    python process_single_pdf.py --input-pdf "../pdf scans/book9part1.pdf" --output-dir "../OCR-output"
"""

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# OCR settings
DEFAULT_PSM = 3  # Page segmentation mode: 3 = fully automatic page segmentation
DEFAULT_OEM = 3  # OCR Engine mode: 3 = default, based on what is available

# OCRmyPDF command line arguments
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
    "--output-type",
    "none",
]

def run_ocr(input_pdf: Path, output_dir: Path) -> Path:
    """Run OCR on a single PDF and return path to text output."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define output paths
    sidecar_txt = output_dir / f"{input_pdf.stem}_ocr.txt"
    
    if sidecar_txt.exists():
        logger.info("[skip] %s already OCR'd", input_pdf.name)
        return sidecar_txt
    
    # Construct OCR command
    cmd = OCR_ARGS + ["--sidecar", str(sidecar_txt), str(input_pdf), "-"]
    
    # Run OCR with progress reporting
    logger.info("Processing %s...", input_pdf.name)
    
    start_time = time.time()
    process = None
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Set up progress bar if tqdm is available
        if HAS_TQDM:
            pbar = tqdm(total=100, desc=f"OCR {input_pdf.name}", unit="%")
            last_progress = 0
        
        # Check process output for progress info
        while process.poll() is None:
            # Read any available stderr output
            line = process.stderr.readline()
            if line:
                # Look for progress information
                if "Progress: " in line:
                    try:
                        progress = int(line.split("Progress: ")[1].split("%")[0])
                        if HAS_TQDM and progress > last_progress:
                            pbar.update(progress - last_progress)
                            last_progress = progress
                        else:
                            elapsed = time.time() - start_time
                            eta = (elapsed / max(1, progress)) * (100 - progress) if progress > 0 else "unknown"
                            eta_str = f"{eta:.1f}s" if isinstance(eta, float) else eta
                            sys.stdout.write(f"\rProgress: {progress}% (ETA: {eta_str})")
                            sys.stdout.flush()
                    except (ValueError, IndexError):
                        pass
                
                # Log any warnings/errors
                if "error" in line.lower() or "warning" in line.lower():
                    logger.warning(line.strip())
            
            # Small sleep to prevent CPU thrashing
            time.sleep(0.1)
        
        # Close progress bar
        if HAS_TQDM:
            pbar.close()
        else:
            sys.stdout.write("\n")
            
        # Check return code
        if process.returncode != 0:
            stderr_output = process.stderr.read()
            logger.error("OCR failed: %s", stderr_output)
            raise RuntimeError(f"OCR failed for {input_pdf.name}")
            
        elapsed = time.time() - start_time
        logger.info("OCR completed successfully in %.1f seconds → %s", elapsed, sidecar_txt)
        return sidecar_txt
        
    except Exception as e:
        logger.error("Error processing %s: %s", input_pdf.name, e)
        raise
    finally:
        # Ensure process is terminated if exception occurs
        if process and process.poll() is None:
            process.terminate()

def main():
    parser = argparse.ArgumentParser(description="Process a single PDF file from Cavaliers & Pioneers")
    parser.add_argument("--input-pdf", type=Path, required=True, help="Path to input PDF file")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for OCR output")
    parser.add_argument("--psm", type=int, default=DEFAULT_PSM, help="Tesseract Page Segmentation Mode")
    parser.add_argument("--oem", type=int, default=DEFAULT_OEM, help="Tesseract OCR Engine Mode")
    parser.add_argument("--log-level", type=str, default="INFO", 
                       choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    
    args = parser.parse_args()
    logging.getLogger().setLevel(args.log_level)
    
    # Update OCR args with custom PSM/OEM if provided
    if args.psm != DEFAULT_PSM:
        OCR_ARGS[OCR_ARGS.index("--tesseract-pagesegmode") + 1] = str(args.psm)
    if args.oem != DEFAULT_OEM:
        OCR_ARGS[OCR_ARGS.index("--tesseract-oem") + 1] = str(args.oem)
    
    try:
        output_txt = run_ocr(args.input_pdf, args.output_dir)
        print(f"OCR text output: {output_txt}")
        
        # Show first few lines of OCR output to verify quality
        try:
            with open(output_txt, 'r', encoding='utf-8') as f:
                print("\nFirst 10 lines of OCR output:")
                print("-" * 40)
                for i, line in enumerate(f):
                    if i >= 10:
                        break
                    print(line.rstrip())
                print("-" * 40)
        except Exception as e:
            logger.error("Could not read OCR output: %s", e)
    
    except Exception as exc:
        logger.error("Processing failed: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main() 