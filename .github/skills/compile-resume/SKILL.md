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

## Directory Layout
- Source:        `Career/resumes/latex/*.tex`
- PDF output:    `Career/resumes/pdf/`
- Build artifacts: `Career/resumes/obj/` (gitignored — never committed)

## Steps
1. Resolve the full path to the `.tex` file:
   - If given a bare name like `resume_bigtech_2026`, expand to `Career/resumes/latex/resume_bigtech_2026.tex`
   - If given a relative path, treat as relative to the repo root
2. Ensure `Career/resumes/obj/` exists: `mkdir -p Career/resumes/obj`
3. Run pdflatex with obj as the aux directory and pdf as the output destination:
   ```
   pdflatex -interaction=nonstopmode \
     -output-directory=Career/resumes/obj \
     Career/resumes/latex/<filename>.tex
   mv Career/resumes/obj/<filename>.pdf Career/resumes/pdf/
   ```
4. Check the exit code:
   - **Exit 0:** Report "✅ Compiled successfully → Career/resumes/pdf/<filename>.pdf"
   - **Non-zero:** Extract error lines from `Career/resumes/obj/<filename>.log` (lines starting with `!`) and report them clearly
5. Leave obj/ contents in place (gitignored); do NOT delete them (useful for debugging)

## Output Format
```
✅ resume_bigtech_2026.pdf compiled successfully → Career/resumes/pdf/resume_bigtech_2026.pdf
```
or
```
❌ Compile failed. Errors:
  ! Undefined control sequence.
  l.42  \somecommand
```
