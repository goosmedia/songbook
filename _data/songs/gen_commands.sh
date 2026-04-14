#!/bin/bash
# Generate convert commands for all txt files

CONVERT_SCRIPT="/Users/aarongoos/Dropbox/DEV-Ubuntu-Shared/GITHUB_Goosmedia_local/songbook/tools/convert_song.py"
INPUT_DIR="/Users/aarongoos/Dropbox/DEV-Ubuntu-Shared/GITHUB_Goosmedia_local/songbook/_data/TXT_FILES_OK_2_DELETE"
OUTPUT_DIR="/Users/aarongoos/Dropbox/DEV-Ubuntu-Shared/GITHUB_Goosmedia_local/songbook/_data/songs"

# Create output dir if needed
mkdir -p "$OUTPUT_DIR"

for txt in "$INPUT_DIR"/*.txt; do
  [ -e "$txt" ] || continue
  filename=$(basename "$txt")

  # Get first non-empty line, strip control chars
  first=$(head -n 1 "$txt" | tr -d '\x00-\x08\x0b\x0c\x0e-\x1f\x7f' | sed 's/^[[:space:]]*//')

  # Extract title and artist from patterns
  # Pattern: "TITLE - ARTIST"
  if [[ "$first" =~ ^([^-]+)\ -\ (.*)$ ]]; then
    title="${BASH_REMATCH[1]}"
    artist="${BASH_REMATCH[2]}"
  # Pattern: "Title" (artist in next lines or filename)
  else
    # Try filename pattern "Song by Artist"
    if [[ "$filename" =~ ^(.+)\ by\ (.*)\.txt$ ]]; then
      title="${BASH_REMATCH[1]}"
      artist="${BASH_REMATCH[2]}"
    else
      title="${first}"
      artist="Unknown"
    fi
  fi

  # Clean whitespace
  title=$(echo "$title" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  artist=$(echo "$artist" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  # Copy to output dir (cleaning control chars during copy)
  output_file="$OUTPUT_DIR/$filename"
  tr -d '\x00-\x08\x0b\x0c\x0e-\x1f\x7f' < "$txt" > "$output_file"

  # Generate command
  echo "python3 \"$CONVERT_SCRIPT\" -f \"$output_file\" -t \"$title\" -a \"$artist\" -p -g -r 5"
done