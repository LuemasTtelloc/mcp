# Interview Method — finding the gap, asking the question, keeping the words

This is the judgement layer on top of the deterministic scanner. The scanner
finds *where* the vault is thin; this file is *how* to choose the one thing to
ask about and *how* to ask it so the answer is worth keeping.

## Detecting thin spots (ranked by leverage)

Score each candidate gap; ask about the highest-leverage one first.

| Signal | How to spot it | Why it's high-leverage |
|---|---|---|
| **Named-but-empty person** | A name appears in `[[links]]` or prose across ≥2 notes but has no note of its own (or only a stub). | The story keeps referencing someone the vault can't describe. Closing it lights up every note that links to them. |
| **Uncovered period** | Notes allude to a year/company/move/loss ("after the WagoCo wind-down…") with no note that actually covers it. | Foundational context that everything else hangs off. |
| **Asserted-but-unexplained belief** | A value/principle stated flat ("I don't do partnerships") with no origin note. | Beliefs without origins can't be reasoned about or trusted by downstream agents. |
| **Thin relationship** | A person note exists but has no texture — no how-met, no turn, no unresolved. | Cheap to deepen, high payoff for the People graph. |
| **Dangling thread** | An open `> [!todo]` or `status: unrouted` card in `_inbox` that one answer would close. | Converts a known unknown into memory in a single question. |

Leverage = (inbound links to the gap) × (how foundational to the founder's
story). Pick **one**. Announce it: *"This session I'm filling the gap on X,
because N notes reference it and it has no coverage."*

## Designing the questions

Three questions maximum. Each anchored to a **real detail already in the vault**
— that anchor is what makes the question land instead of bounce.

The three-shape default:

1. **Origin** — where it began. *"How did you and Lyn first meet — what was the
   moment you knew this was someone who'd matter?"*
2. **Turn** — what changed it. *"What was the turning point that ended things
   with David Williams, and when did you actually know it was over?"*
3. **Meaning** (optional) — what it taught him. *"Looking back, what did that
   period teach you that still shapes how you decide today?"*

Rules:

- **Specific beats open.** Anchor to a name, date, place, or quote from the
  vault. Never "tell me about your career."
- **Ask *why* and *what changed*, not just *what*.** Facts are cheap; the vault
  wants judgement, cause, and turning points.
- **One thread, not a survey.** All questions should circle the same thin spot,
  pulling it deeper — not scatter across topics.
- **Plain, human, his register.** No therapy-speak, no leading, no flattery.
  A sharp question from someone who's read his notes, not a form.
- **Respect declines.** If he's skipped or declined a thread before, drop it.

## Capture format (keep his words)

Personal memory is worthless as a paraphrase. The card distils for retrieval,
but the **transcript preserves the founder's own voice** — that verbatim record
is also the corpus the local-model ladder later learns his register from.

```markdown
---
title: <human title — the thing learned, not "answer to question 3">
date: <YYYY-MM-DD>
type: memory
route: samuel
vault_path: Samuel/Personal Memory      # or People/<name>, Spiritual/, etc.
source: memory-interviewer <YYYY-MM-DD>
entities: [<person/place/period>, ...]
tags: [<topic>, ...]
status: active
related: [[<note the gap was found in>]]
---

## Summary
<2-4 sentences distilling what this answer establishes — the memory, in the
third person, for fast retrieval.>

## Why it matters
<one line: the relationship/belief/period this now makes legible.>

## Transcript
**Q:** <the question exactly as asked>
**A:** <Samuel's answer, verbatim — lightly cleaned of filler only, never
reworded. This is the keep-his-words rule.>

## Follow-up thread
<the next question this opened, if any — becomes a future session's thin spot.>

## Source
[[<note the gap was found in>]] · memory-interviewer <YYYY-MM-DD>
```

## The ledger (resume cleanly, never repeat)

Persist progress to `Samuel Command/04 Memory Candidates/_MemoryInterviewer/_ledger.md`
(or `_meta/memory-interview.md` if the vault uses a `_meta/` convention). One
row per asked thin spot:

```markdown
| Date | Thin spot | Questions asked | Status | Follow-up thread |
|---|---|---|---|---|
| 2026-06-11 | David Williams — no person note | origin, turn | answered → card on shelf | the 2019 fallout (next) |
| 2026-06-12 | "I don't do partnerships" — no origin | origin | declined | — |
```

On a new session: read the ledger first. Skip answered and declined threads,
follow open follow-ups, and only then scan for a fresh thin spot. Depth over
breadth — one thread pulled all the way is worth more than ten opened.
