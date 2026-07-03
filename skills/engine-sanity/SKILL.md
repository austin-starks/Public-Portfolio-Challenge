---
name: engine-sanity
description: "The mandatory pre-flight contract checks (Stage S0) that must pass before trusting NexusTrade's certification engine for any strategy work. Use at the start of a bakeoff or certification campaign to prove the walk-forward engine runs end-to-end, windows don't leak, fold winners persist, and the engine doesn't fabricate values for dead/not-yet-listed names. Each check has a STOP-and-report failure mode; these runs do NOT count toward any certification minimum."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /engine-sanity
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Engine Sanity Checks (Stage S0)

**MANDATORY; blocks everything.** Four contract checks that prove the certification engine is
trustworthy before any design work. Each has a STOP-and-report failure mode — a failure here means the
engine itself is broken (**bug-protocol**), and no downstream number can be trusted. These S0 runs
(and S1 baseline scoring) explicitly **DO NOT COUNT** toward the certification-body minimum — they are
contract checks and benchmarks, not candidate certifications.

## The four checks

1. **Walk-forward sweep smoke.** `create_portfolio` a trivial book (e.g. `SPY > SMA50`). Run
   `run_walk_forward_study` with `mode:"validation"`, `fold_count:2`, `engine_kind:"sweep"`, one
   `gene_intent` × 3 values, `certification:false`. It must start and complete with per-fold OOS +
   aggregate.
   *Proves: the certification engine actually runs end-to-end.*

2. **Window fidelity (one fold).** Backtest the materialized fold winner on its validation and OOS
   windows; the fold's `validationStatistics` / `oosStatistics` must match standalone backtests within
   rounding. Confirm **disjointness**: train∩validation, train∩OOS, validation∩OOS all empty, and OOS
   starts after validation ends.
   *Proves: the walk-forward windowing isn't leaking.*

3. **Persistence.** `get_walk_forward_study_results` returns a real `selectedChatPortfolioId` for every
   completed fold.
   *Proves: fold winners materialize as real objects you can inspect/deploy.*

4. **Dead-name handling.** Tiny 2022-window backtest on the full universe including a name not yet
   listed then (e.g. SNDK). **Pass:** the name is absent, or appears in a not-yet-listed reject list
   **with no fabricated price/indicator values**. **Fail:** the engine errors, or returns any non-null
   reading for a name that didn't trade.
   *Proves: the engine doesn't fabricate data on not-yet-listed names.*

## On failure

Any failed S0 check → **STOP**, file the **bug-protocol** hand-off doc, and do not proceed to design
work. A broken engine invalidates everything downstream; there is no point certifying strategies on it.
