# My Songbook

A dark-mode songbook for displaying chords and lyrics. Hosted on GitHub Pages.

## Adding Songs

### Step 1: Create the song file

Create a new `.txt` file in the `songs/` folder:

```
songs/my-song.txt
```

### Step 2: Add YAML front matter and content

```yaml
---
title: "Song Title"
artist: "Artist Name"
piano: true
guitar: true
readiness: 5
---
      C                    G
First line of lyrics

      Am                   F
Second line of lyrics
```

### Step 3: Register the song

Add the filename to `songs-manifest.json`:

```json
["burning-pile.txt", "my-song.txt"]
```

### Step 4: Push to GitHub

```bash
git add .
git commit -m "Add my-song"
git push
```

## Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| title | string | Song title |
| artist | string | Artist name |
| piano | boolean | Has piano parts |
| guitar | boolean | Has guitar parts |
| readiness | integer | 1-10 readiness score |

Add new boolean fields as needed (e.g., `electro: true`).

## Adding New Table Columns

1. Add the field to your song's YAML front matter
2. Update the `COLUMNS` array in `index.md` JavaScript:

```javascript
const COLUMNS = [
  { key: 'title', label: 'Title', type: 'link' },
  { key: 'artist', label: 'Artist', type: 'text' },
  { key: 'piano', label: 'Piano', type: 'icon' },
  { key: 'guitar', label: 'Guitar', type: 'icon' },
  { key: 'readiness', label: 'Readiness', type: 'number' },
  { key: 'myfield', label: 'My Field', type: 'text' },  // Add new columns here
];
```

## File Structure

```
├── index.html           (generated)
├── index.md             (table of contents)
├── song.html            (song viewer)
├── songs/
│   ├── manifest.json
│   └── *.txt           (song files)
├── assets/
│   └── main.css
└── _layouts/
    └── default.html
```

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000/songbook/` to preview.

## Deployment

Push to GitHub - GitHub Pages will automatically build and deploy.
