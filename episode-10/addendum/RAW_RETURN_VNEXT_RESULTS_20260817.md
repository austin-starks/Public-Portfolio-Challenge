# Episode 10 Addendum — Raw-Return vNext

**Decision date:** 2026-08-17

**Objective:** favor raw return over drawdown reduction, accepting materially higher risk

**Owner decision:** deploy the aggressive finalist after preserving the prior live rules in paper trading

## Executive verdict

The selected vNext is the same 19-name trend-coherence strategy family already validated in the
Episode 10 addendum, but with more capital committed to every eligible name and a wider profit target:

- 6% maximum allocation per name, up from 5%;
- 60% total strategy budget, up from 40%;
- +300% take-profit, up from +250%;
- unchanged seven-day rebalance cooldown, VIX below 35 gate, 365–730 DTE long calls, 180-DTE exit,
  and thesis exit when price is below SMA100 **and** ROC63 is negative.

This is not a lower-risk upgrade. It is a deliberate raw-return trade: the ordinary full-history
replay improved from **+987.49%** to **+1,423.49%**, while maximum drawdown worsened from
**22.33%** to **29.89%** and Sortino declined from **3.73** to **3.37**. The five-fold anchored
walk-forward study also favored vNext on mean OOS return, **69.07%** versus **61.96%**, with vNext
winning raw return in four of five folds.

## Matched evidence

| Test | Prior live rules | Raw-return vNext | Read-through |
| --- | ---: | ---: | --- |
| Full replay, 2022-01-01–2026-08-14 | +987.49% | **+1,423.49%** | vNext wins raw return |
| Full Sortino | **3.73** | 3.37 | risk-adjusted return declines |
| Full maximum drawdown | **22.33%** | 29.89% | vNext takes materially more risk |
| 2022 return | **+4.13%** | -6.51% | vNext is weaker in the bear regime |
| 2022 maximum drawdown | **20.06%** | 29.89% | downside is meaningfully worse |
| 2025-02-15–2025-05-15 return | **+0.77%** | +0.51% | no stress-period improvement |
| 2025 spring maximum drawdown | **6.83%** | 9.14% | higher stress drawdown |
| 2025-08-15–2026-08-14 return | +44.00% | **+65.13%** | strong recent raw-return win |
| Recent maximum drawdown | **6.44%** | 8.25% | recent gain came with more risk |
| Five-fold mean OOS return | 61.96% | **69.07%** | vNext wins 4/5 folds |
| Five-fold mean OOS Sortino | **4.50** | 4.28 | modest quality trade-off |
| Five-fold worst OOS drawdown | **13.60%** | 13.73% | nearly tied |

SPY gained approximately **72.2%** over the full replay window. Both strategy versions beat that
simple baseline in the modeled backtest, but the comparison is not leverage-neutral: these books use
long-dated options, and their path, financing, execution, and tail risks are materially different.

## Event and capacity audit

The vNext event replay contained 9,980 events, 542 filled-order events, and 265 completed option
positions. All 19 liquid names participated. Median deployment rose to **40.38%**, the 90th
percentile was **62.0%**, and peak deployment reached **79.7%**. Top-five entry-notional
concentration was **39.98%**. The longest underwater period was **509 days**.

Historical option execution remains the largest fidelity limitation: more than half of option prices
in the replay were modeled rather than observed from historical NBBO. Absolute P/L should therefore
be treated as simulated evidence, not as a promise of executable returns.

## Winners and losers

Realized historical contribution in the audited vNext replay was concentrated but not limited to one
name.

| Largest winners | Realized P/L | Win record where audited |
| --- | ---: | ---: |
| AMAT | +$34,359.99 | 8 / 17 |
| GS | +$13,907.78 | 12 / 19 |
| ADI | +$12,147.61 | 6 / 20 |
| APP | +$9,639.05 | — |
| LLY | +$9,264.18 | — |
| XOM | +$8,159.09 | — |
| DDOG | +$7,922.23 | — |

| Largest or weakest contributors | Realized P/L | Win record where audited |
| --- | ---: | ---: |
| OSCR | -$3,759.21 | 2 / 13 |
| OKTA | -$872.88 | 3 / 12 |
| DUOL | +$57.30 | — |
| HOOD | +$1,254.00 | — |
| ANET | +$2,040.00 | — |
| META | +$2,219.00 | — |
| SPCX | no completed trade | — |

## Search results that were rejected

- **6% per name / 50% budget / TP300:** +965.49%, 29.89% drawdown. Increasing sleeve size without
  enough total budget underperformed the prior rules.
- **5% / 40% / TP400:** +1,107.72%, 28.07% drawdown. This was the runner-up, but it left meaningful
  raw return behind the selected finalist.
- **GA cadence mutation:** +437.13%, 28.54% drawdown, 725 closed trades and $1,047.80 in fees. The
  optimizer mutated the weekly cadence into daily eligibility, increased churn, and failed recent and
  spring-stress comparisons; it was rejected.
- **7% variants:** attractive in the recent regime but only approximately +698% to +772% over the
  fixed full period, with roughly 26% to 31% drawdown. They were treated as recent-regime overfits.
- **120/180/240 DTE rolls:** inert in the tested paths.
- **Budgets above 60%:** saturated; no additional benefit was observed.

One engine caveat remains: an earlier optimizer report gave the selected fixed configuration
approximately +1,104.03%, while the ordinary same-path replay produced +1,423.49%. Both favored
vNext directionally, but their absolute return levels do not reconcile. The deployment decision is
therefore based on the matched ordinary replays, walk-forward direction, and event audit—not on
pretending the optimizer and ordinary engine are numerically interchangeable.

## Deployment record

Before changing the live portfolio, its exact 22-strategy control was deployed as a brand-new paper
portfolio at the then-current **$30,542.54** NAV, with Constant evaluation and the prior 5% / 40% /
TP250 rules. Paper control portfolio: `6a8388a11bd4572b8e940b98`.

The live Public Portfolio Challenge portfolio `69a7dc7acdb6bf6a4681d36c` then replaced all 22 strategy
definitions with vNext while preserving the existing brokerage account, cash, history, holdings, and
open option legs. A current-book delta reconcile at `2026-08-17T22:18:54.940Z` returned **zero
orders**, **$0 estimated cost**, **$0 realized P/L**, no canceled orders, no wash-sale flags, and no
warnings. No held position had reached TP300, DTE at or below 180, or the combined thesis exit at that
evaluation.

## Operating interpretation

Deploying vNext is defensible only under the stated preference for raw return. It is expected to be
more volatile, to lose more in hostile regimes, and potentially to remain underwater for well over a
year. The paper control is the clean counterfactual: compare live vNext against it without changing
the control, and judge the live book on realized fills, deployment, concentration, and thesis-exit
behavior—not headline backtest return alone.
