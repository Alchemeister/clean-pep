# PeptideCleanScore — Static Site

**Live URL (after deploy):** `peptidecleanscore.com` or `peptidecleanscore.vercel.app`

A static HTML/CSS comparison site ranking peptide vendors by a **Cleanliness Score (1–10)** based on what their COAs actually prove — not just "99% purity" claims.

## Data Source
Finnrick Analytics public data — 7,466 tests, 212 vendors, 15 products. Last synced: 22 May 2026.
- `finnrick.com/llms.txt` — Machine-readable summary
- `finnrick.com/llms-full.txt` — Full vendor/product tables with real scores/dates
- `finnrick.com/vendors` — Per-vendor detail pages (JS-rendered, manual verification needed)

All data in this site is **public, verifiable, and manually checkable** — no scrapers, no APIs, no purchases, no automated tools.

## Files
```
src/
  index.html         — Homepage (hero, scoreboard, quick product summary)
  retatrutide.html   — Full Retatrutide table (2,778 tests, 173 vendors)
  tirzepatide.html   — Tirzepatide table (1,930 tests, 140 vendors)
  bpc157.html        — BPC-157 + TB-500 tables (551 + 102 tests)
  coa-guide.html     — How to Read a COA guide
  about.html         — About, methodology, full disclaimer
  style.css          — Shared stylesheet (dark mode, mobile-first)
```

## Deploy (Free)

### Vercel (recommended — instant, free, auto SSL)
```bash
# Install vercel CLI if not already
npm i -g vercel

# Deploy
cd src
vercel
# Follow prompts → deploy as "peptide-clean-score"
# Done. Live at https://peptide-clean-score.vercel.app
```

### Netlify (also free)
Drop `src/` folder onto netlify.com/drop — done.

### Any VPS
```bash
cd src && python3 -m http.server 8080
# Or: nginx, apache, caddy — just serve the src/ folder
```

### Custom Domain
Buy peptidecleanscore.com (~$10/year via Namecheap/Porkbun) → point DNS to Vercel/Netlify. Takes 5 minutes.

## Affiliate Setup
Before launch, replace affiliate link placeholders with your actual URLs. Search the HTML files for `[AFFILIATE]` (none present — links are direct to vendor URLs with `?aff=YOURID` style params). Add your affiliate IDs to:
- Paradigm Peptide links
- LiveWell Peptides links
- PS Peptides links
- Ascension links
- Onyx links
- Limitless Biotech links
- Core Peptides links

## Updating Scores
Finnrick updates their data weekly. To refresh:
1. Visit finnrick.com/vendors for each vendor
2. Note new scores + dates
3. Update the HTML table rows
4. Bump the "Data last updated" timestamp
5. Redeploy (`vercel --prod`)

Each table row takes ~2 min to verify and update. Full refresh: ~20 min.

## Traffic Launch (Post Templates)

### Reddit — r/Peptides
```
Title: I built a site ranking peptide vendors by what they ACTUALLY test for (solvents/TFA/metals — not just purity)

Got sick of the same 5 vendor lists. Built PeptideCleanScore — research-use-only, pulls from Finnrick Analytics' public data (7,466 tests, 212 vendors). The only list showing batch dates + multi-lab sources so you know if the data is fresh.

Top Retatrutide: Paradigm Peptide (9/10), Peptide Partners (8/10), Jeep Bio (8/10).

Affiliate-funded. No inventory. Research use only.
[URL]
```

### X/Twitter Thread (4 tweets)
```
1/ I built PeptideCleanScore — vendor comparison that ranks by contamination panels, not just "99% purity." 7,466 Finnrick tests. 212 vendors. No inventory. The only list with dates + multi-lab sources.

2/ Dirty secret: "99% purity" means nothing if your vial is 40% residual solvent. 2023 Belgian study: 5/12 "pure" vendors had dangerous solvent levels. I built a site that scores by what vendors PROVE.

3/ Scoring: HPLC + TFA quant + solvents + ICP-MS metals + endotoxins. +1 bonus for 2026 batches from 2+ independent labs. Paradigm Peptide leads at 9/10.

4/ Full tables at [URL]. Affiliate-funded. Research use only.
```

### Discord
```
PeptideCleanScore — vendor comparison by actual test data, not vibes.

Scored 1–10 by contamination panel transparency: solvents, TFA, ICP-MS metals, endotoxins. Finnrick data (7,466 tests) + Janoshik/MZ Biolabs cross-reference with batch dates.

Top 3 Reta: Paradigm (9/10), Peptide Partners (8/10), Jeep Bio (8/10).
[URL]

(Research use only. Affiliate links. No inventory. Heavy disclaimers on every page.)
```

## Honest Caveats
- Finnrick vendor pages are JS-rendered (SPA) — you must VERIFY scores manually in a browser
- Per-vendor contamination panel data (solvents/TFA/metals) is from community reports + public COA patterns — not directly scraped
- All "Verify live" rows in tables mean: open finnrick.com/vendors/[name] in a browser, check current scores
- This is editorially scored, not scientifically measured
- **Always update before publishing** — Finnrick data changes weekly

## Cost
- **Build:** $0
- **Hosting:** $0 (Vercel/Netlify free tier)
- **Domain:** $0 (use vercel.app subdomain) or $10/year (custom domain)
- **Affiliate applications:** $0 (apply as content creator)
- **Total to launch:** $0
