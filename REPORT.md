## Task 1A — Bare agent

### What is the agentic loop?
The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously: Perceive → Reason/Plan → Act → Observe → Reflect/Iterate. This loop continues until the goal is achieved.

### What labs are available in our LMS?
The agent explored local repo files and found Lab 8 tasks (Task 1-4 required, Task 1 optional). It did NOT return real backend data — answered from documentation instead.

## Task 1B — Agent with LMS tools

### What labs are available?
Lab 01–Lab 07 and lab-08 — real data from backend via mcp_lms_lms_labs tool.

### Is the LMS backend healthy?
Agent called lms_health and returned real health result with item count.

### Which lab has the lowest pass rate?
Agent chained lms_labs + lms_completion_rate for each lab. Lab 08 has 0% (no submissions yet), among active labs — Lab 02 and Lab 03 tied at 89.1%.

## Task 1C — Skill prompt

### Show me the scores (without specifying a lab)
Agent called lms_labs first, then asked which lab to show scores for, presenting all 8 labs as a numbered list.

## Task 2A — Deployed agent

Nanobot gateway started successfully on port 18790.
Logs show: "Starting nanobot gateway version 0.1.4.post5"
MCP LMS server connected.
No channels enabled yet (webchat added in Part B).

## Task 2B — Web client

Flutter web client accessible at /flutter, protected by NANOBOT_ACCESS_KEY.
Agent answers questions using real LMS data via MCP tools.

![Task 2B screenshot](report-assets/task2b.png)

## Task 3A — Structured logging

![VictoriaLogs query result](report-assets/task3a.png)

### Happy-path log excerpt
```
request_started → auth_success → db_query (INFO) → request_completed (200)
trace_id=305c90833e99c6aae1ebe1e802523fcb
```

### Error-path log excerpt
```
request_started → auth_success → db_query (INFO) → db_query (ERROR) → items_list_failed_as_not_found → request_completed (404)
trace_id=6566cfd8d142cc017985ad4aea24f566
```

## Task 3A — Structured logging

![VictoriaLogs query result](report-assets/task3a.png)

### Happy-path log excerpt
```
request_started → auth_success → db_query (INFO) → request_completed (200)
trace_id=305c90833e99c6aae1ebe1e802523fcb
```

### Error-path log excerpt
```
request_started → auth_success → db_query (INFO) → db_query (ERROR) → items_list_failed_as_not_found → request_completed (404)
trace_id=6566cfd8d142cc017985ad4aea24f566
```

## Task 3C — Observability MCP tools

### Normal conditions (no errors)
"Good news! There have been no errors reported by the Learning Management Service in the last 10 minutes."

### After stopping PostgreSQL
"I can confirm there have been 2 errors in the Learning Management Service in the last 10 minutes. Both errors show: [Errno -2] Name or service not known. This indicates the LMS service is having trouble connecting to its database."
