---
name: tracker-stats
description: >
  Print summary statistics from Career/applications/applications_2026.csv.
  Shows counts by Status, Track, and Tier without loading the full CSV into context.
  Use when asked "how many applications", "what's my pipeline", or similar queries.
allowed-tools:
  - bash
---

Print a concise summary of job application statistics from the tracker CSV.

## Steps
Run the following to produce a summary (do not `cat` or `view` the full file):

```bash
python3 - << 'EOF'
import csv, collections

with open('Career/applications/applications_2026.csv', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

total = len(rows)
by_status = collections.Counter(r.get('Status', '').strip() for r in rows)
by_track  = collections.Counter(r.get('Track', '').strip() for r in rows)
tier1 = sum(1 for r in rows if 'Tier 1' in r.get('Notes', ''))
tier2 = sum(1 for r in rows if 'Tier 2' in r.get('Notes', ''))

print(f"Total roles: {total}")
print()
print("By Status:")
for status, count in sorted(by_status.items(), key=lambda x: -x[1]):
    print(f"  {status or '(blank)'}: {count}")
print()
print("By Track:")
for track, count in sorted(by_track.items(), key=lambda x: -x[1]):
    print(f"  {track or '(blank)'}: {count}")
print()
print(f"Tier 1 (apply immediately): {tier1}")
print(f"Tier 2 (apply this week):   {tier2}")
EOF
```

## Output Format
```
Total roles: 572

By Status:
  To Apply: 410
  Applied: 120
  ...

By Track:
  BigTech: 280
  ...

Tier 1 (apply immediately): 45
Tier 2 (apply this week):   90
```
