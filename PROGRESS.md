# May Workshop Updates — Progress Log

**Branch:** `may_updates`
**Last updated:** 2026-05-18 (afternoon)

Live status of the agent's work. See `TASKS.md` for the full task list. **This file is updated on `may_updates` and mirrored to `main` so Shakti / other agents can pull current state.**

---

## Status board

| # | Task | Status | Blocking on |
|---|------|--------|-------------|
| 1 | Catalog override + Genie Code prompt in `00_Setup.ipynb` | ✅ Done | — |
| 2 | Architecture diagram in `03_Medallion Architecture.ipynb` | ✅ Done | — |
| 3 | Genie hint in `02_Databricks_Notebook_Tour.ipynb` | ✅ Done (TODO marker for screenshot) | Screenshot from John |
| 4 | Lakeflow Designer notebook replacing `06_Declarative_Pipeline.ipynb` | 🔄 In progress | Holly's example would help |
| 5 | Remove `07_SQL_Editor.sql` | ✅ Done | — |
| 6 | New `07_Dashboard_Builder.ipynb` | 🔄 In progress | — |
| 7 | Trim `09_Genie_Room.ipynb` to single prompt | ✅ Done | — |
| 8 | Remove `10_Agent_Bricks.ipynb` | ✅ Done | — |
| 9 | Refresh `10_Databricks_One.ipynb` (renumbered from 11) + mobile preview | ⏳ Pending | Mobile screenshot from John |
| 10 | Update `README.md` | ⏳ Pending | Tasks 4, 6, 9 |
| 11 | Flag stale screenshots in `01_Platform_Tour.ipynb` | ⏳ Pending | — |

**Legend:** ⏳ pending · 🔄 in progress · ✅ done · 🚧 blocked

---

## Decisions & structural changes

* **Notebook renumbering** — closing the gap left by removing Agent Bricks. New flow:
  * `00_Setup` → `05_Job_Creation` (unchanged)
  * `06_Lakeflow_Designer.ipynb` *(replaces `06_Declarative_Pipeline.ipynb`)*
  * `07_Dashboard_Builder.ipynb` *(new — Genie Code prompt that builds the dashboard)*
  * `08_Formula_1_Dashboard.lvdash.json` *(kept as pre-baked reference)*
  * `09_Genie_Room.ipynb`
  * `10_Databricks_One.ipynb` *(renumbered from 11)*

* **Deleted files** (committed on `may_updates`):
  * `notebooks/07_SQL_Editor.sql`
  * `notebooks/10_Agent_Bricks.ipynb`
  * `notebooks/06_Declarative_Pipeline.ipynb`
  * `notebooks/06_Formula1_Declarative_Pipeline/` (folder + contents)
  * Orphan images: Agent Bricks (2), SQL Editor, Declarative Pipeline (5)

* **Screenshots John needs to add** (markdown cells reference these paths):
  * `notebooks/Images/Notebook_Genie_Locations.png` — used in `02_Databricks_Notebook_Tour.ipynb`
  * `notebooks/Images/Genie_Space_Setup.png` — used in `09_Genie_Room.ipynb`
  * Mobile app preview screenshot for `10_Databricks_One.ipynb`
  * Refresh of any 01_Platform_Tour screenshots that are stale (agent will flag specific ones)

---

## Log

### 2026-05-18

* Branch `may_updates` created off latest `main` (after pulling 36 commits the local clone was behind).
* `TASKS.md` and `PROGRESS.md` created + committed to `main` so Shakti can see scope.
* **Decisions** (in user Q&A):
  * Keep `11_Databricks_One` name (vs renaming to Genie dashboards) — but renumbering to `10` since gap looks broken.
  * Keep `05_Job_Creation.ipynb` as-is.
  * Catalog fix uses markdown cell + Genie Code prompt approach.
  * Flow Designer notebook drafted now based on Holly Smith's LinkedIn post; John can refine.
* Task #1 done — added catalog override markdown cell + Genie Code prompt to `00_Setup.ipynb`.
* Task #3 done — added Genie/Assistant hint cell to `02_Databricks_Notebook_Tour.ipynb` (with screenshot TODO marker).
* Task #2 done — added ASCII architecture diagram to top of `03_Medallion Architecture.ipynb`.
* Task #7 done — rewrote `09_Genie_Room.ipynb` to a single paste-in prompt that configures the whole Genie space (name, description, instructions, sample questions, trusted SQL).
* Task #5 done — deleted `07_SQL_Editor.sql` + image.
* Task #8 done — deleted `10_Agent_Bricks.ipynb` + 2 images.
* Renumbered `11_Databricks_One.ipynb` → `10_Databricks_One.ipynb` (git mv preserves history).
* Removed `06_Declarative_Pipeline.ipynb`, `06_Formula1_Declarative_Pipeline/` folder, and 5 DLT screenshots.
* Next: write `06_Lakeflow_Designer.ipynb` and `07_Dashboard_Builder.ipynb`, then refresh `10_Databricks_One.ipynb`, then update README.
