---
layout: default
title: Songbook
---
<div class="container">
  <h1 class="page-title">My Songbook</h1>

  <div class="filters" id="filters">
    <span class="filter-label">Filter:</span>
  </div>

  <div class="search-wrapper">
    <input type="text" id="search-input" class="search-input" placeholder="Search songs..." autocomplete="off">
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
  const STATIC_COLUMNS = [
    { key: 'title', label: 'Title', type: 'link' },
    { key: 'artist', label: 'Artist', type: 'text' }
  ];

  let songs = [];
  let tagColumns = [];
  let sortKey = 'title';
  let sortDir = 'asc';
  let searchQuery = '';

  function getTagValue(song, key) {
    return (song.tags && song.tags[key] !== undefined) ? song.tags[key] : null;
  }

  function getSortValue(song, key) {
    const val = getTagValue(song, key) || song[key];
    if (typeof val === 'boolean') return val ? 1 : 0;
    if (typeof val === 'number') return val;
    return (val || '').toString().toLowerCase();
  }

  function searchRelevance(song, q) {
    let score = 0;
    if ((song.filename || '').toLowerCase().includes(q)) score += 3;
    if ((song.title || '').toLowerCase().includes(q)) score += 3;
    if ((song.artist || '').toLowerCase().includes(q)) score += 2;
    if ((song.content || '').toLowerCase().includes(q)) score += 1;
    const tagValues = Object.values(song.tags || {});
    if (tagValues.some(v => String(v).toLowerCase().includes(q))) score += 1;
    return score;
  }

  function buildColumns() {
    return [...STATIC_COLUMNS, ...tagColumns];
  }

  function renderHeader() {
    const columns = buildColumns();
    const headerRow = document.getElementById('table-header');
    headerRow.innerHTML = columns.map(col => `
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
    const val = getTagValue(song, col.key);
    if (col.type === 'icon') {
      return `<td class="icon-cell"><span class="icon ${val ? 'active' : 'inactive'}">${val ? '●' : '○'}</span></td>`;
    }
    if (col.type === 'link') {
      return `<td class="title-cell"><a href="${song.url}">${song.title}</a></td>`;
    }
    return `<td>${val !== null && val !== undefined ? val : '—'}</td>`;
  }

  function renderTable() {
    const tbody = document.getElementById('table-body');
    const columns = buildColumns();

    let filtered = songs.filter(song => {
      const checkboxes = document.querySelectorAll('.filter-tag');
      const anyChecked = Array.from(checkboxes).some(cb => cb.checked);

      if (!anyChecked) return true;

      for (const cb of checkboxes) {
        if (cb.checked) {
          const tagKey = cb.dataset.tag;
          const val = getTagValue(song, tagKey);
          if (val === true || (val !== null && val !== undefined && val !== false)) return true;
        }
      }

      return false;
    });

    const q = searchQuery.trim().toLowerCase();
    if (q) {
      filtered = filtered.filter(song => {
        const fields = [song.filename, song.title, song.artist, song.content];
        const tagVals = Object.values(song.tags || {}).map(v => String(v));
        return [...fields, ...tagVals].some(f => f && f.toLowerCase().includes(q));
      });
    }

    const sorted = [...filtered].sort((a, b) => {
      if (q) {
        const sa = searchRelevance(a, q);
        const sb = searchRelevance(b, q);
        if (sa !== sb) return sb - sa;
      }
      const aVal = getSortValue(a, sortKey);
      const bVal = getSortValue(b, sortKey);
      if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });

    if (sorted.length === 0) {
      tbody.innerHTML = `<tr><td colspan="${columns.length}" class="empty">No songs match your filters</td></tr>`;
      return;
    }

    tbody.innerHTML = sorted.map(song => `
      <tr>${columns.map(col => renderCell(song, col)).join('')}</tr>
    `).join('');

    renderHeader();
  }

  function buildFilters() {
    const allTagKeys = new Set();
    songs.forEach(song => {
      Object.keys(song.tags || {}).forEach(key => allTagKeys.add(key));
    });

    const filtersContainer = document.getElementById('filters');
    const label = filtersContainer.querySelector('.filter-label');

    allTagKeys.forEach(key => {
      const hasTrueValue = songs.some(song => getTagValue(song, key) === true);
      if (!hasTrueValue) return;

      const wrapper = document.createElement('label');
      wrapper.className = 'filter-checkbox';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'filter-tag';
      checkbox.dataset.tag = key;
      checkbox.checked = true;
      checkbox.addEventListener('change', renderTable);

      const span = document.createElement('span');
      span.textContent = key.charAt(0).toUpperCase() + key.slice(1);

      wrapper.appendChild(checkbox);
      wrapper.appendChild(span);
      filtersContainer.appendChild(wrapper);

      tagColumns.push({ key, label: key.charAt(0).toUpperCase() + key.slice(1), type: hasTrueValue ? 'icon' : 'text' });
    });
  }

  function loadSongs() {
    fetch('./songs.json')
      .then(r => r.json())
      .then(data => {
        songs = data;
        buildFilters();
        renderTable();
      })
      .catch(() => {
        document.getElementById('table-body').innerHTML =
          '<tr><td colspan="5" class="error">Failed to load songs. Make sure Jekyll is running.</td></tr>';
      });
  }

  document.getElementById('search-input').addEventListener('input', function() {
    searchQuery = this.value;
    renderTable();
  });

  renderHeader();
  loadSongs();
})();
</script>
