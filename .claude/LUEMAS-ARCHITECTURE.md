# LUEMAS ARCHITECTURE — Source of Truth

**Status:** canonical · **Established:** June 2026 · **Supersedes:** all prior
assumptions, including "every vault is a destination" and any four-vault model.

> The system does not need more storage. The system needs a librarian.

This document is the single architectural reference for Luemas, OpenClaw, the
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
L1 CAPTURE      Desktop intake folders (dump zone, zero filing decisions)
L2 ARCHIVIST    The librarian agent — classify, decide, route   ← PRIORITY 1
L3 ARCHIVE      "HoWA Index" — immutable evidence, everything enters, nothing lost
L4 KNOWLEDGE    Two vaults only: Samuel Command + HoWA (distilled understanding)
L5 GRAPH        Relationships across people/companies/projects (future)
L6 SURFACES     CEO Command Centre (outcomes) + AI Engine Room (agents)
```

### L1 — Capture
Desktop is the universal capture surface. Existing intake folders stay:
Personal Intake, AI Command Intake, HoWA Intake, Voice Notes, Screenshots.
Workflow: drag, drop, continue. No decisions.

### L2 — Archivist Agent (the missing keystone)
A dedicated, single-responsibility digital librarian. **Not** a CEO, strategist,
or assistant. It monitors intake, analyses each file, and runs the process
below. See `.claude/skills/luemas-archivist/SKILL.md` for the implementation.

### L3 — Master Archive ("HoWA Index")
Permanent **evidence** layer. Everything enters; nothing is deleted; it is
immutable. Holds raw source material only: PDFs, images, emails, exports,
screenshots, contracts, audio, video, notes.
**Archive ≠ knowledge. Archive = evidence.** (Note: the folder is named "HoWA
Index" but is the archive for the *whole* system, not the HoWA vault.)

### L4 — Knowledge System (exactly two vaults)
Knowledge is distilled understanding, separated from evidence. **Vaults contain
knowledge only — never raw dumps, never inboxes, never archives.**

**SAMUEL COMMAND VAULT — the founder's brain.** People (Family, Alex, Lyn,
David Williams), Finance (Personal Finance, Creditors, Legal Matters), Health,
Spiritual, AI Systems, CEO Command, Luemas, Personal Memory, Strategic Thinking.

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
