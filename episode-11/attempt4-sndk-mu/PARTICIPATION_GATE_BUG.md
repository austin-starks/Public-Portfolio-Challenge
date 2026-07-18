# Diagnose: walk-forward fold gate excludes trading folds as "zero participation" on direct OpenOption books

> **STATUS: RESOLVED 2026-07-03.** Human fixed the engine. Verification rerun `6a480c9490a070a491e5c0b3` (identical params to the quarantined study `6a47fde3bfe7b4bb6c3a0e1c`) completed with 5/5 folds producing full OOS statistics. Quarantined study superseded by the rerun.

## One-line
A `backtest_only` walk-forward study on a two-name direct-OpenOption book (no RebalanceOption / no universe) marked **all 5 folds `NO_SIGNAL` with error "Training window had zero participation"** even though every fold's own statistics show real trading (dollarsSold ≈ $54k, fees ≈ $367, winRate ≈ 64%), so the study completed with **zero OOS statistics** and cannot issue a verdict for this book shape — likely because the gate keys on `participationRate`, which is structurally 0 when `universeSize` = 0.

## Expected vs observed
- **Expected:** `inner_mode: backtest_only` certifies the fixed book: each fold runs train/validation/OOS backtests and reports per-fold OOS return/Sortino/maxDD; a fold is excluded only if it genuinely never traded.
- **Observed:** study `6a47fde3bfe7b4bb6c3a0e1c` — every fold `status: "NO_SIGNAL"`, `error: "Training window had zero participation; fold excluded from selection scoring."`, `aggregate.foldsComplete: 0`, no `oos*` stats at all. Yet the same folds' `trainingStatistics` show `dollarsSold: 52768–54324`, `totalFees: 358–367`, `winRate: 64.2–64.5%`, `medianDeployment` up to 14.4% — the book demonstrably traded in the training windows. "Zero participation" contradicts the fold's own tape.

## Reproduction
- Portfolio: `6a47fd429abb2b74b1e33003` ("Semiconductor Momentum Spreads V3 (30d/15d affordable)") — two direct OpenOption vertical strategies (MU, SNDK; 30Δ/15Δ call debit spreads, 21–30 DTE, $2,667/ticket, RSI(14)>50 entry, OptionSpreadCount<1 gate) + one CloseOption rule. No RebalanceOption, no universe, no LaunchAgent.
- Study: `6a47fde3bfe7b4bb6c3a0e1c` — validation mode, anchored, 5 folds, 2022-01-01→2026-07-03, oos_width 252, embargo 14, `inner_mode: backtest_only`. Root optimizer `6a47fde3bfe7b4bb6c3a0e20`.
- Supporting single backtest: `6a47fd4f9abb2b74b1e33032` (same portfolio, 2024-01-01→2026-07-03, $8k): `percentChange +605.4%`, `dollarsSold $937k`, **`participationRate: 0`, `universeNamesTraded: 0`, `universeSize: 0`** — participation is 0 even on a wildly active run.

## Leading hypothesis (verify, don't assume)
*Hypothesis:* the fold-inclusion gate tests `participationRate > 0` (or `universeNamesTraded > 0`). Those metrics are computed from the rebalance-universe machinery and are **always 0 for direct OpenOption strategies** (universeSize = 0 ⇒ participation undefined ⇒ reported as 0). So every fold of any non-universe options book is excluded regardless of actual trading, and `backtest_only` certification is structurally impossible for this book shape.

## Alternatives to rule out (so this isn't a false alarm)
1. **Metric definition.** If "participation" is *defined* as universe participation, the metric itself is correct — but then the fold gate is using the wrong metric for non-universe books; `dollarsSold > 0` or trade count is the honest activity test. Either way the fold exclusion is wrong.
2. **By design.** Possibly the cert engine only supports RebalanceOption books (all prior challenge certs were SelectTop-21 books). If so, `run_walk_forward_study` should reject direct-OpenOption books up front instead of returning a COMPLETE study with an empty verdict.

## Where to look
- The fold scoring/exclusion code path that emits "Training window had zero participation; fold excluded from selection scoring" — check which statistic it reads.
- The statistics assembler that leaves `participationRate`/`universeSize` at 0 for books with no RebalanceOption strategy.

## Diagnostic checks
1. Minimal: run the same study on any single-name direct OpenOption book that provably trades in every window; if all folds return NO_SIGNAL, the gate is metric-broken.
2. A/B: same signal expressed as a 2-name RebalanceOption book vs direct OpenOption — the RebalanceOption variant should produce fold stats while the direct book is excluded, isolating the gate.

## Impact on prior results (why this blocks conclusions)
- Study `6a47fde3bfe7b4bb6c3a0e1c` is **not a valid certification verdict** in either direction — quarantined. No OOS numbers exist.
- Plain `backtest_portfolio` runs are unaffected (they report fine; only `participationRate` is meaningless on them).
- Independent of this bug, the fold **training statistics stand as evidence**: the V3 book loses ~−99% in every training window that includes 2022–2023 (see CAMPAIGN_LOG) — the strategy is regime-dependent and would very likely FAIL a working cert. The bug blocks the *formal* verdict, not that observation.
- Any future certification of episode-11/attempt3 candidates (direct OpenOption shape) is blocked until fixed, or the book must be re-expressed as a RebalanceOption universe book to be certifiable.
