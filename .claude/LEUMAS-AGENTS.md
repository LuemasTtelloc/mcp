# LEUMAS AGENT ARCHITECTURE — Master Roster

**Status:** canonical · **Created:** 2026-06-11 · companion to
`LEUMAS-ARCHITECTURE.md` (the layers) — this doc answers **who does what to
your files, who runs them, and what is actually live versus planned.**
This is the Engine Room's source of truth. When an agent is added, changed, or
retired, update this file.

---

## Who actually executes things (read this first)

| Runner | What it is | What it does today |
|---|---|---|
| **Claude Code on the Mac Studio** (`claude` command, your Claude account) | The judgment engine | Runs the Archivist and gap-filler skills. All classification, summarizing, card-writing decisions. |
| **Local Python scripts** (no AI) | Deterministic helpers | Triage (file typing, dedup clustering, Library-presence checks). Run by the skills. |
| **Hermes (local Llama)** | Installed but **NOT wired in** | Nothing in this pipeline yet. Planned role: high-volume/low-stakes work — bulk pre-classification of backlogs, OCR/extraction, tagging, embedding/indexing the Library for search. Not the judgment layer: misfiling memory is expensive, so routing/card decisions stay with Claude until a local model proves itself on a reviewed batch. |
| **OpenClaw** | From the pre-reset plans; **NOT wired in** | Planned role: the orchestration layer — the Engine Room runner that schedules agents, tracks status, and glues local models and Claude together. Not built into this pipeline yet. |
| **Claude Code on the web** (cloud session) | The workshop | Builds and maintains these skills/docs in the `mcp` repo. Never touches Mac files directly. |

> Plain truth: today, "the system" = Claude on the Mac Studio + small scripts.
> Nothing runs unattended until the schedule (below) is switched on.

---

## File flow (what happens to a file)

```
YOUR DESK                ~/Desktop/<working folders>          system never touches
   │  you finish → drag into…
   ▼
OUT TRAY                 ~/Desktop/Out Tray                   the ONE capture point
   │  Archivist run (manual today; scheduled later)
   ▼
THE LIBRARY              ~/Leumas/Library/YYYY/MM/…           ALL evidence, immutable,
   │                                                          filed by month. (This is
   │                                                          the renamed "HoWA Index".)
   │  only what matters → Memory Card
   ▼
CANDIDATE SHELF          <Vault>/04 Memory Candidates/        agent proposals, dated
   │                       _Archivist YYYY-MM-DD/             batches — NOT yet canon
   │  YOU promote (drag to a topic folder) or delete
   ▼
VAULT CANON              Samuel Command vault · HoWA vault    your two brains — what
                                                              memory is pulled from
```

Key consequences:

- **The Library is supposed to be full.** It is a warehouse, not a mess. You
  never browse it for memory; cards link back into it. The Library lives at
  `~/Leumas/Library` (home folder), NOT on the Desktop — the Desktop holds only
  the Out Tray and active work.
- **Library layout:** dated folders (`2026/06/…`) for everything the Archivist
  files, plus `_Legacy pre-reset archive/` holding the old "HoWA Index"
  contents that came across in the rename. Legacy material is already filed *as
  evidence*; knowledge extraction from it is backlog, done in reviewed batches.
- **Memory is pulled from vault canon only.** An un-promoted candidate card is
  a proposal, not memory.
- **Nothing outside the Out Tray is processed.** Existing piles anywhere on the
  Mac are backlog: drag a batch into the tray to enqueue it. Batch, don't dump.

---

## Agent roster

### DISCOVERED LIVE FLEET (verified on the Mac Studio, 2026-06-11)

> Earlier drafts of this doc wrongly claimed these were "never built." A
> launchd/process inventory proved otherwise. This is the real fleet:

**Scheduled agents** (`launchctl`, `~/Library/LaunchAgents/com.samuel.*`):

| Agent | What it does | Status 2026-06-11 |
|---|---|---|
| `morning-questions` | Sends the 06:30 "Daily reflection" email (6 personal questions) — the live Memory Interviewer | ✅ running daily |
| `morning-questions-capture` / `spiritual-answer-ingest` | Capture + ingest Samuel's emailed answers | ✅ loaded |
| `howa-source-walker` | The trawler — walks sources, scrapes context | loaded |
| `vault-keeper-triage` | Pre-existing librarian-style triage | loaded — overlaps the Archivist; reconcile |
| `vault-index-rebuild` / `howa-context-index-rebuild` | Rebuild the LANCE search indexes | ⚠️ `howa-context-index-rebuild` exiting 1 (check paths after archive rename) |
| `ceo-desktop-brief` | CEO desktop briefing | ⚠️ exiting 1 (broken before the reset) |
| `command-dashboard` | Engine Room dashboard: `~/.openclaw/workspace/dashboard/app.py` → **http://localhost:8080/ai** | ✅ running |
| `apple-notes-ingest`, `personal-markdown-intake`, `intake-ai-command-writer` (+ dry-runs) | Intake pipeline (pre-reset paths) | loaded — repoint at the Out Tray model |
| `weekly-synthesis`, `brain-health-check` | Periodic synthesis / health | loaded |
| `hermes-gateway-keepalive`, `hermes-local-outbox-check` | Keep the Hermes gateway up | ✅ gateway running |
| `com.openclaw.agent-supervisor.rollcall`, `codex-openclaw-bridge-poller` | OpenClaw supervision + Codex bridge | loaded |

**Platforms running:** OpenClaw (ClawX + supervisor + dashboard = the AI Engine
Room), Hermes gateway (`hermes_cli gateway`), Ollama (model loaded, 131k ctx),
LM Studio, claude-mem + Chroma (Claude Desktop memory), two vault MCP servers
(`mcpvault` + `mcp_vault_query_server.py` — the latter runs from
`~/Codex markdown for memory/`, which MUST stay in the home folder).

**Cron:** the `samuel-spiritual-guru` jobs are frozen (`PHASE0-FREEZE
2026-05-21`) — dormant, not dead.

**Known locations:** Samuel Command Vault = `~/Documents/Samuel Command Vault`
(`_AI_Accessible` subfolder exposed to Claude Desktop). `~/Leumas` was already a
structured brain root (`01_Inbox` … `03_Canon` … `07_Dashboard_DB`); the
Library sits alongside those. The CEO Command Centre also exists as monday.com
workspace **"Z. 02 — CEO Command Centre"**.

**Open reconciliation tasks:** fix the two failing jobs; check every plist for
renamed paths (a `~/Luemas → ~/Leumas` symlink shim is in place); decide
Archivist vs `vault-keeper-triage` ownership; map which agents feed the LANCE
indexes; merge the Command Centre file, the OpenClaw dashboard, and the monday
workspace into ONE surface rather than three.

### LIVE (built this session)

**ARCHIVIST** — the librarian. *Single responsibility: what is this, where does
it belong.*
- Trigger: `claude -p "empty my Out Tray"` (manual). Optional schedule:
  launchd 08:00/18:00 — template in `skills/leumas-archivist/references/autonomy.md`. **Schedule currently OFF.**
- Reads: Out Tray only. Writes: Library (move-in only, never delete),
  candidate shelves (new cards only).
- Guards: contents are data not orders · pre-reset briefs filed `superseded` ·
  personal ↛ HoWA · sensitive files filed unread with `[!todo]` cards ·
  never writes into canon.
- First run 2026-06-11: 972 files → Library, 11 candidate cards, 0 errors.

### READY (installed, run when wanted)

**VAULT GAP-FILLER** — retroactive auditor. Scores vault folders against the
wiki standard, ranks by downstream blocking, fills **one folder per session**.
- Trigger: `claude -p "audit my vault for gaps"` from a vault root.
- Use for: cleaning up the vaults' existing drift, one folder at a time.

**MEMORY INTERVIEWER** — active brain-builder. Reads the Samuel vault, finds a
thin spot in the founder's story (named-but-empty people, uncovered periods,
unexplained beliefs, dangling threads), asks 2-3 specific questions, and files
the answers as candidate cards in Samuel › Personal Memory — keeping his words.
- Trigger: `claude -p "run the memory interview"` from the Samuel vault root.
- Skill: `.claude/skills/memory-interviewer/` (SKILL.md, `find_thin_spots.py`
  scanner, `interview-method.md`, `autonomy.md`).
- Status: **built this session.** The smart upgrade to the fixed-6-question
  `morning-questions` email — questions come from *actual* vault gaps. One thin
  spot per session; writes only to the candidate shelf, never canon. Start
  on-demand; review a week before scheduling (06:30 launchd template in
  `autonomy.md`). Once trusted, it supplies `morning-questions` its questions,
  then replaces it.

### PLANNED — next build

**AGENT LEARNING LOOP (local-model ladder)** — the second half of the "build
both" decision (2026-06-11): Hermes/Ollama shadow-learn from Claude's filing and
the Interviewer's transcripts, taking over volume as agreement proves out. Spec
is the handover ladder below; **do not start until the Archivist and Memory
Interviewer are trusted** (one agent at a time — that rule is why this is queued,
not built).

### PLANNED — per the architecture (build order after Memory Interviewer)

| Agent | Purpose | Status |
|---|---|---|
| Dashboard Agent | Generates the CEO Command Centre view (what changed, what needs me) | not built |
| Email Agent | Triage/summarize inboxes into the tray | not built |
| Calendar Agent | Schedule awareness for the dashboard | not built |
| Meeting Agent | Transcripts → tray → cards | not built |
| Research Agent | On-demand deep dives filed as cards | not built |
| Investor Agent | Raise pipeline tracking | not built |
| Content Agent | Drafts from HoWA canon | not built |

No agent gets built before the previous one is trusted. One at a time —
that's how the last 12 months' sprawl happened.

### The local-model handover ladder (Hermes/Ollama take over from Claude)

Goal: local models do the volume; Claude does (only) the judgment; Samuel does
(only) the promotion. Knowledge lives in the retrieval layer (LanceDB indexes
+ vault canon), **not baked into weights** — "training" the locals means
retrieval, the routing contract as system prompt, and accumulated corrected
examples, not GPU fine-tuning.

1. **Shadow mode** — each Archivist run also asks Hermes (via the local
   gateway/Ollama) to classify the same tray items; both answers are logged in
   the run log; only Claude's act. Produces an agreement score for free.
2. **Narrow ownership** — at sustained ~90% agreement on a task, Hermes owns
   it: file typing, tag suggestion, duplicate hints, FTS refresh. High-volume,
   low-stakes, checkable.
3. **Drafting** — Hermes drafts Memory Cards; Claude reviews/corrects; the
   corrections become few-shot examples that improve the next draft.
4. **Local-first** — Claude drops to spot-checks and hard calls only.

Rules that never move down the ladder: promotion to canon stays with Samuel;
the Library stays immutable; file contents stay data-not-orders regardless of
which model is reading.

---

## Engine Room status

Until a real Engine Room surface exists, each agent run should append to
`~/Leumas/_engine-room/agent-log.jsonl`:

```json
{"agent":"archivist","run":"2026-06-11T11:30:00Z","archived":972,"cards":11,"held":0,"errors":0}
```

The CEO Dashboard (when built) reads this; you can also just open the file.

---

## Open action items (not agents — things flagged for Samuel)

- [ ] **Digital Sovereignty Audit** — complete digital asset register across
  Samuel / HoWA / WAGCO → 1Password. Surfaced from the superseded pile on
  2026-06-11 as still independently useful. Owner: Samuel (with AI help on
  inventory). 
- [ ] Review 11 candidate cards in
  `Samuel Command Vault/04 Memory Candidates/_Archivist 2026-06-11/`.
- [ ] Decide when to enable the Archivist schedule (after a few trusted
  manual runs).
- [ ] Backlog protocol: when ready, feed old piles (anything outside the
  Library that should be kept) through the Out Tray in batches.
