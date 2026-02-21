---
name: scrape-jobs
description: >
  Run the job scraper to find new roles and append them to the applications tracker.
  Deduplicates automatically. Reports how many new roles were added.
  Use when asked to "find new jobs", "update the tracker", or "run the scraper".
allowed-tools:
  - bash
---

Run the job scraper and report new roles found.

## Steps
1. Count rows in the tracker before running:
   ```bash
   before=$(wc -l < Career/applications/applications_2026.csv)
   ```
2. Run the scraper:
   ```bash
   python Career/scripts/scrape_jobs.py
   ```
3. Count rows after:
   ```bash
   after=$(wc -l < Career/applications/applications_2026.csv)
   ```
4. Report: `Added $((after - before)) new roles. Tracker now has $((after - 1)) total roles.`
   (Subtract 1 for the header row.)
5. If the scraper exits non-zero, report the error output.

## Notes
- The scraper deduplicates by Company+Role automatically.
- Location filter is already configured in the script: NYC, Austin, Miami, Remote.
- Sources: Greenhouse API, Ongig API, HRT admin-ajax, Jane Street JSON API, BuiltInAustin, Playwright.
- Scraper may take several minutes due to Playwright rendering.
