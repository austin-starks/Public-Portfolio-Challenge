---
name: breadth-audit
description: "Measure a NexusTrade options book's TRUE participation at a fixed cold-start capital base, defeating the compounded-NAV breadth illusion. Use whenever a book's headline \"holds N/21 names\" needs validating, when a live book collapses to a single name (the OSCR trap), when checking whether a SelectTop / per-name-allocation / total-budget change degraded simultaneous participation, or when a certification needs a breadth gate. Uses audit_backtest_breadth at held-fixed $25k."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /breadth-audit
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Fixed-Capital Breadth Audit

Breadth is measured at **FIXED $25k**, never inferred from a compounded backtest. This is the whole
point of the participation lesson: a headline like "19/21 names" is almost always an artifact.

## The breadth illusion

"19/21 names" on a full-cycle run means **nothing** — it is NAV compounding + distinct-names-*over-time*.
A book that compounds to ~$300k notional will touch many names across the run while, at cold-start
$25k, it funds only the cheapest one or two and strands the rest. The live proof of this: a certified
book that "held 19/21" deployed live and **only bought OSCR**, because at $25k a 5%-per-name budget
(~$1,200–1,450) only ever afforded the cheapest underlying's LEAP.

**Root cause pattern:** at low NAV a per-name budget affords only the cheapest name's contract, and the
sizing policy **strands the budget on unaffordable top-weighted names** instead of flowing it to the
next affordable one → the book collapses to one name.

## How to measure

Use `mcp__nexustrade__audit_backtest_breadth` at a **held-fixed** capital base (don't let the run
compound). Capture, per the current config:

- **simultaneous distinct names held** (the headline number — lead with it),
- `participation`,
- `distinctNamesFilled`,
- per-name `cannotAfford` counts.

Run it on the 12-month window and separately on the full cycle. For a live collapse, also pull
`query_portfolio_events` (`OptionResolutionAttempt`) to see the "Cannot afford even 1 contract"
rejections and which names cleared — that is the live evidence.

## SelectTop truncates BEFORE affordability

`SelectTop N` truncates the candidate pool *before* the affordability backfill runs. A narrow top-N
re-creates the single-name collapse — which is exactly why the certified incumbent is **top-21** (21 of
21 never truncates, so the rank ORDER only decides funding priority, never membership). If you narrow
SelectTop, re-run this audit.

## The breadth gate (in certification)

A variant must **not degrade cold-start participation** vs the incumbent. Concretely for a
participation-repair campaign: simultaneous distinct names ≥ target, `participation ≥ ~0.5`,
`cannotAfford` sharply down vs the *before* state. **A config that certifies but still funds one name
is a non-answer** — breadth without gain and gain without breadth both FAIL a participation attempt.

Entry filters (S3-style alt-data filters) are the main breadth risk — the filtered subset must stay
affordable and broad, so always re-check cold-start breadth after adding one.

## Levers that move breadth (all keep outright-calls-only)

- **Raise per-name allocation** — funds ≥1 contract on more names, but fewer simultaneous slots.
- **Affordability-aware backfill / guarantee-1-contract-to-top-N** — the most direct low-NAV lever;
  verify the engine actually backfills (it has historically *not*). Note: the backfill loop is also
  where the `totalBudget` over-deployment bug lived — see **bug-protocol**.
- **Rung depth / count** — deeper OTM cheaper rungs let premium names enter; watch convexity erosion.
- **Total budget** — more slots fillable; interacts with per-name alloc.

Changing any sizing lever is a **structural change** → re-sweep, don't inherit knobs
(**sweep-reoptimization**).
