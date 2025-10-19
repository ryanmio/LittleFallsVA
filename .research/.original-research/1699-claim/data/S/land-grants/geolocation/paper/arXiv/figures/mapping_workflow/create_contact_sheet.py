"""create_contact_sheet.py - Create a grid of all grant maps as a single large image

Usage:
  python create_contact_sheet.py [--rows ROWS] [--cols COLS] [--output OUTPUT]

This script arranges all the map PNGs from map_outputs into a grid contact sheet.
"""
import os
import sys
import argparse
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

# Paths
THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "map_outputs"


def parse_args():
    parser = argparse.ArgumentParser(description='Create a contact sheet from grant maps')
    parser.add_argument('--rows', type=int, help='Number of rows (default: auto-calculated)')
    parser.add_argument('--cols', type=int, help='Number of columns (default: auto-calculated)')
    parser.add_argument('--output', type=str, default='contact_sheet.png',
                      help='Output filename (default: contact_sheet.png)')
    parser.add_argument('--thumb-size', type=int, default=600,
                      help='Thumbnail size in pixels (default: 600)')
    parser.add_argument('--border', type=int, default=10,
                      help='Border size in pixels (default: 10)')
    parser.add_argument('--dpi', type=int, default=300,
                      help='Output DPI (default: 300)')
    return parser.parse_args()


def get_map_files():
    """Get all grant map PNG files, sorted by grant number."""
    files = list(OUTPUT_DIR.glob('grant_*_map.png'))
    
    # Sort by grant number (extract number from 'grant_X_map.png')
    def get_grant_num(path):
        try:
            return int(path.stem.split('_')[1])
        except (IndexError, ValueError):
            return 999999
            
    # Filter out grants 10 and 38, then sort
    excluded_grants = [10, 38]
    filtered_files = [f for f in files if get_grant_num(f) not in excluded_grants]
    return sorted(filtered_files, key=get_grant_num)


def create_contact_sheet(files, rows=None, cols=None, thumb_size=600, border=10, output_file='contact_sheet.png', dpi=300, title="Virginia Land Grant Geolocation Maps", format="PNG"):
    """Create a contact sheet from the list of image files."""
    if not files:
        print("No map files found!")
        return False
        
    # Calculate rows/columns if not specified
    num_images = len(files)
    if not rows and not cols:
        # Square-ish grid
        cols = int(math.ceil(math.sqrt(num_images)))
        rows = int(math.ceil(num_images / cols))
    elif rows and not cols:
        cols = int(math.ceil(num_images / rows))
    elif cols and not rows:
        rows = int(math.ceil(num_images / cols))
        
    print(f"Creating contact sheet with {rows} rows and {cols} columns ({num_images} images)")
        
    # Add space for title
    title_height = 60 if title else 0
    sheet_height = rows * (thumb_size + border) + border + title_height
    
    # Create a new blank image
    sheet_width = cols * (thumb_size + border) + border
    contact_sheet = Image.new('RGB', (sheet_width, sheet_height), (255, 255, 255))
    draw = ImageDraw.Draw(contact_sheet)
    
    # Try to load a font, if not available, we'll use default
    try:
        label_font = ImageFont.truetype("Arial", 24)
        title_font = ImageFont.truetype("Arial", 36)
    except IOError:
        try:
            label_font = ImageFont.truetype("DejaVuSans", 24)
            title_font = ImageFont.truetype("DejaVuSans", 36)
        except IOError:
            label_font = ImageFont.load_default()
            title_font = label_font
    
    # Add title (center it)
    if title:
        title_x = sheet_width // 2
        # Try to use anchor for centering if supported
        try:
            draw.text((title_x, 20), title, fill=(0, 0, 0), 
                     font=title_font, anchor="ma")
        except (TypeError, ValueError):
            # Fallback centering for older PIL versions
            text_width = draw.textlength(title, font=title_font) if hasattr(draw, 'textlength') else title_font.getlength(title)
            draw.text((title_x - text_width // 2, 20), title, fill=(0, 0, 0), 
                     font=title_font)
    
    # Place images on the contact sheet
    for i, file_path in enumerate(files):
        if i >= rows * cols:
            print(f"Warning: Only showing {rows * cols} of {num_images} images")
            break
            
        row = i // cols
        col = i % cols
        
        # Calculate position (with offset for title)
        x = col * (thumb_size + border) + border
        y = row * (thumb_size + border) + border + title_height
        
        try:
            # Open and resize image (use high quality resampling for better results)
            img = Image.open(file_path)
            resample_method = Image.Resampling.LANCZOS
            img = img.resize((thumb_size, thumb_size), resample_method)
            
            # Place on contact sheet
            contact_sheet.paste(img, (x, y))
            
            # Add grant number label in top-left
            grant_num = file_path.stem.split('_')[1]
            label = f"Grant {grant_num}"
            text_color = (0, 0, 0)  # Black text 
            # More visible label with semi-transparent background
            draw.rectangle([x, y, x+130, y+36], fill=(255, 255, 255, 220), outline=(0, 0, 0))
            draw.text((x+5, y+5), label, fill=text_color, font=label_font)
            
        except Exception as e:
            print(f"Error adding {file_path.name}: {e}")
            # Create a placeholder
            draw.rectangle([x, y, x+thumb_size, y+thumb_size], outline=(200, 200, 200), fill=(240, 240, 240))
            draw.text((x+thumb_size//3, y+thumb_size//2), f"Error: {file_path.name}", fill=(150, 150, 150), font=label_font)
    
    # Save the contact sheet
    output_path = THIS_DIR / output_file
    
    # Use specified format
    format = format.upper()
    if format == "PDF":
        try:
            contact_sheet.save(output_path, format="PDF", resolution=dpi)
        except (ValueError, ImportError):
            # If direct PDF support not available, save as PNG and indicate
            contact_sheet.save(str(output_path).replace(".pdf", ".png"), format="PNG", dpi=(dpi, dpi))
            print(f"Warning: Direct PDF export not supported, saved as PNG instead: {output_path}")
    else:
        contact_sheet.save(output_path, format=format, dpi=(dpi, dpi))
    
    print(f"Contact sheet saved to {output_path} ({dpi} DPI)")
    return True


def main():
    args = parse_args()
    files = get_map_files()
    print(f"Found {len(files)} map files")
    
    # Regular version
    create_contact_sheet(
        files=files, 
        rows=args.rows, 
        cols=args.cols, 
        thumb_size=args.thumb_size,
        border=args.border,
        output_file=args.output,
        dpi=args.dpi, 
        title="Virginia Land Grant Geolocation Test Set: All Methods Comparison"
    )
    
    # Higher-resolution versions
    resolutions = [
        # (dpi, thumb_size_multiplier, name_suffix)
        (600, 1.0, "_hi_dpi"),
        (2400, 2.0, "_ultra_hi_dpi"),
    ]
    
    for dpi, size_mult, suffix in resolutions:
        # Adjust thumbnail size proportionally for higher DPI
        hi_thumb_size = int(args.thumb_size * size_mult)
        hi_dpi_output = args.output.replace(".png", f"{suffix}.png")
        
        create_contact_sheet(
            files=files, 
            rows=args.rows, 
            cols=args.cols, 
            thumb_size=hi_thumb_size,
            border=args.border,
            output_file=hi_dpi_output,
            dpi=dpi, 
            title="Virginia Land Grant Geolocation Test Set: All Methods Comparison"
        )
    
    # Create PDF version
    pdf_output = args.output.replace(".png", ".pdf")
    create_contact_sheet(
        files=files, 
        rows=args.rows, 
        cols=args.cols, 
        thumb_size=int(args.thumb_size * 2.0),  # Double size for PDF
        border=args.border,
        output_file=pdf_output,
        dpi=1200, 
        title="Virginia Land Grant Geolocation Test Set: All Methods Comparison",
        format="PDF"
    )


if __name__ == "__main__":
    main() 