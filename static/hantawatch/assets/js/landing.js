/* ── GSAP setup ─────────────────────────────────────── */
gsap.registerPlugin(ScrollTrigger);

/* ── Text scramble effect ───────────────────────────── */
class Scramble {
  constructor(el) {
    this.el = el;
    this.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    this.frame = 0;
    this.queue = [];
    this.raf = null;
    this.update = this.update.bind(this);
  }
  run(text) {
    cancelAnimationFrame(this.raf);
    const old = this.el.textContent;
    const len = Math.max(old.length, text.length);
    this.queue = [];
    for (let i = 0; i < len; i++) {
      const from  = old[i] || '';
      const to    = text[i] || '';
      const start = Math.floor(Math.random() * 12);
      const end   = start + Math.floor(Math.random() * 14) + 6;
      this.queue.push({ from, to, start, end, char: '' });
    }
    this.frame = 0;
    this.update();
  }
  update() {
    let out = '', done = 0;
    for (let i = 0; i < this.queue.length; i++) {
      const { to, start, end } = this.queue[i];
      if (this.frame >= end) {
        done++;
        out += to;
      } else if (this.frame >= start) {
        if (!this.queue[i].char || Math.random() < .28) {
          this.queue[i].char = this.chars[Math.floor(Math.random() * this.chars.length)];
        }
        out += `<span class="s-char">${this.queue[i].char}</span>`;
      } else {
        out += this.queue[i].from;
      }
    }
    this.el.innerHTML = out;
    if (done < this.queue.length) {
      this.frame++;
      this.raf = requestAnimationFrame(this.update);
    }
  }
}

/* ── Counter animation ──────────────────────────────── */
function animCount(el, target, suffix, dur = 1100) {
  const start = performance.now();
  const ease  = t => 1 - Math.pow(1 - t, 3);
  function step(now) {
    const t = Math.min((now - start) / dur, 1);
    el.textContent = Math.round(ease(t) * target) + (suffix || '');
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* ── Stat counters — live from CSV ──────────────────── */
(async () => {
  try {
    const res = await fetch('https://raw.githubusercontent.com/kraemer-lab/Hondius_hantavirus_h2026/main/data/linelist/2026_hantavirus.csv');
    if (!res.ok) return;
    const text  = await res.text();
    const rows  = text.trim().split('\n');
    const heads = rows[0].split(',').map(h => h.trim().replace(/"/g, '').toLowerCase());
    const si = heads.indexOf('status');
    const oi = heads.indexOf('outcome');
    const ni = heads.indexOf('nationality');
    let confirmed = 0, probable = 0, deaths = 0;
    const nats = new Set();
    for (let r = 1; r < rows.length; r++) {
      const cols = rows[r].split(',');
      const st  = (cols[si] || '').trim().replace(/"/g, '').toLowerCase();
      const out = (cols[oi] || '').trim().replace(/"/g, '').toLowerCase();
      const nat = (cols[ni] || '').trim().replace(/"/g, '');
      if (st === 'confirmed') confirmed++;
      if (st === 'probable')  probable++;
      if (/death|deceas|died/.test(out)) deaths++;
      if (nat) nats.add(nat);
    }
    const ce = document.getElementById('statCases');
    const de = document.getElementById('statDeaths');
    const ne = document.getElementById('statNats');
    if (ce) animCount(ce, confirmed + probable, ce.dataset.suffix, 1200);
    if (de) animCount(de, deaths,               de.dataset.suffix, 1200);
    if (ne) animCount(ne, nats.size,            ne.dataset.suffix, 1200);
  } catch (_) { /* silent fail — stats stay as — */ }
})();

/* ── Scramble hero lines on load ────────────────────── */
const lines = [
  { el: document.getElementById('scramble0'), text: 'HANTAVIRUS' },
  { el: document.getElementById('scramble1'), text: '2026 OUTBREAK' },
  { el: document.getElementById('scramble2'), text: 'INTELLIGENCE' },
];

lines.forEach(({ el, text }, i) => {
  if (!el) return;
  el.textContent = '';
  setTimeout(() => {
    const s = new Scramble(el);
    s.run(text);
  }, 300 + i * 180);
});

/* ── GSAP scroll reveals ────────────────────────────── */
document.querySelectorAll('.reveal').forEach(el => {
  gsap.to(el, {
    opacity: 1,
    y: 0,
    duration: .7,
    ease: 'expo.out',
    delay: parseFloat(getComputedStyle(el).getPropertyValue('--delay') || '0') / 1000,
    scrollTrigger: {
      trigger: el,
      start: 'top 88%',
      toggleActions: 'play none none none',
    },
  });
});

/* ── Nav scroll state ───────────────────────────────── */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

/* ── Directional hover glow for buttons ─────────────── */
document.querySelectorAll('.btn-primary, .btn-ghost, .nav-cta, .feed-card').forEach(el => {
  el.addEventListener('mousemove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
});

/* ── Citation date ──────────────────────────────────── */
const now = new Date();
const fmt = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
const d = document.getElementById('citeDate');
if (d) d.textContent = fmt(now);
const s = document.getElementById('syncDate');
if (s) s.textContent = fmt(now);

/* ── Scroll hint fade out on scroll ─────────────────── */
const hint = document.getElementById('scrollHint');
window.addEventListener('scroll', () => {
  if (hint) hint.style.opacity = Math.max(0, 1 - window.scrollY / 200);
}, { passive: true });

/* ── Cursor glow (desktop only) ─────────────────────── */
if (window.matchMedia('(hover:hover) and (pointer:fine)').matches) {
  const glow = Object.assign(document.createElement('div'), {
    style: `position:fixed;pointer-events:none;z-index:9999;width:280px;height:280px;
            border-radius:50%;background:radial-gradient(circle,rgba(220,48,67,.06) 0%,transparent 70%);
            transform:translate(-50%,-50%);transition:opacity .3s;will-change:transform;`
  });
  document.body.appendChild(glow);
  document.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top  = e.clientY + 'px';
  }, { passive: true });
}
