# My Songbook

A dark-mode songbook for displaying chords and lyrics with monospace alignment. Hosted on GitHub Pages.

## Adding Songs

### Step 1: Open `songs-data.js`

All songs are stored in a single JavaScript file: `songs-data.js`

### Step 2: Add a new song entry

Copy the template below and add it to the `SONGS` array:

```javascript
{
  filename: 'my-song',
  title: 'Song Title',
  artist: 'Artist Name',
  piano: true,
  guitar: false,
  readiness: 5,
  content: `      C                    G
First chord line

      Am                   F
Second chord line

      C
First lyric line

      G
Second lyric line`
},
```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add my-song"
git push
```

---

## Song Format

Each song entry has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filename` | string | Yes | Unique identifier (no spaces, no extension) |
| `title` | string | Yes | Song title |
| `artist` | string | Yes | Artist name |
| `piano` | boolean | No | Has piano parts (default: false) |
| `guitar` | boolean | No | Has guitar parts (default: false) |
| `readiness` | number | No | 1-10 readiness score (default: 5) |
| `content` | string | Yes | Chords and lyrics in monospace format |

### Adding New Fields

To add a new boolean field (e.g., `electro`):

1. Add the field to each song entry: `electro: true`
2. Add to song.html display:
   ```javascript
   if (song.electro) metaContainer.innerHTML += '<span class="meta-tag electro">Electro</span>';
   ```
3. Add CSS for `.meta-tag.electro` in `assets/main.css`

---

## Content Format

The `content` field uses backticks (template literal) to preserve:

- **Chords**: Placed above lyrics they accompany
- **Line breaks**: Single blank line = paragraph break, double = section separation
- **Section markers**: `[Verse]`, `[Chorus]`, etc.
- **Spacing**: Spaces are preserved for chord alignment

Example:
```
      Am                   G
Your lyrics go here

      F                    C
More lyrics with chords above
```

---

## File Structure

```
├── index.html        (generated)
├── index.md          (table of contents)
├── song.html         (song viewer)
├── songs-data.js     (ALL songs - metadata + content)
├── assets/
│   └── main.css
└── _layouts/
    └── default.html
```

---

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000/songbook/` to preview.
