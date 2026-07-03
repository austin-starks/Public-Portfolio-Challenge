---
name: lockbox-holdout
description: "The single-touch lockbox — a final anti-overfitting holdout run once, after design freeze, on a window held out from every fold, sweep, and search. Use when finalizing a bakeoff winner before deploy, setting up the A/B/C baselines as OOS bars, or running the S1.5 gate-coherence auto-relax. Covers why looking at the lockbox twice burns it, the lockbox pass conditions, and the three baselines. The lockbox is distinct from the walk-forward OOS folds."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /lockbox-holdout
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Single-Touch Lockbox & Baselines

The lockbox is a final holdout that no fold, sweep, or search ever touches — the last line of defense
against calendar-fit selection pressure. It is **distinct** from the walk-forward OOS folds
(**walk-forward-oos**), which are used repeatedly during search; the lockbox is touched **exactly once.**

## The lockbox

- **What:** the walk-forward span stops `lockbox_width_days = 126` (~6 months) *before* the run date.
  That final window `(run date − 126d) → run date` is the lockbox — held out from ALL folds, ALL
  sweeps, ALL search.
- **How:** only the assembled deploy-shape book that **already passed every gate on the walk-forward
  aggregate** runs over the lockbox, **exactly once**, *after design freeze* (Stage S2).
- **Pass conditions (frozen at S0, do not move them after seeing results):**
  - lockbox OOS return ≥ worst single-fold walk-forward OOS return;
  - lockbox maxDD ≤ 55%;
  - posture clean (`audit_backtest_posture`, all four conditions);
  - breadth ≥ 9 eligible names (`audit_backtest_breadth` — see **breadth-audit**).

## Single-touch is absolute

**If you look at the lockbox and then iterate the design, the lockbox is burned** — move the
walk-forward span back and hold out a fresh tail before any deploy. A lockbox failure is treated as
calendar-fit selection pressure and means **no deploy**, except by a logged owner override that
explicitly names the lockbox.

## The three baselines (A/B/C) as OOS bars (Stage S1)

Loaded from committed `snapshots/*.json` via `create_portfolio`. Score A and B on the current engine;
copy C's frozen published numbers as the bar to beat.

- **A — equity buy&hold** (the full universe). A **return bar only, never a Sortino bar** — its Sortino
  reflects an equity-rally smoothness a leveraged long-premium book can't match.
- **B — naive LEAP ladder** (canonical spec: all names, no rank/filter, 14-day cadence, 8%-of-portfolio
  per name under 95% budget, structure = first affordable rung of
  `[Δ0.50 call → Δ0.55/0.25 → Δ0.55/0.40 → Δ0.50/0.42 vertical]`, all 180–365 DTE, single exit at
  DTE ≤ 45). A **Sortino bar only in folds with ≥ 9/20 breadth.**
- **C — frozen incumbent bar** with published per-fold OOS numbers, copied verbatim (do not re-run to
  "improve" them).

## S1.5 — Gate-coherence auto-relax (deterministic, no owner round-trip)

Before designing, check whether "beat Baseline B" and the ≤55% posture cap are **jointly satisfiable**
— B is a ~95%-deployed book, so a posture-capped finalist can't out-deploy it. If unsatisfiable,
**AUTO-RELAX Baseline B**: derate B's `totalBudget` until its own median daily deployment ≤ 55%, re-run
its S1 scoring, and log original vs posture-matched B. This is **not a gate relaxation and not an owner
decision** — only the benchmark is made comparable; the thresholds stay frozen.
