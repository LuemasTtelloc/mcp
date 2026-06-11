---
name: vault-gap-filler
description: >-
  Audit an Obsidian/markdown knowledge vault against a wiki standard, then fill
  the gaps one folder at a time. Use when the user says things like "audit my
  vault for gaps", "check my vault against the wiki standard", "what's missing
  in my vault", "fill in the next folder", or asks which vault folder to work on
  next. Phase 1 reports whether the structure matches the standard and ranks
  folders by how much downstream work they block; Phase 2 fills exactly one
  folder per session.
---

# Vault Gap Filler

A two-phase workflow for bringing a markdown knowledge vault (Obsidian-style,
but any folder-of-`.md`-files vault works) up to a defined wiki standard.

- **Phase 1 — Audit (read-only).** Determine the standard, score every
  top-level folder against it, rank folders by *downstream blocking impact*,
  and answer one question definitively: *does the structure match the standard?*
- **Phase 2 — Fill (one folder per session).** Take the highest-ranked folder
  and bring it to standard, drawing on existing vault material. Then stop and
  record progress so the next session resumes cleanly.

## Hard constraints

1. **One folder per session.** Phase 2 fills exactly one folder, then stops.
   Do not "just also do the next one." This keeps each session reviewable and
   prevents large unverifiable rewrites. If the user explicitly asks for more,
   confirm folder-by-folder.
2. **Never invent facts.** Gap-filling means scaffolding structure, surfacing
   and linking content that already exists elsewhere in the vault, and marking
   genuine unknowns as `> [!todo]` stubs — *not* fabricating information. If a
   required note has no source material, create the stub and list it as an open
   item; do not write plausible-sounding content.
3. **Audit before filling.** Always run Phase 1 (or load the most recent
   ledger) before touching files in Phase 2. The ranking decides what to fill.

## Phase 1 — Audit

### 1. Locate the vault and the standard

- The vault root is the current working directory unless the user points
  elsewhere. Confirm if ambiguous.
- Determine the **wiki standard** in this order of preference:
  1. An explicit standard the user has written, e.g. `_meta/wiki-standard.md`,
     `STANDARD.md`, or a `templates/` folder. Read it and use it verbatim.
  2. The skill's reference standard at `references/wiki-standard.md`, adapted to
     what the vault's most complete folders already do.
  3. If neither exists, infer the standard from the 2–3 most complete folders
     (they are the de-facto exemplars) and **state the inferred standard back to
     the user** before scoring, so they can correct it.

### 2. Run the audit scan

Run the bundled scanner from the vault root:

```bash
python3 .claude/skills/vault-gap-filler/scripts/audit_vault.py <vault-root>
```

It walks every top-level folder and reports, per folder:

- presence of an index / MOC note,
- note count, empty notes, and notes missing YAML frontmatter,
- a **completeness score** (0–100) against the default checks, and
- a **blocking score** = how many notes *elsewhere* in the vault link *into*
  this folder (inbound `[[wikilinks]]` and markdown links). High inbound links
  + low completeness = high downstream blocking.

The scanner is deterministic and read-only. Treat its numbers as the backbone
of the report; layer the standard-specific judgement (required sections, naming,
frontmatter fields) on top of it. Pass `--json` if you want to post-process.

### 3. Write the gap report and ledger

Produce a short report for the user and persist a ledger so future sessions
resume. Use `references/audit-ledger-template.md` and write it to
`_meta/vault-audit.md` in the vault (create `_meta/` if needed). The report must:

- State plainly **whether the structure matches the standard** (the user's
  first question), with the specific deviations.
- List folders **ranked by blocking impact**, each with its completeness score
  and the concrete missing items.
- Name the **single folder to fill next** (the top of the ranking). The brief's
  expectation is that high-leverage folders such as `Raise` or `HoWA` surface
  first because they block the most downstream notes — verify that against the
  actual scores rather than assuming it.

Stop here. Do not start filling in the same step unless the user says to
continue into Phase 2.

## Phase 2 — Fill (one folder per session)

### 1. Pick the folder

Default to the top-ranked folder from the ledger. If the user named a folder,
use that. Announce which folder you're filling and why (its rank/score).

### 2. Bring it to standard

Working only inside that folder:

- Create the missing **index / MOC** note linking the folder's notes.
- Add required **frontmatter** to notes that lack it (per the standard).
- Scaffold **missing required notes** from the template, with real content
  pulled from existing vault material where it exists, and `> [!todo]` stubs
  where it does not.
- Fix **broken or missing links** within the folder and to its known
  dependencies.
- Normalize **naming** to the standard's convention.

Keep edits scoped to this one folder. Do not refactor the rest of the vault.

### 3. Record and stop

- Update `_meta/vault-audit.md`: mark this folder's status, note remaining open
  `todo` items, and re-confirm the next folder in the ranking.
- Summarize for the user: what was created/changed, what open items remain, and
  which folder is queued next.
- **Stop.** One folder per session.

## Resuming

On a later invocation, if `_meta/vault-audit.md` exists and is recent, offer to
skip straight to Phase 2 on the next-ranked folder instead of re-auditing. Re-run
Phase 1 if the vault has changed materially or the user asks for a fresh audit.

## Routing across vaults

Per the June 2026 architecture reset (`.claude/LUEMAS-ARCHITECTURE.md`), there
are **two knowledge vaults** — **Samuel Command** (founder's brain) and **HoWA**
(company's brain, including the House of Willow Alexander brand under HoWA ›
Brand) — plus a **universal evidence archive** (the Library, formerly "HoWA Index") that is separate
from the vaults. Vaults hold distilled knowledge only.
`references/routing-contract.md` points at the canonical routing rules. During
Phase 1, flag notes whose `route:` is the legacy `house` value or otherwise
mismatches the two-vault model, and flag raw/evidence material sitting in a
vault that belongs in the archive. During Phase 2, misrouted notes are
*reported*, not silently moved — list them for the user.

## Files in this skill

- `scripts/audit_vault.py` — deterministic, stdlib-only Phase 1 scanner.
- `references/wiki-standard.md` — the default standard; the user customizes this
  or points the skill at their own.
- `references/routing-contract.md` — pointer to the canonical two-vault routing
  rules (Samuel Command / HoWA, plus the Library as universal evidence).
- `references/audit-ledger-template.md` — shape of `_meta/vault-audit.md`.
