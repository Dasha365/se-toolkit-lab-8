---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

## Available tools
- `lms_health` — check backend health and item count
- `lms_labs` — list all available labs
- `lms_pass_rates` — get pass rates for a specific lab
- `lms_completion_rate` — get completion rate for a specific lab
- `lms_timeline` — get submission timeline for a specific lab
- `lms_groups` — get group performance for a specific lab
- `lms_top_learners` — get top learners for a specific lab
- `lms_learners` — get learner list
- `lms_sync_pipeline` — trigger ETL sync

## Strategy

- If the user asks for scores, pass rates, completion, groups, timeline, or top learners WITHOUT naming a specific lab, call lms_labs first, then ask the user which lab they want
- Do NOT fetch data for all labs at once — always ask which lab first
- If multiple labs are available, present them as a numbered list and ask the user to choose one
- Use each lab title as the user-facing label
- Let the shared structured-ui skill decide how to present choices on supported channels

## Formatting
- Format percentages with one decimal place (e.g. 89.1%)
- Show counts alongside percentages when available
- Keep responses concise

## When asked "what can you do?"
Explain that you can query live LMS data: list labs, check pass rates, completion rates, group performance, top learners, submission timeline, and trigger data sync.
