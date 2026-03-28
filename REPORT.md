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
