---
layout: default
title: Songbook
---
<div class="container">
  <h1 class="page-title">My Songbook</h1>

  <div class="filters">
    <span class="filter-label">Filter:</span>
    <label class="filter-checkbox">
      <input type="checkbox" id="filter-piano" checked>
      <span>Piano</span>
    </label>
    <label class="filter-checkbox">
      <input type="checkbox" id="filter-guitar" checked>
      <span>Guitar</span>
    </label>
    <label class="filter-checkbox">
      <input type="checkbox" id="filter-other">
      <span>Other</span>
    </label>
  </div>

  <div class="table-wrapper">
    <table id="song-table">
      <thead>
        <tr id="table-header"></tr>
      </thead>
      <tbody id="table-body">
        <tr><td colspan="5" class="loading">Loading songs...</td></tr>
      </tbody>
    </table>
  </div>
</div>

<script>
(function() {
  const COLUMNS = [
    { key: 'title', label: 'Title', type: 'link' },
    { key: 'artist', label: 'Artist', type: 'text' },
    { key: 'piano', label: 'Piano', type: 'icon' },
    { key: 'guitar', label: 'Guitar', type: 'icon' },
    { key: 'readiness', label: 'Readiness', type: 'number' }
  ];

  let songs = [];
  let sortKey = 'title';
  let sortDir = 'asc';

  function parseYAMLFront(text) {
    const match = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (!match) return null;
    
    const yamlStr = match[1];
    const content = match[2];
    const data = {};
    
    yamlStr.split('\n').forEach(line => {
      const colonIndex = line.indexOf(':');
      if (colonIndex === -1) return;
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();
      
      if (value === 'true') value = true;
      else if (value === 'false') value = false;
      else if (!isNaN(value) && value !== '') value = parseInt(value, 10);
      else if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
      else if (value.startsWith("'") && value.endsWith("'")) value = value.slice(1, -1);
      
      data[key] = value;
    });
    
    return { meta: data, content: content };
  }

  function getSortValue(song, key) {
    const val = song[key];
    if (typeof val === 'boolean') return val ? 1 : 0;
    if (typeof val === 'number') return val;
    return (val || '').toString().toLowerCase();
  }

  function renderHeader() {
    const headerRow = document.getElementById('table-header');
    headerRow.innerHTML = COLUMNS.map(col => `
      <th class="sortable" data-key="${col.key}">
        ${col.label}
        <span class="sort-icon">${sortKey === col.key ? (sortDir === 'asc' ? '↑' : '↓') : ''}</span>
      </th>
    `).join('');

    headerRow.querySelectorAll('th').forEach(th => {
      th.addEventListener('click', () => {
        const key = th.dataset.key;
        if (sortKey === key) {
          sortDir = sortDir === 'asc' ? 'desc' : 'asc';
        } else {
          sortKey = key;
          sortDir = 'asc';
        }
        renderTable();
      });
    });
  }

  function renderCell(song, col) {
    if (col.type === 'icon') {
      return `<td class="icon-cell"><span class="icon ${song[col.key] ? 'active' : 'inactive'}">${song[col.key] ? '●' : '○'}</span></td>`;
    }
    if (col.type === 'link') {
      const filename = song.filename;
      return `<td class="title-cell"><a href="./song/?f=${encodeURIComponent(filename)}">${song.title}</a></td>`;
    }
    return `<td>${song[col.key] || '—'}</td>`;
  }

  function renderTable() {
    const tbody = document.getElementById('table-body');
    const filtered = songs.filter(song => {
      const pianoChecked = document.getElementById('filter-piano').checked;
      const guitarChecked = document.getElementById('filter-guitar').checked;
      const otherChecked = document.getElementById('filter-other').checked;

      if (song.piano && pianoChecked) return true;
      if (song.guitar && guitarChecked) return true;
      if (!song.piano && !song.guitar && otherChecked) return true;

      return false;
    });

    const sorted = [...filtered].sort((a, b) => {
      const aVal = getSortValue(a, sortKey);
      const bVal = getSortValue(b, sortKey);
      if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });

    if (sorted.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="empty">No songs match your filters</td></tr>';
      return;
    }

    tbody.innerHTML = sorted.map(song => `
      <tr>${COLUMNS.map(col => renderCell(song, col)).join('')}</tr>
    `).join('');

    renderHeader();
  }

  function loadSongs() {
    fetch('./songs-manifest.json')
      .then(r => r.json())
      .then(filenames => {
        return Promise.all(filenames.map(filename => 
          fetch(`./songs/${filename}`)
            .then(r => r.text())
            .then(text => {
              const parsed = parseYAMLFront(text);
              if (parsed) {
                return { ...parsed.meta, filename: filename, content: parsed.content };
              }
              return null;
            })
        ));
      })
      .then(results => {
        songs = results.filter(s => s !== null);
        renderTable();
      })
      .catch(err => {
        console.error('Failed to load songs:', err);
        document.getElementById('table-body').innerHTML = 
          '<tr><td colspan="5" class="error">Failed to load songs.</td></tr>';
      });
  }

  document.getElementById('filter-piano').addEventListener('change', renderTable);
  document.getElementById('filter-guitar').addEventListener('change', renderTable);
  document.getElementById('filter-other').addEventListener('change', renderTable);

  renderHeader();
  loadSongs();
})();
</script>
