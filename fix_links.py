#!/usr/bin/env python3
import re
from pathlib import Path
import argparse

# Vendor affiliate links - easy to update here
files_vendors = {
    "retatrutide.html": [
        ("Paradigm Peptide", "https://paradigmpeptides.com"),
        ("Peptide Partners", "https://peptidepartners.com"),
        ("Nuscience Peptides", "https://nusciencepeptides.com"),
        ("Aavant Research", "https://aavantresearch.com"),
        ("Guangzhou Jeep Biotech", "https://finnrick.com/vendors"),
        ("Atomik Labz", "https://atomiklabz.com"),
        ("Huaian Hanyou Peptide", "https://finnrick.com/vendors"),
        ("Inno Peptides", "https://finnrick.com/vendors"),
        ("Lejian Biotech", "https://finnrick.com/vendors"),
        ("Lipeptides", "https://finnrick.com/vendors"),
        ("Marvel Peptide", "https://finnrick.com/vendors"),
        ("NextechLabs", "https://finnrick.com/vendors"),
        ("Noble Dragons", "https://finnrick.com/vendors"),
        ("Peptide Crafters", "https://peptidecrafters.com"),
        ("PurePeptides", "https://finnrick.com/vendors"),
        ("Shandong Shengyuan", "https://finnrick.com/vendors"),
        ("Yabang Peptide", "https://finnrick.com/vendors"),
        ("YB Peptide", "https://finnrick.com/vendors"),
    ],
    "semaglutide.html": [
        ("Amino Amigos", "https://aminoamigos.com"),
        ("Astro Peptides", "https://astropeptides.com"),
        ("Bulk Peptide Supply", "https://bulkpeptidesupply.com"),
        ("HK Peptides", "https://hkpeptides.com"),
        ("Peptide Crafters", "https://peptidecrafters.com"),
        ("Planet Peptide", "https://planetpeptide.com"),
        ("Skye Peptides", "https://skyepeptides.com"),
    ],
    "bpc157.html": [
        ("Peptide Sciences", "https://peptidesciences.com"),
        ("HkRoids", "https://hkroids.com"),
        ("Nuscience Peptides", "https://nusciencepeptides.com"),
        ("Peptide Partners", "https://peptidepartners.com"),
    ],
    "ipamorelin.html": [
        ("Astro Peptides", "https://astropeptides.com"),
        ("Oupeptide", "https://oupeptide.com"),
        ("Paramount Peptides", "https://paramountpeptides.com"),
        ("Peptide Partners", "https://peptidepartners.com"),
        ("Peptide Sciences", "https://peptidesciences.com"),
        ("Yiwu Aozuo Trading", "https://finnrick.com/vendors"),
        ("ZLZ Peptide", "https://finnrick.com/vendors"),
    ],
    "ghk-cu.html": [
        ("Peptidology", "https://peptidology.com"),
        ("Shanghai Baoju", "https://finnrick.com/vendors"),
        ("Paradigm Peptide", "https://paradigmpeptides.com"),
        ("Peptide Partners", "https://peptidepartners.com"),
        ("Nuscience Peptides", "https://nusciencepeptides.com"),
    ],
    "cjc-1295.html": [
        ("Pure Tested Peptides", "https://puretestedpeptides.com"),
        ("NuLife Peptides", "https://nulipeptides.com"),
        ("Atomik Labz", "https://atomiklabz.com"),
    ],
    "tesamorelin.html": [
        ("Pure Tested Peptides", "https://puretestedpeptides.com"),
        ("TCI", "https://finnrick.com/vendors"),
        ("Lux Synth Aminos", "https://finnrick.com/vendors"),
    ],
    "index.html": [
        ("Paradigm Peptide", "https://paradigmpeptides.com"),
        ("Peptide Partners", "https://peptidepartners.com"),
        ("Nuscience Peptides", "https://nusciencepeptides.com"),
    ],
}

def fix_affiliate_links(src_dir: str = "src") -> None:
    """Wrap vendor cards with affiliate links using regex."""
    src_path = Path(src_dir).resolve()
    if not src_path.exists():
        print(f"Directory not found: {src_path}")
        return

    for fn, vendors in files_vendors.items():
        file_path = src_path / fn
        if not file_path.exists():
            print(f"WARN: {fn} not found")
            continue
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            
            changed = 0
            for vendor_name, url in vendors:
                v = re.escape(vendor_name)
                # Improved pattern for full card
                pattern = r'(<div class="card">\s+<div class="rank">[^<]*</div>\s+<div class="vendor-name">' + v + r'</div>.*?</div>\s*</div>)'
                link_open = f'<a href="{url}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit">'
                replacement = link_open + r'\1</a>'
                new_content, n = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
                if n > 0:
                    content = new_content
                    changed += 1
                    print(f"  {fn}: Linked {vendor_name}")
                else:
                    print(f"  WARN: {fn}: No match for {vendor_name}")
            
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(content)
            print(f"✅ {fn}: {changed}/{len(vendors)} links fixed")
        except Exception as e:
            print(f"❌ Error in {fn}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix affiliate links in HTML vendor cards.")
    parser.add_argument("--src", default="src", help="Path to source directory (default: src)")
    args = parser.parse_args()
    fix_affiliate_links(args.src)
    print("\nAll done!")
