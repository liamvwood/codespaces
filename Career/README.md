# Career — Liam Wood

Agent entry point. Read this file first before touching anything in this directory.

## Candidate

| Field | Value |
|---|---|
| Name | Liam Wood |
| Location | Austin, TX (open to relocation) |
| Email | general.lvwood@gmail.com |
| Phone | (305) 790-9093 |
| Current role | Software Engineer II — Platform Infrastructure @ Microsoft (July 2022–Present) |
| Target roles | Senior Platform / Infrastructure Engineer |
| Target companies | Big Tech, Finance/HFT, high-growth startups |

## Directory Structure

```
Career/
├── README.md                          ← you are here
├── resumes/
│   ├── latex/                         ← editable source (LaTeX)
│   │   ├── resume_bigtech_2026.tex    ← Big Tech track
│   │   ├── resume_finance_2026.tex    ← Finance/HFT track
│   │   ├── resume_startup_2026.tex    ← Startup track
│   │   └── resume_citadel_2026.tex    ← Citadel-specific (original)
│   ├── html/
│   │   └── resume_citadel_2026.html
│   └── pdf/
│       ├── resume_citadel_2026.pdf
│       └── resume_fall_2021.pdf       ← archived
├── cover_letters/
│   ├── cover_letter_bigtech_2026.md   ← Big Tech track
│   ├── cover_letter_finance_2026.md   ← Finance/HFT track
│   └── cover_letter_startup_2026.md   ← Startup track
├── applications/
│   └── applications_2026.csv          ← application tracker (319 rows)
└── scripts/
    └── scrape_jobs.py                 ← job scraper (re-run to append new roles)
```

## Resume Variants

| File | Leads With | Use For |
|---|---|---|
| `resume_bigtech_2026.tex` | 6B events/month, AKS/K8s, CI/CD, observability | Google, Meta, AWS, Stripe, Cloudflare |
| `resume_finance_2026.tex` | Visa settlement engine, fault-tolerant state machines, exactly-once processing | Jane Street, Two Sigma, Jump, HRT, Citadel |
| `resume_startup_2026.tex` | End-to-end ownership, $500k–$750k cost savings, weekly deploy cadence | Databricks, Anduril, Anthropic, Rippling, Figma |
| `resume_citadel_2026.tex` | Citadel-specific variant | Citadel Securities only |

## Cover Letters

Templates in `cover_letters/`. Substitute `[Company]` and `[Hiring Manager Name]` before sending.

| File | Opening angle |
|---|---|
| `cover_letter_bigtech_2026.md` | 6B events/month scale → KEDA savings → CI/CD velocity |
| `cover_letter_finance_2026.md` | Visa settlement engine (trillions in txn volume) → exactly-once correctness |
| `cover_letter_startup_2026.md` | End-to-end ownership → shipping velocity → measurable cost impact |

## Application Tracker

`applications/applications_2026.csv` — columns:

```
Company | Track | Role | URL | Status | Resume Variant | Cover Letter | Notes
```

Status lifecycle: `To Apply` → `Applied` → `Phone Screen` → `Interview` → `Offer` / `Rejected`

Track values: `BigTech`, `Finance`, `Startup`

## Scraper

Re-run at any time to append new roles (deduplicates automatically):

```bash
python Career/scripts/scrape_jobs.py
```

Sources scraped:
- **Generic Playwright**: Google, Meta, Stripe, Cloudflare, AWS, Citadel, Jump Trading, Databricks, Rippling, Figma
- **BuiltInAustin**: `builtinaustin.com/jobs?search=Senior+DevOps+Engineer` (3 pages, card-based)
- **Jane Street JSON API**: `janestreet.com/jobs/main.json`
- **Greenhouse API**: Anthropic (`anthropic`), Anduril (`andurilindustries`)

Setup (once):
```bash
pip install playwright beautifulsoup4 lxml
python -m playwright install chromium
# If Chromium fails: sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2t64
```

## Key Resume Facts

Use these when tailoring applications or writing cover letters:

- **6B+ events/month** — distributed notification infra (OneDrive / SharePoint)
- **KEDA autoscaling** → $500k–$750k/year in cost savings
- **AKS migration** + full infra-as-code re-architecture
- **Multi-region failover** (Azure FrontDoor + Traffic Manager) — 99.99% availability
- **CI/CD**: 6-week cycles → weekly deployments with automated rollback
- **Visa**: state-machine settlement engine, trillions in annual txn volume, exactly-once processing
- **B.S. Computer Science**, University of Florida (2022)
- **Languages**: C++, Python, C#/.NET, Node.js, JavaScript
