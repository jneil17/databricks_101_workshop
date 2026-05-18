# May Workshop Updates — Progress Log

**Branch:** `may_updates`
**Last updated:** 2026-05-18 (end of session)

Live status of the agent's work. See `TASKS.md` for the full task list. **This file is updated on `may_updates` and mirrored to `main` so Shakti / other agents can pull current state.**

---

## Status board

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | Catalog override + Genie Code prompt in `00_Setup.ipynb` | ✅ Done | Markdown cell inserted before "What's Next?". Includes paste-ready prompt. |
| 2 | Architecture diagram in `03_Medallion Architecture.ipynb` | ✅ Done | ASCII diagram of bronze → silver → gold flow. |
| 3 | Genie hint in `02_Databricks_Notebook_Tour.ipynb` | ✅ Done | TODO marker for screenshot `Notebook_Genie_Locations.png`. |
| 4 | `06_Lakeflow_Designer.ipynb` replacing Declarative Pipeline | ✅ Done | 3-node sample pipeline on F1 silver tables. TODO markers for 2 screenshots. |
| 5 | Remove `07_SQL_Editor.sql` | ✅ Done | (SQL editor still referenced inline in Genie + Dashboard notebooks.) |
| 6 | New `07_Dashboard_Builder.ipynb` (Genie Code prompt) | ✅ Done | Pre-baked `08_*.lvdash.json` kept as fallback. |
| 7 | Trim `09_Genie_Room.ipynb` to single prompt | ✅ Done | One-shot prompt configures name, instructions, sample Qs, trusted SQL. |
| 8 | Remove `10_Agent_Bricks.ipynb` | ✅ Done | + removed 2 Agent Bricks images. |
| 9 | Refresh `10_Databricks_One.ipynb` + mobile preview | ✅ Done | Renumbered from 11. Mobile section added with TODO marker for screenshot. |
| 10 | Update `README.md` | ✅ Done | New notebook table, "Advanced Features" bullets, troubleshooting, docs links, last-updated date. |
| 11 | Flag stale screenshots in `01_Platform_Tour.ipynb` | ✅ Done | Inline HTML comment lists 7 screenshots to verify. Text updated (Lakeflow vs DLT). |

**Legend:** ✅ done · ⏳ pending · 🔄 in progress · 🚧 blocked

---

## Structural changes

* **Notebook flow:** `00 → 10` (Agent Bricks gone, gap closed).
  * `00_Setup` → `05_Job_Creation` (unchanged)
  * `06_Lakeflow_Designer.ipynb` *(replaces `06_Declarative_Pipeline.ipynb`)*
  * `07_Dashboard_Builder.ipynb` *(new — Genie Code prompt)*
  * `08_Formula_1_Dashboard.lvdash.json` *(unchanged — pre-baked reference)*
  * `09_Genie_Room.ipynb` *(rewritten as single one-shot prompt)*
  * `10_Databricks_One.ipynb` *(renumbered from 11, added mobile section)*

* **Files removed:**
  * `notebooks/06_Declarative_Pipeline.ipynb`
  * `notebooks/06_Formula1_Declarative_Pipeline/` (folder + contents)
  * `notebooks/07_SQL_Editor.sql`
  * `notebooks/10_Agent_Bricks.ipynb`
  * 7 orphan PNGs (Agent Bricks ×2, Declarative Pipeline ×5)
  * (`SQL Editor.png` was kept — still referenced by `01_Platform_Tour.ipynb`.)

---

## 📸 Screenshots John still needs to add

All referenced by markdown cells with `📸 TODO (John)` markers — just drop the file into `notebooks/Images/` at the named path and they'll render:

| File path | Used in |
|-----------|---------|
| `notebooks/Images/Notebook_Genie_Locations.png` | `02_Databricks_Notebook_Tour.ipynb` |
| `notebooks/Images/Lakeflow_Designer_Create.png` | `06_Lakeflow_Designer.ipynb` |
| `notebooks/Images/Lakeflow_Designer_DAG.png` | `06_Lakeflow_Designer.ipynb` |
| `notebooks/Images/Genie_Space_Setup.png` | `09_Genie_Room.ipynb` |
| `notebooks/Images/Databricks_One_Mobile.png` | `10_Databricks_One.ipynb` |
| (verify 7 existing screenshots in `01_Platform_Tour.ipynb` — see inline HTML comment) | `01_Platform_Tour.ipynb` |

---

## Open follow-ups (not agent-owned)

* **Shakti:** FY27 pitch slides, signup for May 20, presenter feedback sync, ask Tyler about workshop survey.
* **John:** Lakeflow Designer example flow from Holly (if/when shared, swap the agent's draft for it). Mobile app screenshot. Verify Platform Tour screenshots.
* **Both:** Feedback survey for end of workshop. Better attendance tracking.

---

## Log

### 2026-05-18

* Branch `may_updates` created off latest `main` (`b4b4e66`).
* All 11 agent-owned tasks completed in single session.
* Two pushes to `main` so far:
  1. `b4b4e66` — initial `TASKS.md` / `PROGRESS.md`
  2. `f12911f` — first PROGRESS.md sync (mid-session)
* Final commit + push to `main` for end-of-session sync pending.
* No screenshots taken by agent — all marked with inline TODOs.
