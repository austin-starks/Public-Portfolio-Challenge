# Hybrid Cadence Minute Test

Date: 2026-07-24

## Verdict

**REJECT. Do not replace the current F1 book with this variant.**

Confining entries and rotations to one 10:00 ET opportunity after the seven-day cooldown did not
preserve the recent Minute OOS performance of the current F1 book. The hybrid remained profitable in
both folds, but retained only `15.67%` of F1's mean return, had much lower risk-adjusted performance,
traded fewer names, and produced a worse worst-fold drawdown.

No live portfolio, strategy, position, or order was changed by this experiment.

## Hypothesis

Keep exits responsive on every Minute evaluation while reducing entry and rotation timing noise:

- entries and rotations: at most weekly, evaluated at 10:00 ET;
- thesis, expiry, take-profit, and rotation exits: evaluated every minute.

The options structure, universe, indicators, sizing, and exit rules were held fixed relative to the
current F1 book.

## Exact rule change

The current F1 `RebalanceOption` gate already requires:

- `DaysSinceLastRebalanceOptionOrder >= 7`;
- `VIX < 35`.

The hybrid added:

- `MinutesAfterOpen = 30`.

That permits a rebalance at 10:00 ET on the first eligible trading day after the cooldown. It does
not turn the strategy into a day-trading book. All 21 ticker-specific `CloseOption` strategies remain
eligible on every Minute evaluation.

The following were unchanged:

- the 19-name research universe;
- 100-day SMA and 63-day ROC eligibility;
- 126-day ROC ranking and `SelectTop 19`;
- 63-day ROC weighting;
- 40% total budget and 5% per-name cap;
- outright long calls, 365–730 DTE;
- the ATM through +100% OTM affordability ladder;
- thesis exit, 180-DTE backstop, and +250% take-profit.

Hybrid draft portfolio: `6a63e700a6248fba1267d574`

## Behavioral preflight

An initial market-open variant used `MinutesAfterOpen = 0`. Its event replay showed the gate firing
at 09:30 ET but no option fills resolving. That draft is not the tested candidate.

The corrected 10:00 ET hybrid passed structured portfolio validation and a short event-bearing
Minute replay:

- backtest: `6a63e7064ba0007fa584f7fb`;
- dates: 2026-06-29 through 2026-07-17;
- `16,656` events;
- `11` open-option signals;
- `3` orders;
- one filled OSCR buy;
- `5,473` close-option-signal evaluations.

The replay verified the intended cadence: the entry gate became true at minute 30, while close
strategies continued evaluating intraday. This short replay was used only as a behavioral check, not
as performance evidence.

## Matched recent Minute OOS test

Hybrid study: `6a63e73f1e2c5df8d028fdee`

Current F1 comparison: `6a63e16aa6248fba1267d1fe`

Both studies used:

- global calendar: 2025-07-01 through 2026-07-24;
- interval: `Minute`;
- fixed-book `backtest_only` mode;
- two anchored folds;
- 90-calendar-day OOS windows;
- 14-day embargo;
- certification policy enabled.

The hybrid study charged `16.976` research tokens.

## Results

| Fold | OOS dates | F1 return | Hybrid return | F1 Sortino | Hybrid Sortino | F1 max DD | Hybrid max DD | Names F1 / hybrid | Median deployment F1 / hybrid |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2026-01-26 → 2026-04-26 | 1.05% | 0.84% | 0.18 | 0.10 | 7.72% | 9.64% | 5 / 4 | 9.85% / 10.35% |
| 1 | 2026-04-26 → 2026-07-24 | 21.50% | 2.69% | 7.53 | 1.29 | 5.56% | 2.15% | 5 / 3 | 12.16% / 5.44% |
| **Mean** | — | **11.28%** | **1.77%** | **3.85** | **0.70** | **6.64%** | **5.90%** | — | **11.00% / 7.89%** |

Additional comparisons:

- mean return fell by `9.51` percentage points;
- mean Sortino fell by `3.16`;
- mean max drawdown improved by only `0.74` percentage points;
- worst-fold drawdown worsened from `7.72%` to `9.64%`;
- fold-1 return fell by `18.81` percentage points;
- breadth fell from five names per fold to four and three;
- aggregate OOS fees fell from `$14.95` to `$9.10`, consistent with less activity rather than a
  superior return profile;
- both hybrid folds were profitable, but profitability alone is insufficient for promotion.

## Interpretation

The exact-time entry restriction is too severe for this options implementation. It removes most of
the current F1 book's ability to resolve and enter candidates when contracts are actually available,
especially in the recent fold. The resulting lower activity slightly reduced average drawdown, but
the reduction was not consistent: the hybrid's worst fold drew down more than current F1.

This does **not** show that intraday exits are harmful. Both candidates retained intraday exit
evaluation. It shows that forcing entries and rotations into one exact weekly clock-time is inferior
to F1's existing “first eligible Minute after the seven-day cooldown” behavior.

## Decision

- Keep the current F1 live strategy unchanged.
- Reject hybrid draft `6a63e700a6248fba1267d574`.
- Do not reconcile or stage orders from the hybrid.
- If cadence work continues, test a wider entry window or explicit session-aware resolver as a new
  hypothesis; do not tune the 10:00 time against these same OOS folds.
