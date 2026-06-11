# FLEET REPAIR BRIEF — repoint the OpenClaw agents to the Leumas architecture

**For:** Claude Code running ON the Mac Studio (`cd ~/luemas-setup && claude`,
then: *"read .claude/FLEET-REPAIR-BRIEF.md and carry it out"*).
**Goal:** bring the failing/stranded `com.samuel.*` agents back online by
repointing them from dead Desktop paths to the Leumas structure. No agent is
deleted; superseded ones are retired with the user's approval.

## Ground rules

1. **Back up before editing:**
   `cp -R ~/.openclaw/workspace/scripts ~/.openclaw/workspace/scripts.bak-$(date +%Y%m%d)`
2. Edit paths only — do not restructure logic. One script at a time; test; move on.
3. Nothing is deleted. Retiring an agent = `launchctl unload` + move its plist
   into `~/Library/LaunchAgents/_retired/` (folder already exists).
4. Ask the user before retiring anything; report every change at the end.
5. Agents must not read/write `~/Desktop` (macOS TCC blocks launchd agents
   there, and the architecture reserves the Desk for the human). The one
   exception is the Out Tray, which only the Archivist (run via `claude`,
   not launchd-python) processes.

## Path translation table (old → new)

| Old path (in scripts) | New path |
|---|---|
| `~/Desktop/HoWA Index Intake` | `~/Leumas/Library/_Legacy pre-reset archive/` *(verify exact subfolder — `_extracted_pdf_text` etc. live somewhere under here; `find` it first)* |
| `~/Desktop/CEO_Command_Centre_Initial_Import.csv` | `~/Leumas/07_Dashboard_DB/CEO_Command_Centre_Initial_Import.csv` *(restore from Library first — step 1)* |
| `~/Desktop/CEO Command Centre — What Matters Today.md` (output) | `~/Leumas/07_Dashboard_DB/CEO Command Centre — What Matters Today.md` |
| `~/Desktop/AI Command Strategy Intake`, `~/Desktop/AI Command Intake` | retired — superseded by the Out Tray + Archivist |
| `~/Desktop/Personal Markdown Intake`, `~/Desktop/Personal Memory Intake` | retired — superseded by the Out Tray + Archivist |
| `~/HOWA_INDEX` (weekly synthesiser) | `~/HOWA_INDEX_LANCE` *(confirm by reading how the script uses it; `~/HOWA_INDEX` does not exist)* |
| `~/Luemas/...` anywhere | `~/Leumas/...` (a compat symlink exists, but fix the source) |

## Work order

### 1. Restore the CEO CSV from the Library
`find ~/Leumas/Library/2026 -iname "CEO_Command_Centre*"` — it arrived inside
the archived "CEO master comand centre doc" folder. **Copy** (don't move — the
Library keeps its evidence copy) to `~/Leumas/07_Dashboard_DB/`.

### 2. Fix `samuel_command.py` + `ceo_desktop_brief.sh`
- `CSV_PATH` → the new `07_Dashboard_DB` location.
- All output writes (including the `.md.tmp` → `.md` rename in the shell
  script) → `~/Leumas/07_Dashboard_DB/`.
- Test: `bash ~/.openclaw/workspace/scripts/ceo_desktop_brief.sh`, then
  `launchctl kickstart -k gui/$(id -u)/com.samuel.ceo-desktop-brief` and check
  the err log is clean.

### 3. Fix `howa_context_index_rebuild.py`
- Locate the real new home of `_extracted_pdf_text` under
  `~/Leumas/Library/_Legacy pre-reset archive/` and repoint line 29.
- Run it once by hand (`/usr/bin/python3 …`), confirm it rebuilds, then
  `launchctl kickstart` the job and verify exit status 0 via `launchctl list`.

### 4. Fix read-only consumers
`brain_health_check.py` (path fine — verify), `connector_weekly_synthesiser.py`
(`~/HOWA_INDEX` → correct index path), `finetune_corpus_build.py` (same check).

### 5. Propose retirements (ASK FIRST, one by one)
Superseded by the Archivist/Out Tray: `intake_ai_command_runner/writer`,
`intake_personal_memory_runner`, `intake_howa_runner`, `auto_local_model_ingest`,
`howa_source_batch_synth`, `screenshot_visual_memory_batch`, `stub_upgrade`,
and possibly `howa_source_walker` + `vault-keeper-triage` (they overlap the
Archivist's job — the user decides which librarian survives; default
recommendation: the Archivist owns intake, the walker is retired).

### 6. Report
Write a summary of every edit/retirement into `~/Leumas/Command Centre.md`
under AGENT ACTIVITY + RUN LOG, and tell the user: which jobs are green
(`launchctl list | grep samuel` statuses), which are retired, what's pending.

---

# PHASE 2 — Switch on the Archivist schedule

Only after Phase 1 is green:

1. **Permissions.** Merge the scoped allow-rules from
   `.claude/skills/leumas-archivist/references/autonomy.md` (Step 1) into
   `~/.claude/settings.json` — preserve any existing settings; add, don't
   replace. Vault path for the rules: `~/Documents/Samuel Command Vault`
   (plus the HoWA vault path once confirmed).
2. **Schedule.** Install the launchd plist from `autonomy.md` as
   `~/Library/LaunchAgents/com.leumas.archivist.plist` (08:00 + 18:00),
   `launchctl load` it, then `launchctl kickstart` once and verify a clean run
   in `~/Library/Logs/leumas-archivist.log`.
3. Add an `Archivist (scheduled)` row to the Command Centre AGENT ACTIVITY
   table.

# PHASE 3 — One morning surface (default decision)

Working default — confirmed overridable by Samuel: **the OpenClaw dashboard
(`http://localhost:8080/ai`) is THE morning view.** The Command Centre file is
its data source, not a competitor.

1. Read `~/.openclaw/workspace/dashboard/app.py`. If it's a simple
   Flask/FastAPI app, add (with user approval) a panel or route that renders
   `~/Leumas/Command Centre.md` and the latest
   `~/Leumas/07_Dashboard_DB/CEO Command Centre — What Matters Today.md`.
   Keep the change minimal — render the markdown, nothing fancier.
2. If app.py is complex or fragile, do NOT modify it — instead leave a note in
   the Command Centre and report back; the wiring becomes a follow-up task.
3. The monday.com "Z. 02 — CEO Command Centre" workspace stays as-is for now
   (business ops live there); no changes to monday in this session.

# Done means

- `launchctl list | grep -E "samuel|leumas"` shows no status-1 rows except
  deliberately retired ones.
- The Archivist runs at 08:00/18:00 unattended.
- One browser tab (localhost:8080/ai) shows: what changed, what needs Samuel,
  agent activity.
- Command Centre.md reflects all of it, and every change made in this session
  is listed there.
