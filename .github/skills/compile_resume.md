---
name: compile-resume
description: >
  Compile a LaTeX resume variant to PDF using pdflatex and report the result.
  Use this skill before and after any resume edit to validate it compiles cleanly.
  Accepts a resume filename (e.g. resume_bigtech_2026) or full path.
allowed-tools:
  - bash
---

Compile a LaTeX resume variant and report success or errors.

## Usage
Call this skill with the resume variant name, for example:
- `compile-resume resume_bigtech_2026`
- `compile-resume resume_finance_2026`
- `compile-resume Career/resumes/latex/resume_startup_2026.tex`

## Steps
1. Resolve the full path to the `.tex` file:
   - If given a bare name like `resume_bigtech_2026`, expand to `Career/resumes/latex/resume_bigtech_2026.tex`
   - If given a relative path, treat as relative to the repo root
2. Change to the file's directory (pdflatex writes output files alongside the source)
3. Run: `pdflatex -interaction=nonstopmode <filename>.tex`
4. Check the exit code:
   - **Exit 0:** Report "✅ Compiled successfully → <filename>.pdf"
   - **Non-zero:** Extract error lines from the `.log` file (lines starting with `!`) and report them clearly
5. Clean up auxiliary files (`.aux`, `.log`) after a successful compile

## Output Format
```
✅ resume_bigtech_2026.pdf compiled successfully.
```
or
```
❌ Compile failed. Errors:
  ! Undefined control sequence.
  l.42  \somecommand
```
