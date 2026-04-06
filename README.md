# My Songbook

A dark-mode songbook for displaying chords and lyrics with monospace alignment. Hosted on GitHub Pages.

## Adding Songs

### Step 1: Copy the template

Copy `_data/songs/00_template.yml` and rename it (e.g., `my-song.yml`).

### Step 2: Edit the new file

```yaml
title: "Song Title"
artist: "Artist Name"
piano: true
guitar: true
readiness: 5
content: |
      C                    G
First lyric line here

      Am                   F
Second lyric line here
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add my-song"
git push
```

---

## Song Format

Each song file has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Song title |
| `artist` | string | Yes | Artist name |
| `piano` | boolean | No | Has piano parts (default: false) |
| `guitar` | boolean | No | Has guitar parts (default: false) |
| `readiness` | number | No | 1-10 readiness score (default: 5) |
| `content` | string | Yes | Chords and lyrics in monospace format |

### Content Format

The `content` field uses YAML literal block scalar (`|`) to preserve:
- **Chords**: Placed above lyrics they accompany
- **Line breaks**: Single blank line = paragraph break
- **Spacing**: Extra indentation is preserved for alignment

Example:
```
      Am                   G
Your lyrics go here

      F                    C
More lyrics with chords above
```

### Key Rules

- Extra indentation within content is **preserved** - use it for alignment
- Special characters (`#`, `:`, `&`) are safe inside the content block
- Wrap the content in `<pre>` tags for monospace display

---

## Adding New Fields

To add a new field (e.g., `electro`):

1. Add the field to each song file: `electro: true`
2. Update `songs.json` to include the field
3. Update `song.html` to display it
4. Add CSS for the new tag in `assets/main.css`

---

## File Structure

```
├── _data/songs/
│   ├── burning-pile.yml    (song files - one per song)
│   └── 00_template.yml    (copy this to create new songs)
```

---

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000/songbook/` to preview.
