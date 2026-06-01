# CleanPep

CleanPep is a static peptide vendor comparison site focused on public proof, not affiliate noise.

The site ranks vendors by what their COAs actually show: identity, HPLC purity, content/fill or assay, residual solvents, TFA/counterion disclosure, endotoxin, sterility/bioburden where applicable, and source transparency.

## Key Data

- `data/coas.json` is the verified COA database. Do not add claims here without source proof.
- `data/coa_sources.json` lists seed URLs for COA discovery.
- `data/coa_candidates.json` stores unverified candidate links found during discovery.
- `data/affiliates.json` tracks affiliate status separately from ranking logic.
- `data/partnership_targets.json` tracks higher-quality vendor, lab, and partnership targets.
- `docs/partner_outreach.md` contains vendor outreach and lab quote templates.

## Affiliate Rules

- Affiliate status must not change vendor ranking, panel scoring, or source labels.
- Prefer vendors that provide batch-specific COAs and expanded panels.
- Ask approved vendors for both a tracking link and a dedicated public code.
- Treat purity/identity-only COAs as incomplete until residual solvents, TFA/counterion, endotoxin, content/fill, and identity evidence are verified.
- Broken, stale, or brand-confusing affiliate paths should be marked honestly in `data/affiliates.json`.

## Local Preview

This is a static site. Open `src/index.html` directly, or serve it locally:

```bash
cd src
python -m http.server 4173
```

Then open `http://127.0.0.1:4173/index.html`.

## Deployment

The project is configured for Vercel with `vercel.json`.

Pushes to the active PR trigger Vercel preview deployments automatically.

## Updating Evidence

1. Add candidate source URLs to `data/coa_sources.json`.
2. Run or update `tools/aggregate_coas.py` to discover candidate proof links.
3. Manually verify candidate COAs before moving anything into `data/coas.json`.
4. Keep missing panels visible. Do not turn absence of evidence into a clean claim.

## Positioning

CleanPep should make the market uncomfortable in the right way: vendors with real full-panel proof become easy to explain, and vendors with only cheap purity screenshots stay visibly incomplete.
