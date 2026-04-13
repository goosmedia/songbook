#!/usr/bin/env python3
"""Generate convert commands for txt files."""

import os
import re
import unicodedata

CONVERT_SCRIPT = "/Users/aarongoos/Dropbox/DEV-Ubuntu-Shared/GITHUB_Goosmedia_local/songbook/tools/convert_song.py"
INPUT_DIR = "/Users/aarongoos/Dropbox/DEV-Ubuntu-Shared/GITHUB_Goosmedia_local/songbook/_data/TXT_FILES_OK_2_DELETE"
OUTPUT_DIR = "/Users/aarongoos/Dropbox/DEV-Ubuntu-Shared/GITHUB_Goosmedia_local/songbook/_data/songs"

def clean_text(text):
    """Remove control characters."""
    return ''.join(c for c in text if unicodedata.category(c) != 'Cc' or c in '\n\t')

def extract_title_artist(filename, first_line):
    """Extract title and artist from first line or filename."""
    first = clean_text(first_line.strip())
    
    # Pattern: "TITLE - ARTIST"
    match = re.match(r'^(.+?)\s*-\s*(.+)$', first)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Pattern: "Song by Artist" in filename
    match = re.match(r'^(.+?)\s+by\s+(.+?)\.txt$', filename, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Use first line as title
    if first:
        return first, "Unknown"
    
    # Use filename as title
    title = re.sub(r'\.txt$', '', filename)
    return title, "Unknown"

os.makedirs(OUTPUT_DIR, exist_ok=True)

txt_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.txt')])

for filename in txt_files:
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Clean content
    clean_content = clean_text(content)
    
    # Find first non-empty line
    first_line = ""
    for line in clean_content.split('\n'):
        if line.strip():
            first_line = line
            break
    
    title, artist = extract_title_artist(filename, first_line)
    
    # Copy cleaned file to output dir
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    # Print command
    print(f'python3 "{CONVERT_SCRIPT}" -f "{output_path}" -t "{title}" -a "{artist}" -p -g -r 5')