# LEUMAS ARCHITECTURE — Source of Truth

**Status:** canonical · **Established:** June 2026 · **Supersedes:** all prior
assumptions, including "every vault is a destination" and any four-vault model.

> The system does not need more storage. The system needs a librarian.

This document is the single architectural reference for Leumas, OpenClaw, the
CEO Command Centre, the AI Engine Room, and the move onto the iMac. When any
skill, agent, or doc in this repo conflicts with this file, **this file wins.**

---

## The core problem

Capture was never the problem — organisation is. Files arrive continuously
(Claude Code, Codex, sweeps, email, voice) and no single autonomous process
decides four things: *what a file is, whether it matters, where it belongs, and
what knowledge to create from it.* The result is duplication, overlapping
vaults, noisy search, and fragmented knowledge.

## Design principle

The user decides only one thing: **"keep it."** The system decides everything
else. The user never organises files, never wonders where information belongs,
never manually maintains knowledge.

---

## The six layers

```
L1 CAPTURE      Your Desk (untouched) + ONE Out Tray (the only dump folder)
L2 ARCHIVIST    The librarian agent — classify, decide, route   ← PRIORITY 1
L3 LIBRARY      Master archive (formerly "HoWA Index") — immutable evidence, everything enters, nothing lost
L4 KNOWLEDGE    Two vaults only: Samuel Command + HoWA (distilled understanding)
L5 GRAPH        Relationships across people/companies/projects (future)
L6 SURFACES     CEO Command Centre (outcomes) + AI Engine Room (agents)
```

### L1 — Capture: the Desk and the Out Tray

How Samuel actually works: an active folder on the Desktop holds the files for
whatever he's working on now; when the work is finished, the files should "go
away" — correctly, without filing decisions.

- **The Desk** — any working folder on the Desktop. **The system never touches
  it.** No agent reads, moves, or indexes active work.
- **The Out Tray** — `~/Desktop/Out Tray`, the **single** dump folder and the
  only capture surface. Finished with something? Drag it (or the whole folder)
  into the tray and continue working. That drag is the only filing decision
  that exists: "I'm done with this, keep it."

The earlier five intake folders (Personal Intake, AI Command Intake, HoWA
Intake, Voice Notes, Screenshots) are retired as separate destinations — they
become ordinary contents of the Out Tray (existing ones get dragged in once
and processed). One tray, zero decisions.

### L2 — Archivist Agent (the missing keystone)
A dedicated, single-responsibility digital librarian. **Not** a CEO, strategist,
or assistant. On each run it empties the Out Tray: every file into the Library,
Memory Cards for what matters. See
`.claude/skills/leumas-archivist/SKILL.md` for the implementation.

### L3 — The Library (master archive; formerly "HoWA Index")
Permanent **evidence** layer for the *whole* system — renamed from "HoWA
Index" because that name wrongly implied it belonged to the HoWA vault.
Everything enters; nothing is deleted; it is immutable. Filed by date:
`~/Leumas/Library/YYYY/MM/<file>`, so "where did it go?" always has the same
answer — *the Library, under the month you finished it.* Holds raw source
material only: PDFs, images, emails, exports, screenshots, contracts, audio,
video, notes.
**Library ≠ knowledge. Library = evidence.**

### L4 — Knowledge System (exactly two vaults)
Knowledge is distilled understanding, separated from evidence. **Vaults contain
knowledge only — never raw dumps, never inboxes, never archives.**

**SAMUEL COMMAND VAULT — the founder's brain.** People (Family, Alex, Lyn,
David Williams), Finance (Personal Finance, Creditors, Legal Matters), Health,
Spiritual, AI Systems, CEO Command, Leumas, Personal Memory, Strategic Thinking.

**HOWA VAULT — the company's brain.** HoWA Product (Assistant, Housekeeper,
Steward), Brand (Almanac, Pattern, Creative System), Operations (ServiceOS,
Contractors, Scheduling), Investors, Technology, Insurance, Marketplace.
*(House of Willow Alexander brand/parent material lives here, under Brand —
it is no longer a separate vault.)*

### L5 — Knowledge Graph (future)
Relationships across People, Companies, Projects, Tasks, Investors, Legal
Matters, Products, Conversations. Eventually replaces folder-centric navigation
as the reasoning layer.

### L6 — Surfaces

**CEO Command Centre** — a *generated interface*, not a vault. Pulls from
Archivist, vaults, graph, tasks, agents. Answers "what do I need to know?":
What changed today · Critical issues · Projects · Waiting For · Legal · Finance
· Investors · HoWA · Operations · Personal · AI Systems · Recent Files · Agent
Activity.

**AI Engine Room** — orchestration/visibility of all agents. Answers "what are
the agents doing?": per agent — Name, Purpose, Status, Last Run, Errors, Tasks
Completed. (Archivist, Email, Calendar, Meeting, Research, Investor, Content,
Dashboard agents.)

> The CEO Dashboard and the Engine Room are **different systems — do not merge
> them.** One consumes outcomes; the other manages agents.

---

## Hardware roles

- **Mac Studio — the Founder Factory.** Primary AI infrastructure: agent
  execution, indexing, knowledge processing, vault updates, graph, dashboard
  generation, Engine Room, archive storage.
- **iMac — the Founder Cockpit (future).** Executive interface: consumption,
  review, decisions, approvals, strategy, dashboard interaction.

---

## Priority order

1. **Archivist Agent** ← nothing else creates clarity until this exists
2. Knowledge Promotion System (Memory Cards → vaults)
3. Knowledge Graph
4. CEO Dashboard integration
5. AI Engine Room integration
6. iMac Founder Cockpit

Until the Archivist exists, every other system accumulates complexity faster
than it creates clarity.

---

## One-time migration (do these on the Mac Studio)

The reset only takes effect once the physical setup matches. **The easy way:**
clone/pull this repo on the Mac Studio and run the bundled script — dry-run
first (prints the plan, changes nothing), then apply:

```bash
.claude/skills/leumas-archivist/scripts/setup_leumas.sh           # review the plan
.claude/skills/leumas-archivist/scripts/setup_leumas.sh --apply   # execute
```

It performs steps 1–3 and 5 below (never deletes anything; collisions get a
numeric suffix). Or do it by hand:

1. **Rename the archive.** "HoWA Index" → `~/Leumas/Library`. It is the
   evidence store for the *whole* system, not the HoWA vault. (Keep its
   contents; just rename/move the root and re-point any scripts.)
2. **Create the Out Tray.** `~/Desktop/Out Tray` — the single dump folder.
3. **Retire the five intake folders.** Drag the current contents of Personal
   Intake, AI Command Intake, HoWA Intake, Voice Notes, and Screenshots into
   the Out Tray once, then delete the empty folders. From now on there is one
   tray.
4. **Confirm the two vaults exist** with the folder maps in
   `leumas-archivist/references/routing-rules.md`: `Samuel Command` and `HoWA`
   (with House of Willow Alexander brand under `HoWA/Brand`).
5. **Deploy the skills.** Copy `.claude/skills/leumas-archivist` and
   `.claude/skills/vault-gap-filler` into `~/.claude/skills/`.
6. **First run, on-demand.** `claude -p "empty my Out Tray"` against a small
   batch. Check the routing, correct any mis-routes, then enable the schedule
   in `leumas-archivist/references/autonomy.md`.

After this, the daily loop is: work on the Desk → drag finished files to the
Out Tray → the Archivist files them into the Library and promotes what matters.
