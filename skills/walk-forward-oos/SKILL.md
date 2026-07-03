---
name: walk-forward-oos
description: "Run and read a NexusTrade walk-forward out-of-sample study — the certification engine behind the Public Portfolio Challenge. Use when certifying a fixed portfolio (backtest_only) or re-optimizing one (sweep), when setting fold_count / anchored / validation / embargo params, when monitoring a run_walk_forward_study to completion, when reading per-fold OOS returns/Sortino/drawdown, or when a variant's fold calendar needs calendar-alignment against a base control. Invoke with the NexusTrade MCP connected."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /walk-forward-oos
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Walk-Forward OOS Certification

The deterministic out-of-sample engine. Walk-forward, **validation mode, anchored, 5 folds,
2022→today** — the OOS folds are the verdict, not a single backtest.

## The study call

`mcp__nexustrade__run_walk_forward_study` (tools are deferred — load via ToolSearch). Always run
`preview_only: true` FIRST to see the fold calendar + cost, confirm it spans 2022→today (must include
both the **2022 bear** and the **April-2025 selloff** — this book's deepest drawdown is an April-2025
event, so the folds have to span it), then flip to `false` and record the `study_id`.

```jsonc
{
  "portfolio_id": "<SUBJECT or a clean clone>",
  "global_start_date": "2022-01-01",
  "global_end_date":   "<TODAY>",
  "fold_count": 5,
  "walk_forward_mode": "anchored",
  "mode": "validation",              // per-fold independent OOS
  "oos_width_days": 252,
  "embargo_days": 14,
  "interval": "Day",
  "inner_mode": "backtest_only",     // certify the FIXED book — no per-fold optimizer
  "preview_only": true               // flip to false to actually run
}
```

- **Certify a fixed book:** `inner_mode: "backtest_only"` (engine_kind ga/default — a sweep is
  rejected for a fixed-config cert).
- **Re-optimize (only on FAIL or a structural change):** `engine_kind: "sweep"`,
  `inner_mode: "optimize"`, `certification: true`, plus `gene_intents`. **GA overfits and is rejected
  for deploy certification — sweep is the certified path.** See **sweep-reoptimization**.
- `certification: true` applies the activity-floor + `percentChange ≥ 0` + `sortino ≥ 0.5` policy and
  defaults `validation_percent` to 50.

## Pre-flight before certifying a live book

1. `get_portfolio` — capture the strategy set, `conditionFieldAudit`, and the exit ladder.
2. **Strip the LaunchAgent.** A LaunchAgent strategy can't run historically — it fires once and logs
   thousands of `cooldownSkip` events, contaminating folds. Certify a LaunchAgent-free clone
   (rebalance + close rules only) and say you did so.
3. **Spread-shape check** the live structures (see **options-structure-rules**). A long-dated vertical
   spread is a hard violation → the book cannot certify as-is; go straight to re-opt.
4. **Convexity-cap footgun:** if multiple "always" take-profit closes exist (e.g. P/L ≥ 20% / 50% /
   200%), the *lowest binds first* and caps every winner at ~+20%, defeating the outright-call
   rationale. Flag it — it's the most likely reason returns trail a let-winners-run book.

## Monitor the study

Poll `list_walk_forward_studies` / `get_walk_forward_study_results <study_id>` until terminal
(`COMPLETE` / `ERROR` / `CANCELLED`). **Parse with jq — payloads are large, don't dump them.** Watch
for known failure modes and surface them (don't paper over — that's a **bug-protocol** trigger):

- **Silent-fail / ERROR** — no fold stats / empty `validationAggregate`. Report it; don't invent a verdict.
- **Wrong window** — fold calendar not starting 2022-01-01 / skipping the bear.
- **Backtest contamination** — LaunchAgent firing in folds (should have been stripped in pre-flight).
- **Zero-trade / NaN folds** — upstream position-marking corruption; report which folds, never average over NaNs.
- A study genuinely hung past its estimated cost/time → stop, summarize, wait for the human (the
  engine may be under repair in another tab).

## The mandatory per-fold checks (these ARE the verdict)

1. **Per-fold OOS table** — for each fold: train window, OOS window, OOS return, OOS maxDD, OOS
   Sortino, median deployment, distinct underlyings, participation. Plus the `validationAggregate`.
2. **Independent re-backtest spot-check** — `backtest_portfolio` ($25k) on the full cycle
   (2022-01-01→today), the 2022 bear (2022-01-01→2023-01-01), and the last 12 months;
   `audit_backtest_posture` the full-cycle run. Study folds must agree with a fresh standalone
   backtest. **Baseline ≠ SPY** for an options book — use a material underlying or equal-weight
   universe B&H, and note it.
3. **Degradation** — train vs OOS per fold. Large train→OOS collapse = overfit, even if the
   full-cycle backtest looks great.
4. **Drawdown honesty** — OOS maxDD next to OOS return per fold; lead with risk. At this leverage a
   fold can post a huge return and a 50–77% drawdown.
5. **Breadth gate** at FIXED $25k (**breadth-audit**).
6. **Reproducibility / field audit** — `conditionFieldAudit` matches intended knobs;
   `compare_backtests {tolerance_bps: 0}` on a re-run. Verify by field, never display name.
7. **Spread-shape compliance** (**options-structure-rules**) — hard reject on violation.

## Calendar alignment (variant vs base)

The walk-forward engine **clips the fold calendar to the indicator's / data's coverage**, so a
variant's study can silently get different folds than the base's. Always run a base CONTROL with the
**same `global_end_date`** as the variant's clipped calendar and compare **fold-for-fold**. Report
per-fold signal coverage next to per-fold OOS. A variant that only wins where the signal exists is a
finding, not a cheat — but say it.
