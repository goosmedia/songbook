#!/usr/bin/env python3
"""
Convert a song .txt file to .yml format for the songbook.

Usage:
    python3 tools/convert_song.py [options]

Options:
    -f, --filepath FILE    Input .txt filename (required)
    -t, --title TITLE      Song title (required)
    -a, --artist ARTIST    Artist name (required)
    --tag KEY=VALUE        Add tag (e.g., --tag piano=true --tag key=G --tag readiness=5)

If no options provided, runs in interactive mode.
"""

import argparse
import os
import sys

def process_file(input_file, title, artist, tags=None, content_text=None):
    """Process a single song file."""

    if tags is None:
        tags = {}

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

    if content_text is None:
        with open(input_file, 'r', encoding='utf-8') as f:
            content_text = f.read()

    content_text = content_text.replace('\u2028', '\n').replace('\u2029', '\n').replace('\f', '\n')

    lines = content_text.split('\n')
    processed_lines = []
    for line in lines:
        processed_lines.append('  ' + line.lstrip())

    processed_content = '\n'.join(processed_lines)

    tags_yaml = '\n'.join(f'  {k}: {v}' for k, v in tags.items())

    yaml_output = f'''title: "{title}"
artist: "{artist}"
tags:
{tags_yaml}
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

    print()
    print("Enter tags (format: key=value, empty line to finish):")
    tags = {}
    while True:
        tag_input = input("  Tag: ").strip()
        if not tag_input:
            break
        if '=' not in tag_input:
            print("  Invalid format. Use key=value")
            continue
        key, value = tag_input.split('=', 1)
        key = key.strip().lower()
        value = value.strip()
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        tags[key] = value

    print()
    print("=" * 50)

    if process_file(input_file, title, artist, tags):
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
    parser.add_argument('--tag', action='append',
                        help='Add tag as key=value (e.g., --tag piano=true --tag key=G)')

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

        tags = {}
        if args.tag:
            for t in args.tag:
                if '=' not in t:
                    print(f"ERROR: Invalid tag format: {t}. Use key=value")
                    sys.exit(1)
                key, value = t.split('=', 1)
                key = key.strip().lower()
                value = value.strip()
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                tags[key] = value

        process_file(
            args.filepath,
            args.title,
            args.artist,
            tags
        )
    else:
        interactive_mode()

if __name__ == '__main__':
    main()
