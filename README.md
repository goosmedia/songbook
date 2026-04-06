# My Songbook

A Jekyll-based songbook for displaying chords and lyrics with GitHub Pages.

## Adding Songs

Add a new `.md` file to the `_songs/` folder with the following format:

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

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| title | string | Song title |
| artist | string | Artist name |
| piano | boolean | Has piano parts |
| guitar | boolean | Has guitar parts |
| readiness | integer | 1-10 readiness score |

### Adding New Columns

To add a new metadata column to the table:

1. Add the field to your song's YAML front matter
2. Update the `COLUMNS` array in `assets/main.js`

```javascript
const COLUMNS = [
  { key: 'title', label: 'Title', type: 'link' },
  { key: 'artist', label: 'Artist', type: 'text' },
  { key: 'piano', label: 'Piano', type: 'icon' },
  { key: 'guitar', label: 'Guitar', type: 'icon' },
  { key: 'readiness', label: 'Readiness', type: 'number' },
  { key: 'tempo', label: 'Tempo', type: 'number' },  // Add new columns here
];
```

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000` to preview.

## Deployment

Push to GitHub and GitHub Pages will automatically build and deploy the site.
