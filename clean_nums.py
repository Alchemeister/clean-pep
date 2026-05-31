#!/usr/bin/env python3
import re
from pathlib import Path
import argparse
from datetime import datetime

def clean_html_files(src_dir: str = "src") -> None:
    """Clean line number prefixes from HTML files in the source directory.
    Optimized for robustness, backups, and logging."""
    src_path = Path(src_dir).resolve()
    if not src_path.exists():
        print(f"Directory not found: {src_path}")
        return
    
    cleaned_count = 0
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    for html_file in src_path.glob("*.html"):
        try:
            content = html_file.read_text(encoding="utf-8")
            # More robust regex for line numbers (handles various formats like 1|, 22|22|, etc.)
            cleaned = re.sub(r'^\s*\d+\|(?:\d+\|)*\s*', '', content, flags=re.MULTILINE)
            if cleaned != content:
                # Backup original
                backup = html_file.with_name(f"{html_file.name}.bak.{timestamp}")
                html_file.rename(backup)
                html_file.write_text(cleaned, encoding="utf-8")
                print(f"✅ Cleaned line numbers in {html_file.name} (backup created)")
                cleaned_count += 1
            else:
                print(f"No changes needed in {html_file.name}")
        except Exception as e:
            print(f"❌ Error processing {html_file.name}: {e}")
    print(f"\nDone! Cleaned {cleaned_count} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean line-number prefixes from HTML files.")
    parser.add_argument("--src", default="src", help="Path to source directory containing HTML files (default: src)")
    args = parser.parse_args()
    clean_html_files(args.src)
