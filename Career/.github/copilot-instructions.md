# Career — Copilot Instructions

## Entry Point
**Read `Career/README.md` first.** It is the authoritative source for directory
structure, resume variants, cover letter index, scraper usage, and candidate facts.

## Owner
- **Liam Wood** | Austin, TX — targeting NYC, Austin, Miami
- **Email:** general.lvwood@gmail.com | **Phone:** (305) 790-9093
- **Current role:** Software Engineer II — Platform Infrastructure @ Microsoft
- **Target roles:** Senior Platform / Infrastructure Engineer
- **Target companies:** Big Tech, Finance/HFT, high-growth startups

## Key Paths

| What | Path |
|---|---|
| Full guide (read first) | `Career/README.md` |
| Resume source files (LaTeX) | `Career/resumes/latex/` |
| Cover letters | `Career/cover_letters/` |
| Application tracker | `Career/applications/applications_2026.csv` |
| Job scraper | `Career/scripts/scrape_jobs.py` |

## Resume Variants

| File | Use For |
|---|---|
| `resume_bigtech_2026.tex` | Google, Meta, AWS, Stripe, Cloudflare |
| `resume_finance_2026.tex` | Jane Street, HRT, Citadel, Virtu, Two Sigma |
| `resume_startup_2026.tex` | Anthropic, Anduril, Databricks, Rippling, Figma |
| `resume_citadel_2026.tex` | Citadel Securities only |

## Cover Letters

Company-specific letters exist for: Google, Anthropic, Meta, Cloudflare, HRT, Anduril, Virtu.
Generic track templates: `cover_letter_bigtech_2026.md`, `cover_letter_finance_2026.md`, `cover_letter_startup_2026.md`.
Always replace `[Hiring Manager Name]` before use.

## Tracker Conventions
- CSV columns: `Company, Track, Role, URL, Status, Resume Variant, Cover Letter, Notes, Location`
- Track values: `BigTech`, `Finance`, `Startup`
- Status lifecycle: `To Apply` → `Applied` → `Phone Screen` → `Interview` → `Offer` / `Rejected`
- Notes: `Tier 1` = apply immediately (company-specific cover letter ready); `Tier 2` = apply this week

## Scraper
Re-run at any time to append new roles (deduplicates automatically):
```bash
python Career/scripts/scrape_jobs.py
```
Sources: Greenhouse API, Ongig API, HRT admin-ajax, Jane Street JSON API, BuiltInAustin, generic Playwright.
Location filter: NYC, Austin, Miami, Remote.
