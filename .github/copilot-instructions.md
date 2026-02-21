# GitHub Copilot Instructions

## Repository Purpose
This is **Liam Wood's** personal career repository. It contains resumes, job application
tracking, and tooling for the 2026 job search.

## Owner Profile
- **Name:** Liam Wood
- **Location:** Austin, TX (open to relocation)
- **Email:** general.lvwood@gmail.com | **Phone:** (305) 790-9093
- **Current role:** Software Engineer II — Platform Infrastructure @ Microsoft (July 2022–Present)
- **Target roles:** Senior Platform / Infrastructure Engineer
- **Target companies:** Big Tech, Finance/HFT, high-growth startups

## Repository Structure

```
Career/
  Resumes/
    latex/                    # LaTeX source for all resume variants
      Resume_Citadel_2026.tex     # Citadel Securities (Finance/HFT)
      Resume_BigTech_2026.tex     # Google, Meta, Apple, AWS, Stripe, Cloudflare
      Resume_Finance_2026.tex     # Jane Street, Two Sigma, Jump, HRT — leads with Visa work
      Resume_Startup_2026.tex     # Databricks, Anduril, Rippling, Figma — leads with ownership/velocity
    html/                     # HTML versions (mirrors latex/)
    references/               # Reference letters / contacts
  jobs/
    applications_2026.csv     # Application tracker — columns: Company, Track, Role, URL,
                              #   Status, Resume Variant, Cover Letter, Notes
  scripts/
    scrape_jobs.py            # Playwright + BeautifulSoup job scraper (see below)
```

## Resume Variants — When to Use Which

| File | Emphasis | Best For |
|------|----------|----------|
| `Resume_BigTech_2026.tex` | Scale (6B events/month), AKS/K8s, CI/CD, observability | Google, Meta, AWS, Stripe, Cloudflare |
| `Resume_Finance_2026.tex` | Fault-tolerant state machines, Visa settlement engine (trillions in txn volume), correctness | Jane Street, Two Sigma, Jump, HRT, Citadel |
| `Resume_Startup_2026.tex` | Full ownership, shipping velocity (6-week→weekly), $500k–$750k cost savings | Databricks, Anduril, Rippling, Figma |
| `Resume_Citadel_2026.tex` | Citadel-specific (original) | Citadel Securities only |

## Job Scraper (`Career/scripts/scrape_jobs.py`)

Re-run at any time to find new roles and append them to `applications_2026.csv`:

```bash
python Career/scripts/scrape_jobs.py
```

- Uses **Playwright** (headless Chromium) + **BeautifulSoup** (lxml)
- Deduplicates against existing CSV rows
- Automatically assigns the correct `Resume Variant` per company track
- Requirements: `pip install playwright beautifulsoup4 lxml && python -m playwright install chromium`
- System deps (if Chromium fails to launch):
  `sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2t64`

## Application Tracker (`Career/jobs/applications_2026.csv`)

CSV columns: `Company, Track, Role, URL, Status, Resume Variant, Cover Letter, Notes`

Status values: `To Apply` → `Applied` → `Phone Screen` → `Interview` → `Offer` / `Rejected`

## Cover Letters

When drafting cover letters for Liam, use these track-specific angles:

- **BigTech:** Lead with 6B+ events/month scale, KEDA autoscaling savings ($500k–$750k),
  AKS, multi-region failover, CI/CD velocity (6-week → weekly).
- **Finance/HFT:** Lead with Visa settlement engine (trillions in annual txn volume),
  fault-tolerant exactly-once state machines, Linux production ops under financial pressure.
- **Startup:** Lead with end-to-end ownership, shipping velocity, measurable cost savings,
  and full-stack breadth (Node.js, Vue.js, C++, Python).

## Key Resume Facts (for tailoring applications)

- 6B+ events/month — distributed notification infra (OneDrive / SharePoint)
- KEDA autoscaling → $500k–$750k/year in cost savings
- AKS migration + infra-as-code re-architecture
- Multi-region failover (Azure FrontDoor + Traffic Manager) — 99.99% availability
- CI/CD: 6-week cycles → weekly deployments with automated rollback
- Visa: state-machine settlement engine, trillions in annual txn volume, exactly-once processing
- B.S. Computer Science, University of Florida (2022)
- Languages: C++, Python, C#/.NET, Node.js, JavaScript
