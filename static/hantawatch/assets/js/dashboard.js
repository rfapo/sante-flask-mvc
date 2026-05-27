/* ── Config ─────────────────────────────────────────── */
const RAW = 'https://raw.githubusercontent.com/kraemer-lab/Hondius_hantavirus_h2026/main/data';
const URLS = {
  linelist: `${RAW}/linelist/2026_hantavirus.csv`,
  news:     `${RAW}/news%20sources/hantavirus_articles.json`,
};
/* Cache-bust: append timestamp so neither browser cache nor GitHub's Fastly
   CDN (cache-control max-age=300) ever serves a stale copy on reload. */
const bust = (u) => u + (u.includes('?') ? '&' : '?') + 't=' + Date.now();

/* ── Chart palette (no cyan — crimson + teal + amber) ── */
const C = {
  RED:    '#dc3043',
  TEAL:   '#0d9488',
  AMBER:  '#d97706',
  SLATE:  '#475569',
  BLUE:   '#2563eb',
  PURPLE: '#7c3aed',
  TEXT2:  '#8a94ab',
  GRID:   'rgba(255,255,255,.06)',
};

Chart.defaults.color          = '#8a94ab';
Chart.defaults.borderColor    = C.GRID;
Chart.defaults.font.family    = "'DM Sans', sans-serif";
Chart.defaults.font.size      = 11;
Chart.defaults.plugins.legend.labels.boxWidth = 10;
Chart.defaults.plugins.legend.labels.padding  = 12;

/* ── State ──────────────────────────────────────────── */
let allCases = [], allNews = [], leafletMap = null, markers = null;

/* ── Utils ──────────────────────────────────────────── */
const $  = id => document.getElementById(id);
const norm = s => (s || '').toString().trim().toLowerCase();
const esc  = s => (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

function progress(p) { $('loadFill').style.width = p + '%'; }

function fmtDate(s) {
  if (!s || s === 'NA' || s === 'na') return '—';
  const d = new Date(s);
  if (isNaN(d)) return s;
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
}

function animCount(el, target, dur = 1000) {
  if (!el) return;
  const start = performance.now();
  const ease  = t => 1 - Math.pow(1 - t, 3);
  function step(now) {
    const t = Math.min((now - start) / dur, 1);
    el.textContent = Math.round(ease(t) * target);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* ── Routing ────────────────────────────────────────── */
function switchSection(sec) {
  document.querySelectorAll('.sb-link').forEach(a => {
    a.classList.toggle('active', a.dataset.section === sec);
  });
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const el = $(sec);
  if (el) el.classList.add('active');
  const link = document.querySelector(`.sb-link[data-section="${sec}"]`);
  $('tbTitle').textContent = link ? link.textContent.trim() : sec;
  if (sec === 'map' && allCases.length) setTimeout(renderMap, 80);
  history.replaceState(null, '', '#' + sec);
}

document.querySelectorAll('.sb-link').forEach(a => {
  a.addEventListener('click', e => { e.preventDefault(); switchSection(a.dataset.section); });
});

function routeHash() {
  const h = window.location.hash.slice(1);
  if (h && $(h)) switchSection(h); else switchSection('overview');
}
window.addEventListener('hashchange', routeHash);

/* ── Sidebar toggle ─────────────────────────────────── */
$('sbToggle').addEventListener('click', () => {
  const sb = $('sidebar');
  if (window.innerWidth <= 768) sb.classList.toggle('open');
  else sb.classList.toggle('collapsed');
});

/* ── Dates ──────────────────────────────────────────── */
const ymd = (() => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
})();
if ($('citeDate')) $('citeDate').textContent = ymd;
if ($('sbDate'))   $('sbDate').textContent   = ymd;

/* ── KPI population ─────────────────────────────────── */
function populateKPIs(cases) {
  const confirmed = cases.filter(c => norm(c.status) === 'confirmed').length;
  const probable  = cases.filter(c => norm(c.status) === 'probable').length;
  const activeCases = confirmed + probable;
  const deaths   = cases.filter(c =>
    /death|deceas|died/i.test(c.outcome || '')).length;
  const nats = new Set(cases.map(c => (c.nationality || '').trim()).filter(Boolean));
  const cfr  = activeCases ? ((deaths / activeCases) * 100).toFixed(1) : '—';

  // Topbar
  animCount($('kCases'),     activeCases, 800);
  animCount($('kDeaths'),    deaths,      800);
  animCount($('kCountries'), nats.size,   800);

  // Overview panel
  animCount($('ovCases'),     activeCases, 1100);
  animCount($('ovDeaths'),    deaths,      1100);
  animCount($('ovConfirmed'), confirmed,   1100);
  animCount($('ovNat'),       nats.size,   1100);
  if ($('ovCFR')) $('ovCFR').textContent = `CFR: ${cfr}%`;
}

/* ── Chart helpers ──────────────────────────────────── */
function donut(id, labels, data, colors) {
  const el = $(id);
  if (!el) return;
  new Chart(el, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data, backgroundColor: colors,
        borderColor: '#0b1018', borderWidth: 2, hoverOffset: 4,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } },
      animation: { animateRotate: true, duration: 900 },
    }
  });
}

/* ── Build all charts ───────────────────────────────── */
function buildCharts(cases) {
  /* Timeline */
  const dc = {};
  cases.forEach(c => {
    const d = (c.symptom_onset || '').slice(0, 10);
    if (d && d !== 'NA') dc[d] = (dc[d] || 0) + 1;
  });
  const dates = Object.keys(dc).sort();
  let cum = 0;
  const cumData = dates.map(d => { cum += dc[d]; return cum; });

  new Chart($('chartTimeline'), {
    type: 'line',
    data: {
      labels: dates.map(fmtDate),
      datasets: [
        {
          label: 'New cases', data: dates.map(d => dc[d]),
          borderColor: C.TEAL, backgroundColor: 'rgba(13,148,136,.09)',
          fill: true, tension: .4, pointRadius: 3, pointHoverRadius: 5,
          yAxisID: 'y',
        },
        {
          label: 'Cumulative', data: cumData,
          borderColor: C.AMBER, backgroundColor: 'transparent',
          fill: false, tension: .4, pointRadius: 0, borderDash: [5,4],
          yAxisID: 'y2',
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: { grid: { color: C.GRID }, ticks: { maxRotation: 30, font: { size: 9 } } },
        y: { grid: { color: C.GRID }, title: { display: true, text: 'New', font: { size: 9 } } },
        y2: {
          position: 'right', grid: { drawOnChartArea: false },
          title: { display: true, text: 'Cumul.', font: { size: 9 } }
        }
      },
      plugins: { legend: { position: 'top', labels: { font: { size: 10 } } } },
      animation: { duration: 900, easing: 'easeOutQuart' },
    }
  });

  /* Status */
  const st = {};
  cases.forEach(c => { const v = norm(c.status) || 'unknown'; st[v] = (st[v]||0)+1; });
  donut('chartStatus',
    Object.keys(st).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
    Object.values(st),
    [C.TEAL, C.AMBER, C.SLATE, C.BLUE, C.RED]
  );

  /* Sex */
  const sx = {};
  cases.forEach(c => { const v = norm(c.sex) || 'unknown'; sx[v] = (sx[v]||0)+1; });
  donut('chartSex',
    Object.keys(sx).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
    Object.values(sx),
    [C.BLUE, C.RED, C.SLATE]
  );

  /* Outcome */
  const oc = {};
  cases.forEach(c => { const v = norm(c.outcome) || 'unknown'; oc[v] = (oc[v]||0)+1; });
  donut('chartOutcome',
    Object.keys(oc).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
    Object.values(oc),
    [C.RED, C.TEAL, C.AMBER, C.SLATE]
  );

  /* Crew */
  const crew = cases.filter(c => norm(c['cruise.crew..y.n.']) === 'y').length;
  const pass = cases.filter(c => norm(c['passenger..y.n.'])   === 'y').length;
  const oth  = Math.max(0, cases.length - crew - pass);
  donut('chartCrew',
    ['Crew', 'Passenger', 'Other'],
    [crew, pass, oth],
    [C.PURPLE, C.BLUE, C.SLATE]
  );

  /* Nationality bar */
  const nc = {};
  cases.forEach(c => {
    const n = (c.nationality || 'Unknown').trim();
    nc[n] = (nc[n]||0)+1;
  });
  const sorted = Object.entries(nc).sort((a,b) => b[1]-a[1]);
  new Chart($('chartNat'), {
    type: 'bar',
    data: {
      labels: sorted.map(([k]) => k),
      datasets: [{
        data: sorted.map(([,v]) => v),
        backgroundColor: sorted.map((_, i) => i === 0 ? C.RED : 'rgba(220,48,67,.3)'),
        borderRadius: 4, borderSkipped: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 35 } },
        y: { grid: { color: C.GRID }, ticks: { stepSize: 1 } },
      },
      animation: { duration: 900, easing: 'easeOutQuart' },
    }
  });
}

/* ── Badges ─────────────────────────────────────────── */
function statusBadge(s) {
  const n = norm(s);
  const map = { confirmed: 'b-confirmed', probable: 'b-probable', negative: 'b-negative', monitored: 'b-monitored', tested: 'b-tested', suspected: 'b-probable' };
  const cls = map[n] || 'b-na';
  return `<span class="badge ${cls}">${esc(s) || '—'}</span>`;
}

function outcomeBadge(s) {
  const n = norm(s);
  if (/death|deceas|died/.test(n)) return `<span class="badge b-deceased">Deceased</span>`;
  if (/alive|surviv|recov/.test(n)) return `<span class="badge b-alive">Alive</span>`;
  return `<span class="badge b-na">${esc(s) || '—'}</span>`;
}

function roleBadge(c) {
  if (norm(c['cruise.crew..y.n.']) === 'y') return `<span class="badge b-crew">Crew</span>`;
  if (norm(c['passenger..y.n.'])   === 'y') return `<span class="badge b-passenger">Pax</span>`;
  return `<span class="badge b-na">—</span>`;
}

/* ── Line list table ────────────────────────────────── */
function renderTable(data) {
  if ($('listCount')) $('listCount').textContent = `${data.length} case${data.length !== 1 ? 's' : ''}`;
  const tbody = $('caseBody');
  if (!data.length) {
    tbody.innerHTML = '<tr><td colspan="10" class="tbl-loading" style="color:var(--text3)">No cases match.</td></tr>';
    return;
  }
  tbody.innerHTML = data.map(c => `
    <tr>
      <td class="mono" style="color:var(--accent);font-size:.7rem">${esc(c.Gh_ID)||'—'}</td>
      <td>${statusBadge(c.status)}</td>
      <td style="font-size:.75rem">${fmtDate(c.symptom_onset)}</td>
      <td>${esc(c.age)||'—'}</td>
      <td>${esc(c.sex)||'—'}</td>
      <td>${esc(c.nationality)||'—'}</td>
      <td>${outcomeBadge(c.outcome)}</td>
      <td>${roleBadge(c)}</td>
      <td style="max-width:110px;overflow:hidden;text-overflow:ellipsis">${esc(c.travel_from)||'—'}</td>
      <td style="font-size:.72rem">${fmtDate(c.confirmation_date)}</td>
    </tr>`
  ).join('');
}

function setupTableFilters() {
  function apply() {
    const q  = norm($('listSearch').value);
    const st = norm($('fStatus').value);
    const oc = norm($('fOutcome').value);
    const data = allCases.filter(c => {
      const mq = !q || Object.values(c).some(v => norm(v).includes(q));
      const ms = !st || norm(c.status) === st;
      const mo = !oc ||
        (oc === 'deceased' && /death|deceas|died/.test(norm(c.outcome))) ||
        (oc === 'alive'    && /alive|surviv|recov/.test(norm(c.outcome)));
      return mq && ms && mo;
    });
    renderTable(data);
  }
  $('listSearch').addEventListener('input', apply);
  $('fStatus').addEventListener('change', apply);
  $('fOutcome').addEventListener('change', apply);
  renderTable(allCases);
}

/* ── Map ────────────────────────────────────────────── */
const GEO = {
  'Netherlands': [52.37, 4.90], 'South Africa': [-33.92, 18.42],
  'Switzerland': [47.38, 8.54], 'Singapore':    [1.35, 103.82],
  'Spain':       [40.42, -3.70],'France':        [48.86, 2.35],
  'Germany':     [52.52, 13.40],'Argentina':     [-34.60, -58.38],
  'British':     [51.51, -.13], 'Dutch':         [52.37, 4.90],
  'German':      [52.52, 13.40],'French':        [48.86, 2.35],
  'Spanish':     [40.42, -3.70],'Swiss':         [47.38, 8.54],
  'Singaporean': [1.35, 103.82],'American':      [38.90, -77.04],
  'Argentinian': [-34.60, -58.38], 'Chilean': [-33.45, -70.67],
};

function lookupCoords(c) {
  const fields = [c.nationality, c.travel_from, c.travel_to];
  for (const f of fields) {
    if (!f) continue;
    for (const [key, coords] of Object.entries(GEO)) {
      if ((f || '').toLowerCase().includes(key.toLowerCase())) return coords;
    }
  }
  return null;
}

function renderMap() {
  const mapEl = document.getElementById('leafletMap');
  if (!mapEl) return;

  if (!leafletMap) {
    leafletMap = L.map('leafletMap', { zoomControl: true }).setView([20, 10], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors', maxZoom: 12,
      subdomains: 'abc',
    }).addTo(leafletMap);
    markers = L.layerGroup().addTo(leafletMap);

    /* Keep the map in sync with its container — when the Geography panel
       toggles from display:none → block, Leaflet must be told to recompute
       tile coverage, otherwise only a sliver of the world renders. */
    const observer = new ResizeObserver(() => {
      if (leafletMap) leafletMap.invalidateSize(false);
    });
    observer.observe(mapEl);
  } else {
    markers.clearLayers();
  }

  const countryCounts = {};

  allCases.forEach(c => {
    const coords = lookupCoords(c);
    if (!coords) return;
    const isDead = /death|deceas|died/i.test(c.outcome || '');
    const isConf = norm(c.status) === 'confirmed';
    const col = isDead ? '#dc3043' : (isConf ? '#0d9488' : '#475569');
    const marker = L.circleMarker(
      [coords[0] + (Math.random()-.5)*.5, coords[1] + (Math.random()-.5)*.5],
      { radius: 7, color: col, fillColor: col, fillOpacity: .65, weight: 1.5 }
    );
    marker.bindPopup(`
      <div style="font-family:'DM Sans',sans-serif">
        <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#4d5a70;margin-bottom:.3rem">${esc(c.Gh_ID)||''}</div>
        <div style="font-weight:600;margin-bottom:.2rem">${esc(c.nationality)||'—'} · ${esc(c.sex)||'—'} · ${esc(c.age)||'—'}y</div>
        <div style="font-size:.78rem;color:#8a94ab">Status: ${esc(c.status)||'—'}</div>
        <div style="font-size:.78rem;color:#8a94ab">Outcome: ${esc(c.outcome)||'—'}</div>
        <div style="font-size:.78rem;color:#8a94ab">Onset: ${fmtDate(c.symptom_onset)}</div>
      </div>`);
    markers.addLayer(marker);

    const key = (c.nationality || c.travel_from || 'Unknown').split(/[,;/]/)[0].trim();
    countryCounts[key] = (countryCounts[key]||0) + 1;
  });

  const cl = $('countryList');
  if (cl) {
    cl.innerHTML = Object.entries(countryCounts)
      .sort((a,b) => b[1]-a[1])
      .map(([name, n]) => `
        <div class="cy-row">
          <span class="cy-name">${esc(name)}</span>
          <span class="cy-cnt">${n}</span>
        </div>`).join('');
  }

  // Force map to recalculate size after panel becomes visible.
  // Multiple ticks: the panel may still be animating in the first 100ms.
  [50, 200, 600].forEach(delay =>
    setTimeout(() => leafletMap && leafletMap.invalidateSize(false), delay)
  );
}

/* ── News feed ──────────────────────────────────────── */
function renderNews(articles) {
  const feed = $('newsFeed');
  if (!articles.length) { feed.innerHTML = '<div style="color:var(--text3);padding:2rem">No articles found.</div>'; return; }
  $('newsCount').textContent = `${articles.length} article${articles.length !== 1 ? 's' : ''}`;
  feed.innerHTML = articles.slice(0, 60).map((a, i) => {
    const snippet = (a.text || '').slice(0, 220);
    const date    = fmtDate(a.publish_date || '');
    const source  = esc(a.media_name || '');
    const title   = esc(a.title || 'Untitled');
    const url     = esc(a.url  || '#');
    return `
      <div class="news-card" style="animation-delay:${(i%12)*35}ms">
        <div class="nc-meta">
          ${source ? `<span class="nc-source">${source}</span>` : ''}
          <span>${date}</span>
        </div>
        <p class="nc-title">${title}</p>
        ${snippet ? `<p class="nc-body">${esc(snippet)}…</p>` : ''}
        <a href="${url}" target="_blank" rel="noopener" class="nc-link">Read article →</a>
      </div>`;
  }).join('');
}

function setupNewsFilters() {
  function apply() {
    const q    = norm($('newsSearch').value);
    const lang = $('newsLang').value;
    const sort = $('newsSort').value;
    let filtered = allNews.filter(a =>
      (!q    || norm(a.title).includes(q) || norm(a.text).includes(q)) &&
      (!lang || (a.language||'').toLowerCase() === lang)
    );
    filtered.sort((a,b) => sort === 'oldest'
      ? (a.publish_date||'') < (b.publish_date||'') ? -1 : 1
      : (a.publish_date||'') > (b.publish_date||'') ? -1 : 1
    );
    renderNews(filtered);
  }
  $('newsSearch').addEventListener('input', apply);
  $('newsLang').addEventListener('change', apply);
  $('newsSort').addEventListener('change', apply);
}

/* ── Data loaders ───────────────────────────────────── */
/* Map the kraemer-lab Gh CSV schema → the lowercase shape this dashboard uses.
   The source schema uses Pascal_Snake_Case ("Case_status", "Nationality") and
   space-containing names ("WHO_case number", "Location_Admin 0"); we normalize
   once at load time so the rest of the code keeps reading c.status, c.age, etc. */
function mapRow(r) {
  const mapped = {
    id:                 r['Gh_ID'] || r['WHO_case number'] || '',
    status:             r['Case_status'] || '',
    outcome:            r['Outcome'] || '',
    nationality:        r['Nationality'] || '',
    age:                r['Age'] || '',
    sex:                r['Gender'] || '',
    travel_from:        r['Travel_from'] || '',
    travel_to:          r['Travel_to'] || '',
    symptom_onset:      r['Date_onset'] || '',
    confirmation_date:  r['Date_confirmation'] || '',
    cruise_crew:        r['Cruise_crew'] || '',
    cruise_passenger:   r['Cruise_passenger guest'] || r['Cruise_passenger'] || '',
    location_country:   r['Location_Admin 0'] || '',
    location_admin1:    r['Location_Admin 1'] || '',
    location_admin2:    r['Location_Admin 2'] || '',
    hospitalised:       r['Hospitalised'] || '',
    intensive_care:     r['Intensive_care'] || '',
    isolated:           r['Isolated'] || '',
    symptoms:           r['Symptoms'] || '',
    /* Keep originals available for any reader that asks by source-column name. */
    ...r,
  };
  /* Legacy R-style keys still referenced by older parts of dashboard.js
     (chartCrew + transport badge). Defined here so we don't have to touch
     those readers — they keep working unchanged. */
  mapped['cruise.crew..y.n.']  = mapped.cruise_crew;
  mapped['passenger..y.n.']    = mapped.cruise_passenger;
  return mapped;
}

function loadLinelist() {
  return new Promise(res => {
    /* No downloadRequestHeaders here: any custom header triggers a CORS
       preflight that raw.githubusercontent.com doesn't satisfy. The
       ?t=<ts> query string is enough to defeat the browser + Fastly cache. */
    Papa.parse(bust(URLS.linelist), {
      download: true, header: true, skipEmptyLines: true,
      complete: r => res({ ok: true, data: r.data.map(mapRow) }),
      error:    () => res({ ok: false, data: [] }),
    });
  });
}

function showDataBanner(msg) {
  const b = document.getElementById('dataBanner');
  if (!b) return;
  b.querySelector('.db-msg').textContent = msg;
  b.hidden = false;
}

async function loadNews() {
  try {
    const r = await fetch(bust(URLS.news), { cache: 'no-store' });
    if (!r.ok) return [];
    const parsed = JSON.parse(await r.text());
    return Array.isArray(parsed) ? parsed : (parsed.articles || []);
  } catch { return []; }
}

/* ── Boot ───────────────────────────────────────────── */
async function init() {
  progress(10);
  const [linelistResult, news] = await Promise.all([loadLinelist(), loadNews()]);
  progress(75);

  if (!linelistResult.ok) {
    showDataBanner(
      'Line list data could not be loaded — the source file may have moved or GitHub is unreachable. Charts will be empty until data is available.'
    );
  }

  allCases = linelistResult.data;
  allNews  = (Array.isArray(news) ? news : []).sort((a,b) =>
    (a.publish_date||'') > (b.publish_date||'') ? -1 : 1
  );

  populateKPIs(allCases);
  buildCharts(allCases);
  setupTableFilters();
  setupNewsFilters();
  renderNews(allNews);

  // Map lazy-init on first visit
  document.querySelector('[data-section="map"]').addEventListener('click', () => {
    setTimeout(renderMap, 80);
  }, { once: true });

  progress(100);
  setTimeout(() => { $('loadFill').style.width = '0'; }, 600);

  renderUpdatedStamp(allCases.length);

  // Route to hash after data ready
  routeHash();
}

/* "Last updated · Refresh" pill — fixed-position bottom-right so it doesn't
   collide with sidebar citation or topbar KPIs. */
function renderUpdatedStamp(rowCount) {
  let host = document.getElementById('updatedStamp');
  if (!host) {
    host = document.createElement('div');
    host.id = 'updatedStamp';
    host.style.cssText = [
      'position:fixed', 'bottom:14px', 'right:14px', 'z-index:9999',
      'display:inline-flex', 'gap:8px', 'align-items:center',
      'background:rgba(11,16,24,0.92)', 'backdrop-filter:blur(6px)',
      'border:1px solid rgba(255,255,255,0.08)', 'border-radius:999px',
      'padding:6px 14px',
      'font-family:"DM Mono",monospace', 'font-size:11px', 'color:#8a94ab',
      'box-shadow:0 6px 24px rgba(0,0,0,0.4)',
    ].join(';');
    document.body.appendChild(host);
  }
  const stamp = new Date().toLocaleString();
  host.innerHTML =
    `<span style="color:#0d9488">●</span>` +
    `<span>${stamp} · ${rowCount} cases</span>` +
    `<button id="updatedRefresh" style="background:#0d9488;color:#fff;border:0;border-radius:999px;padding:3px 10px;font-size:11px;font-family:inherit;cursor:pointer;">↻ Refresh</button>`;
  document.getElementById('updatedRefresh').addEventListener('click', () => location.reload());
}

init();
