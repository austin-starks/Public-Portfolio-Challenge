---
name: options-structure-rules
description: "The hard structural constraints for the Public Portfolio Challenge momentum-LEAP options book — the spread-shape rule, the take-profit convexity-cap footgun, the affordability ladder, and the known losers not to re-test. Use whenever building or auditing an options strategy structure, checking spread-shape compliance before a certification, choosing DTE/strike rungs, or deciding whether a proposed structure change is even allowed. A violation is an automatic certification FAIL."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /options-structure-rules
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 runbooks
---

# Options Structure Rules

The options structure family is **settled** by episode evidence — only the *signal* (ranking /
weighting / filtering) is normally in play. These are hard constraints; a violation is an **automatic
certification FAIL**.

## The spread-shape rule (hard constraint)

- **Long-dated exposure (≥ ~120 DTE) = outright long calls ONLY.** Uncapped convexity, no short leg.
  No long-dated debit or vertical spreads (e.g. a Mar-'27 ATM/+3/+10/+20 capped vertical is a
  violation and cannot certify).
- **Any debit / vertical spread must be short-dated — expiring in ≤ ~30 DTE.** Thin is fine there.

Re-confirm compliance on every finalist by reading leg DTE/strikes from `get_portfolio`. Violation =
automatic FAIL, no exceptions.

### Short-dated verticals are candidates, not banned

A prior thin **+3%-wide, uncapped, every-name-eligible** ≤30-DTE sleeve FAILED cert (theta bleed,
fee churn, cratered the April-2025 fold). That disproved **one point**, not the class. A short-dated
**wide, share-capped** debit spread is a different structure — let the sweep + OOS cert adjudicate it,
but instrument it so the failure mode can't hide: **width is a gene**, **sleeve share is a capped
gene**, and it must clear the same OOS gates **plus a turnover/fee guardrail** (report per-fold fees +
turnover + sleeve share; a prior sleeve ballooned fees to $1.5–8.9k/fold vs the incumbent's ~$100–600
and must survive the April-2025 fold).

## The settled structure family

Outright-calls-only momentum-LEAP: a **7-rung deep-OTM ladder** (ATM / +10 / +20 / +35 / +50 / +75 /
+100% OTM, 365–730 DTE), TP +250%, affordability backfill, SelectTop 21. Alt-data may touch the rank
signal, entry filters, per-name tilts, or an overlay condition — **never** the structure rungs, the
spread-shape rule, or the universe.

## The take-profit convexity-cap footgun

If multiple "always" take-profit closes exist (e.g. P/L ≥ 20% / 50% / 200%), the **lowest one binds
first** and effectively caps every winner at ~+20% — defeating the uncapped-convexity rationale for
outright calls. It is the single most likely reason returns trail a let-winners-run book. Sanity-check
the exit ladder for this on any live book; the deploy config uses a single high TP (e.g. +250%) or none.

## The affordability ladder (structural feasibility)

At $25k cold start, a single-template ~$1k-per-name book **structurally fails**. Minimum defined-risk
structures on the expensive tail (META / LLY / GS / TSM / ADI / AVGO) cost **$1.3–2.4k per contract**.

- Every template set must end in a rung the **most expensive name can fill** — never remove the
  cheapest rung when sweeping structures.
- Order templates **expensive→cheap** so the engine fills the first affordable rung.
- Cheap structures as the *primary* mechanism = kill path; the ladder must give every name an
  affordable unit.
- `totalBudget ≥ K × perNameAllocation` per tier. Budgets cap **cost basis, not market value** —
  always verify on the tape with `audit_backtest_posture`. Dollar budgets do NOT de-risk like
  %-of-NAV sizing.

See **breadth-audit** for measuring whether the ladder actually participates at fixed $25k.

## Known losers on this book (don't re-test without new cause)

- **Stop-losses on long calls / hold-to-expiry LEAP books** — whipsaw; tested twice, hurt twice.
- **SPY > 200-SMA regime gates** — go flat in 2022 → can't clear the certification activity floor; a
  200D-SMA momentum filter also tested WORST.
- **Long-dated verticals** — banned by the spread-shape rule.
- **Thin short-dated sleeves at uncapped share** — theta-bleed FAIL (see above).
- **Narrow ranked rotation** (top-K ≤ 5 with shared cadence) — keep K > 5.

Cadence note: `DaysSinceLastRebalanceOptionOrder` / `DaysSinceOrder` — `null >= N` is TRUE on fresh
books; the cadence clock is shared across RebalanceOption strategies.
