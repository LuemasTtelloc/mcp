# Routing Contract — see canonical sources

> **Superseded by the June 2026 architecture reset.** The earlier four-vault
> model (Samuel / HoWA / House / Archive) is retired. There are now **two
> knowledge vaults** plus a universal evidence archive.

The single source of truth is:

- **`.claude/LEUMAS-ARCHITECTURE.md`** — the layered architecture and the two
  knowledge domains.
- **`.claude/skills/leumas-archivist/references/routing-rules.md`** — the
  operational four-question router, vault folder maps, and worked examples.

## What the gap-filler needs to know

- **Two vaults only:** **Samuel Command** (founder's brain) and **HoWA** (the
  company's brain). House of Willow Alexander brand is **not** a separate vault
  — it lives in **HoWA › Brand**.
- **Archive is universal evidence** (the Library, formerly "HoWA Index"), separate from the vaults.
  Vaults hold distilled knowledge only — never raw dumps or archive material.
- During audit, flag any note whose `route:` frontmatter is `house` (legacy) or
  doesn't match the two-vault model, and any raw/evidence material sitting in a
  vault that belongs in the archive.

Use `leumas-archivist` for forward-flow intake; use this skill (vault-gap-filler)
to clean up vaults that already drifted.
