# Recent Minute OOS resolution check

**Run date:** 2026-07-24
**Status:** COMPLETE — MIXED; supplemental evidence, not a new certification pass

## Question

Does the deployed F1 exit-discipline book still look defensible when the engine evaluates the
underlying and option book at Minute resolution instead of the daily interval used for certification?

## Design

- Fixed books only; no sweep, GA search, or parameter tuning.
- F1: `6a639f2d8851af28134e0379`
- Former TP250 control: `6a639dbfe490b0ae31ed30c5`
- Interval: `Minute`
- Global calendar: 2025-07-01 through 2026-07-24
- Walk forward: anchored validation mode, two folds
- OOS width: 90 calendar days
- Embargo: 14 days
- Certification policy enabled
- Estimated and charged research cost: `16.976` tokens per study, `33.952` total

The preview produced identical calendars and no cost or fidelity warnings. Each expanding historical
window stayed within the engine's recommended 365-day maximum for Minute studies.

This is OOS with respect to each fixed walk-forward fold and no parameters were selected on the OOS
results. It is **not** a new untouched strategy lockbox: F1 had already been studied on these dates at
Day resolution.

## Study IDs

- F1 Minute OOS: `6a63e16aa6248fba1267d1fe`
- TP250 control Minute OOS: `6a63e176a6248fba1267d20f`

## OOS results

| Fold | OOS dates | Control return | F1 return | Control Sortino | F1 Sortino | Control max DD | F1 max DD | Names control / F1 | Median deployment control / F1 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2026-01-26 → 2026-04-26 | 20.86% | 1.05% | 3.94 | 0.18 | 5.35% | 7.72% | 10 / 5 | 28.10% / 9.85% |
| 1 | 2026-04-26 → 2026-07-24 | 7.52% | 21.50% | 1.81 | 7.53 | 4.18% | 5.56% | 6 / 5 | 16.13% / 12.16% |
| **Mean** | — | **14.19%** | **11.28%** | **2.88** | **3.85** | **4.77%** | **6.64%** | — | **22.12% / 11.00%** |

Additional checks:

- Both books were profitable in both OOS folds.
- F1 retained `79.47%` of the control's mean recent Minute OOS return.
- F1 had the higher mean Sortino by `0.98`.
- F1 had the higher mean max drawdown by `1.87` percentage points and the higher worst-fold
  drawdown by `2.37` points.
- OOS option fees were identical in aggregate: `$14.95` per book.
- F1 traded only five of 19 names in each fold and deployed roughly half as much capital as the
  control on average.
- F1 reported 391 null-gated evaluations in fold 0 OOS and none in fold 1. That count is consistent
  with approximately one full regular trading session and should not be silently treated as zero.

## Interval-sensitivity finding

The former control contains `DaysSinceStrategyFired >= 0`. At Minute resolution that condition is
eligible on essentially every evaluation rather than expressing a real cooldown. Its fixed-book
training and validation segments show extreme churn:

- roughly `$1,236` in training fees in each fold;
- validation fees of about `$618` and `$896`;
- training drawdown of `86.75%`;
- validation drawdown of `80.89%` and `74.27%`.

The control's OOS segments happened not to reproduce that churn, but the surrounding fixed-window
evidence proves the former strategy is highly interval-sensitive. Its recent Minute OOS returns
therefore remain the exact matched result, while its behavior is not a stable intraday benchmark.

## Verdict

**MIXED / NO NEW PASS.**

The Minute study does not invalidate the deployed daily-certified F1 book: F1 was profitable in both
recent OOS folds, had the better mean Sortino, and strongly won the most recent fold. It also does not
provide a clean intraday confirmation: F1 lost the first fold badly, retained less than 80% of mean
control return, had higher drawdown in both folds, traded fewer names, and maintained much lower
deployment.

Keep the existing daily certification as the deployment basis. Treat Minute mode as execution-fidelity
evidence and investigate F1's low Minute breadth, low deployment, fold-0 null-gated session, and the
control's zero-day cooldown sensitivity before claiming intraday robustness.
