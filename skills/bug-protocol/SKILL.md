---
name: bug-protocol
description: "The \"loudly declare\" protocol for platform, engine, or data bugs during a NexusTrade certification campaign — bugs are a first-class deliverable, not something to route around. Use whenever a NexusTrade tool errors, hangs, or returns numbers that contradict the config; whenever you're tempted to write \"probably an engine quirk\"; or when a discovered bug invalidates prior backtests and results must be quarantined. Includes the bug hand-off doc template (see references/BUG_TEMPLATE.md)."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /bug-protocol
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 / episode-11 runbooks
---

# Bug Protocol — "Loudly Declare"

The compute + engine stack is new and moves. **Every failure gets this protocol.** Never paper over an
error to keep a campaign moving — a swallowed bug is worse than a blocked stage. A confabulated
mechanism (inventing why the engine did something) is the worst failure mode: the campaign's worst
moments have been confabulated reconcile events, pricing behavior, and budget behavior. **Verify,
don't assert.**

Precedent: a `totalBudget` over-deployment bug (a book with a 40% budget deployed ~96% of NAV at cold
start) was caught exactly this way and **invalidated weeks of results**. See
`episode-11/attempt2/TOTALBUDGET_BUG.md` for the canonical worked example.

## The five steps (apply on every failure)

1. **Stop and characterize** — is it config (my fault), data (source-side), or engine (NexusTrade)?
   Reproduce **minimally** — the smallest job/backtest that still shows it.
2. **Log it immediately** in the run's `CAMPAIGN_LOG.md` under a `⚠️ BUG/ISSUE` heading: symptom,
   repro IDs, expected-vs-observed, current hypothesis (labeled *hypothesis*), what it blocks.
3. **If it's a real engine/data bug, write a hand-off doc** `<NAME>_BUG.md` in the run directory,
   modeled on the template in `references/BUG_TEMPLATE.md` (one-line summary, expected vs observed,
   reproduction with IDs, leading hypothesis, alternatives to rule out, where to look, impact on
   results).
4. **Quarantine affected results** — mark every backtest/study that ran before the fix as
   suspect/invalid. Re-run after the fix. If the bug inflated leverage, both returns AND drawdowns are
   inflated and any sweep gene it touched may be non-differentiating — re-validate all of it.
5. **Tell the human, prominently, in the chat.** Bugs are a co-equal deliverable of the episode with
   the trading result — not an embarrassment to route around.

## What is NOT a bug (honest-signal failures — don't file these)

- A fold returning `NoEligibleCandidate` = an honest signal, not a bug. Widen validation; don't drop
  the certification floors.
- A dead / not-yet-listed name (e.g. SNDK in 2022) being **absent or in a reject list with no
  fabricated values** = correct behavior. The engine *fabricating* a price/indicator value for a name
  that didn't trade IS a bug (see **engine-sanity**).
- A single-tick reconcile target = the live strategy accretes the rest over daily rebalances — say so,
  don't re-diagnose it as a bug (see **deploy-gate**).

## Verify-don't-assert checklist

Before writing any claim about engine behavior into a deliverable, back it with one of:
`query_backtest_events` / `query_portfolio_events`, a `conditionFieldAudit`, or a minimal
reproduction. "The engine probably…" is not evidence.
