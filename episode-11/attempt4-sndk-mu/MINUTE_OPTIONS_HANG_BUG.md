# Diagnose: Minute-interval backtests hang indefinitely on options portfolios

> **DOWNGRADED 2026-07-03 after Fly log inspection (`fly logs -a nexustrade-backtesting`):** NOT a hang. Machine `080d411c104978` shows both jobs as the 2 active HEAVY workers, actively feeder-fetching the exact expected data (`intraday_options_v3 … 2026-02..06 type=call dte=000-030` + `intraday_stock 2026-01..07`, ~3 GiB and climbing at normal per-file latencies). Minute-options prep is simply a multi-GiB job. The remaining (minor) issue: **`query_backtest_status` reports a frozen `updatedAt` and a reset `timeElapsed` (~0) during the long prep phase**, which is indistinguishable from a dead job from the API side. Suggested fix: heartbeat the backtest doc's `updatedAt`/progress during prep, or expose a phase field (PREPPING vs TICKING). The rest of this doc is kept for the original observations.

## One-line
Minute-interval `backtest_portfolio` runs on options (RebalanceOption) books hang — status stuck `RUNNING` for 20+ minutes with `updatedAt` frozen and `timeElapsed` reset to ~0 — while an equity-only book over the same window/interval completes in 12 seconds, blocking the intraday validation requested for the SNDK/MU deploy candidate.

## Expected vs observed
- **Expected:** Minute-interval backtest of a 2-name options rotation over ~6 months (2026-01-01→2026-07-03) completes in minutes (Day-interval equivalent completes in ~6s; equity Minute over same window: 12.5s).
- **Observed:** Two options-book Minute runs stuck: status `RUNNING`, `updatedAt` frozen at `2026-07-03T22:38:10Z` (>20 min stale at last poll), `timeElapsed` regressed from ~67s to ~1e-6 (suggests a restart/requeue loop), `validationStatisticsCount: 0`.

## Reproduction
- Hung run 1: backtest `6a4838786d6c7f417c898269` — portfolio `6a4838694ed7c21e3f3adb74` (S10 convertible ladder, RebalanceOption + CloseOption), 2026-01-01→2026-07-03, `interval: Minute`, $8k.
- Hung run 2: backtest `6a4838796d6c7f417c898275` — portfolio `6a482abcd89cad8e9a8aa809` (S5, simpler RebalanceOption book), same window/interval.
- Control (works): backtest `6a48387b002d7bfafa820357` — equity B&H 50/50 (`6a48260ab9817f2ac2926ac4`), same window, `interval: Minute` → COMPLETE in 12.5s.
- Control (works): same S10 portfolio at `interval: Day`, any window → completes in ~6s.

## Leading hypothesis (verify, don't assume)
*Hypothesis:* the minute-resolution options pricing/resolution path (chain lookups or greeks resolution per minute bar) either livelocks or crashes the worker, and the job restarts (timeElapsed reset ~67s → 0) without terminal status. Isolated to options books — equity minute path is fine.

## Alternatives to rule out
1. **Just slow:** ~180 trading days × 390 min bars ≈ 70k ticks; even at 10ms/tick that's ~12 min of compute. But `updatedAt` frozen + `timeElapsed` reset argue restart-loop, not slow progress.
2. **Queue starvation:** two options jobs submitted together; but the frozen heartbeat persists after the equity job drained.

## Where to look
- Minute-interval branch of the options backtest engine (contract resolution per bar; expiration handling inside a day).
- Job supervisor/retry logic — why a restarted job reports `RUNNING` with reset timeElapsed instead of ERROR.

## Diagnostic checks
1. Single-day Minute options backtest (2026-07-01→2026-07-02) on `6a482abcd89cad8e9a8aa809` — if that hangs, the repro is minimal.
2. Same book, Minute, but 1-week window — bisect where it stalls.

## Impact on prior results
- No prior results contaminated (all prior certs/backtests were Day interval and completed).
- Blocks: the human-requested intraday (Minute) 2026 validation of S10/S5. Fallback used: Day-interval 2026-YTD runs. Deploy decision does not strictly depend on Minute resolution, but the requested evidence is incomplete until fixed.
