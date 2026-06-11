# Wiki Standard (default)

This is the default standard the **vault-gap-filler** skill checks folders
against. It is intentionally generic — **replace or extend it** with your own
vault's conventions, or point the skill at `_meta/wiki-standard.md` /
`STANDARD.md` in your vault and it will use that instead.

A folder is considered **to standard** when all of the following hold.

## 1. Every folder has an index / MOC

Each top-level folder contains a Map-of-Content note that links to the folder's
notes. Accepted file names (case-insensitive): `index.md`, `<FolderName>.md`,
`_MOC.md`, `README.md`. The MOC should:

- one-line statement of what the folder is for,
- a linked list (or Dataview) of the notes inside it,
- links out to the folders/notes this one depends on or feeds into.

## 2. Every note has frontmatter

```yaml
---
title: <human title>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [<area>, ...]
status: draft | in-progress | complete
---
```

## 3. No empty or orphaned notes

- No zero-content notes. A placeholder must at minimum carry frontmatter and a
  `> [!todo]` callout describing what belongs there.
- Every note is reachable: linked from its folder's MOC or another note.

## 4. Consistent naming

Pick one convention per vault and keep it (e.g. `Title Case.md` or
`kebab-case.md`). The skill flags mixed conventions within a folder.

## 5. Links resolve

Internal `[[wikilinks]]` and relative markdown links point at notes that exist.
Broken links are gaps.

---

## Customizing per folder

If specific folders need required notes (for example a project folder that must
contain `Overview`, `Decisions`, `Open Questions`, `Log`), list them here under
a per-folder section and the skill will treat missing ones as gaps:

```
## Folder: Raise
required: [Overview, Decisions, Open Questions, Log]

## Folder: HoWA
required: [Overview, Scope, Status, References]
```

> [!note] The bundled scanner enforces the structural checks (1–5) generically.
> Per-folder required-note lists are applied by the skill when it reads this
> file, so keep this list current for the folders you care most about.
