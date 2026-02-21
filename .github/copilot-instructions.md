# GitHub Copilot Instructions

## Repository
Personal workspace for **Liam Wood** — contains independent projects in separate
top-level directories. Each directory may have its own `.github/copilot-instructions.md`
with context specific to that project; read it before working in that directory.

## General Conventions
- Filenames: `snake_case`
- Commit messages: concise imperative summary line, details in body
- Secrets and credentials must never be committed

## Development Workflow
- **TDD:** Write a failing test (or validation step) before implementing. Run tests after every change.
  For Career tasks this means: compile LaTeX before editing, compile again after — failure = revert and fix.
- **Sub-agents:** Delegate aggressively to sub-agents to keep main context clean and tokens lean.
  Use `explore` for "what is / where is" questions; use `task` for builds, tests, and script runs.
- **Context management:** Run `/compact` proactively after large file reads. Never load the full
  applications CSV into main context — use the `application-tracker` agent instead.
- **Plan mode:** For any multi-file or multi-step change, enter plan mode first (`Shift+Tab`).

## Agent & Skill Usage
Custom agents live in `.github/agents/`. Available agents:
- `resume-editor` — LaTeX resume editing; knows all 4 variants and candidate facts
- `recruiter` — Reviews resumes from a hiring manager's perspective; flags ATS gaps and weak bullets
- `application-tracker` — Reads/writes `applications_2026.csv`; fast Haiku model
- `cover-letter-writer` — Drafts/tailors cover letters; can web-search company context

Custom skills live in `.github/skills/`. Available skills:
- `compile-resume` — Compiles a LaTeX resume variant via `pdflatex`, reports errors
- `tracker-stats` — Prints application counts by status, track, and tier
- `scrape-jobs` — Runs the job scraper and reports new roles found

## Top-Level Directories

| Directory | Purpose | Instructions |
|---|---|---|
| `Career/` | 2026 job search — resumes, cover letters, applications tracker, scraper | `Career/.github/copilot-instructions.md` |

