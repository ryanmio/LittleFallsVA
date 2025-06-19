import argparse
import shutil
from pathlib import Path
import filecmp
import sys


###############################################################################
# Configuration                                                               #
###############################################################################
# Edit the mappings below to control which source folders / files are synced  #
# into which destination locations. All paths should be absolute OR relative  #
# to the user's home directory (prefix with ~).                                #
#                                                                             #
# Each mapping is a dict with:                                                 #
#   type:   "dir"   – copy *entire* directory subtree                         #
#           "files" – copy only specific files listed in "items"              #
#   src:    source directory (str)                                            #
#   dest:   destination directory (str)                                       #
#   items:  (only for type=="files") list[str] – filenames to copy            #
###############################################################################

DEFAULT_MAPPINGS = [
    {
        "type": "dir",
        "src": "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/analysis",
        "dest": "/Users/ryanmioduskiimac/Downloads/colonial-virginia-llm-geolocation/data/analysis",
    },
    {
        "type": "files",
        "src": "/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/paper",
        "dest": "/Users/ryanmioduskiimac/Downloads/colonial-virginia-llm-geolocation/paper",
        "items": [
            "main.md",
            "Journal of Spatial Information Science template",
            "josisacm.bst",
            "josis.cls",
            "github_link.tex",
            "code_style.tex",
            "refs.bib",
            "build.sh",
            "apa.csl",
            "math_fix.tex",
        ],
    },
]

###############################################################################
# Helper functions                                                            #
###############################################################################

def _expand(path: str) -> Path:
    """Return a resolved Path, expanding ~ and making parents if needed."""
    p = Path(path).expanduser().resolve()
    return p


def _copy_file(src: Path, dest: Path, verbose: bool = True):
    """Copy one file if it differs in size or mtime."""
    if dest.exists() and filecmp.cmp(src, dest, shallow=False):
        if verbose:
            print(f"  [skip] {dest.relative_to(dest.parent.parent)} (up-to-date)")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    if verbose:
        print(f"  [copy] {src} -> {dest}")


def _sync_dir(src_dir: Path, dest_dir: Path, verbose: bool = True):
    """Recursively copy directory contents preserving structure."""
    if not src_dir.exists():
        print(f"[warn] Source directory {src_dir} does not exist – skipped.", file=sys.stderr)
        return

    for src in src_dir.rglob('*'):
        if src.is_dir():
            continue
        rel_path = src.relative_to(src_dir)
        dest = dest_dir / rel_path
        _copy_file(src, dest, verbose)


def _sync_selected_files(src_dir: Path, dest_dir: Path, items: list[str], verbose: bool = True):
    for name in items:
        src = src_dir / name
        dest = dest_dir / name
        if not src.exists():
            print(f"[warn] File or directory {src} not found – skipped.", file=sys.stderr)
            continue
        if src.is_dir():
            # Recursively copy directory
            for sub_src in src.rglob('*'):
                if sub_src.is_dir():
                    continue
                rel_path = sub_src.relative_to(src_dir)
                sub_dest = dest_dir / rel_path
                _copy_file(sub_src, sub_dest, verbose)
        else:
            _copy_file(src, dest, verbose)

###############################################################################
# Main logic                                                                  #
###############################################################################

def run_sync(mappings, dry_run: bool = False, verbose: bool = True):
    for mapping in mappings:
        mtype = mapping['type']
        src = _expand(mapping['src'])
        dest = _expand(mapping['dest'])

        if verbose:
            print(f"Syncing {mtype}:\n  src:  {src}\n  dest: {dest}")
        if dry_run:
            print("  [dry-run] No files will be copied.")
            continue

        if mtype == 'dir':
            _sync_dir(src, dest, verbose)
        elif mtype == 'files':
            items = mapping.get('items', [])
            _sync_selected_files(src, dest, items, verbose)
        else:
            print(f"[error] Unknown mapping type: {mtype}", file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(description="One-way sync selected directories & files from private research repo to public repository.")
    parser.add_argument('--config', type=str, help='Path to alternate JSON/YAML config defining mappings.')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be copied without making changes.')
    parser.add_argument('--quiet', action='store_true', help='Reduce logging output.')
    return parser.parse_args()


def main():
    args = parse_args()

    # Future: load external config here if supplied.
    mappings = DEFAULT_MAPPINGS

    run_sync(mappings, dry_run=args.dry_run, verbose=not args.quiet)


if __name__ == '__main__':
    main() 