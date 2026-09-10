#!/usr/bin/env python3
"""
generate_distribution_release_archive.py
Packages the complete master release archive for Project 35: Willy Nelson.
Creates Project35-WillyNelson-MasterArchive.zip and generates MD5 checksum verification.
"""

import hashlib
import os
import zipfile
from pathlib import Path

def compute_md5(filepath: Path) -> str:
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def create_archive():
    project_root = Path(__file__).resolve().parent.parent
    dist_dir = project_root / "distribution"
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    zip_path = dist_dir / "Project35-WillyNelson-MasterArchive.zip"
    checksums_path = dist_dir / "RELEASE_CHECKSUMS.md"
    
    print("Building Project 35 Master Release Archive...")
    
    checksum_lines = [
        "# MASTER RELEASE ARCHIVE & CHECKSUM MANIFEST",
        "",
        "**Project:** Project 35: Willy Nelson (9/11 Master Mixtape Rendition)",
        "**Archive File:** `Project35-WillyNelson-MasterArchive.zip`",
        "",
        "---",
        "",
        "## 🔒 SHA256 / MD5 File Integrity Registry",
        ""
    ]
    
    files_to_zip = []
    
    # Collect all project files
    for p in project_root.rglob("*"):
        if p.is_file():
            rel_str = str(p.relative_to(project_root)).replace("\\", "/")
            if not rel_str.startswith(".git") and "Project35-WillyNelson-MasterArchive.zip" not in rel_str and "RELEASE_CHECKSUMS.md" not in rel_str:
                files_to_zip.append(p)
                
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_zip:
            rel = f.relative_to(project_root)
            zf.write(f, rel)
            md5 = compute_md5(f)
            checksum_lines.append(f"* `{rel}` — MD5: `{md5}`")
            
    with open(checksums_path, "w", encoding="utf-8") as cf:
        cf.write("\n".join(checksum_lines))
        
    archive_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Master archive created: {zip_path.name} ({archive_size_mb:.2f} MB, {len(files_to_zip)} files)")
    print(f"Checksum manifest written to {checksums_path.name}")

if __name__ == "__main__":
    create_archive()
