#!/usr/bin/env python3
"""
Migrate all song YAML files from flat metadata to nested tags format.

Before:
  title: "Song"
  artist: "Artist"
  piano: true
  guitar: false
  readiness: 5
  content: |

After:
  title: "Song"
  artist: "Artist"
  tags:
    piano: true
    guitar: false
    readiness: 5
  content: |
"""

import os
import sys
import re

TAG_FIELDS = {'piano', 'guitar', 'readiness'}
SONGS_DIR = os.path.join(os.path.dirname(__file__), '..', '_data', 'songs')


def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the content: line — everything from there onward stays untouched
    content_line_idx = None
    for i, line in enumerate(lines):
        if line.startswith('content:'):
            content_line_idx = i
            break

    if content_line_idx is None:
        print(f"  SKIP: no content: field found in {os.path.basename(filepath)}")
        return False

    # Parse metadata lines (before content:)
    meta_lines = lines[:content_line_idx]
    content_lines = lines[content_line_idx:]

    # Extract tag values and remove them from meta
    extracted_tags = {}
    new_meta = []
    for line in meta_lines:
        stripped = line.rstrip('\n')
        # Check if this line is one of our tag fields
        match = re.match(r'^(piano|guitar|readiness)\s*:\s*(.+)$', stripped)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            extracted_tags[key] = value
        else:
            new_meta.append(line)

    if not extracted_tags:
        print(f"  SKIP: no tag fields found in {os.path.basename(filepath)}")
        return False

    # Build new metadata with tags: block
    # Insert tags: block right before content:
    tags_block = ['tags:\n']
    for key in ['piano', 'guitar', 'readiness']:
        if key in extracted_tags:
            tags_block.append(f'  {key}: {extracted_tags[key]}\n')

    new_lines = new_meta + tags_block + content_lines

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"  OK: {os.path.basename(filepath)} — migrated {len(extracted_tags)} tags")
    return True


def main():
    if not os.path.isdir(SONGS_DIR):
        print(f"ERROR: Songs directory not found: {SONGS_DIR}")
        sys.exit(1)

    yml_files = sorted([
        f for f in os.listdir(SONGS_DIR)
        if f.endswith('.yml') and not f.startswith('00_')
    ])

    if not yml_files:
        print("No .yml files found to migrate.")
        sys.exit(1)

    print(f"Migrating {len(yml_files)} song files...\n")

    migrated = 0
    skipped = 0
    for filename in yml_files:
        filepath = os.path.join(SONGS_DIR, filename)
        if migrate_file(filepath):
            migrated += 1
        else:
            skipped += 1

    print(f"\nDone: {migrated} migrated, {skipped} skipped")


if __name__ == '__main__':
    main()
