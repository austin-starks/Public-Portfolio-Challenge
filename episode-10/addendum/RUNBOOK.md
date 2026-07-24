# Episode 10 Addendum — Entry + Exit Redesign

> **Status:** F1 STRATEGIES LIVE; TARGET REPLAY VERIFIED; GLD THESIS EXIT FILLED AT $8.65.
> Current-book delta reconcile is clean: the carried target equals the live holdings and no orders
> are required. See `CAMPAIGN_LOG.md`.
>
> This attempt redesigns the current Public Portfolio Challenge strategy so positions can leave for
> reasons other than a +250% take-profit while preserving as much of the incumbent's historical edge
> as possible. Entry logic, rank signal, cadence, sizing, strike, and DTE may also change. The live
> book is the control, not a structure that candidates must copy.

## The job

Build a strategy that:

1. enters only when a name has a defensible forward thesis;
2. exits when that thesis weakens, risk expands, or the position becomes stale;
3. proves through event traces that the new exits actually bind;
4. keeps historical OOS return and risk-adjusted performance near the current book; and
5. does not degrade fixed-$25,000 participation.

A high-return candidate whose new exit never fires is not a solution. A low-drawdown candidate that
destroys the incumbent's convex upside is not a solution either.

## Current subject — verify by field at the start of every run

| Role | ID | Current field-level state on 2026-07-24 |
|---|---|---|
| **LIVE SUBJECT** | `69a7dc7acdb6bf6a4681d36c` | Active Public brokerage portfolio; two strategies; approvals off |
| **Entry strategy** | `6a4bb58f3e30382af6e23bf1` | RebalanceOption, 19 names, 40% total budget, 5%/name, 365–730 DTE outright long-call ladder |
| **Exit strategy** | `6a45ab46664648e51f979bcd` | CloseOption on any position; only trigger is P/L ≥ +250% |

Current universe:

`ANET DUOL HOOD LLY GS META TSM AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD SPCX`

Current entry fields:

- SelectTop 19 by 252-day price ROC; weight by 63-day price ROC.
- VIX < 30.
- `DaysSinceStrategyFired >= 0`, which is not a meaningful cooldown.
- SPY price < `820.1824565959556 × 924-day SPY maximum`, which appears effectively always true.
  Verify against actual condition values before classifying it as inert.
- Seven outright long-call rungs: ATM, +10%, +20%, +35%, +50%, +75%, +100% OTM; 365–730 DTE.
- `positionScope: portfolio`; `automaticOrderApproval: false`.

The live account currently contains legacy holdings that are not all products of the current strategy,
including an LLY long-dated vertical. Historical tests must run on a clean chat clone with only the
current strategy rules. Do not use live holdings as the starting state.

## What the current engine exposes

`get_sweep_surface` on the live subject currently exposes:

- strategy: `EntryCooldownDays`, `ExitCondition`;
- action: `RankSignal`, `BuyingPowerPct`, `AllocationPct`, `TotalBudgetPct`, `TakeProfitPct`;
- option leg: `OptionDelta`, `StrikeDistance`, `DteBracket`;
- universe pipeline: `SelectTopLimit`, `UniversePipelineFilter`.

Notable current indicators include `DaysUntilEarnings`, `DaysSinceEarnings`, `DaysSinceOptionOrder`,
`PositionPercentChange`, `PositionMaxDrawdown`, `UnderlyingMaxDrawdown`,
`OptionPositionPercentChange`, `OptionPositionMaxDrawdown`, `OptionDaysToExpiration`,
`OptionDaysHeld`, `OptionGrossExposurePercent`, `CrossAbove`, `CrossBelow`, `ConsecutiveTrue`,
`CountTrue`, ATR, VWAP, gap, volume, index, fundamental, and economic indicators.

Do not infer behavior from this list. Every authored field must pass `build_portfolio`, field audit,
and an event-bearing minimal backtest.

## Frozen comparison discipline

- **Capital:** $25,000.
- **Interval:** Day, unless a design explicitly requires Minute and receives a separate cost/fidelity
  review.
- **Primary calendar:** 2022-01-01 through the freshest common date supported by all candidate data.
- **Walk forward:** anchored, validation mode, five folds, 252-day OOS, 14-day embargo.
- **Fees:** use the engine's shared option default and persist the same fee config across control and
  candidates.
- **Control:** a fresh, LaunchAgent-free clone of the live two-strategy rule set.
- **Comparison:** control and candidate must use identical dates, capital, fill model, fees, universe,
  and baseline.

Freeze the fresh control's fold table before inspecting candidates. Older Attempt 2 numbers are context,
not the current-engine bar.

## Success bars — freeze after the fresh control, before candidate results

### Required sell-behavior gate

- At least one non-TP exit must execute in an event-bearing reproduction.
- Non-TP exits must execute in at least three OOS folds or the strategy must show an equally strong,
  documented reason that a specific fold had no eligible position.
- Report close evaluations, trigger count, filled closes, trigger-to-close latency, exit reason,
  holding days, P/L at exit, and re-entry within 1/5/10 trading days.
- No uncontrolled sell/rebuy churn. A thesis exit needs an engine-supported re-entry cooldown or
  re-entry recovery condition.
- Every open option must have a non-profit terminal path: thesis break, time/DTE, risk/retracement, or
  a combination. TP250 alone does not satisfy this gate.

### Historical-performance retention gate

Use the freshly rerun control as 100%:

- mean OOS return ≥ 85% of control;
- minimum-fold OOS return no more than 15 percentage points below control;
- minimum OOS Sortino ≥ 85% of control and never below 0.5;
- worst OOS max drawdown no worse than control, unless a return improvement clearly compensates;
- majority of folds profitable;
- fixed-$25,000 participation no worse by more than two names and participation ≥ 0.5.

A candidate may receive a **TRADE-OFF** verdict, not PASS, if it improves worst drawdown by at least
three percentage points while retaining at least 75% of control mean OOS return. Deployment still
requires a separate human decision.

## Stage A — current-engine baseline and inventory

1. `fetch_portfolios` and `get_portfolio` the live subject. Record strategies, field audit, holdings,
   cash, buying power, approval state, and recent pending/order events.
2. Query recent `OpenOptionSignal`, `CloseOptionSignal`, `Order`, and `OptionResolutionAttempt` events.
   Confirm whether any sell other than TP250 has occurred; do not infer from the strategy name.
3. Build a clean structured clone with `build_portfolio`, then persist it with `create_portfolio`.
   Strip live positions and any LaunchAgent.
4. Run:
   - full-cycle control with events;
   - 2022 bear;
   - April-2025 stress;
   - last 12 months;
   - fixed-config five-fold walk-forward.
5. Audit breadth and posture. Freeze the control fold table and compute the numeric success bars above.

Deliver a one-paragraph before state before designing candidates.

## Stage B — explore entry + exit mechanisms

Screen genuinely different mechanisms. Do not run one giant grid that mixes every idea.

### Family 1 — momentum coherence

- Entry candidates: positive 63/126-day ROC, price above an underlying SMA/EMA, cross-above or
  consecutive-true confirmation, volatility-adjusted momentum rank, and real cooldowns.
- Exit candidates: underlying ROC crosses below zero, price crosses below an underlying trend line,
  or entry conditions fail for multiple consecutive sessions.
- Pair every thesis exit with a re-entry recovery condition or cooldown.

### Family 2 — winner protection / retracement

Use `OptionPositionMaxDrawdown`, `PositionMaxDrawdown`, `UnderlyingMaxDrawdown`, or a supported
high-water-mark expression to protect a winner after it has made progress. This is different from a
fixed premium stop: it should let convex winners run, then respond to a meaningful retracement.

Verify the exact unit and evaluation scope with a minimal event backtest before search.

### Family 3 — stale-position and expiry discipline

Test a non-profit terminal path using `OptionDaysHeld` and/or `OptionDaysToExpiration`. Candidate
windows should be proportionate to the chosen DTE family. Report theta/turnover consequences and
ensure the rule closes the existing contract before a replacement is opened.

### Family 4 — entry-quality redesign

The current buy gate contains a likely inert SPY condition and no real cooldown. Explore:

- momentum lookbacks and rank/weight combinations;
- underlying trend/volatility filters;
- earnings-aware entry avoidance;
- VIX or broader-regime gates;
- 180–365 versus 365–730 DTE;
- strike distance/delta, allocation, budget, SelectTop, and cooldown.

The universe remains fixed for the first campaign so entry/exit effects remain comparable. If a later
campaign changes the universe, it is a new structural attempt with a new control.

### Family 5 — matched negative controls

Retest a blunt premium stop only once on the current engine because older tests found long-call
stop-loss whipsaw. Use it to determine whether engine changes altered the result, not as the assumed
answer. Likewise retain TP250-only as the incumbent control.

## Stage C — search, then certify

1. Call `get_sweep_surface` on each clean family seed.
2. Use `build_portfolio` or `create_portfolio_variant` dry runs before persistence.
3. Run a small matched design screen. Search metrics may KILL or PROMOTE only.
4. For the promoted design, re-sweep that exact structure:
   - `engine_kind: sweep`;
   - `inner_mode: optimize`;
   - at least three supported axes with at least three values each;
   - `preview_only: true` before spending research tokens.
5. Select the cross-fold robust candidate, never a per-fold argmax.
6. Materialize the fixed candidate and run `inner_mode: backtest_only` certification on the same five
   folds as the fresh control.
7. Re-run the finalist at zero tolerance and field-audit the materialized strategy.

If the current compiler cannot express an important mechanism, record the limitation and use a small
hand-built immutable grid. Never pretend an unsupported gene ran.

## Stage D — first-principles exit audit

For the control and every finalist, generate events and report:

| Audit | Required output |
|---|---|
| Exit reasons | TP, thesis/trend, retracement, time/DTE, stop, rotation, expiry |
| Binding proof | evaluations, true triggers, close signals, filled close orders |
| Position lifecycle | entry date, exit date, holding days, P/L, MFE/MAE if available |
| Churn | re-entry after 1/5/10 days, fees, turnover |
| Tail behavior | largest loss, largest giveback, positions reaching expiry |
| Breadth | simultaneous names and participation at fixed $25k |
| Risk | per-fold OOS return, Sortino, maxDD, posture |

Any authored exit with zero executed closes is non-binding and cannot support a safety claim.

## Stage E — verdict, then stop

Lead with one line: **PASS**, **TRADE-OFF**, **FAIL**, or **BLOCKED**.

Include:

- the fresh control fold table;
- candidate-versus-control fold table;
- exact finalist rules in plain English and field audit;
- entry/exit binding evidence;
- parameter provenance;
- fixed-$25k breadth;
- April-2025 behavior;
- bug ledger and quarantined artifacts;
- what was and was not run.

Do not deploy. Deployment requires the separate explicit phrase **“deploy + clean up”** and a named
finalist.

## Bug protocol

Any timeout, compiler mismatch, zero-trade surprise, field mutation, or event/strategy contradiction is
a first-class result:

1. stop and reproduce minimally;
2. log symptom, expected versus observed, IDs, and what it blocks;
3. write a dedicated bug document for a confirmed engine/data defect;
4. quarantine affected results and rerun after a fix;
5. tell the owner prominently.
