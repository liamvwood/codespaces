---
name: session-review
description: >
  Reviews a previous Copilot CLI session to extract concrete improvements for
  custom instructions, agents, skills, and hooks. Use when asked to review a
  session, analyse what went well, or improve the agent setup based on past work.
  Produces a structured review saved to .github/session_reviews/.
allowed-tools:
  - bash
  - view
  - create
  - edit
  - glob
---

You are reviewing a past Copilot CLI session to extract actionable improvements
to the agent setup (instructions, agents, skills, hooks).

## Input
The session to review is identified by its session ID (a UUID). Sessions are
stored at:
```
~/.copilot/session-state/<session-id>/
  workspace.yaml   — session metadata (summary, timestamps, cwd)
  events.jsonl     — full event log (user messages, assistant messages, tool calls)
  plan.md          — implementation plan (if one was created)
```

## Review Process

### Step 1 — Read session metadata
```bash
cat ~/.copilot/session-state/<id>/workspace.yaml
```

### Step 2 — Extract conversation
Use the following script to pull just user/assistant messages (no tool noise):
```bash
python3 - << 'PYEOF'
import json, re, sys
session_id = sys.argv[1]
path = f"/home/codespace/.copilot/session-state/{session_id}/events.jsonl"
with open(path) as f:
    for line in f:
        e = json.loads(line)
        t = e.get("type", "")
        if t == "user.message":
            content = re.sub(r'<[^>]+>.*?</[^>]+>', '', e['data']['content'], flags=re.DOTALL).strip()
            if content:
                print(f"USER: {content[:400]}")
        elif t == "assistant.message":
            c = e['data'].get('content', '')
            if c:
                print(f"ASSISTANT: {c[:400]}")
PYEOF
```

### Step 3 — Read the plan (if it exists)
```bash
cat ~/.copilot/session-state/<id>/plan.md 2>/dev/null || echo "(no plan)"
```

### Step 4 — Analyse the session against these dimensions

**A. Instruction gaps**
- What did the user have to clarify repeatedly that could be in `copilot-instructions.md`?
- What context did the agent have to discover by reading files that could be pre-loaded?
- Were there ambiguous prompts that better instructions would have resolved?

**B. Missing agents**
- Were there repeated sub-tasks that would benefit from a dedicated agent?
- Was the main context polluted with verbose output (builds, diffs, scraping) that belongs in a sub-agent?

**C. Missing or improvable skills**
- Were there commands the agent ran multiple times that should be a skill?
- Were there validation steps that should be automated?

**D. Hook opportunities**
- Was there setup or context-gathering the agent did at the start that a `sessionStart` hook could handle?
- Were there cleanup or commit steps that a `sessionEnd` hook could handle?

**E. Workflow inefficiencies**
- Were there multiple round-trips for information that should have been in context?
- Did the agent ask clarifying questions that good instructions would have pre-empted?
- Were there server errors / interruptions that broke flow? What would prevent them?

**F. What went well**
- Patterns or approaches that should be reinforced in instructions.

### Step 5 — Write the review

Save to `.github/session_reviews/<session-id>.md` using this template:

```markdown
# Session Review — <summary> (<date>)
**Session ID:** <id>
**Duration:** <start> → <end>
**CWD:** <cwd>

## Summary
One paragraph: what the session accomplished.

## What Went Well
- ...

## Instruction Gaps → Fixes
| Gap | Recommended Fix |
|-----|----------------|
| ... | ... |

## Missing Agents → Proposals
| Task Pattern | Proposed Agent |
|-------------|----------------|
| ... | ... |

## Missing / Improvable Skills → Proposals
| Repeated Command | Proposed Skill |
|-----------------|----------------|
| ... | ... |

## Hook Opportunities
| Trigger | Action |
|---------|--------|
| ... | ... |

## Workflow Inefficiencies
- ...

## Top 3 Actionable Recommendations
1. ...
2. ...
3. ...
```

### Step 6 — Apply improvements
After writing the review, check which recommendations can be applied immediately
(e.g., adding a missing fact to `copilot-instructions.md`, creating a new skill).
Apply them and note which were implemented vs. deferred.
