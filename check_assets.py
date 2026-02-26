#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asset Validation Tool for Ren'Py Image Directory
================================================================
Scans the game/images/ folder for:
  1. Double-suffix files (.png.jpg, .jpg.png, etc.)
  2. Files with illegal special characters
  3. Naming convention violations
  
Usage: python check_assets.py
"""

import os
import re
from pathlib import Path


def check_assets():
    """Main asset validation function."""
    
    # Define the images directory path
    images_dir = Path("game/images")
    
    if not images_dir.exists():
        print(f"❌ Error: Directory '{images_dir}' not found!")
        return
    
    print("=" * 70)
    print("📦 Ren'Py Asset Validation Scanner")
    print("=" * 70)
    print(f"Target directory: {images_dir.resolve()}\n")
    
    issues = {
        "double_suffix": [],
        "illegal_chars": [],
        "warnings": []
    }
    
    # List all files in images directory
    all_files = list(images_dir.iterdir())
    valid_files = [f for f in all_files if f.is_file()]
    
    print(f"Total files found: {len(valid_files)}\n")
    
    # Valid image extensions for Ren'Py
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
    
    # Pattern for legal Ren'Py image names (lowercase, alphanumeric, underscore, hyphen)
    legal_name_pattern = re.compile(r"^[a-z0-9_\-]+\.(jpg|jpeg|png|webp|gif|bmp)$", re.IGNORECASE)
    
    for file_path in sorted(valid_files):
        filename = file_path.name
        
        # ========================================
        # Check 1: Double Suffix Detection
        # ========================================
        # Count the number of dots (periods) in the filename
        dot_count = filename.count(".")
        
        if dot_count > 1:
            # Check if it's a double-suffix issue (e.g., .png.jpg)
            parts = filename.rsplit(".", 1)  # Get the last extension
            if len(parts) == 2:
                name_part = parts[0]
                # Check if the name part ends with a known extension
                for ext in valid_extensions:
                    if name_part.lower().endswith(ext):
                        issues["double_suffix"].append(filename)
                        break
        
        # ========================================
        # Check 2: Illegal Characters Detection
        # ========================================
        # Ren'Py image names should only contain: a-z, A-Z, 0-9, _, -
        # File extension should be one of the valid types
        
        illegal_chars = re.findall(r"[^a-zA-Z0-9_\-\.]", filename)
        
        if illegal_chars:
            issues["illegal_chars"].append({
                "file": filename,
                "chars": list(set(illegal_chars))  # Unique illegal chars
            })
        
        # ========================================
        # Check 3: Naming Convention Warnings
        # ========================================
        # Check for uppercase letters (convention: use lowercase)
        if any(c.isupper() for c in filename.split(".")[0]):
            # This is just a warning, not a hard error
            issues["warnings"].append({
                "file": filename,
                "reason": "Contains uppercase letters (convention: use lowercase)"
            })
    
    # ========================================
    # Report Results
    # ========================================
    
    print("\n" + "=" * 70)
    print("🔍 SCAN RESULTS")
    print("=" * 70)
    
    has_errors = False
    
    # Report double-suffix files
    if issues["double_suffix"]:
        has_errors = True
        print("\n🚨 CRITICAL: Double-Suffix Files (Risk Level: 🔴 HIGH)")
        print("-" * 70)
        for filename in issues["double_suffix"]:
            print(f"  ❌ {filename}")
            # Suggest correction
            corrected = filename.rsplit(".", 1)[0]  # Remove last extension
            # Find the actual extension
            base = filename.rsplit(".", 2)[0] if filename.count(".") > 1 else filename
            actual_ext = filename.rsplit(".", 1)[-1]
            corrected = f"{base}.{actual_ext}"
            print(f"     → Suggest: {corrected}")
    else:
        print("\n✅ No double-suffix files detected.")
    
    # Report illegal characters
    if issues["illegal_chars"]:
        has_errors = True
        print("\n⚠️  WARNING: Illegal Characters (Risk Level: 🟠 MEDIUM)")
        print("-" * 70)
        for item in issues["illegal_chars"]:
            print(f"  ⚠️  {item['file']}")
            print(f"     Illegal chars: {', '.join(repr(c) for c in item['chars'])}")
    else:
        print("\n✅ No illegal characters detected.")
    
    # Report naming convention warnings
    if issues["warnings"]:
        print("\n💡 SUGGESTIONS: Naming Convention (Risk Level: 🟡 LOW)")
        print("-" * 70)
        for item in issues["warnings"]:
            print(f"  💡 {item['file']}")
            print(f"     {item['reason']}")
    else:
        print("\n✅ All files follow naming conventions.")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total files scanned:      {len(valid_files)}")
    print(f"Double-suffix files:      {len(issues['double_suffix'])}")
    print(f"Illegal character files:  {len(issues['illegal_chars'])}")
    print(f"Convention warnings:      {len(issues['warnings'])}")
    
    if has_errors:
        print("\n⚠️  ACTION REQUIRED: Fix critical and warning issues above!")
    else:
        print("\n✅ All assets are properly named!")
    
    print("=" * 70)


if __name__ == "__main__":
    check_assets()
