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

## Job Search Preferences
- **Target locations:** NYC, Austin TX, Miami, Remote — always filter scraped/searched roles to these locations only.
- **Target seniority:** Senior IC (L5/L6 equivalent) — skip roles below Senior or above Staff unless explicitly asked.
- **Scripts and output files:** Always write to the repo (never `/tmp/`). Scripts go in `Career/scripts/`, output in `Career/applications/`.

## Token Economy
- **Read `Career/README.md` first** — it is the authoritative source; don't re-ask what the agent can read.
- If prompted to "pick up", "resume", or "continue where you left off" — read `Career/CHECKPOINT.md` first.
- Use the `explore` agent for any lookup question ("which companies have cover letters?", "what's in this resume?").
- Never load the full `applications_2026.csv` into the main context; use the `application-tracker` agent.
- Prefer the `task` agent to run the scraper or compile LaTeX — keeps verbose output out of main context.

## Testing & Validation
- **LaTeX resumes:** Before editing any `.tex` file, confirm it compiles (`compile-resume` skill). After editing, compile again. A broken compile is a blocker — revert before proceeding.
- **Tracker CSV:** Before writing to `applications_2026.csv`, verify column count matches the schema:
  `Company, Track, Role, URL, Status, Resume Variant, Cover Letter, Notes, Location` (9 columns).
  Valid `Status` values: `To Apply`, `Applied`, `Phone Screen`, `Interview`, `Offer`, `Rejected`.
- **Cover letters:** Always confirm `[Hiring Manager Name]` has been replaced before marking a letter as ready.
- **Resumes:** Always run the `recruiter` agent review before marking a resume variant ready to send to any company.
