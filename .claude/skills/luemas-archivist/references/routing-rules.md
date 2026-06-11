# Routing Rules — Two Vaults + Universal Archive

Canonical model from `.claude/LUEMAS-ARCHITECTURE.md`. Everything is archived as
evidence; only what *matters* gets a Memory Card promoted into **one of two
vaults**.

## Where agent-written cards land: the candidate shelf (review gate)

The archivist NEVER writes directly into a vault's canon. Every card it creates
lands on that vault's **candidate shelf** — a review zone the user promotes
from. In the live vaults this is a numbered folder, e.g. Samuel Command's
`04 Memory Candidates/` (and a `10 Candidate Shelves/` equivalent). Write cards
to a dated batch subfolder so each run is reviewable and reversible:

```
<Vault>/04 Memory Candidates/_Archivist <YYYY-MM-DD>/<card>.md
```

The human promotes a card into canon (the appropriate numbered topic folder)
when they accept it; until then it is a proposal, not knowledge. Mirror the
vault's existing numbered-folder convention rather than inventing flat folder
names — discover the real structure by listing the vault before writing.

## The four questions (in order, first yes wins)

1. **Is it dead / does it not matter?** → **Archive only.** No Memory Card.
   (NatWest, UNCON decoupling, WagoCo liquidation, Povey evidence, AMR payroll,
   CRW lease, auto-replies, superseded drafts, transient noise.) Still archived
   as evidence — just no knowledge promoted.
2. **Is it about ME?** → **Samuel Command vault.** Beliefs, taste, reflections,
   judgement, people/relationships, health, spiritual, personal finance/legal
   position, strategic thinking, AI systems, CEO command, Luemas, personal
   memory.
3. **Is it about the PRODUCT?** → **HoWA vault.** Product canon (Assistant /
   Housekeeper / Steward), IVP, technical briefs, db schema, sitemaps,
   integration & payment architecture, product GTM, investor narrative & raise
   decks, Technology, Insurance, Marketplace.
4. **Is it about WHO SELLS IT (brand / ops)?** → **HoWA vault**, under the
   right wing: Brand (Almanac, Pattern, Creative System — incl. House of Willow
   Alexander brand), Operations (ServiceOS, Contractors, Scheduling), Investors.

No clear yes on 2–4 (but it does matter) → `Samuel/_inbox`, `status: unrouted`.

## Vault folder maps

**SAMUEL COMMAND**
```
People/            (Family, Alex, Lyn, David Williams, …)
Finance/           (Personal Finance, Creditors, Legal Matters)
Health/
Spiritual/
AI Systems/
CEO Command/
Luemas/
Personal Memory/
Strategic Thinking/
_inbox/            (unrouted — needs human decision)
```

**HOWA**
```
Product/           (Assistant, Housekeeper, Steward)
Brand/             (Almanac, Pattern, Creative System; House of Willow Alexander)
Operations/        (ServiceOS, Contractors, Scheduling)
Investors/
Technology/
Insurance/
Marketplace/
```

## Why House of Willow Alexander is not a separate vault

Per the June 2026 architecture reset, only two knowledge domains exist:
founder (Samuel) and company (HoWA). The House of Willow Alexander brand is
*part of the company's brain*, so it lives in **HoWA › Brand**. Live group
finance (e.g. Xero structure) is company knowledge → **HoWA › Operations** (or
Investors if it's raise-facing). Personal finance/creditors/legal → Samuel.

## Worked examples (from the 2026-05 intake)

| Item | Archive? | Card route |
|---|---|---|
| `HoWA_IVP_AI_Comprehensive_Final_Guide` (+copies) | yes | HoWA › Product (copies → `duplicates:`) |
| `HoWA_Seed_Plus_Investor_Deck.pptx` | yes | HoWA › Investors |
| House brand guidelines / `House Brand docs/` | yes | HoWA › Brand |
| `HoWA_Group_Xero_Structure.docx` | yes | HoWA › Operations |
| `HoWA_Marketing_Strategy_FULL.pdf` | yes | HoWA › Brand |
| `Service OS training` contracts | yes | HoWA › Operations |
| WagoCo liquidation, CRW lease, NatWest, UNCON | yes | **archive only — no card** |
| Povey statements, AMR payroll | yes | archive only (cite from a Samuel › Finance › Legal card if a live matter references it) |
| Personal reflection / impact notes | yes | Samuel › Personal Memory / Strategic Thinking |
| A reusable prompt or agent spec | yes | Samuel › AI Systems |
