---
name: sweep-reoptimization
description: "Re-optimize a NexusTrade strategy with a walk-forward SWEEP and label parameter provenance — the discipline that prevents deploying inherited knobs. Use whenever a structural change (sizing, rung depth, universe membership, DTE family, adding a rank signal) forces a re-sweep, when authoring gene_intents from get_sweep_surface, when choosing sweep over GA for a deploy cert, or when selecting the cross-fold-robust winner instead of the per-fold argmax. Invoke with the NexusTrade MCP connected."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /sweep-reoptimization
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Sweep Re-Optimization & Provenance

The three standing methodology rules that exist because a deploy candidate was once certified on knobs
**inherited from a sweep on a *different* structure** and presented as "optimal."

## The three standing rules (binding on all future episodes)

1. **Re-optimize on ANY structural change — never inherit a genome across structures.** Knobs (TP,
   total budget, per-name size, rank window, VIX gate, entry cooldown, DTE bracket) are
   **structure-dependent**. Whenever the structure changes — affordability rungs, strike depths,
   universe membership (e.g. adding a name), DTE family, entry/exit shape, or **adding an alt-data rank
   signal** — re-run the `engine_kind:"sweep"` walk-forward on the NEW book *before* certifying. A
   `backtest_only` cert on inherited knobs only confirms the book **generalizes**; it does **not**
   establish the knobs are **good for that structure**.
2. **Separate "explore designs" from "optimize the chosen design."** Screen candidate designs → pick
   one → **then sweep that exact design's knobs** → **then** `backtest_only`-certify. If the screen
   picks design X, the sweep base must be **X itself**, not its neighbours. Never sweep the losers'
   variants while leaving the chosen book hand-tuned.
3. **Label every deployed parameter's provenance** in the deliverable —
   `swept-on-this-book` / `inherited-from <study-id>` / `hand-set`. **"Inherited" is amber, not green,**
   until re-swept on the current structure.

**Self-check trigger words:** "carry over the knobs," "reuse the winner's params," "same config on the
new ladder," "already certified, no need to re-sweep," "just raise the allocation." Each must prompt:
*did the structure change since those knobs were searched? If yes → re-sweep before certifying.*

## Running the sweep

1. `get_sweep_surface` on the chosen book (or a clean clone) FIRST to get the **real sweepable field
   names**. **Re-sweep from a CLEAN seed** — re-sweeping an already-swept book can stack/duplicate
   genes; field-audit for duplicated conditions.
2. `run_walk_forward_study` with `engine_kind:"sweep"`, `inner_mode:"optimize"`, `certification:true`,
   `mode:"validation"`, anchored, 5 folds (4 acceptable), 2022→today, `oos_width_days:252`. See
   **walk-forward-oos** for the full param block. **GA overfits and is rejected for deploy
   certification — sweep is the certified path.** `preview_only:true` first to compile genes + cost-check.
3. **Each sweep must be non-trivial: ≥3 `gene_intents` axes × ≥3 values each** (e.g. `BuyingPowerPct`,
   `TakeProfitPct`, `RollTriggerDte`, rank depth, delta band, DTE). A 1-axis or 2-value sweep does not
   qualify.

### Exact sweep field mappings (get these wrong and the sweep is meaningless)

- **Take-profit = `TakeProfitPct` on Action scope.** *Never* sweep it as
  `ExitCondition`/`OptionPositionPercentChange`.
- **Roll DTE = `RollTriggerDte` on Action scope** (roll the CloseOption only).
- `CloseOption` pnl triggers: `minPnlPercent:100` = +100% TP; `maxPnlPercent:-50` = −50% stop;
  DTE roll = `{type:"dte","maxDte":45}`.

## Selecting the winner (robust, not argmax)

Read `aggregate.crossFoldRobustSelection` — `metric:"minSortino"`, `candidateKey`, `score`,
`perFoldSortino`: **the grid cell with the highest *minimum* validation Sortino across folds.** Compare
it against each fold's `selectedCandidateKey`, `aggregate.dominantCandidateKey`, and
`winnerStableAcrossFolds`. **Deploy the cross-fold-robust config, never the per-fold argmax** — the
per-fold winner is high-variance noise.

Then run the full **walk-forward-oos** Stage-C checks 1–7 on that winner before it may be the finalist,
and attach provenance labels (rule 3).

## Custom indicators are NOT sweepable

The sweep engine's `allowedIndicatorTypes` does not include `CustomIndicator`, so alt-data
indicator-shape exploration is a **hand-built variant grid** (`create_portfolio_variant`: deep-copy
base + JSON-Pointer patch, `dry_run` first), each certified `backtest_only` and labeled **hand-set
(amber)**. The classic knobs (alloc / budget / TP / SelectTop / DTE) remain sweepable if a winner
warrants a knob re-sweep. See **alt-data-indicators**.
