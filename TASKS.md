# May Workshop Updates — Task List

**Branch:** `may_updates`
**Driver:** John (with Claude Code agent assistance)
**Deadline:** May 20, 2026 (first workshop)
**Last updated:** 2026-05-18

This file tracks what the agent is working on so Shakti can see scope and avoid duplicate work. See `PROGRESS.md` for live status.

---

## Source

Tasks derived from the May 8, 2026 transcript between John and Shakti. The full transcript is in chat history — these are the actionable items.

---

## Tasks

### Agent-owned (Claude is doing these)

| # | Task | Notes |
|---|------|-------|
| 1 | Add catalog override + Genie Code prompt to `00_Setup.ipynb` | Markdown cell + paste-in prompt. Needs screenshot of Genie Code panel from John. |
| 2 | Add architecture diagram to `03_Medallion Architecture.ipynb` | Shows bronze/silver/gold tables before code runs. |
| 3 | Add Genie hint screenshot to `02_Databricks_Notebook_Tour.ipynb` | Markdown cell calling out Genie/Assistant in notebook UI. Needs screenshot from John. |
| 4 | Replace `06_Declarative_Pipeline.ipynb` with Lakeflow Designer walkthrough | Based on Holly Smith's LinkedIn post about Lakeflow Designer. |
| 5 | Remove `07_SQL_Editor.sql` | SQL editor will be referenced inline during Genie portion instead. |
| 6 | Add Dashboard Builder notebook (Genie Code prompt) | Keep existing `08_Formula_1_Dashboard.lvdash.json` as pre-baked reference. |
| 7 | Trim `09_Genie_Room.ipynb` to single full prompt | One paste-in prompt that builds the whole Genie space. |
| 8 | Remove `10_Agent_Bricks.ipynb` | Agent Bricks changed too much (no custom LLM, no knowledge assistant). |
| 9 | Refresh `11_Databricks_One.ipynb` screenshots + add mobile app preview | Keeping the "Databricks One" name. Needs mobile screenshot from John. |
| 10 | Update `README.md` for new notebook structure | Reflect removed/renamed notebooks. |
| 11 | Flag stale screenshots in `01_Platform_Tour.ipynb` | Agent will list what needs to be updated; John replaces. |

### Owner: John (out of scope for the agent)

- [ ] Replace flagged screenshots in 01, 02, 09, 11
- [ ] Send agent the Lakeflow Designer flow / example Holly posted
- [ ] Confirm whether to publish `TASKS.md` and `PROGRESS.md` to the repo (currently uncommitted)

### Owner: Shakti

- [ ] Update slides to FY27 pitch
- [ ] Send out signup for May 20 workshop
- [ ] Schedule 15-min feedback sync with presenters before changes land
- [ ] Ask Tyler about workshop feedback survey wiring

### Joint / TBD

- [ ] Feedback survey for end of workshop (decide whether to build new vs reuse Tyler's)
- [ ] Better attendance tracking (current Salesforce campaign dashboard is too slow — John is looking at building a Claude-built dashboard off the campaign table)

---

## What the agent is NOT doing

- Slides — Shakti owns
- Taking new screenshots — John owns
- Scheduling, signups, sending Slack — humans only
- Pushing or merging the branch — confirm with John first

---

## How to read this file

- "Agent-owned" tasks are things Claude can do in code in this repo.
- Anything else is on a human. Don't pick up agent-owned tasks without checking `PROGRESS.md` first to make sure they're not in-flight.
- If you want to redirect or kill a task, edit this file and Slack John.
