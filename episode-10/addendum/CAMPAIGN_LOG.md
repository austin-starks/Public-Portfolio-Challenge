# Episode 10 Addendum — Entry + Exit Redesign Campaign Log

**Started:** 2026-07-24

**Status:** F1 STRATEGIES LIVE; GLD EXIT FILLED; CURRENT-BOOK RECONCILE CLEAN

**Capital:** $25,000 fixed for research

**Deployment:** 22 F1 strategies cloned to the Public live portfolio on 2026-07-24

## Mandate

Replace the Public Portfolio Challenge's TP250-only lifecycle with entry and exit rules that actually
respond to thesis deterioration, risk, or staleness, while retaining most of the current strategy's
historical OOS performance. Entry logic and option selection may change.

## Frozen methodology

- Current live strategy is the control, not a required candidate structure.
- Search may promote or kill; fixed-config walk-forward OOS decides.
- Every sell claim requires event-level trigger and filled-close evidence.
- Fixed-$25k breadth is required.
- No live mutation, reconcile, staged orders, or deployment.

## Stage A inventory — 2026-07-24

### Live subject

- Portfolio `69a7dc7acdb6bf6a4681d36c`, `Public Portfolio Challenge`, active live/Public brokerage.
- Entry `6a4bb58f3e30382af6e23bf1`:
  - RebalanceOption across 19 names;
  - SelectTop 19 by 252-day ROC, weighted by 63-day ROC;
  - 40% total budget, 5% of portfolio per name;
  - seven outright long-call rungs from ATM through +100% OTM, 365–730 DTE;
  - VIX < 30, `DaysSinceStrategyFired >= 0`;
  - SPY price < `820.1824565959556 × 924-day SPY maximum` stored as a condition;
  - approvals off.
- Exit `6a45ab46664648e51f979bcd`: only CloseOption trigger is P/L ≥ +250%; approvals off.
- Live cash/buying power read: $18,778.47.
- Live holdings read: COP, GLD, HOOD, OSCR, XOM outright calls plus a legacy LLY bull-call vertical.
  The legacy vertical is not part of the current entry structure and will not seed research runs.

### Current engine surface

Applicable sweep fields: `EntryCooldownDays`, `ExitCondition`, `RankSignal`, `BuyingPowerPct`,
`AllocationPct`, `TotalBudgetPct`, `TakeProfitPct`, `OptionDelta`, `StrikeDistance`, `DteBracket`,
`SelectTopLimit`, and `UniversePipelineFilter`.

New/useful indicators observed include earnings distance, position/option/underlying max drawdown,
option days held, option DTE, option exposure, cross events, consecutive/count true, ATR, VWAP, gap,
volume, fundamental, economic, and expanded index metrics.

### ⚠️ TOOL/QUERY ISSUE — 30-day event summary did not return promptly

- Request: live portfolio event summary for 2026-06-24 through 2026-07-24, launched alongside study
  and optimization inventory reads.
- Observed: the combined read remained non-terminal beyond 90 seconds and was terminated.
- Expected: bounded aggregate summary and list responses.
- Classification: not yet a confirmed engine bug; likely a wide cold-event scan or one slow parallel
  dependency.
- Next step: retry event summary over the hot seven-day window and run study/optimization list reads
  separately. No strategy results are affected.

## Success bars

Numeric thresholds will be computed from a fresh current-engine control before candidate results:

- mean OOS return ≥ 85% of control;
- minimum fold no more than 15 percentage points below control;
- minimum OOS Sortino ≥ 85% of control and ≥ 0.5;
- worst OOS drawdown no worse than control;
- fixed-$25k breadth within two names of control and participation ≥ 0.5;
- verified non-TP closes without uncontrolled re-entry churn.

## Artifact ledger

| Stage | Artifact | Result | Status |
|---|---|---|---|
| Live inventory | `69a7dc7acdb6bf6a4681d36c` | TP250-only exit confirmed by raw action fields | PASS |
| Engine surface | live subject | Entry, exit, rank, filter, cooldown, structure, and sizing axes exposed | PASS |
| Recent event summary | 30-day combined call | Non-terminal beyond 90s; terminated | RETRIED NARROW |
| Recent event summary | 2026-07-17 through 2026-07-24 | 3,396 close evaluations; no close order; one pending HOOD buy | PASS |
| Clean control | `6a639dbfe490b0ae31ed30c5` | Current live rules, zero starting positions, $25,000 | PASS |
| Control fixed OOS | `6a639febe490b0ae31ed3499` | Five complete matched folds | PASS |
| F1 seed | `6a639f2d8851af28134e0379` | Trend-coherence entry, trend/DTE/TP exits | PROMOTED |
| F1 fixed OOS | `6a63a0cee490b0ae31ed3569` | Five profitable folds; all frozen gates pass | PASS |
| F1 event fold 0 | `6a63a11b8851af28134e05a1` | Filled non-TP thesis exits | PASS |
| F1 event fold 2 | `6a63a1228851af28134e05a9` | Filled non-TP thesis exits | PASS |
| F1 event fold 4 | `6a63a1298851af28134e05b1` | Filled non-TP thesis exits | PASS |
| Reoptimization sweep | `6a639fd78851af28134e04db` | Robust key resolves to F1; training rows defective | QUARANTINE TRAINING |
| Historical holdout | `6a63a8094ba0007fa584c223` | +25.16% vs frozen +29.66% return floor | FAIL |

## Before state — corrected

The user's concern is directionally correct but needs one nuance. The current control is not literally
incapable of selling: `RebalanceOption` rotates contracts and the +250% CloseOption takes winners.
In the last 12-month control replay (`6a639dd4e490b0ae31ed31ef`), both rotation sells and TP250 sells
executed. The dangerous gap is that the strategy has no thesis-loss, retracement, time, or DTE exit.
The live seven-day audit saw 3,396 CloseOption evaluations and no close order, consistent with a
TP-only close strategy that leaves ordinary losers and deteriorating names untouched.

## Fresh control

Clean control `6a639dbfe490b0ae31ed30c5` exactly restates the current two strategies without live
positions. Full-cycle backtest `6a639dcce490b0ae31ed31ba` returned:

- `+653.43%`, Sortino `2.57`, max drawdown `44.09%`;
- all `19/19` names traded at fixed $25,000;
- median deployment `55.28%`;
- top-five entry-notional concentration `35.83%`.

Stress slices:

| Window | Return | Sortino | Max DD | Participation |
|---|---:|---:|---:|---:|
| 2022 bear | -31.04% | -1.44 | 44.09% | 17/19 |
| Mar–May 2025 | +4.95% | 0.92 | 17.09% | 16/19 |
| Recent 12 months | +158.38% | 4.84 | 21.13% | 17/19 |

## Mechanism screen

All families were allowed to change both entries and exits.

| Family | Entry and lifecycle | Full return | Full Sortino | Full max DD | 2022 return | 2022 max DD |
|---|---|---:|---:|---:|---:|---:|
| Control | 252d rank; TP250 only | +653.43% | 2.57 | 44.09% | -31.04% | 44.09% |
| F1 Trend Coherence | positive trend filter; weekly recovery; trend + DTE + TP exits | +946.75% | 3.87 | 17.29% | -0.83% | 17.29% |
| F2 Retracement + Loss Trend | 150d trend; winner giveback and losing-trend exits | +906.49% | 3.35 | 27.02% | +1.61% | 15.15% |
| F3 Top-15 Rotation | positive 63d momentum; 14d cadence; DTE + TP | +752.44% | 3.35 | 28.54% | -25.90% | 28.19% |

F1 won because it paired the best risk reduction with simpler, directly auditable exit semantics.
F2 remains research-worthy, but it produced much higher condition-evaluation noise and fees. F3 did
not repair the bear regime enough.

## Finalist rules — F1 Trend Coherence

Portfolio: `6a639f2d8851af28134e0379`

Entry:

- fixed 19-name universe;
- eligible only when the candidate's price is above its 100-day SMA and its 63-day ROC is positive;
- rank eligible names by 126-day ROC, SelectTop 19, weight by 63-day ROC;
- book gate: VIX below 35 and at least seven days since the last RebalanceOption order;
- 40% total budget, 5% per name;
- the same seven outright long-call rungs from ATM through +100% OTM, 365–730 DTE.

Exit:

- preserve TP250;
- close any remaining option at DTE <= 180;
- for each underlying, close all of its long calls when price is below its own 100-day SMA **and**
  63-day ROC is negative.

Re-entry is not timer-only. A thesis-exited name must recover to the opposite entry state—price above
its own 100-day SMA and positive 63-day ROC—and then pass the book's weekly rebalance gate.

## Matched five-fold fixed OOS certification

Both studies use the same anchored calendar, five 252-day OOS folds, 14-day embargo, daily interval,
$25,000 initial capital, and fee model.

| Fold | Control return | F1 return | Control Sortino | F1 Sortino | Control max DD | F1 max DD | Control names | F1 names |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 25.39% | 32.81% | 1.73 | 3.31 | 20.52% | 10.08% | 15 | 15 |
| 1 | 78.85% | 65.73% | 4.69 | 4.78 | 12.73% | 11.61% | 16 | 15 |
| 2 | 43.67% | 29.66% | 2.71 | 1.89 | 22.12% | 12.05% | 17 | 15 |
| 3 | 120.67% | 112.63% | 5.79 | 6.92 | 17.73% | 9.77% | 16 | 16 |
| 4 | 119.51% | 104.61% | 7.26 | 9.23 | 11.43% | 7.86% | 15 | 14 |
| **Mean** | **77.62%** | **69.09%** | **4.44** | **5.23** | **16.91%** | **10.28%** | — | — |

Frozen-gate evaluation:

- return retention: `69.09 / 77.62 = 89.01%`, above the 85% bar;
- minimum return: `29.66%`, above both control's `25.39%` and the `10.39%` floor;
- minimum Sortino: `1.89`, above control's `1.73` and the `1.47` retention floor;
- worst fold drawdown: `12.05%` versus control `22.12%`;
- profitable folds: `5/5`;
- minimum participation: `14/19 = 0.737`; no fold trails control by more than two names;
- total fold fees: approximately `$306.80` versus control `$1,333.15`.

The F1 April-2025 stress replay `6a63a1ae9925d1bb4e64d560` returned `+5.67%` with `6.77%`
max drawdown, versus control `+4.95%` with `17.09%` max drawdown.

## Exit-binding audit

Direct event reproductions exactly matched fixed-study fold metrics and proved non-TP closes in three
separate OOS folds:

- fold 0: thesis exits filled for XOM, AMAT, GLD, META, GS, NET, DDOG, OKTA, and other names;
- fold 2: thesis exits filled for TSM, AMAT, ANET, GS, AVGO, GLD, COP, and OSCR;
- fold 4: thesis exits filled for META, HOOD, ANET, XOM, GLD, GS, and TSM.

Representative ANET lifecycle in fold 4:

| Entry | Exit | Entry premium | Exit premium | Approx P/L | Holding days | Exit reason |
|---|---|---:|---:|---:|---:|---|
| 2026-03-04 | 2026-03-06 | $14.44 | $14.16 | -1.9% | 2 trading days | trend thesis |
| 2026-03-19 | 2026-03-26 | $12.12 | $11.43 | -5.7% | 5 trading days | trend thesis |
| 2026-04-08 | 2026-05-11 | $18.21 | $16.96 | -6.9% | 23 trading days | trend thesis |

For these three exits, recovery-qualified ANET re-entry occurred zero times within one trading day,
once within five trading days, and three times within ten trading days. This is active rotation, but
not same-day sell/rebuy churn. The 180-DTE backstop was present but did not produce a filled close in
the checked OOS event samples; thesis exits and ordinary portfolio rotation reached those positions
first.

## Breadth and posture

Full-cycle F1 breadth audit:

- `18/19` names filled, participation `0.9474`;
- SPCX had resolution rejections and zero fills;
- top-five entry-notional share `38.32%`, close to control's `35.83%`;
- median deployment `39.55%` versus control `55.31%`;
- EOD max drawdown `15.8%` versus control `44.1%`;
- longest underwater stretch `199` days versus control `475` days.

SPCX is a disclosed breadth blemish, not a hidden zero. The finalist still passes the frozen breadth
gate.

## Engine/compiler findings

### Confirmed defect

Sweep study `6a639fd78851af28134e04db` completed 545 units and selected cross-fold robust key
`174357490c9db17753b3eb6ef02e008ac32987800479bb124b3f5156488e27f0`, which resolves to the
exact F1 seed: template 63/126-day ranking, SelectTop 19, 180-DTE roll, and 40% budget.

However, its training statistics are byte-for-byte identical across all five expanding training
windows. The matched fixed study reports different training values, confirming a sweep reporting,
caching, or execution defect. See `SWEEP_TRAINING_STATISTICS_BUG.md`. Sweep training rows are
quarantined; the verdict relies on the independent fixed study.

### Unsafe generic exit compilation

A generic `ExitCondition` sweep intent for “candidate underlying price below its 100-day SMA”
compiled to SPY price below SPY SMA and targeted the existing CloseOption with `replace: false`.
That would gate TP250 rather than add an independent per-name exit. The addendum therefore used explicit
per-underlying CloseOption strategies validated by `build_portfolio` and event fills. Do not use the
generic ExitCondition surface for this lifecycle without inspecting the compiled target and field
audit.

## Verdict

**RESEARCH PASS — F1 Trend Coherence.**

It adds real thesis exits and a DTE terminal path, retains 89% of control mean OOS return, improves
minimum OOS Sortino, cuts worst-fold drawdown by about ten percentage points, lowers fees, and passes
fixed-$25,000 breadth.

### Deployment holdout — FAIL

The five-fold study accidentally consumed the intended recent 126-day tail: fold 4 runs through
2026-07-23. That makes the canonical recent-tail lockbox unavailable; re-running March–July 2026
would be a contaminated replay, not new evidence.

The frozen F1 portfolio therefore received one single-touch historical holdout on the untouched
126-calendar-day window immediately before the campaign span, 2021-08-29 through 2022-01-02:

- backtest `6a63a8094ba0007fa584c223`;
- return `+25.16%` versus the frozen `+29.66%` minimum: **FAIL by 4.50 percentage points**;
- Sortino `4.22`;
- max drawdown `13.61%` in completed statistics and `12.50%` on the EOD posture tape;
- median deployment `32.43%`, p90 `51.70%`, maximum `59.39%`, and zero days above 70%: **posture PASS**;
- 15/19 names filled, participation `0.7895`, top-five entry-notional share `55.28%`: **breadth PASS**.

This window is valid anti-overfitting evidence because the addendum's search and walk-forward span began
on 2022-01-03, but it is a historical pre-period holdout rather than the canonical forward tail. The
strict deployment verdict is nevertheless **FAIL** because the frozen return condition was missed.
Do not iterate F1 against this result and then reuse this window; the single touch is burned.

At this point in the campaign nothing had been deployed, reconciled, staged, approved, or ordered.
Under the frozen rules, replacing the live book with F1 required an explicit owner override that
named this failed holdout, or a new strategy campaign with a genuinely untouched future lockbox.

## Owner override and deployment gate — 2026-07-24

The owner explicitly removed the return floor and directed immediate deployment of F1 because the
holdout remained profitable with materially lower risk. This is the logged override of the failed
`+29.66%` return condition; no other research result was changed.

Pre-deploy inspection confirmed the live target as `69a7dc7acdb6bf6a4681d36c`, active
`Public Portfolio Challenge`, Public brokerage, with `automaticOrderApproval: false`. An initial
event-history read incorrectly treated expired HOOD order `6a5f74654acceb7915ece745` as currently
pending. The owner reported no such order in the current UI; the event was historical, not an
authoritative current-order read. It was removed as a blocker.

`clone_strategies_to_portfolio` then replaced the two incumbent strategies with all 22 F1
strategies. Target-side event replay `6a63a9168b861d24bd40db3d` exactly reproduced the frozen F1
holdout: `+25.1616%`, Sortino `4.2207`, max drawdown `13.6116%`, 15/19 names. This verifies that the
deployed target objects trade equivalently to the frozen source.

Reconcile preview `6a63a95a37f23e31d00b2f8e` initially produced an empty single-tick
fresh-deploy target and seven close legs:

- close COP, GLD, HOOD, OSCR, and XOM outright calls;
- close both legs of the legacy LLY vertical;
- estimated net credit `$11,095`;
- estimated realized P/L `+$346`;
- no wash-sale flags.

No reconcile orders were staged. Immediately after cloning, the new GLD thesis-exit strategy itself
generated unapproved close order `6a63a90d97f31acb8cdc22b0`. That is a fresh F1 signal, not the old
HOOD record and not a reconcile side effect. It overlaps the GLD leg in the preview, so it must be
canceled or approved before staging any reconcile delta; never stage a duplicate GLD close.

### ⚠️ RECONCILE PREVIEW QUARANTINED — open-order suppression

The seven-close preview is **not** a valid statement that F1 wants the whole portfolio liquidated.
The preview's generated audits show every F1 strategy returning `NoSignal` with
`audit.type: openOrder`, all referencing the fresh GLD order
`6a63a90d97f31acb8cdc22b0` in `Pending User Approval`. The reconciler therefore observed an
artificial empty target while strategy evaluation was globally suppressed and converted that empty
target into closes for every current holding.

Do not stage the seven orders from preview `6a63a95a37f23e31d00b2f8e`. First resolve the fresh GLD
exit order in the UI. Once no order is open, run a new reconcile preview and use only that later
preview to decide whether migration trades are appropriate.

Cancellation does not resolve the GLD block while the thesis condition remains true. Order
`6a63a90d97f31acb8cdc22b0` was canceled, F1 restaged order `6a63ac6697f31acb8cdc6674`
at `$8.50`, that order was canceled, and F1 restaged
`6a63afb797f31acb8cdca955` at `$8.45`. This is the intended persistent-exit behavior: canceling an
unapproved exit does not falsify price-below-SMA plus negative-ROC. The order cannot be ignored for
reconcile because any open order globally suppresses target evaluation. Either let the GLD thesis
exit complete, or explicitly change/disable that rule; only then can reconcile produce a trustworthy
target.

The owner approved the latest GLD exit. It was submitted to Public as a limit sell at `$8.65`
with broker order id `00000000-6a63-afb7-97f3-1acb8cdca955`. The latest verification still shows
`Accepted`, not `Filled`, and GLD remains in positions. Reconcile remains blocked until the order
fills or otherwise reaches a terminal state.

### Cancel-first reconcile retest

The GLD exit subsequently filled at `$8.65` on `2026-07-24T18:55:15Z`. A current portfolio read
confirms that GLD is gone and cash is `$19,643.48`.

After the reconciler was changed to cancel open orders before resolving its target, preview
`6a63ba83ed8ac595f3f10cdb` was run at `2026-07-24T19:18:26Z`. There was no open order left to
cancel (`canceledOrders: []`), and the preview placed nothing. It returned six close legs:

- close COP, HOOD, OSCR, and XOM outright calls;
- close both legs of the legacy LLY vertical;
- estimated net credit `$10,220`;
- estimated realized P/L `+$596`;
- no wash-sale flags.

This preview is still **not approved for staging**. Its target is empty because the one-tick
fresh-deploy resolver did not emit a new entry while the weekly RebalanceOption entry gate was not
eligible. That is an entry-timing result, not an exit decision on the existing holdings. Concurrent
live CloseOption audits identify active thesis conditions for ADI, APP, AVGO, GLD, META, and TSM;
none of the remaining COP, HOOD, LLY, OSCR, or XOM holdings is firing its ticker-specific thesis
exit, and none is at the 250% take-profit or 180-DTE backstop.

No reconcile orders were staged. A safe migration needs a carry-forward/hold-aware target or a
preview that distinguishes “no entry today” from “desired target is cash”; converting an empty
cooldown-gated entry result into close-all remains quarantined.

### Current-book reconcile — PASS

After deployment added explicit `target_basis` and `mode` parameters, reconcile was rerun with:

```json
{
  "portfolio_id": "69a7dc7acdb6bf6a4681d36c",
  "target_basis": "current_book",
  "mode": "delta"
}
```

Preview `6a63c7228987c2f90136bc24` returned a carried target identical to the current six legs:
four OSCR calls; one COP call; one HOOD call; one XOM call; and both legs of the LLY vertical.
It produced `orders: []`, estimated cost `$0`, realized P/L `$0`, no wash-sale flags, no warnings,
and no canceled orders. The fresh-deploy close-all preview remains valid only for
`target_basis: fresh_deploy`; it is no longer a blocker for the intended current-book migration.
