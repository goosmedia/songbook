#!/usr/bin/env python3
"""
Convert a song .txt file to .yml format for the songbook.

Usage:
    Interactive: python3 tools/convert_song.py
    CLI:        python3 tools/convert_song.py --filepath song.txt --title "Title" --artist "Artist" [--piano] [--guitar] [--readiness 5]
"""

import argparse
import os
import sys

def process_file(input_file, title, artist, piano=True, guitar=True, readiness=5):
    """Process a single song file."""
    
    # Validate extension
    if not input_file.endswith('.txt'):
        print(f"ERROR: File must end in .txt, got: {input_file}")
        return False
    
    # Check file exists
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        return False
    
    # Generate output filename
    output_file = input_file[:-4] + '.yml'
    
    # Check if output already exists
    if os.path.exists(output_file):
        overwrite = input(f"Output file '{output_file}' exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Skipped.")
            return False
    
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
    
    piano_input = input("Piano (true/false) [true]: ").strip().lower()
    piano = piano_input != 'false'
    
    guitar_input = input("Guitar (true/false) [true]: ").strip().lower()
    guitar = guitar_input != 'false'
    
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

def cli_mode(args):
    """Run in CLI mode with arguments."""
    # Handle piano/guitar defaults
    piano = True
    guitar = True
    if args.piano_flag == 'piano_false':
        piano = False
    if args.guitar_flag == 'guitar_false':
        guitar = False
    
    success = process_file(
        args.filepath,
        args.title,
        args.artist,
        piano,
        guitar,
        args.readiness
    )
    if not success:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert song .txt file to .yml format for the songbook.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Interactive:
    python3 tools/convert_song.py
    
  CLI with all options:
    python3 tools/convert_song.py --filepath song.txt --title "Song Title" --artist "Artist Name" --piano --guitar --readiness 7
    
  CLI with defaults (piano=true, guitar=true, readiness=5):
    python3 tools/convert_song.py --filepath song.txt --title "Song Title" --artist "Artist Name"
'''
    )
    
    parser.add_argument('--filepath', '-f', type=str, required=False,
                        help='Input .txt filename')
    parser.add_argument('--title', '-t', type=str, required=False,
                        help='Song title (required in CLI mode)')
    parser.add_argument('--artist', '-a', type=str, required=False,
                        help='Artist name (required in CLI mode)')
    parser.add_argument('--piano', dest='piano_flag', action='store_const', const='piano_true',
                        help='Has piano parts')
    parser.add_argument('--no-piano', dest='piano_flag', action='store_const', const='piano_false',
                        help='Disable piano')
    parser.add_argument('--guitar', dest='guitar_flag', action='store_const', const='guitar_true',
                        help='Has guitar parts')
    parser.add_argument('--no-guitar', dest='guitar_flag', action='store_const', const='guitar_false',
                        help='Disable guitar')
    parser.add_argument('--readiness', '-r', type=int, default=5,
                        help='Readiness 1-10 (default: 5)')
    
    args = parser.parse_args()
    
    # If any CLI args provided, use CLI mode
    if args.filepath or args.title or args.artist:
        # Validate required arguments
        if not args.filepath:
            print("ERROR: --filepath is required in CLI mode")
            sys.exit(1)
        if not args.title:
            print("ERROR: --title is required in CLI mode")
            sys.exit(1)
        if not args.artist:
            print("ERROR: --artist is required in CLI mode")
            sys.exit(1)
        
        # Set defaults if flags not provided
        piano = True
        guitar = True
        if args.piano_flag == 'piano_false':
            piano = False
        if args.guitar_flag == 'guitar_false':
            guitar = False
        
        cli_mode(args)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == '__main__':
    main()
