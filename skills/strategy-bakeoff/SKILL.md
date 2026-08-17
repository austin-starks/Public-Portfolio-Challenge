---
name: strategy-bakeoff
description: "Run a multi-family strategy bakeoff — the SEARCH→CERTIFY funnel that screens many candidate mechanisms down to a certified deploy winner without letting the cheap search layer issue a verdict. Use when replaying the Episode 10 bakeoff, when exploring several distinct strategy families before certifying, when deciding whether \"no deployable winner\" is even a legal conclusion, or when building the per-family certification ledger. Enforces verdict-integrity: only certification can end a campaign."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /strategy-bakeoff
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 runbooks
---

# Multi-Family Strategy Bakeoff

A two-layer **SEARCH → CERTIFY** funnel with a mandated minimum body of work. The central rule:
**a verdict is FORBIDDEN from the search layer.** Only walk-forward certification (**walk-forward-oos**)
can end the campaign.

## Two tools, two jobs

- **SEARCH layer** (cheap): `backtest_portfolio`, `create_portfolio_variant`, `optimize_portfolio`,
  `systematic_sweep`. It may only **KILL or PROMOTE** an idea into certification. It outputs "a ranked
  set of SEEDS" and **may never issue a verdict.**
- **CERTIFY layer** (workhorse): walk-forward sweep certification on promoted seeds. Only this layer
  can conclude PASS / FAIL or "no deployable winner."

`systematic_sweep` over the **deployment × structure × DTE × delta** grid is **mandatory** in the
search layer before any neighborhood is declared dead.

## The mandated minimum body

- **≥ 3 distinct mechanism families certified** before any "no winner" verdict. Genuinely different
  mechanisms, not three tweaks of one family. Family menu (pick ≥3): (a) momentum long calls/verticals;
  (b) regime-switch long/flat; (c) defined-credit / short-premium (earns in flat/down tape); (d)
  calendar / diagonal time-spreads; (e) protective-collar or put-spread-financed longs.
- **Up to 3 certification attempts per family** (re-sweep from a CLEAN seed with refined
  `gene_intents`, deeper grid, or wider validation) before a family is "exhausted."
- **Realistic total: ~3–9 sweep certifications**, plus the incumbent certified as a seed.
- **Each sweep non-trivial: ≥3 `gene_intents` axes × ≥3 values each** (see **sweep-reoptimization** for
  the exact field mappings). A 1-axis or 2-value sweep does NOT qualify.

## Per-family certification ledger (required)

Log this table in the run log — **a family with no ledger row was NOT explored:**

```
| Family | Seed id | get_sweep_surface ✓ | gene_intents axes | Study id | crossFoldRobustSelection key | Assembled book id | Per-fold OOS gate result | PROMOTE / KILL (reason) |
```

## Per-seed certification loop

`get_sweep_surface` → `run_walk_forward_study` (`preview_only` first) → read
`aggregate.crossFoldRobustSelection` → assemble the deploy-shape book → gate on the **assembled**
object → write the ledger row. Certification floors (`certification:true`): participation ≥ 0.35,
distinct names ≥ 9, validation return ≥ 0, validation Sortino ≥ 0.5.

## Verdict-integrity rules (the campaign's central discipline)

- **Zero optimizing certifications = INVALID, not "an honest no-deploy."** Issuing any verdict —
  *especially* "no deployable winner" / "structural infeasibility" — without optimizing certifications
  having run on candidate seeds makes the campaign INVALID. (A prior run declared infeasibility having
  run ZERO optimizing certifications.)
- **No infeasibility claim from N hand-built points** — must cite `systematic_sweep` + the ≥3-family
  body and name the SINGLE binding gate per family with study-id evidence.
- **One counterexample in your own data forbids a blanket infeasibility claim** — localize the binding
  constraint, don't generalize.
- **Binding-constraint attribution:** every kill names the single failed gate + certified evidence.
  "It generally underperformed" is not a kill reason.
- **One mechanism change per candidate** — so a kill/promote attributes cleanly.
- **Remedy-coherence:** a proposed remedy must not contradict the killed candidate's measured state
  (don't propose "raise deployment" for a book that failed under the posture cap; don't propose "add
  convexity" for one that failed on drawdown).

See **options-structure-rules** for the affordability-ladder kill path and known losers, and
**lockbox-holdout** for the baselines (A/B/C) and the final single-touch confirmation.
