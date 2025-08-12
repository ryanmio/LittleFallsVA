### Cavaliers & Pioneers (and related) PDF → Parsed CSV (Geolocation-ready)

This is the finalized, working pipeline we used in this repo to convert scanned PDFs into structured CSVs ready for downstream geolocation. It reflects only the steps and scripts we actually used successfully.

We assume you are working in this same repo; no environment setup or external prereqs are described here.

---

### Step 0 — Prepare a new volume/workspace and copy the working code
Example new volume: `cavalier-northern-neck-1`

- Create the directory tree and copy the finalized scripts we used for Volume 2:

```bash
mkdir -p \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/pdf-scans" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-output" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/extracted_entries" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/combined" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/code"

# Copy scripts from the working Volume 2 pipeline
cp \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/code/ocr_and_extract_volume2.py" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/code/ocr_settings_experiment.py" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/code/extract_book.py" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-vol2-extraction/code/cp_extract_volume2.py" \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/code/"
```

- Open `cavalier-northern-neck-1/code/ocr_and_extract_volume2.py` and update these constants to point at the new volume paths:
  - `DEFAULT_INPUT_DIR` → `.../cavalier-northern-neck-1/pdf-scans`
  - `DEFAULT_OUTPUT_DIR` → `.../cavalier-northern-neck-1/OCR-output`
  - `DEFAULT_VOLUME_NAME` → a suitable stem (e.g., `nn1`)
  - `DEFAULT_PROCESSING_ORDER` → exact PDF filenames in the order you want processed

- (Optional) If you want a separate parser name, copy `cp_extract_volume2.py` to `cp_extract_current_volume.py` and use that filename below.

---

### Step 1 — Place the scanned PDFs
Put all scanned PDFs under:
```
/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/pdf-scans
```
Name files clearly if split (e.g., `book6pt1.pdf`, `book6pt2.pdf`, etc.) and reflect that in `DEFAULT_PROCESSING_ORDER`.

---

### Step 2 — (Optional) OCR settings experiment (sample pages)
Use a representative PDF to compare OEM/PSM (we used OEM 3 / PSM 3):

```bash
python \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/code/ocr_settings_experiment.py" \
  --input-pdf \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/pdf-scans/one_book.pdf" \
  --pages 6 \
  --oem-list 3 \
  --psm-list 3,4,6 \
  --output-dir \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-experiments"
```

---

### Step 3 — OCR all PDFs to sidecar text and merge at volume level
`ocr_and_extract_volume2.py` will:
- OCR each PDF to sidecar `*_ocr.txt`
- Concatenate to `<volume>_ocr.txt`
- Clean to `<volume>_clean.txt`
- Extract coarse “grant blobs” to `grant_blobs_<volume>.csv` (one column `raw_entry`)

Run:
```bash
python \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/code/ocr_and_extract_volume2.py" \
  --log-level INFO > \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-output/run.log" 2>&1
```

Key outputs:
- `OCR-output/<volume>_ocr.txt`
- `OCR-output/<volume>_clean.txt`
- `OCR-output/grant_blobs_<volume>.csv`

You can tail the log for progress:
```bash
tail -f \
"/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-output/run.log"
```

---

### Step 4 — Merge per-book OCR parts (only if a book is split)
If a book was scanned as parts, create merged per-book OCR text (examples from Volume 2):
- `book6_ocr.txt` = `book6pt1_ocr.txt + book6pt2_ocr.txt + book6pt3_ocr.txt`
- `book7_ocr.txt` = `book7pt1_ocr.txt + book7p2_ocr.txt`

For the new volume, adjust book names/parts accordingly and write the merged outputs into:
```
/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-output
```

---

### Step 5 — Extract structured per-book rows (volume, book, raw_entry)
Use the per-book extractor to emit `bookX_raw.csv` with schema `volume,book,raw_entry`:

```bash
python \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/code/extract_book.py" \
  --input \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/OCR-output/book6_ocr.txt" \
  --book 6 \
  --output-dir \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/extracted_entries"
```
Repeat for each book in the new volume.

---

### Step 6 — Combine per-book raw CSVs
```bash
python - << 'PY'
import pandas as pd, os
base = "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1"
ind = os.path.join(base, "extracted_entries")
books = [6,7,8]  # update for your volume
paths = [os.path.join(ind, f"book{b}_raw.csv") for b in books]
dfs = [pd.read_csv(p) for p in paths if os.path.exists(p)]
combined = pd.concat(dfs, ignore_index=True)
out = os.path.join(base, "combined", "books_combined.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
combined.to_csv(out, index=False)
print(out)
PY
```

Output:
- `combined/books_combined.csv` (schema: `volume,book,raw_entry`)

---

### Step 7 — Parse to cp_grants-style CSV (geolocation-ready)
Use the copied parser (`cp_extract_volume2.py`, or rename to `cp_extract_current_volume.py`). It produces:
- Schema: `grant_id,name_std,acreage,year,county_text,raw_entry`
- Output under `combined/`

```bash
python \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/code/cp_extract_volume2.py" \
  --input  \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/combined/books_combined.csv" \
  --output \
  "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/cavalier-northern-neck-1/combined/cp_grants_nn1.csv"
```

Notes on parsing heuristics (already built into the copied parser):
- Robust county token regex (`Co/Cnty/County/City/Citty`), city synonyms for `Elizabeth City`, `James City`, `Charles City`
- “Par./Parish of X” (with Upper/Lower prefixes) → county X
- Directional “S./N. side of <County> Co.” → county X
- Extensive abbreviation map for common OCR variants (Rappahannock, Nansemond, Northumberland, Westmoreland, Northampton, Henrico, Isle of Wight, etc.)
- Avoid generic “of X” person-origin phrases

This sequence mirrors what we finalized for Volume 2 and is intended as a reliable template for new books/volumes in this repo.
