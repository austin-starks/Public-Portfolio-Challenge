# Runbook: Walk-Forward Options Campaign → Deploy Live

> **Paste this whole file into a fresh LLM session** with the NexusTrade MCP server connected.
> Self-contained. Follow top to bottom. Do not ask clarifying questions; execute.
> Every runtime step uses MCP tools only, no repo checkout.

---

## Design philosophy

**This runbook prescribes WHAT must be true, never HOW to achieve it.**

- **Fixed:** the universe, the capital, the calendar, the gates, the selection method, the
  live-monitoring rules, the capital-posture policy, the lockbox, and the deploy procedure.
- **Yours to design:** everything else — signals, structures, deltas, DTEs, cadence, breadth,
  filters, exits, sizing, regime switches. If a design clears the gates, it is valid.

### The hard-won lesson that shapes everything (read twice)

These are methodology lessons from prior campaign runs, not open engine defects. The certification
engine (sweep walk-forward, fold-winner persistence, validation-window scoring, cross-fold robust
selection, field-level audits) is the current production contract.

1. **Validation score is a noisy proxy for out-of-sample. Maximizing it per fold does not find the
   OOS-best book.** Picking the single highest-validation candidate on each fold is high-variance.
   **You do not deploy the per-fold argmax.** You deploy the parameterization that is **robust across
   folds** — use `aggregate.crossFoldRobustSelection` (minimax validation Sortino) plus the Selection
   method below. This is mandatory, not advisory.
2. **The value lives in the DESIGN, not the optimizer.** Treat the optimizer as a modest, robust
   knob-setter that confirms a design's neighborhood, never as a discoverer of magic. Spend effort
   on the family; ask the optimizer for little.
3. **Only the deployable object is real. Verify it at the FIELD level, never by name.** Strategy
   and condition _display names_ can be stale; the `comparison`/`value`/`window` fields are what
   trade. Every certification, reproducibility, and parity check reads `conditionFieldAudit` (raw
   fields), never `strategy.name` or `condition.name`.
4. **Reproducibility is a property of the PROCESS, not a backtest number.** Make the process
   deterministic, field-verified, and auditable; live performance is the only true out-of-sample.

### What this campaign optimizes for

"Best" = highest risk-adjusted return that is **real out of sample**, obeys the capital posture,
and is **robust across folds** (not carried by one). A high backtest number over one window proves
nothing; a high validation number on one fold proves nothing.

**The method is walk-forward validation.** History is tiled into sequential folds. Each fold
optimizes on its own in-sample development window and is scored on a held-out OOS window the
optimizer never saw. Overfitting shows up directly: an OOS aggregate that collapses, a result
carried by a single lucky fold, or a winner that changes every fold.

Three operating principles follow:

1. **Two tools, two jobs.** _Standard optimization / variants / backtests_ are the SEARCH layer:
   invent and tune candidate designs fast and cheap. _Walk-forward_ is the CERTIFICATION layer:
   the go/no-go on whether the design generalizes. Run walk-forward on the design you're ready to
   defend, not on every idea.
2. **Walk-forward certifies a DESIGN, then names a robust parameterization.** Each fold can pick a
   different optimized winner — that is the noise signal. The deploy book is a **separately
   assembled, fixed deploy-shape portfolio** chosen by the cross-fold selection method below; its
   right to deploy is earned by the WF OOS aggregate on that assembled object, the lockbox
   confirmation, and field-level reproducibility/parity.
3. **OOS is the only headline.** Training and validation are in-sample. Never present a train or
   validation number as evidence the book generalizes. The per-fold OOS table and its aggregate
   are the result.

**Strategy intent:** a deliberately high-risk momentum book on my favorite names. Aggressive is
fine — leverage, convexity, concentration-in-time are on the table. The gates shape the risk; they
are not there to make the book timid.

## The watchlist (fixed universe, 20 names, do not change)

ANET, DUOL, HOOD, LLY, GS, META, TSM, AVGO, XOM, COP, OSCR, AMAT, ADI, DDOG, OKTA, NET, APP, GLD, MU, SNDK

> **Listing-date note.** SNDK began regular-way Nasdaq trading on 2025-02-24, so it has no data
> before the final fold and the lockbox. It is a valid 2025+ name, not a universe error. Its
> early-fold absence is governed by the **not-yet-listed rule in Gate 1** and must not be read as a
> defect. Before auditing breadth, verify every name's first-trade date against each fold's
> dev-window start **programmatically**; do not eyeball the list. SNDK is the only span violation in
> the current 20; the other 19 trade across the whole 2022 → now span.

## Capital posture (POLICY — gateable, not optional)

I do not want to be fully invested most of the time. I want dry powder deployed aggressively when
opportunity is rich, and a small book when it isn't.

Measured from each window's daily equity tape (deployment_t = positionValue_t / value_t; regime
from the SPY trailing-high ratio). Audit with `audit_backtest_posture`; one call per backtest
returns every number this policy gates on.

1. **Median daily deployment ≤ 55%** of NAV, per window.
2. **Deployment above 70% only on days when an objective opportunity regime is active.** Define the
   regime yourself, but it must be: (a) computed from data available at the time, (b) written into
   the strategy (conditions/indicators, not narrative), and (c) stated in the deliverable.
3. **Up to 100% is permitted in the strong/extreme version of that regime** (e.g. a major
   drawdown). The ceiling is full deployment; what is forbidden is being maxed out with no
   opportunity-regime signal active. Flag any such day.
4. Report per window: median, p90, % of days >70%, and whether every >70% day fell inside the
   declared regime. Never audit posture from optimizer statistics; only from full-window
   backtests / OOS segments.

## Fixed constants

| Parameter                                | Value                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| `initial_value`                          | 25000                                                                  |
| `interval`                               | Day                                                                    |
| Walk-forward span                        | 2022-01-01 → (run date − `lockbox_width_days`)                         |
| `lockbox_width_days`                     | 126 (~6 months), held out from ALL folds and ALL search (see Stage S2) |
| Lockbox window                           | (run date − 126d) → run date; finalist touches exactly once at S2      |
| `walk_forward_mode` (calendar)           | anchored                                                               |
| `mode` (study)                           | validation                                                             |
| `engine_kind` (certification)            | **sweep** (bounded, typed search — see "Engine choice")                |
| `fold_count`                             | 4 (minimum 3)                                                          |
| `oos_width_days`                         | 252 (~1y OOS per fold)                                                 |
| `validation_percent`                     | **50** (long validation windows — mandatory, see "Why 50")             |
| `certification`                          | **true** (activity + quality floors on fold-winner selection)          |
| `baseline_symbol`                        | SPY                                                                    |
| Live deploy target                       | `69a7dc7acdb6bf6a4681d36c` — no writes until human sign-off            |
| Baseline A (equity B&H, 20 names)        | build at S1                                                            |
| Baseline B (naive LEAP ladder, 20 names) | build at S1                                                            |

**Why `validation_percent: 50` is mandatory.** Short validation splits make fold-winner selection
noisy on convexity books and can yield `NoEligibleCandidate` under the quality floors — honest
information, not a bug. Long validation windows (8–20 months) are the biggest lever for stable
selection. The server defaults to 50 when `certification: true`; do not override without a logged
reason.

**Why `certification: true`.** Activity and quality floors (participation ≥ 0.35, distinct names ≥
9, validation return ≥ 0, validation Sortino ≥ 0.5) evict degenerate thin-book validation winners.
A fold returning `NoEligibleCandidate` means the design cannot be cleanly certified on that window
— widen validation or rethink the design; do not drop the floors.

Build both baselines on the current engine at S1 and record their IDs + per-fold OOS in
CAMPAIGN_LOG.md before designing anything. Do not reuse stale baseline runs.

Seed affordability note: any single-template ~$1k-per-name book structurally fails Gate 1. Minimum
defined-risk structures on the expensive tail (META/LLY/GS/TSM/ADI/AVGO) cost $1.3–2.4k per
contract. Every template set must end in a rung the most expensive name can fill at the configured
per-name allocation. Do not remove the cheapest rung when sweeping structures.

Baseline B definition: all 20 names, no rank, no filter, 14-day cadence, 8%-of-portfolio per name
under a 95% budget, structure = first affordable rung of [Δ0.50 call → Δ0.55/0.25 vertical →
Δ0.55/0.40 vertical → Δ0.50/0.42 vertical], all 180–365 DTE, single exit at DTE ≤ 45. Naive in
mechanism, honest in participation. Baselines are benchmarks, not candidates.

**Baseline validity rule (applied per fold):**

- **Baseline A is a return bar only**, never a Sortino bar. Its Sortino reflects equity-rally
  smoothness a leveraged long-premium book cannot match; comparing to it is incoherent.
- **Baseline B is a return bar, and a Sortino bar in folds where it has ≥ 9/20 breadth**
  (`rollups.distinctNamesFilled` from `audit_backtest_breadth` on that OOS segment). Where B fails
  breadth in a fold, the absolute Sortino floor (Gate 2) is the only Sortino constraint there.

---

## Engine choice: sweep, not GA (fixed)

Certification uses `engine_kind: sweep` — a bounded, typed grid over a small number of knobs.
Open-ended GA is **not** used for deploy-grade certification (`certification: true` + GA is
rejected unless `allow_ga_certification: true`). Reason: GA mutates genome structure (comparators,
constants, window lengths), producing degenerate thin-book winners and scrambled conditions. A
bounded sweep only moves the knobs you name.

**Authoring a sweep (the only supported path):**

1. `get_sweep_surface` on the seed portfolio first — valid `scope`/`field` pairs, default gene
   templates, authoring controls. Do not hand-guess field names.
2. Build genes with **`gene_intents`** (plain English, one per axis). The server compiles and
   validates them. Prefer this over hand-authored `sweep_config` JSON.
   - Take-profit is `TakeProfitPct` on **Action** scope. Never sweep take-profit as an
     `ExitCondition` / `OptionPositionPercentChange`.
   - Roll DTE is `RollTriggerDte` on **Action** scope (roll CloseOption only).
3. `run_walk_forward_study` with `preview_only: true` first — compiles genes and estimates cost
   without billing. Confirm compiled `scope`/`field` and value labels, then launch for real.

---

## Selection method (fixed — this is the core of the methodology)

When the study completes, you do **not** deploy the per-fold validation argmax. You select the
parameterization that is **robust across the whole calendar**:

1. From `get_walk_forward_study_results`, read the per-fold OOS table, `aggregate`, and every
   fold's `selectedChatPortfolioId`. Confirm winners persisted and materialized (real IDs, no
   `materializationError`).
2. **Read `aggregate.crossFoldRobustSelection`.** This is the engine's cross-fold robust pick:
   the grid cell with the highest **minimum validation Sortino** across all completed folds
   (`metric: "minSortino"`, `candidateKey`, `score`, `perFoldSortino`). **Start here.** Compare
   its `candidateKey` to each fold's `selectedCandidateKey` and to
   `aggregate.dominantCandidateKey` / `winnerStableAcrossFolds`.
3. **Prefer cross-fold robustness over single-fold spikes.** If `crossFoldRobustSelection` disagrees
   with one fold's argmax, treat that as the expected noise signal — do not deploy fold-3's winner
   because it spiked. If `winnerStableAcrossFolds` is false and `crossFoldRobustSelection` is
   absent or weak (no cell covers all folds), the surface is noise: deepen search or widen
   validation; you have no deployable winner yet.
4. **Assemble the deploy book from the robust parameterization** (`crossFoldRobustSelection.candidateKey`
   or a centroid of the top cluster — parameter values most common among top-ranked cells), not by
   cloning a single fold's materialized winner. Build deploy-shape with structured
   `create_portfolio` (validated strategy objects); posture encoded in conditions/budgets.
5. **Measure the assembled book directly.** Backtest it on each fold's OOS window and the aggregate.
   The deploy decision rests on _the assembled object's measured OOS_, never on certified fold-winner
   numbers for a different object.

---

## Stage S0 — Engine sanity (MANDATORY; blocks everything)

Quick contract checks before trusting certification. Record every S0 outcome in CAMPAIGN_LOG.md.

1. **Walk-forward sweep smoke.** `create_portfolio` a trivial chat book (e.g. SPY > SMA50).
   `run_walk_forward_study`: `mode: validation`, `fold_count: 2`, `engine_kind: sweep`, one
   `gene_intent` × 3 values, `certification: false`. Must start and complete with per-fold OOS +
   aggregate via `get_walk_forward_study_results`. Failure → **STOP, report.**
2. **Window fidelity (one fold).** On a completed fold from (1) or a prior cert: note validation and
   OOS windows. `backtest_portfolio` the materialized fold winner on each window; fold
   `validationStatistics` and `oosStatistics` must match standalone backtests within rounding.
   Also confirm disjointness: train ∩ validation, train ∩ OOS, validation ∩ OOS empty; OOS starts
   after validation ends. Mismatch → **STOP, report.**
3. **Persistence.** `get_walk_forward_study_results` returns a real `selectedChatPortfolioId` for
   every completed fold. Missing → **STOP, report.**
4. **Dead-name handling (SNDK).** Tiny `backtest_portfolio` over a 2022 window on the 20-name
   universe. **Pass:** SNDK absent or in not-yet-listed reject lists with **no fabricated price/
   indicator values**. **Fail:** engine errors, or any non-null reading for a name that did not
   trade.

Only after S0 passes do you design anything.

---

## Stage S1 — Baselines as OOS bars

Run `run_walk_forward_study` (anchored, `fold_count: 4`, `oos_width_days: 252`,
`validation_percent: 50`, `mode: validation`, walk-forward span ending at lockbox cutoff) on
Baseline A and Baseline B. Record per baseline: each fold's OOS return + Sortino + maxDD, OOS
aggregate, and per-fold breadth (which folds give B ≥ 9/20). Confirm Baseline B's per-fold breadth
audit shows no `namesWithZeroResolutionAttempts` for **eligible** names whose signals should
have fired.

---

## Stage S2 — Lockbox confirmation (single touch, after design freeze)

The walk-forward span stops `lockbox_width_days` before the run date. That final window is the
lockbox: no fold, sweep, or search touches it. Only the assembled deploy-shape book that **passed
every gate on the WF aggregate** runs over the lockbox exactly once after design freeze.

**Pass conditions (frozen at S0):**

- Lockbox OOS return ≥ worst single-fold WF OOS return.
- Lockbox maxDD ≤ 55%.
- Posture clean over the lockbox (`audit_backtest_posture`, all four conditions).
- Breadth ≥ 9 **eligible** names over the lockbox (`audit_backtest_breadth`).

A lockbox failure is calendar-fit selection pressure. Do not deploy except by logged owner
override naming the lockbox.

**Single-touch is absolute.** If you look at the lockbox and then iterate the design, the lockbox is
burned — move the WF span back and hold out a fresh tail before any deploy.

---

## Gates — the ONLY constraints on design. The finalist must pass ALL.

Evaluated on the **walk-forward OOS aggregate and per fold**, on the assembled deploy-shape book,
measured directly (never on certified fold-winner numbers for a different object).

1. **Breadth & anti-concentration** (per fold dev backtest AND OOS segments, via
   `audit_backtest_breadth`):
   - **Not-yet-listed names** excluded from breadth shortfall reasoning per fold (Gate 1 rule).
   - `gates.namesWithRejectionsAndZeroFills` empty for eligible names.
   - Cumulative participation ≥ 13/20; ≥ 9/20 in each OOS segment.
   - Concentration (per fold dev): no single name > 25% entry notional; top-5 ≤ 60%.
   - `gates.namesWithZeroResolutionAttempts` empty for eligible names whose signal should have fired.
2. **OOS beats buy & hold:**
   - **Return:** aggregate OOS beats Baseline A AND SPY (≥ +10pp vs each on aggregate); majority of
     folds beat both.
   - **Sortino (absolute floor):** aggregate OOS Sortino ≥ 1.9; no fold below 0.9. Fixed floor.
3. **OOS robustness (the overfitting gate):**
   - OOS return positive in ≥ `ceil(0.75 × fold_count)` folds.
   - Worst single-fold OOS return ≥ −15%.
   - `winnerStableAcrossFolds` true OR `crossFoldRobustSelection.candidateKey` matches
     `dominantCandidateKey` with ≥ half the folds, OR cross-fold robust pick covers all folds with
     acceptable min Sortino. **A result carried by one fold fails.**
4. **Beats Baseline B:** per baseline validity rule.
5. **Drawdown:** OOS maxDD ≤ 55% every fold.
6. **Capital posture:** all four conditions on every fold dev window AND OOS segment.
7. **Reproducibility (field-level).** Re-fire assembled-book backtest on one OOS window;
   `compare_backtests {tolerance_bps: 0}` → `identical: true`. `get_portfolio` +
   `conditionFieldAudit` matches intended design (fields, not names).
8. **Live parity (field-level).** After clone, before approving orders: `get_portfolio` target vs
   source field-for-field; `query_portfolio_events` with `include_condition_audit: true` vs same-day
   backtest. Mismatch → stop, decline pending orders, report.

If any gate fails: iterate the **design**. Gates and lockbox conditions are frozen at S0.

---

## Process (stages are scaffolding, not prescriptions)

- **S0 Engine sanity** → **S1 Baselines**, recorded before design work.
- **Search (cheap layer).** `create_portfolio`, variants, backtests, `systematic_sweep` over the WF
  span only — **never the lockbox**. Kill-log every mechanism. Optimizer is a knob-setter.
- **Assemble finalist** deploy-shape book (`create_portfolio`, structured objects).
- **Certify.** `run_walk_forward_study`: `engine_kind: sweep`, `certification: true`,
  `validation_percent: 50`, `gene_intents` after `get_sweep_surface` + `preview_only`. Apply
  **Selection method** using `crossFoldRobustSelection`. Gate on assembled object's OOS. Three
  certification attempts per idea is the ceiling.
- **Lockbox (S2).** Single touch after freeze.
- **Sign-off + deploy** (explicit human "deploy" or logged override):
  1. `get_portfolio 69a7dc7acdb6bf6a4681d36c` — audit positions/cash.
  2. Verify live order pipeline (`query_portfolio_events` — no cold chain / empty-chain audits).
  3. `clone_strategies_to_portfolio` (replaces strategy set; archives monitor).
  4. Field-verify clone (`conditionFieldAudit` source vs target).
  5. Re-backtest live target; `compare_backtests {tolerance_bps: 0}` vs finalist (Gate 7).
  6. Re-attach weekly monitor via `edit_portfolio addStrategies`; verify in `get_portfolio`.
  7. **Gate-8 live parity** on first evaluator tick before approving orders.
  8. Log everything in CAMPAIGN_LOG.md.

---

## Deploy timing + live monitoring (no paper stage)

**When a finalist passes all gates and the lockbox, it deploys LIVE** after sign-off.

- Gates and lockbox frozen at S0. Mid-campaign relaxation invalidates the campaign.
- **Human override:** name the failed gate/lockbox, verbatim justification in CAMPAIGN_LOG.md and
  deliverable.
- No strategy edits after deploy without a new campaign.
- **Live kill thresholds:**
  1. Posture: median ≤ 55%; no day > 70% outside declared regime.
  2. Drawdown brake: pause entries at ≥ 30% from deploy peak; full review at ≥ 55%.
  3. SPY-excess review (not pause): after 12 weeks, excess < −15pp → owner review.
  4. Order health: fills on eligible signals; no cannot-afford rejections; no
     `OPTION_CHAIN_EMPTY_FOR_REQUESTED`.
  5. Condition integrity: weekly field audit vs intended design.
- **Weekly agent monitor (mandatory):** `LaunchAgent`, `Day = Monday OR CrossBelow(SPY, SMA200(SPY)) = 1`,
  `cooldownMinutes: 1440`, `continueExisting: true`, `google/gemini-3-flash-preview`,
  `maxIterations: 15` — audits thresholds + per-spread P&L/DTE. Keep monitor OFF finalist chat
  portfolio.

---

## Tooling

- **`get_sweep_surface`** — call FIRST. Valid scope/field pairs, gene templates. Zero cost.
- **`run_walk_forward_study`** — certification. `engine_kind: sweep`, `gene_intents`,
  `validation_percent: 50`, `certification: true`, `preview_only: true` to compile/cost-check.
- **`get_walk_forward_study_results`** — per-fold stats, aggregate (`crossFoldRobustSelection`,
  `dominantCandidateKey`, `winnerStableAcrossFolds`), `selectedChatPortfolioId` per fold.
- **`get_portfolio` / `conditionFieldAudit`** — what a book IS (fields, not names).
- **`audit_backtest_breadth`** / **`audit_backtest_posture`** — Gates 1 and 6.
- **`create_portfolio_variant`**, **`compare_backtests`**, **`backtest_portfolio`**,
  **`systematic_sweep`** — search layer (WF span only, not lockbox).

---

## Search constraints (follow these; override only with an A/B pair that disproves them)

- **No stop-losses on hold-to-expiry LEAP/spread books** unless A/B proves otherwise.
- **No narrow ranked rotation (top-K ≤ 5 with shared cadence).**
- **`totalBudget` ≥ K × `perNameAllocation`** per tier.
- **Template ladder** so every name has an affordable unit; cheap structures as primary = kill path.
- **Budgets cap cost basis, not market value** — verify posture on tape.
- **One mechanism change per candidate.**
- **Take-profit is `TakeProfitPct` (Action scope).** `CloseOption` pnl: `minPnlPercent: 100` = +100%
  TP; `maxPnlPercent: -50` = −50% stop.
- **`DaysSinceLastRebalanceOptionOrder` / `DaysSinceOrder`:** `null >= N` is TRUE on fresh books;
  shared cadence clock across RebalanceOption strategies.
- **Dollar budgets do not de-risk like %-of-NAV sizing.**
- **Re-sweep from a clean seed** — re-sweeping an already-swept book can stack genes; field-audit
  for duplicated conditions before trusting.

---

## Indicator vocabulary (materials, not prescriptions; full list in `create_portfolio` schema, ~90 types)

Inside RebalanceOption pipelines, rank `weightIndicator`s, and template `eligibility` conditions, an
indicator with an **empty `targetAsset` (`{"symbol": ""}`) evaluates per candidate name** — that is
how one rank/filter applies across the universe. Named `targetAsset`s (e.g. SPY) make it a
market-level reading.

- **Price & trend:** `Price`, `SimpleMovingAverage`, `ExponentialMovingAverage`,
  `MaximumPrice`/`MinimumPrice`, `MaxDrawdown`/`MaxDrawup`, `PriceRateOfChange`,
  `PriceStandardDeviation`, `AverageTrueRange`, `RelativeStrengthIndex`, `BollingerBand`, `VWAP`,
  `Volume`.
- **Composition:** `Plus`/`Minus`/`Multiply`/`Divide`/`Max`/`Min`/`AbsoluteValue`/`Log`/
  `Exponentiation`.
- **Meta-indicators (windows over indicators):** `IndicatorWindowAgo`,
  `IndicatorSimpleMovingAverage`/`IndicatorExponentialMovingAverage`, `IndicatorStandardDeviation`/
  `IndicatorMeanAbsoluteDeviation`, `IndicatorRateOfChange`, `TrailingSum`.
- **Events & persistence:** `CrossAbove`/`CrossBelow`, `ConsecutiveTrue`/`CountTrue`.
- **Market & macro:** `Index` (`VIX`/`SPX`), `Economic` (`UNRATE`); regime ratio = `Price(SPY)` vs
  `Multiply(k, MaximumPrice(SPY, 252d))`.
- **Fundamentals:** `Fundamental`, `CompoundAnnualGrowthRate(metric, years)`.
- **Book & position state:** `OptionGrossExposurePercent`, `OptionPositionCount`,
  `OptionUnrealizedPnL`, `OptionDaysToExpiration`, `PositionPercentChange`, `PortfolioValue`,
  `BuyingPower`, `DaysSince*` family.
- **Calendar:** `Day`/`Month`/`Date`.

Calibrate thresholds against observed values, never intuition.

### Composed-indicator recipes (copy, modify, or ignore — per-name unless noted)

- **Momentum acceleration:** `ROC(21) − IndicatorWindowAgo(ROC(21), 21d)`.
- **Momentum smoothness (Sharpe-like rank):** `ROC(63) / PriceStandardDeviation(63)`.
- **Vol compression (squeeze):** `ATR(14) / IndicatorSMA(ATR(14), 100d)`, below ~0.8 coiled.
- **Pullback depth in ATR units:** `(MaximumPrice(252) − Price) / ATR(14)`.
- **Parabolic-extension guard:** `(Price − SMA(20)) / ATR(14)`.
- **Trend persistence:** `CountTrue(Price > SMA(50), 63d)`.
- **Relative strength vs market:** `ROC(63, name) − ROC(63, SPY)`.
- **Upside/downside asymmetry:** `MaxDrawup(63) / MaxDrawdown(63)`.
- **Volume thrust:** `Volume / IndicatorSMA(Volume, 50d)`.
- **Adaptive vol regime (market):** `Index(VIX) / IndicatorSMA(Index(VIX), 20d)`.

### Searches worth running (suggestions)

- Per-template `eligibility` gates; structure-by-regime; underlying-state exits;
  exposure-keyed de-risk; entry-condition gates via `gene_intents`.

---

## Deliverable (present at sign-off)

Per-fold table + aggregate row + lockbox row:

| Fold          | Dev window | OOS window                   | OOS return      | OOS maxDD | OOS Sortino     | Names filled /20 | Median deploy | %days >70% (in regime?) | vs A | vs B | vs SPY |
| ------------- | ---------- | ---------------------------- | --------------- | --------- | --------------- | ---------------- | ------------- | ----------------------- | ---- | ---- | ------ |
| 1 … N         |            |                              |                 |           |                 |                  |               |                         |      |      |        |
| **Aggregate** |            |                              | mean/median/min | worst     | mean / min-fold |                  |               |                         |      |      |        |
| **Lockbox**   | (held out) | (run date − 126d) → run date |                 |           |                 | (eligible)       |               |                         |      |      |        |

Plus: walk-forward study id; **`crossFoldRobustSelection` candidateKey and why chosen** (vs per-fold
winners); full strategy rules; declared opportunity regime; kill-log; finalist chatPortfolioId;
OOS-robustness summary; per-fold breadth audit; lockbox PASS/FAIL; field-level reproducibility
PASS/FAIL; Gate-8 live parity; any owner override; weekly monitor reports in CAMPAIGN_LOG.md.

**Headline = OOS aggregate of the assembled, directly-measured book. Never a single-window or
in-sample number.**

## Working rules

- CAMPAIGN_LOG.md at every stage; S0/S1 before design.
- Search with optimize/variants/backtests; certify with walk-forward.
- **Select on cross-fold robustness** (`crossFoldRobustSelection`), not per-fold validation argmax.
- Verify everything that trades real money at FIELD level (`conditionFieldAudit`).
- Measure deploy decisions on the directly-backtested assembled object.
- Lockbox held out from ALL search; touched exactly once at S2.
- Compare certified candidates against both baselines on the same calendar.
- Honest "no deploy" or "no robust winner" = successful outcome.
- Three certification attempts per idea, then widen search.
- Deploy only after explicit human "deploy" or logged override.
