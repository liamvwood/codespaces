# Session Checkpoint
**Written:** 2026-02-21T20:30:00Z

## Application Stats
572 total | 278 to apply | 0 applied | 18 Tier 1 (13 ready, 5 blocked)

## Recent Commits
```
a499d90 Add company-specific cover letters for PayPal and Eloquent AI; flag Google URLs
ead9ee8 Trim all resume variants to 1 page
8f5e0e7 Apply recruiter review fixes to all 3 resume variants
cddd2a0 Add session-review skill, session reviews, sessionEnd hook, and instruction fixes
2f5be32 Fix agent/skill structure; add sessionStart hook
```

## Session Notes
**Last completed:** Company-specific cover letters created for PayPal and Eloquent AI.
All Google Tier 1 rows flagged — URLs need manual lookup at careers.google.com.

## Tier 1 Application Status

### ✅ READY TO APPLY (13 roles)
| Company | Role | Resume | Cover Letter |
|---|---|---|---|
| Google (×5) | Senior/Staff Platforms Infra | Resume_BigTech_2026 | cover_letter_google_2026.md |
| Meta (×2) | Infra / Network Eng | Resume_BigTech_2026 | cover_letter_meta_2026.md |
| Cloudflare (×2) | Distributed Systems Eng | Resume_BigTech_2026 | cover_letter_cloudflare_2026.md |
| PayPal | Sr Staff Cloud Infra | Resume_Startup_2026 | cover_letter_paypal_2026.md |
| Eloquent AI | Senior DevOps/Infra | Resume_Startup_2026 | cover_letter_eloquentai_2026.md ⚠️ |
| Virtu Financial | Systems Engineer | Resume_Finance_2026 | cover_letter_virtu_2026.md |
| HRT | Systems Engineer – R&D | Resume_Finance_2026 | cover_letter_hrt_2026.md |

⚠️ Eloquent AI requires AWS Certification — Liam is Azure-primary. Apply at own discretion.
⚠️ Google URLs are blank — look up each role at https://careers.google.com before applying.

### ❌ BLOCKED (5 roles — need Liam's input)
| Company | Role | Blocker |
|---|---|---|
| Anthropic (×3) | Data Infra / Staff Claude Platform | Data pipeline tooling (Kafka/Airflow/Parquet?) |
| Anduril | Senior Backend Core Platform | Any Rust exposure? |
| HRT | Software Engineer – C++ | P99 latency numbers + C++ depth (lock-free?) |

## Blockers — Answer these to unblock 5 more roles
1. **Rust** — any exposure at all (even hobby level)? → Anduril
2. **Data pipelines** — Kafka, Kinesis, Airflow, Parquet, dbt, Spark used anywhere? → Anthropic
3. **P99 latency** — actual numbers from Microsoft or Visa? → HRT C++
4. **Lock-free C++** — any RAII/C++17/lock-free work at Visa? → HRT credibility

## Pre-Application Checklist (per role)
- [ ] Look up hiring manager name on LinkedIn → replace `[Hiring Manager Name]`
- [ ] Confirm job is still open (check URL)
- [ ] Google roles: find direct URL at careers.google.com
- [ ] Submit resume PDF + cover letter text
- [ ] Mark row as "Applied" in applications_2026.csv + add date in Notes

## Quick Reference
- **Agents:** resume-editor | application-tracker | cover-letter-writer | recruiter
- **Skills:** /compile-resume | /tracker-stats | /scrape-jobs | /session-review
- **Tracker:** `Career/applications/applications_2026.csv`
- **Resumes:** `Career/resumes/pdf/` → bigtech / finance / startup (all 1 page)
- **Cover letters:** `Career/cover_letters/`
