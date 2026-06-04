# Worldcup 2026 · from zero to MVP in 6 days

**Target launch:** Monday before the FIFA World Cup 2026 opener (kickoff Thu).
**Team:** 2 developers + Claude as copilot.
**Outcome:** `worldcup.santehealth.co` live, public, monitored.

---

## What we ship

A daily risk-monitoring product covering all **16 FIFA World Cup 2026 host
cities**, recomputed every 24 h, with opt-in delivery.

### Features in scope

| # | Feature | Surface |
|---|---|---|
| F1  | **16 host-city dashboard** with filters by city / disease class / date range | `worldcup.santehealth.co/cities` |
| F2  | **Per-city detail page** — Santé Index score, 5-component breakdown, 28-day timeline, LLM-generated brief | `…/cities/<city-slug>` |
| F3  | **Santé Index v0** — composite risk score (0–100) recomputed every 24 h | computed server-side, exposed via API |
| F4  | **Daily LLM brief** — 200-word epidemiological brief per city, refreshed daily | rendered inline; also bundled in digests |
| F5  | **Public landing page** with subscribe form | `worldcup.santehealth.co/` |
| F6  | **Email opt-in + daily digest** (per-user selected cities) | Resend |
| F7  | **SMS opt-in + daily digest** (top-line, max 3 cities/user) | Twilio |
| F8  | **Press kit page** — pitch summary, screenshots, contact | `…/press` |
| F9  | **Public API** — JSON endpoints for cities + per-city briefs | `…/api/cities`, `…/api/cities/<slug>` |
| F10 | **Privacy / terms page** (LGPD compliant) | `…/privacy` |

### Features **deliberately not in scope** (cut to fit 6 days)

- Persona-specific dashboards (FIFA Ops / Reinsurance / Sponsor / Public Health) — the demo deck at `/worldcup-2026/` already covers this for the pitch.
- WhatsApp citizen bot — Meta template approval ≥ 5 days, doesn't fit.
- 12-dimension P1–P12 model — Santé Index v0 ships 5 components only.
- Real R_t / forecast — we do not promise prediction, only a watching signal.
- PT-BR translation — EN-only on launch.
- Hantawatch expansion — current state is sufficient for credibility.
- Mobile app — responsive web only.
- WebSockets / real-time — 24 h refresh is the product cadence.

---

## Stack — locked-in decisions

| Layer | Choice | Why |
|---|---|---|
| Backend | Flask (existing app, new blueprint `worldcup_index_bp`) | Reuses auth, deploy, monitoring |
| Data store | DuckDB single file at `/var/lib/sante/scores.duckdb` | Zero ops, 16 cities × 28 days fits in memory |
| Ingestion | Python scripts + systemd timer (every 6 h) | No queue/Airflow needed for this scale |
| Frontend | Jinja templates + Tailwind (already in `base.html`) + Alpine.js + Chart.js via CDN | No build step, no npm |
| LLM | Existing `services/report_generator.py` (Gemini Flash default, OpenAI fallback) configured via `/admin/settings` | Already wired |
| Email | Resend | 100/day free, 3000/mo free tier |
| SMS  | Twilio (replaces WhatsApp; templates aren't ready in time) | Trial credit + per-message billing |
| Analytics | Plausible (or self-hosted Umami) | LGPD-clean, cookie-banner-free |
| Errors | Sentry free tier | Up to 5k errors/mo |
| Uptime | UptimeRobot free | 5-min polling, 50 monitors |
| URL | `worldcup.santehealth.co` (new subdomain) | `santehealth.co` root stays on Wix |

### Santé Index v0 — model card

```
score(city, day) = 100 × sigmoid(
    0.30 · z_28d(news_outbreak_mentions_7d)      # GDELT events API
  + 0.25 · z_28d(disease_search_interest_7d)     # Google Trends per city
  + 0.20 · z_28d(weather_anomaly_7d)             # Open-Meteo daily
  + 0.15 · z_28d(international_arrivals_7d)      # OpenSky arrivals at IATA airport
  + 0.10 · official_alerts_active                # WHO DON + CDC HAN + PAHO (binary)
)
```

- **z_28d** = z-score against the last 28 days of the *same city* (no cross-city competition).
- **Not a forecast.** Marketed as a watching index. Disclaimer published on the dashboard and in every brief.

---

## Prerequisites (each developer)

1. SSH access to the EC2 host (own key) with `ubuntu` user authorization.
2. Push rights on `github.com/rfapo/sante-flask-mvc`.
3. Local Python 3.12 + `git`.
4. Access to the shared secrets store (1Password / shared vault) for: `RESEND_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, `SENTRY_DSN`, `GEMINI_API_KEY`, `AWS_S3_BUCKET` for backups.
5. Authorized to publish a DNS record on `santehealth.co` (or hand-off contact).

All secrets stay in `/etc/sante/secrets.env` on the EC2 host (mode 0640, owner `ubuntu:www-data`) and are referenced by env-var inside the Flask process and the systemd timers. **Nothing in this repo, nothing in git, ever.**

---

## D1 · Foundation

### Tasks

1. Add deps to the venv on EC2: `duckdb`, `pytrends`, `requests-cache`, `resend`, `twilio`, `sentry-sdk`, `tenacity`, `feedparser`, `apscheduler`. Update `requirements.txt`, commit.
2. Create directories on the EC2 host: `/var/lib/sante`, `/var/log/sante`, `/etc/sante`. Owners: `ubuntu` (data + log), `root:ubuntu` mode 0640 (secrets).
3. Create the `worldcup_index_bp` Flask blueprint at `controllers/worldcup_index.py` with placeholder routes mounted under `/worldcup-2026` (landing, `/cities`, `/cities/<slug>`, `/api/cities`, `/api/cities/<slug>`).
4. Create the DuckDB schema in `services/sante_index/schema.sql` and a one-shot `services/sante_index/migrate.py` to (re-)create tables: `cities`, `signals_raw`, `signals_daily`, `scores`, `briefs`, `optins_email`, `optins_sms`, `cost_log`.
5. Create `services/sante_index/cities_seed.py` + `data/host_cities.json` (16 cities with `slug`, `name`, `country`, `lat`, `lon`, `timezone`, `airport_iata`, `disease_keywords`).
6. Implement `services/sante_index/ingest/gdelt.py` — GDELT 2.0 events API, per `(city, disease)` × last 24 h, counts hits and writes to `signals_raw`. CLI: `python -m services.sante_index.ingest.gdelt --backfill 28`.
7. Implement `services/sante_index/ingest/google_trends.py` — pytrends with `requests-cache` to avoid rate-limit. Same CLI shape.
8. Create the new subdomain DNS record: `CNAME worldcup.santehealth.co → demo.santehealth.co` (or A-record direct to EC2 IP). TLS via certbot on the EC2 nginx config.
9. Verify Resend domain auth (1 TXT record on `santehealth.co`). Generate API key, store in `/etc/sante/secrets.env`.
10. Set up Twilio trial account, verify the sender phone, store SID + token + from-number in `/etc/sante/secrets.env`.
11. Write three low-fi wireframes (landing, dashboard, city detail) and pin in the team's shared doc.
12. Draft launch copy: hero (≤15 words), Santé Index v0 disclaimer (≤40 words), email + SMS confirmation templates.

### Acceptance

- `python -m services.sante_index.ingest.gdelt --backfill 28` populates 16 × 28 rows in `signals_raw`.
- Same for Google Trends.
- `https://worldcup.santehealth.co/` returns a 200 (blank scaffold is fine).
- Resend test email lands in two team inboxes.
- Twilio test SMS lands on the verified phone.
- Wireframes signed off.

---

## D2 · All data sources + score computation

### Tasks

13. Implement `services/sante_index/ingest/open_meteo.py` — fetch daily temp + humidity 7-day window per city via Open-Meteo (free, no auth).
14. Implement `services/sante_index/ingest/opensky.py` — count arrivals per airport for the last 24 h. Fallback: hardcoded seasonal baseline if rate-limited.
15. Implement `services/sante_index/ingest/health_alerts.py` — parse WHO DON RSS, CDC HAN RSS, PAHO PHE RSS via `feedparser`. Tag relevant ones to a host city by country / keyword match.
16. Implement `services/sante_index/score.py` with `compute_score(city_slug, day) -> dict` exactly per the model card above. Use `numpy` for z-scores.
17. Add `services/sante_index/jobs/refresh_all.py` orchestrator: for each city, for each disease keyword, run all 5 ingestion sources for the day, then `compute_score`, write to `scores` table.
18. Backfill last 28 days for all 16 cities. Verify `SELECT count(*) FROM scores` returns 448.
19. Sanity check distribution: all scores between 5 and 95, no NaN, no negative.
20. Build `templates/worldcup/landing.html` (Tailwind, mobile-first, hero + opt-in form + 16 city tiles loaded via `/api/cities`).
21. Build `templates/worldcup/dashboard.html` (16-tile grid with filter pills, Alpine.js).
22. Build `templates/worldcup/city_detail.html` skeleton (no data wired yet — placeholders for score, components, timeline, brief).
23. Build `templates/worldcup/_score_badge.html` partial (color-coded badge, 3 bands).

### Acceptance

- 5 ingestion CLIs each backfill 28 days cleanly.
- `SELECT city_slug, date, score FROM scores ORDER BY date DESC LIMIT 16` returns all 16 host cities for today.
- Landing, dashboard, city detail pages render in the browser without server errors.

---

## D3 · LLM brief + frontend wiring

### Tasks

24. Implement `services/sante_index/brief.py` with `generate_brief(city_slug, day) -> str` using `services.report_generator.ReportGenerator` (already supports OpenAI + Gemini per `/admin/settings`).
25. Brief prompt: senior epidemiologist, 180–220 words, must reference the score and its components, must not use forecasting language ("will", "is expected to"), must include 1–2 monitoring actions.
26. Cache: `briefs(city_slug, date, model, text, generated_at, tokens_used)`. Idempotent — never re-generate for the same `(city_slug, date)` unless force-flag set.
27. Add `cost_log` writes per generation (model, prompt tokens, completion tokens, USD estimate).
28. Add the daily orchestrator entry point: `services/sante_index/jobs/daily.py` runs ingest → score → brief, idempotent, safe to re-run.
29. Schedule the daily job via systemd timer: `sante-index-daily.timer` fires at 06:00 UTC, calls `sante-index-daily.service` (oneshot, runs `python -m services.sante_index.jobs.daily`).
30. Implement the public API:
    - `GET /worldcup-2026/api/cities` → list of `{slug, name, country, score, score_delta_24h, lat, lon}`.
    - `GET /worldcup-2026/api/cities/<slug>` → adds `{components, timeline_28d, brief, alerts, computed_at}`.
31. Wire dashboard tiles: Alpine.js fetches the list endpoint on load, renders, sorts.
32. Implement filters client-side: city dropdown, disease pill tabs (Measles / Dengue / Respiratory / Other), date-range slider on the timeline only. Filter state in URL query string.
33. Wire city detail: Chart.js line chart of `timeline_28d.score`, horizontal bar of `components`, brief rendered inline.
34. Mobile responsive pass on all three pages.

### Acceptance

- `GET /worldcup-2026/api/cities` returns 16 entries with valid scores.
- `GET /worldcup-2026/api/cities/mexico-city` returns full detail incl. a non-empty brief.
- Opening `/worldcup-2026/cities/mexico-city` in the browser shows score, components chart, 28-day timeline, today's brief.
- Filters work end-to-end without page reload.

---

## D4 · Opt-in flows + daily digests

### Tasks

35. Implement `controllers/worldcup_index.py` POST handlers:
    - `POST /worldcup-2026/api/optin/email` — body `{email, cities[], consent: true}`. Dedupe on `(email)`. Insert into `optins_email` with `confirmed=false`. Send Resend confirmation email with unsub link.
    - `POST /worldcup-2026/api/optin/sms` — body `{phone_e164, cities[], consent: true}`. Limit `len(cities) ≤ 3`. Send Twilio confirmation SMS. Same flow.
    - `GET /worldcup-2026/api/optin/confirm?token=…` flips `confirmed=true`.
    - `GET /worldcup-2026/api/optin/unsubscribe?token=…` deletes the row.
36. Implement `services/sante_index/jobs/digest_email.py` — at 06:30 UTC, for each confirmed email subscriber, render `templates/email/digest.html` (table-based HTML for Outlook compatibility) with their selected cities + today's score + delta + 1-line summary. Batch send via Resend.
37. Implement `services/sante_index/jobs/digest_sms.py` — at 06:35 UTC, for each confirmed SMS subscriber, render a 140-char message: `Santé · 09/Jun · MEX 78↑ MIA 64→ HOU 52↑ · https://worldcup.santehealth.co`. Send via Twilio.
38. Schedule both digest jobs via systemd timers (`sante-digest-email.timer`, `sante-digest-sms.timer`).
39. Add opt-in forms to `landing.html` and `city_detail.html`. Use a single Alpine.js modal component shared across pages.
40. Email form: email input + city multi-select (default = all 16). SMS form: phone (E.164) + city multi-select (capped client-side at 3 — display "Pick up to 3 cities").
41. Build `templates/email/digest.html` and `templates/email/confirm.html` (table layout, inline CSS, alt text, plain-text fallback in the same Resend call).
42. Build `templates/worldcup/privacy.html` — minimal LGPD-compliant page (controller name, data collected, retention, contact, withdrawal procedure). Link it from every form + every email footer.

### Acceptance

- Email opt-in test: form submit → confirmation email arrives → click confirm → row flips to `confirmed=true`.
- SMS opt-in test: same flow on a verified Twilio number.
- A manual run of `digest_email.py` and `digest_sms.py` delivers digests to two test subscribers covering distinct city lists.
- Unsubscribe links work end-to-end.

---

## D5 · Reliability + monitoring + outreach prep

### Tasks

43. Initialize Sentry in `app.py` and in every cron entry point (`integrations=[FlaskIntegration()]` + `before_send` filter to drop noisy 404s).
44. Wrap every external HTTP call (GDELT, Trends, Open-Meteo, OpenSky, RSS, Resend, Twilio, LLM provider) with `tenacity` retry: max 3 attempts, exponential backoff, jitter.
45. Implement "stale flag" fallback: if a component fails after retries, reuse the last known value and mark the component `stale=true`. The dashboard renders `⚠ source N stale` next to the score; the brief prompt is told which component is stale.
46. Implement LLM cost guard: query `cost_log` for the last 24 h. If sum > $20, the daily job uses a template-only brief (no LLM call) and posts a Sentry warning.
47. Configure UptimeRobot monitors: `/`, `/cities`, `/api/cities`, `/api/cities/mexico-city`, `/api/health` (add the health endpoint returning 200 + DB ping). 5-min interval.
48. Daily backup: cron at 03:00 UTC runs `aws s3 cp /var/lib/sante/scores.duckdb s3://$AWS_S3_BUCKET/backups/$(date +%F).duckdb`. 14-day retention via lifecycle rule.
49. Run an end-to-end 24-h cycle simulation with synthetic data — verify no crash, no Sentry error, all 16 cities have score + brief.
50. Build `templates/worldcup/press.html` — 1-paragraph pitch, 3 screenshots, 1 short factsheet (PDF or inline), contact email.
51. Generate OG / Twitter card images (1200×630 PNG) for landing, dashboard, press. Wire `<meta>` tags.
52. Install Plausible script on all four pages. Verify events arriving.
53. Draft outreach assets:
    - Tweet for launch day (with screenshot).
    - LinkedIn post (longer-form, includes the Santé Index v0 disclaimer).
    - Three warm-intro email templates: host-city PH director, reinsurance head, sponsor brand activation lead.
54. Compile a 50-row Sheet of target leads (LinkedIn URL, email if known, persona, suggested message variant).

### Acceptance

- Simulated 24-h cycle passes without intervention.
- Sentry receives at most 0 errors / handled-only events in the last 4 h.
- All 5 UptimeRobot checks are green for 60 minutes continuous.
- One backup is verified retrievable from S3.
- OG card preview validated via Twitter Card Validator + LinkedIn Post Inspector.
- Lead Sheet reviewed; tweet + LinkedIn post + 3 email templates ready to send.

---

## D6 · Soft launch

### Morning (≤ 09:00 UTC)

55. Switch the systemd timers from manual to enabled (`systemctl enable --now sante-index-daily.timer sante-digest-email.timer sante-digest-sms.timer`).
56. First production run logs reviewed (Sentry + journal). All 16 cities have a fresh score, all 16 have a non-empty brief, today's backup is in S3.
57. Run the pre-launch checklist (below). Every item must be ✓ before going public.

### Pre-launch checklist

```
[ ] DNS  worldcup.santehealth.co resolves to the EC2 host
[ ] HTTPS cert valid (Let's Encrypt, ≥ 30 days to expiry)
[ ] Landing page renders on iPhone-14 viewport (Chrome devtools)
[ ] 16 cities have score AND non-empty brief AND today's components
[ ] Opt-in email: form submit → confirm email → DB row confirmed
[ ] Opt-in SMS:   form submit → confirm SMS   → DB row confirmed
[ ] Daily digest jobs registered:  `systemctl list-timers | grep sante`
[ ] Sentry: 0 unhandled errors in the last 4 h
[ ] UptimeRobot: 5 checks green for ≥ 60 minutes
[ ] Backup: at least one S3 file exists for today's date
[ ] LLM cost: < $5 in the last 24 h
[ ] /privacy reachable and linked from every form + every email footer
[ ] Plausible: events arriving from all four pages
[ ] Press kit at /worldcup-2026/press loads
```

### Afternoon

58. Mirelle / Onicio send the 50 warm-intro emails.
59. Publish the launch tweet and LinkedIn post (with screenshot of the dashboard).
60. Monitor Plausible in real time. Respond to inbound (DMs, replies) within 15 min.

### Evening

61. War room open until 22:00 local. Triage any Sentry error within 30 min.
62. Snapshot metrics at 22:00: unique visitors, email signups, SMS signups, top 3 cities by views, Sentry error count.

### Acceptance · production

`worldcup.santehealth.co` is public, monitored, with today's brief refreshed for all 16 host cities. Email and SMS digests are scheduled to fire at 06:30 / 06:35 UTC tomorrow. Press kit and Mirelle's outreach are out.

---

## Rollback plan

| Scenario | Action |
|---|---|
| Critical: score computation fails for all cities | Re-run with `--use-fallback-weights` (3 hardcoded country buckets); delay soft-launch 24 h |
| Email digest fails on Resend | Ship without email digest; banner on landing reads "subscribe coming Wed" |
| SMS digest fails on Twilio | Same — banner; SMS opt-in form remains but says "queued" |
| Brief generation fails for some cities | Use template-only brief; flag city as `brief_unavailable` in the UI |
| Cosmetic only | Ship as-is, hotfix within 24 h |

---

## Costs (first month, expected)

| Item | Expected |
|---|---|
| EC2 (existing) | $0 incremental |
| Gemini Flash · 16 × 30 × ~3 k tokens | ≈ $1 |
| OpenAI fallback | ≈ $5 |
| Resend · 100/day free, then $20/mo | $0–20 |
| Twilio · capped at 200 active SMS subscribers, ≤ 3 cities each | ≈ $45 |
| Sentry · free tier | $0 |
| UptimeRobot · free | $0 |
| Plausible (or self-host Umami) | $0–9 |
| AWS S3 backup (negligible volume) | < $1 |
| **Total** | **~$70/month burn** |

---

## After launch (D7 onwards)

- Daily metrics review every morning (visitors, signups, top cities, Sentry).
- Press push only after D7 stability is confirmed.
- Week 2 follow-ups: WhatsApp template submission, PT-BR translation, persona-tuned dashboards.

---

*Single source of truth for the build. Update via PR. Daily standups reference task numbers above.*
