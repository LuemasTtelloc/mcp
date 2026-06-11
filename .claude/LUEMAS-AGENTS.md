# LUEMAS AGENT ARCHITECTURE — Master Roster

**Status:** canonical · **Created:** 2026-06-11 · companion to
`LUEMAS-ARCHITECTURE.md` (the layers) — this doc answers **who does what to
your files, who runs them, and what is actually live versus planned.**
This is the Engine Room's source of truth. When an agent is added, changed, or
retired, update this file.

---

## Who actually executes things (read this first)

| Runner | What it is | What it does today |
|---|---|---|
| **Claude Code on the Mac Studio** (`claude` command, your Claude account) | The judgment engine | Runs the Archivist and gap-filler skills. All classification, summarizing, card-writing decisions. |
| **Local Python scripts** (no AI) | Deterministic helpers | Triage (file typing, dedup clustering, Library-presence checks). Run by the skills. |
| **Local Llama models** | Installed but **NOT wired in** | Nothing in this pipeline yet. Candidate future role: cheap bulk pre-classification. Until then they are idle in this workflow. |
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
THE LIBRARY              ~/Luemas/Library/YYYY/MM/…           ALL evidence, immutable,
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
  never browse it for memory; cards link back into it.
- **Memory is pulled from vault canon only.** An un-promoted candidate card is
  a proposal, not memory.
- **Nothing outside the Out Tray is processed.** Existing piles anywhere on the
  Mac are backlog: drag a batch into the tray to enqueue it. Batch, don't dump.

---

## Agent roster

### LIVE

**ARCHIVIST** — the librarian. *Single responsibility: what is this, where does
it belong.*
- Trigger: `claude -p "empty my Out Tray"` (manual). Optional schedule:
  launchd 08:00/18:00 — template in `skills/luemas-archivist/references/autonomy.md`. **Schedule currently OFF.**
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

### PLANNED — next build

**MEMORY INTERVIEWER** — builds out Samuel's brain by asking, not waiting.
- Daily: reads Samuel vault canon, finds a thin spot in your story (people,
  periods, beliefs with no notes), emails you 2–3 specific personal questions.
- Your reply is captured (email thread or a note dropped in the Out Tray) and
  the Archivist files it into Samuel › Personal Memory as a candidate card.
- Status: **does not exist yet.** It appeared in pre-reset briefs but was never
  built. This is the next agent to build once the Archivist has bedded in.

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

---

## Engine Room status

Until a real Engine Room surface exists, each agent run should append to
`~/Luemas/_engine-room/agent-log.jsonl`:

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
