---
name: observability
description: Use observability MCP tools to query logs and traces
always: true
---

# Observability Skill

## Available tools
- `logs_search` — search logs with LogsQL query
- `logs_error_count` — count errors for a service over a time window
- `traces_list` — list recent traces for a service
- `traces_get` — fetch a specific trace by ID

## Strategy

- When the user asks about errors, call logs_error_count first to get the count
- Then call logs_search to find specific error records
- If a trace_id is found in logs, call traces_get to inspect the full trace
- Summarize findings concisely — do not dump raw JSON
- Default service name is "Learning Management Service"
- Default time window is "1h"

## Formatting
- Report error counts clearly: "X errors in the last Y"
- Show the most recent error with timestamp and message
- If a trace shows an error, explain which operation failed and why
