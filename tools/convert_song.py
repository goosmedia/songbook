#!/usr/bin/env python3
"""
Convert a song .txt file to .yml format for the songbook.
Usage: python3 tools/convert_song.py
"""

import os
import sys

def main():
    print("=" * 50)
    print("Song File Converter: .txt -> .yml")
    print("=" * 50)
    print()

    # Get input filename
    input_file = input("Enter input filename (must end in .txt): ").strip()
    
    # Validate extension
    if not input_file.endswith('.txt'):
        print(f"ERROR: File must end in .txt, got: {input_file}")
        sys.exit(1)
    
    # Check file exists
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    # Generate output filename
    output_file = input_file[:-4] + '.yml'
    
    # Check if output already exists
    if os.path.exists(output_file):
        overwrite = input(f"Output file '{output_file}' exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Get metadata
    print()
    print("Enter song metadata (press Enter for defaults where applicable):")
    print("-" * 50)
    
    title = input("Title: ").strip()
    if not title:
        print("ERROR: Title is required")
        sys.exit(1)
    
    artist = input("Artist: ").strip()
    if not artist:
        print("ERROR: Artist is required")
        sys.exit(1)
    
    # Booleans
    piano_input = input("Piano (true/false) [true]: ").strip().lower()
    piano = piano_input != 'false'
    
    guitar_input = input("Guitar (true/false) [true]: ").strip().lower()
    guitar = guitar_input != 'false'
    
    # Readiness
    readiness_input = input("Readiness (1-10) [5]: ").strip()
    try:
        readiness = int(readiness_input) if readiness_input else 5
        if readiness < 1 or readiness > 10:
            print("WARNING: Readiness should be 1-10, using 5")
            readiness = 5
    except ValueError:
        readiness = 5
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process content: add 2 spaces to each line
    lines = content.split('\n')
    processed_lines = []
    for line in lines:
        if line:  # Only add spaces to non-empty lines
            processed_lines.append('  ' + line)
        else:
            processed_lines.append('')  # Preserve blank lines
    
    processed_content = '\n'.join(processed_lines)
    
    # Generate YAML
    yaml_output = f'''title: "{title}"
artist: "{artist}"
piano: {str(piano).lower()}
guitar: {str(guitar).lower()}
readiness: {readiness}
content: |
{processed_content}
'''
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(yaml_output)
    
    print()
    print("=" * 50)
    print(f"SUCCESS: Created {output_file}")
    print("=" * 50)

if __name__ == '__main__':
    main()
