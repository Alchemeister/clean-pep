     1|# CleanPep — Static Site
     2|
     3|**Live URL (after deploy):** `cleanpep.com` or `cleanpep.vercel.app`
     4|
     5|A static HTML/CSS comparison site ranking peptide vendors by a **Cleanliness Score (1–10)** based on what their COAs actually prove — not just "99% purity" claims.
     6|
     7|## Data Source
     8|Finnrick Analytics public data — 7,466 tests, 212 vendors, 15 products. Last synced: 22 May 2026.
     9|- `finnrick.com/llms.txt` — Machine-readable summary
    10|- `finnrick.com/llms-full.txt` — Full vendor/product tables with real scores/dates
    11|- `finnrick.com/vendors` — Per-vendor detail pages (JS-rendered, manual verification needed)
    12|
    13|All data in this site is **public, verifiable, and manually checkable** — no scrapers, no APIs, no purchases, no automated tools.
    14|
    15|## Files
    16|```
    17|src/
    18|  index.html         — Homepage (hero, scoreboard, quick product summary)
    19|  retatrutide.html   — Full Retatrutide table (2,778 tests, 173 vendors)
    20|  tirzepatide.html   — Tirzepatide table (1,930 tests, 140 vendors)
    21|  bpc157.html        — BPC-157 + TB-500 tables (551 + 102 tests)
    22|  coa-guide.html     — How to Read a COA guide
    23|  about.html         — About, methodology, full disclaimer
    24|  style.css          — Shared stylesheet (dark mode, mobile-first)
    25|```
    26|
    27|## Deploy (Free)
    28|
    29|### Vercel (recommended — instant, free, auto SSL)
    30|```bash
    31|# Install vercel CLI if not already
    32|npm i -g vercel
    33|
    34|# Deploy
    35|cd src
    36|vercel
    37|# Follow prompts → deploy as "clean-pep"
    38|# Done. Live at https://clean-pep.vercel.app
    39|```
    40|
    41|### Netlify (also free)
    42|Drop `src/` folder onto netlify.com/drop — done.
    43|
    44|### Any VPS
    45|```bash
    46|cd src && python3 -m http.server 8080
    47|# Or: nginx, apache, caddy — just serve the src/ folder
    48|```
    49|
    50|### Custom Domain
    51|Buy cleanpep.com (~$10/year via Namecheap/Porkbun) → point DNS to Vercel/Netlify. Takes 5 minutes.
    52|
    53|## Affiliate Setup
    54|Before launch, replace affiliate link placeholders with your actual URLs. Search the HTML files for `[AFFILIATE]` (none present — links are direct to vendor URLs with `?aff=YOURID` style params). Add your affiliate IDs to:
    55|- Paradigm Peptide links
    56|- LiveWell Peptides links
    57|- PS Peptides links
    58|- Ascension links
    59|- Onyx links
    60|- Limitless Biotech links
    61|- Core Peptides links
    62|
    63|## Updating Scores
    64|Finnrick updates their data weekly. To refresh:
    65|1. Visit finnrick.com/vendors for each vendor
    66|2. Note new scores + dates
    67|3. Update the HTML table rows
    68|4. Bump the "Data last updated" timestamp
    69|5. Redeploy (`vercel --prod`)
    70|
    71|Each table row takes ~2 min to verify and update. Full refresh: ~20 min.
    72|
    73|## Traffic Launch (Post Templates)
    74|
    75|### Reddit — r/Peptides
    76|```
    77|Title: I built a site ranking peptide vendors by what they ACTUALLY test for (solvents/TFA/metals — not just purity)
    78|
    79|Got sick of the same 5 vendor lists. Built CleanPep — research-use-only, pulls from Finnrick Analytics' public data (7,466 tests, 212 vendors). The only list showing batch dates + multi-lab sources so you know if the data is fresh.
    80|
    81|Top Retatrutide: Paradigm Peptide (9/10), Peptide Partners (8/10), Jeep Bio (8/10).
    82|
    83|Affiliate-funded. No inventory. Research use only.
    84|[URL]
    85|```
    86|
    87|### X/Twitter Thread (4 tweets)
    88|```
    89|1/ I built CleanPep — vendor comparison that ranks by contamination panels, not just "99% purity." 7,466 Finnrick tests. 212 vendors. No inventory. The only list with dates + multi-lab sources.
    90|
    91|2/ Dirty secret: "99% purity" means nothing if your vial is 40% residual solvent. 2023 Belgian study: 5/12 "pure" vendors had dangerous solvent levels. I built a site that scores by what vendors PROVE.
    92|
    93|3/ Scoring: HPLC + TFA quant + solvents + ICP-MS metals + endotoxins. +1 bonus for 2026 batches from 2+ independent labs. Paradigm Peptide leads at 9/10.
    94|
    95|4/ Full tables at [URL]. Affiliate-funded. Research use only.
    96|```
    97|
    98|### Discord
    99|```
   100|CleanPep — vendor comparison by actual test data, not vibes.
   101|
   102|Scored 1–10 by contamination panel transparency: solvents, TFA, ICP-MS metals, endotoxins. Finnrick data (7,466 tests) + Janoshik/MZ Biolabs cross-reference with batch dates.
   103|
   104|Top 3 Reta: Paradigm (9/10), Peptide Partners (8/10), Jeep Bio (8/10).
   105|[URL]
   106|
   107|(Research use only. Affiliate links. No inventory. Heavy disclaimers on every page.)
   108|```
   109|
   110|## Honest Caveats
   111|- Finnrick vendor pages are JS-rendered (SPA) — you must VERIFY scores manually in a browser
   112|- Per-vendor contamination panel data (solvents/TFA/metals) is from community reports + public COA patterns — not directly scraped
   113|- All "Verify live" rows in tables mean: open finnrick.com/vendors/[name] in a browser, check current scores
   114|- This is editorially scored, not scientifically measured
   115|- **Always update before publishing** — Finnrick data changes weekly
   116|
   117|## Cost
   118|- **Build:** $0
   119|- **Hosting:** $0 (Vercel/Netlify free tier)
   120|- **Domain:** $0 (use vercel.app subdomain) or $10/year (custom domain)
   121|- **Affiliate applications:** $0 (apply as content creator)
   122|- **Total to launch:** $0
   123|