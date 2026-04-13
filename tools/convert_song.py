#!/usr/bin/env python3
"""
Convert a song .txt file to .yml format for the songbook.

Usage:
    python3 tools/convert_song.py [options]

Options:
    -f, --filepath FILE    Input .txt filename (required)
    -t, --title TITLE      Song title (required)
    -a, --artist ARTIST    Artist name (required)
    -p, --piano            Song has piano parts (default: false)
    -g, --guitar           Song has guitar parts (default: false)
    -r, --readiness N      Readiness 1-10 (default: 5)

If no options provided, runs in interactive mode.
"""

import argparse
import os
import sys

def process_file(input_file, title, artist, piano=False, guitar=False, readiness=5):
    """Process a single song file."""
    
    if not input_file.endswith('.txt'):
        print(f"ERROR: File must end in .txt, got: {input_file}")
        return False
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        return False
    
    output_file = input_file[:-4] + '.yml'
    
    if os.path.exists(output_file):
        overwrite = input(f"Output file '{output_file}' exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Skipped.")
            return False
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        content = content.replace('\u2028', '\n').replace('\u2029', '\n')

    lines = content.split('\n')
    processed_lines = []
    for line in lines:
        if line:
            processed_lines.append('  ' + line)
        else:
            processed_lines.append('')
    
    processed_content = '\n'.join(processed_lines)
    
    yaml_output = f'''title: "{title}"
artist: "{artist}"
piano: {str(piano).lower()}
guitar: {str(guitar).lower()}
readiness: {readiness}
content: |
{processed_content}
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(yaml_output)
    
    print(f"SUCCESS: Created {output_file}")
    return True

def interactive_mode():
    """Run in interactive mode."""
    print("=" * 50)
    print("Song File Converter: .txt -> .yml")
    print("=" * 50)
    print()
    
    input_file = input("Enter input filename (must end in .txt): ").strip()
    
    if not input_file.endswith('.txt'):
        print(f"ERROR: File must end in .txt, got: {input_file}")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    print()
    print("Enter song metadata:")
    print("-" * 50)
    
    title = input("Title: ").strip()
    if not title:
        print("ERROR: Title is required")
        sys.exit(1)
    
    artist = input("Artist: ").strip()
    if not artist:
        print("ERROR: Artist is required")
        sys.exit(1)
    
    piano = input("Piano? (y/n) [n]: ").strip().lower() == 'y'
    guitar = input("Guitar? (y/n) [n]: ").strip().lower() == 'y'
    
    readiness_input = input("Readiness (1-10) [5]: ").strip()
    try:
        readiness = int(readiness_input) if readiness_input else 5
        if readiness < 1 or readiness > 10:
            print("WARNING: Readiness should be 1-10, using 5")
            readiness = 5
    except ValueError:
        readiness = 5
    
    print()
    print("=" * 50)
    
    if process_file(input_file, title, artist, piano, guitar, readiness):
        print("=" * 50)
    else:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert song .txt file to .yml format for the songbook.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-f', '--filepath', type=str,
                        help='Input .txt filename (required in CLI mode)')
    parser.add_argument('-t', '--title', type=str,
                        help='Song title (required in CLI mode)')
    parser.add_argument('-a', '--artist', type=str,
                        help='Artist name (required in CLI mode)')
    parser.add_argument('-p', '--piano', action='store_true',
                        help='Song has piano parts (default: false)')
    parser.add_argument('-g', '--guitar', action='store_true',
                        help='Song has guitar parts (default: false)')
    parser.add_argument('-r', '--readiness', type=int, default=5,
                        help='Readiness 1-10 (default: 5)')
    
    args = parser.parse_args()
    
    if args.filepath or args.title or args.artist:
        if not args.filepath:
            print("ERROR: --filepath is required in CLI mode")
            sys.exit(1)
        if not args.title:
            print("ERROR: --title is required in CLI mode")
            sys.exit(1)
        if not args.artist:
            print("ERROR: --artist is required in CLI mode")
            sys.exit(1)
        
        process_file(
            args.filepath,
            args.title,
            args.artist,
            args.piano,
            args.guitar,
            args.readiness
        )
    else:
        interactive_mode()

if __name__ == '__main__':
    main()
