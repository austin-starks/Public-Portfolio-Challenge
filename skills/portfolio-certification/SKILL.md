---
name: portfolio-certification
description: "Orchestrate an out-of-sample certification of a NexusTrade trading strategy or live book — the master discipline behind the Public Portfolio Challenge. Use whenever you must decide PASS/FAIL on whether a portfolio holds up out of sample before deploying real money, replaying the episode-10/episode-11 runbooks, or running a \"certify my book\" / \"prove it out of sample\" / \"re-certify the fix\" task with the NexusTrade MCP connected. Pulls in walk-forward-oos, breadth-audit, sweep-reoptimization, options-structure-rules, bug-protocol, and deploy-gate."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /portfolio-certification
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Portfolio Certification

The umbrella skill for the Public Portfolio Challenge. You are the **orchestrator + independent
verifier**: you run the deterministic NexusTrade tools directly and the numbers are your own — there
is no agent whose results you are second-guessing. Certification is a **holistic PASS/FAIL verdict**
read from out-of-sample walk-forward folds, never a single aggregate number.

## First principles (binding across every run)

1. **OOS is the only headline.** Never present train/validation numbers as evidence of
   generalization. A great full-cycle backtest with a train→OOS collapse is a FAIL.
2. **The value lives in the DESIGN, not the optimizer.** The sweep is a modest knob-setter that
   confirms a design's neighborhood. Spend effort on the strategy design; ask the sweep for little.
3. **Deploy the cross-fold-robust config, never the per-fold argmax.** Validation score is a noisy
   proxy; the per-fold winner is high-variance. Use maximin OOS Sortino / robust selection.
4. **Verify at the FIELD level, never by display name.** Use `conditionFieldAudit`; copy indicator
   IDs exactly from the catalog. Confirm the SUBJECT by field/posture, never by its name.
5. **Verify, don't assert.** Every claim about engine behavior gets checked against events, fields,
   or a reproduction before it appears in a deliverable. "Probably an engine quirk" → run the
   **bug-protocol**, don't hand-wave.
6. **A null result honestly reported is a valid outcome.** Don't torture variants until one "wins" —
   that is the per-fold-argmax trap in a costume. Ties or noise-level deltas → keep the incumbent.
7. **No deploy, no orders** until the human explicitly says "deploy + clean up" (the **deploy-gate**).

## Standard run structure

Every certification campaign follows the same staged shape. Adapt the middle; the bookends are fixed.

- **Stage A — Baseline + inventory.** Confirm the SUBJECT by field (`get_portfolio`), re-verify the
  incumbent bar, spot-check one fresh `backtest_portfolio` + `audit_backtest_posture`, and — if the
  book is live — check pending-order state and `automaticOrderApproval`. Deliver a one-paragraph
  *before* state. When live behavior is the problem, reproduce it with hard numbers first
  (`query_portfolio_events`), then fix.
- **Stage B/C — Build + certify.** Run the certification proper. See **walk-forward-oos** for the
  study mechanics and the mandatory per-fold checks, **breadth-audit** for fixed-$25k participation,
  **options-structure-rules** for the hard spread-shape gate, and **sweep-reoptimization** if any
  structural change forces a re-sweep.
- **Stage D — Present, then stop.** Deliver a decision-ready package: **verdict up top, one line**;
  per-fold OOS table + aggregate; side-by-side vs the incumbent with the trade made explicit;
  finalist's plain-English rules + `conditionFieldAudit` + build id; **provenance labels on every
  parameter** (`swept-on-this-book` / `inherited-from <study-id>` / `hand-set` — inherited is amber);
  honest caveats (hindsight in the frozen universe, options fill realism, leverage/fragility, worst
  drawdown was the **April-2025** selloff, baseline caveats). Include the bug ledger. **No deploy.**
- **Stage E — Deploy (GATED).** Only after explicit "deploy + clean up". See **deploy-gate**.

## The holistic PASS test (no per-fold-green rule)

Certify **PASS** when the *majority* of OOS folds are profitable, OOS Sortino is positive and
reasonably steady (rough floor ~0.5), drawdown is within tolerance you'd actually hold, deployment is
stable across folds, and train→OOS degradation is modest. One weak fold ≠ FAIL. Persistent OOS
losses, exploding drawdown, or train-only strength = **FAIL**. A hard-constraint violation
(spread-shape, breadth collapse) = automatic FAIL regardless of return.

## "Better than the incumbent" (variant campaigns)

When testing a variant against a live/certified bar, "better" = held FIXED across the same folds, it
improves OOS return at no-worse risk, OR materially improves risk (Sortino/DD) at similar-ish return,
OR demonstrably improves the weak regime (bear-fold), **with breadth not degraded**. Comparisons must
be **calendar-aligned** (run a base control on the variant's clipped calendar — see walk-forward-oos).

## Self-check trigger words

- "the backtest proves it" → OOS folds or it didn't happen.
- "reuse the winner's knobs" / "already certified" → did the structure change? If yes → re-sweep
  (**sweep-reoptimization**) before certifying.
- "19/21 names" / "great breadth" → measure at FIXED $25k (**breadth-audit**); compounded breadth is
  an illusion.
- "the indicator looks predictive" → certify it, don't eyeball it.
- "probably an engine quirk" → **bug-protocol**: verify, don't assert.

## Source runbooks (worked examples of this discipline)

- `episode-10/BAKEOFF_RUNBOOK.md` — engine sanity checks, 16-variant bakeoff, walk-forward cert, lockbox.
- `episode-11/attempt1/RUNBOOK.md` — certify the live book; re-optimize on FAIL.
- `episode-11/attempt2/RUNBOOK.md` — reproduce a live collapse, repair participation, re-certify.
- `episode-11/attempt3/RUNBOOK.md` — add alternative data to a certified book and prove it OOS.
- `episode-11/attempt*/CAMPAIGN_LOG.md` — the full lessons ledger these skills distill.
