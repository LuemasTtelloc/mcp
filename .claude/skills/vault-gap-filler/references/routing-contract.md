# Routing Contract — Samuel / HoWA / House / Archive

This is the **filing contract** for the whole knowledge system. Every intake
agent (local Llama sweeps, AI command-strategy intake, personal markdown
intake, HoWA index intake) and the vault-gap-filler skill must apply these
rules **at intake time**, before a note is written anywhere.

## The four destinations

Ask the four questions **in order**. First "yes" wins.

### 1. Is it dead? → ARCHIVE (cold storage, not a vault)

Closed matters kept only as evidence: NatWest correspondence, UNCON
decoupling material, WagoCo LTD liquidation, Povey invoice evidence, AMR
payroll emails, CRW lease, out-of-office/auto-reply emails, superseded
contracts.

- Archive is an indexed folder, **not** an Obsidian vault. One index note
  (`Archive Index.md`) lists what is stored and where.
- Rules: never enrich, never summarize, never route into a vault. No
  frontmatter work beyond the index line. Agents spend zero further effort.
- If a live matter needs one fact from the archive, the *vault* note cites the
  archive path; the archive file itself stays untouched.

### 2. Is it about ME? → SAMUEL vault (personal + business self)

Beliefs, taste, reflections, judgement, personal strategy, career, private
impact statements, "how I think" notes, personal finance positions.

- Privacy rule (verbatim from the HoWA intake): *"Keep Samuel's private
  impact/reflection in the Samuel vault."* Nothing personal/reflective ever
  files into HoWA or House.

### 3. Is it about the THING WE SELL? → HOWA vault (the product)

HoWA product canon: Home Intelligence OS concept, product tiers
(Assistant / Housekeeper / Steward), IVP, technical briefs, db schema,
sitemap/page inventory, integration & payment architecture, product GTM,
investor narrative and raise decks for the HoWA raise.

### 4. Is it about WHO SELLS IT? → HOUSE OF WILLOW ALEXANDER vault (parent brand & group)

The trusted institution around the product: brand guidelines and visual
canon, services and the contractor/service model, ecom, marketing strategy,
Willow Alexander Ltd operations, **live** group/Xero structure, partner
relationships.

- Live finance lives here (it belongs to the group). Dead finance is rule 1.
- Org line for reference: *"The House creates trust, HoWA creates
  intelligence, and services turn care into revenue."*

## Intake hygiene rules (apply to every destination)

1. **Dedup before filing.** `X copy.pdf`, `X copy 2`, `X-4`, `X-5`, repeated
   chase emails → keep ONE canonical file, list the duplicates' paths in the
   note's `duplicates:` frontmatter field, do not file them separately.
2. **Normalize naming.** Brand is written `HoWA` (never `HOWA`, `Ho Wa`,
   `howwa`). Strip trailing spaces from file and folder names. One naming
   convention per vault.
3. **Route precisely.** A blanket `Route: howa` on a whole sweep is invalid —
   each item gets its own route from the four questions above.
4. **Media stays at source.** (From the Visual Asset Map handling rule:) do
   not duplicate media files into a vault unless a specific asset is promoted
   to canon/design reference/publishing; link the source path instead.
5. **Unknown route = hold, don't guess.** If none of the four questions gets a
   clear yes, file to an `_inbox/` note in the Samuel vault with
   `status: unrouted` rather than polluting a vault.

## Frontmatter every routed note carries

```yaml
---
title: <human title>
date: <YYYY-MM-DD>
route: samuel | howa | house | archive
source: <original path or Drive link>
tags: [<topic>, ...]
status: draft | active | canon
duplicates: []        # paths of collapsed copies, if any
---
```

`route` must equal the vault the note physically sits in — a mismatch is a
filing error the audit flags.

## Worked examples (from the actual 2026-05 intake)

| Item | Route | Why |
|---|---|---|
| `HoWA_IVP_AI_Comprehensive_Final_Guide` (+ copies 2,3) | howa | Product canon; copies collapsed per hygiene rule 1 |
| `HoWA_Seed_Plus_Investor_Deck.pptx` | howa | Product raise narrative |
| House brand guidelines / `House Brand docs/` | house | Parent brand canon |
| `HoWA_Group_Xero_Structure.docx` | house | Live group finance |
| `HoWA_Marketing_Strategy_FULL.pdf` | house | Brand/services marketing |
| `Service OS training` contracts | house | Contractor/service model |
| WagoCo liquidation docs, CRW lease | archive | Closed matter |
| Povey statements, AMR payroll emails | archive | Evidence only |
| NatWest / UNCON decoupling | archive | Closed matter |
| Personal reflections in sweep output | samuel | Privacy rule |
