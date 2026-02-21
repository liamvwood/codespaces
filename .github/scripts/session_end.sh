#!/usr/bin/env bash
# sessionEnd hook: writes Career/CHECKPOINT.md so the next session can
# immediately pick up without asking "where did we leave off?"

CHECKPOINT="Career/CHECKPOINT.md"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Get last 5 commit messages to summarise recent work
RECENT_COMMITS=$(git --no-pager log --oneline -5 2>/dev/null || echo "(no commits)")

# Get current application stats
CSV="Career/applications/applications_2026.csv"
if [ -f "$CSV" ]; then
  TOTAL=$(tail -n +2 "$CSV" | wc -l | tr -d ' ')
  TO_APPLY=$(tail -n +2 "$CSV" | awk -F',' '{gsub(/"/, "", $5); if ($5 == "To Apply") count++} END {print count+0}')
  APPLIED=$(tail -n +2 "$CSV" | awk -F',' '{gsub(/"/, "", $5); if ($5 == "Applied") count++} END {print count+0}')
  STATS="$TOTAL total | $TO_APPLY to apply | $APPLIED applied"
else
  STATS="(tracker not found)"
fi

cat > "$CHECKPOINT" << CHECKPOINT_EOF
# Session Checkpoint
**Written:** $NOW

## Application Stats
$STATS

## Recent Commits
\`\`\`
$RECENT_COMMITS
\`\`\`

## Session Notes
<!-- The agent that wrote this checkpoint should fill in:
     - Last task completed
     - Any open items or blockers
     - Recommended next action
     This section is left blank by the hook script — add it manually or via a prompt. -->

## Quick Reference
- **Agents:** \`/agent\` → resume-editor | application-tracker | cover-letter-writer | recruiter
- **Skills:** /compile-resume | /tracker-stats | /scrape-jobs | /session-review
- **Tracker:** \`Career/applications/applications_2026.csv\`
- **Resumes:** \`Career/resumes/latex/\`
- **Cover letters:** \`Career/cover_letters/\`
CHECKPOINT_EOF

echo "✅ Checkpoint written to $CHECKPOINT"
