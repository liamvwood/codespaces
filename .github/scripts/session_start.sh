#!/usr/bin/env bash
# Session start orientation hook for Liam's job search workspace.
# Prints a quick status summary so every session begins with context.

CSV="Career/applications/applications_2026.csv"

if [ ! -f "$CSV" ]; then
  echo "⚠️  Tracker not found at $CSV"
  exit 0
fi

# Count by status (skip header)
total=$(tail -n +2 "$CSV" | wc -l | tr -d ' ')
to_apply=$(tail -n +2 "$CSV" | awk -F',' '{gsub(/"/, "", $5); if ($5 == "To Apply") count++} END {print count+0}')
applied=$(tail -n +2 "$CSV" | awk -F',' '{gsub(/"/, "", $5); if ($5 == "Applied") count++} END {print count+0}')
pipeline=$(tail -n +2 "$CSV" | awk -F',' '{gsub(/"/, "", $5); if ($5 ~ /Phone Screen|Interview/) count++} END {print count+0}')
tier1=$(tail -n +2 "$CSV" | grep -i "Tier 1" | wc -l | tr -d ' ')

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   🚀 2026 Job Search — Session Start  ║"
echo "╠══════════════════════════════════════╣"
printf "║  📋 Total tracked roles: %-13s║\n" "$total"
printf "║  📬 To Apply:            %-13s║\n" "$to_apply"
printf "║  ✉️  Applied:             %-13s║\n" "$applied"
printf "║  📞 In pipeline:         %-13s║\n" "$pipeline"
printf "║  ⭐ Tier 1 ready:        %-13s║\n" "$tier1"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Agents: resume-editor | application-tracker | cover-letter-writer | recruiter"
echo "Skills: /compile-resume | /tracker-stats | /scrape-jobs"
echo ""
