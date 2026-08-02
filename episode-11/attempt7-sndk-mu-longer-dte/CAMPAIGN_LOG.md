# Episode 11 Attempt 7 — SNDK + MU Longer-DTE Intraday Retest

**Started:** 2026-07-19
**Capital:** $8,000 fixed cold-start capital
**Intended live target:** `MU + SNDK Live Trading Portfolio`
**Status:** RESEARCH FINALIST CERTIFIED — no deployment or orders authorized

## Mandate

Find an outstanding MU/SNDK intraday options strategy using outright long calls and puts, no debit or
credit spreads and no short option legs. Attempt 7 expands the instrument constraint from exactly 0DTE
to longer DTE while keeping every position flat before the close. Attempt 6 remains an immutable null
result rather than being rewritten after the constraint change.

## Hard constraints

- Universe exactly `MU` and `SNDK`.
- Every entry is one single-leg long call or long put; no spread or short leg.
- Both names and both option types must fill in fresh event evidence.
- Initial screening allocation is exactly one contract and global open option count is below one.
- Entry window remains intraday and all options close before the bell; no overnight exposure.
- Every strategy keeps `automaticOrderApproval: false`.
- No reconciliation, staged order, deployment, or live mutation without explicit authorization.

## Evidence and provenance

- Attempt 6 results are design inspiration only. No prior performance number is inherited as proof;
  every promoted structure receives a new portfolio artifact and a new current-engine run.
- The clean structural seed is AA1 (`6a5c7a964412b1d5eedba11e`): one-ticket impulse entries, 4% OTM
  calls, 3% OTM puts, +1% one-day ROC gate on calls, and minute-360 flatten.
- DTE is a structural change. Every expiration selector and matching `MinutesSinceOptionOrder` DTE
  filter must be patched and field-audited together; all parameters remain hand-set until the exact
  longer-DTE winner is re-swept.

## Frozen first-stage DTE screen

| Family | Entry DTE selector | Preference | Overnight hold |
|---|---|---|---|
| L1 | 1–7 DTE | nearest | none |
| L2 | 8–14 DTE | nearest | none |
| L3 | 15–30 DTE | nearest | none |

The brackets are disjoint. Zero-DTE contracts are excluded from every Attempt 7 candidate.

## Frozen evaluation windows

- Search: 2026-01-02 through 2026-04-30.
- Validation 1: 2026-05-01 through 2026-05-29.
- Validation 2: 2026-06-01 through 2026-06-30.
- Fresh confirmation: 2026-07-01 through 2026-07-10.
- Full continuous path: 2026-01-02 through 2026-07-10 from one $8,000 start.

July 10 remains the latest proven historical option-data endpoint from Attempt 6; no result beyond it
counts until later data is explicitly verified.

## Baseline and pass contract

Primary baseline is the newly rebuilt 50/50 MU/SNDK buy-and-hold control
`6a5df3ed2ee25ecab46bde2f`, current-engine backtest `6a5df416814d31180a1c62a2`:

- Full: +450.85%, Sortino 5.85, maxDD 34.46%.
- Search: +191.54%.
- May: +71.81%.
- June: +21.51%.
- July: −8.07%.

PASS requires fresh completed current-engine evidence, positive return in a majority of validation
partitions, positive full Sortino, full return at least 80% of baseline or at least 65% with no worse
drawdown and materially better risk-adjusted performance, maxDD no worse than baseline and never above
50%, and genuine bull-partition option alpha. Calls and puts must both contribute physically; a result
driven only by downside puts is not the requested bull-market strategy.

## Re-optimization contract

The initial three-family DTE screen may only KILL or PROMOTE. Any promoted exact book must receive a
fresh non-trivial grid of at least three axes with at least three values per axis. Planned axes are DTE
bracket/target, call/put moneyness, and exit timing or entry threshold, subject to the actual sweep
surface and execution behavior. Selection is by cross-window robustness, not the single best return.

## Campaign ledger

| Time | Stage | Artifact | Result | Status |
|---|---|---|---|---|
| 2026-07-19 | Reset | This log | Longer-DTE mandate and frozen screen created | VALID |
| 2026-07-19 | DTE screen | L1 `6a5ce72f14879ee3b06dd527` / BT `6a5ce7783f94098f5434ed10` | +22.70%, maxDD 54.76% | KILL — risk fail |
| 2026-07-19 | DTE screen | L2 `6a5ce73614879ee3b06dd54c` / BT `6a5ce77c14879ee3b06dd6ba` | +19.59%, maxDD 56.96% | KILL — risk fail |
| 2026-07-19 | DTE screen | L3 `6a5ce733ca4e324ade7d1929` / BT `6a5ce78114879ee3b06dd6d1` | +34.70%, maxDD 37.02% | PROMOTE to re-optimization only |
| 2026-07-19 | Re-optimization | Clean seed `6a5ce81814879ee3b06dd8e6` | 27-cell preview valid; optimizer failed before evaluation | QUARANTINED; explicit grid used |
| 2026-07-19 | Explicit grid | 27 immutable variants / 27 completed search backtests | Best: 10–21 DTE, 10% OTM, any TP: +76.00%, Sortino 5.87, maxDD 20.32% | SEARCH ONLY |
| 2026-07-19 | Validation | 10–21 / 10% / TP75 `6a5ce9f33f94098f5434f554` | May −13.86%; June −21.12%; July +22.23%; full +53.61%, maxDD 46.45% | KILL |
| 2026-07-19 | Validation | 21–45 / 5% / TP75 `6a5cea154c459b8ce9c04a78` | May −27.09%; June −15.84%; July +11.89%; one name in each partition | KILL |
| 2026-07-19 | Validation | 3–10 / 10% / TP75 `6a5ce9c814879ee3b06ddbf4` | May −20.62%; June +23.77%; July +129.71%; continuous full pending | SURVIVOR PENDING FULL/EVENT AUDIT |
| 2026-07-19 | Full/event audit | `6a5ce9c814879ee3b06ddbf4` / BT `6a5cec614c459b8ce9c04f32` | Full +201.30%, Sortino 4.41, maxDD 39.14%; 109 paired trades; calls +$5,662.50, puts +$10,441.80 | KILL — 44.65% baseline capture, drawdown worse than baseline, one put supplies 74% of trade P&L |
| 2026-07-19 | Regime-gate redesign | 27 explicit variants, call daily ROC 0/1/2 × put daily ROC 0/−1/−2 × OTM 7.5/10/12.5 | Best search +6.30%, Sortino 0.81, maxDD 29.30% | FAMILY KILL |
| 2026-07-19 | Call-gate isolation | ROC 0% `6a5cef8405df5ce6326590ed` / full BT `6a5cefd005df5ce6326591c1` | Search +71.32%; May −22.37%; June +25.53%; July +1.32%; full +43.07%, DD 43.12% | KILL |
| 2026-07-19 | Independent name slots | `6a5cf03205df5ce6326591ed` / BT `6a5cf047392c6f50da48e4ad` | Search −37.37%, Sortino −1.38, maxDD 56.17% | KILL — global one-ticket gate is protective |

## Candidate ledger

| Family | Portfolio | Field audit | Search | Validation | Full | Verdict |
|---|---|---|---|---|---|---|
| L1 1–7 DTE | `6a5ce72f14879ee3b06dd527` | PASS | +22.70%, DD 54.76% | not promoted | — | KILL |
| L2 8–14 DTE | `6a5ce73614879ee3b06dd54c` | PASS | +19.59%, DD 56.96% | not promoted | — | KILL |
| L3 15–30 DTE | `6a5ce733ca4e324ade7d1929` | PASS | +34.70%, DD 37.02% | promoted to grid | — | SEARCH PROMOTION ONLY |

## Explicit re-optimization surface

All 27 combinations completed on the search window. TP 75/100/150 was non-differentiating at every
DTE/moneyness cell because the intraday flatten exited first; each row below represents three exact
variants/backtests with identical statistics.

| DTE | OTM | Search return | Sortino | MaxDD | Surface verdict |
|---|---:|---:|---:|---:|---|
| 3–10 | 5% | +3.98% | 0.82 | 51.33% | KILL |
| 3–10 | 10% | +68.44% | 4.96 | 20.97% | VALIDATION SURVIVOR |
| 3–10 | 15% | +4.60% | 0.68 | 27.05% | KILL |
| 10–21 | 5% | −20.60% | −0.02 | 65.84% | KILL |
| 10–21 | 10% | +76.00% | 5.87 | 20.32% | SEARCH WINNER; VALIDATION KILL |
| 10–21 | 15% | +14.84% | 1.49 | 38.94% | KILL |
| 21–45 | 5% | +14.56% | 1.29 | 36.55% | VALIDATION KILL |
| 21–45 | 10% | −52.76% | −2.58 | 78.01% | KILL |
| 21–45 | 15% | +3.54% | 0.61 | 40.76% | KILL |

## Event and fill audit — best validation survivor

- Backtest: `6a5cec614c459b8ce9c04f32`; 218 filled option orders paired into 109 complete
  one-leg round trips with zero unpaired fills.
- Calls: 35 trades, +$5,662.50 after per-order fees; MU calls +$4,833.10 and SNDK calls
  +$829.40.
- Puts: 74 trades, +$10,441.80 after per-order fees; MU puts −$602.95 and SNDK puts
  +$11,044.75.
- Both calls and puts contribute physically and economically, but SNDK put
  `SNDK260710P01785000` on 2026-07-02 made $11,946.20 by itself—about 74% of all net trade P&L.
  That concentration is incompatible with an outstanding/certifiable verdict.

## Bug / issue ledger

| Issue | Evidence | Impact | Status |
|---|---|---|---|
| Sweep request-schema mismatch | Initial launch rejected `type` and then `primaryMetric`; preview proved accepted schema is `mode` + `primary` | No evaluations occurred. Corrected without changing the frozen grid. | CLOSED as authoring error |
| Systematic direct-OpenOption sweep terminates before evaluation 1 | DTE optimizers `6a5ce9053f94098f5434f34d` 0/27 and `6a5ce95a14879ee3b06ddb08` 0/3; non-DTE F2 optimizer `6a5cf47e05df5ce63265966d` 0/27; see `SYSTEMATIC_DTE_SWEEP_ZERO_EVALUATION_BUG.md` | The shipped engine fix restored evaluation and winner materialization in post-fix study `6a5da1d09dffb90d2c07de8a`. The old IDs remain quarantined and must never be reinterpreted as performance evidence. | CLOSED by shipped engine fix; superseded by fee-fidelity blocker |
| Direction-specific strike sweep unsupported | F2 preview on seed `6a5cf368392c6f50da48e7d6` rejected the call-only strike gene and refused to run a partial 2-axis grid | No evaluations or results exist. This is an explicit compiler limitation, not an engine-performance bug. Replace with all-leg strike distance plus a direction-neutral normalized gap-filter axis. | CLOSED as authoring limitation |
| Entry-filter preview stamps first ticker | F2 preview compiled `Abs(MU Gap Percentage)` under selector `All`; Rust materialization late-binds each fixed-underlying OpenOption through `action_condition_asset → to_condition → with_asset`; see `SWEEP_ENTRY_FILTER_WRONG_UNDERLYING_BUG.md` | No runtime cross-asset eligibility bug. Preview remains misleading and should expose per-strategy late binding. | CLOSED — preview clarity issue |
| Walk-forward gene-intent compiler emits invalid strike values | Post-fix S0 `run_walk_forward_study(preview_only)` on F2 seed rejected the one-axis intent with `strike target requires StrikeSelector values`; the equivalent `systematic_sweep` compiler previously produced valid `StrikeSelector` objects | No study/evaluation launched and no result exists. S0 will use the exact hand-authored validated SweepConfig to isolate engine execution from LLM compilation. | OPEN compiler-path inconsistency; not yet an engine failure |
| Walk-forward option-fee/window fidelity failure | Fold 0 winner `6a5da266627ac9b74ecee32f` reports OOS +44.0301% and $435.09 fees in old study `6a5da1d09dffb90d2c07de8a`, but exact-window standalone replay `6a5da27655ac577a49d1684a` reports +49.2413% and $18.20 fees; see `WALK_FORWARD_OPTION_FEE_FIDELITY_BUG.md` | The shipped fee fix was verified by fresh study `6a5dc4c82ee25ecab46ba437`: both fold winners reproduce validation/OOS economics exactly under standalone replay. The old study remains quarantined. | CLOSED by shipped fee-contract fix |
| Fly optimizer wake returns HTTP 500 before fold 0 | Qualifying F2 study/optimizer pairs `6a5dc72cea0d6db55c693cd7` / `6a5dc72cea0d6db55c693cdb` and exact retry `6a5dc798814d31180a1c2df1` / `6a5dc798814d31180a1c2df5` are all `ERROR` at 0/112 with `fly_api_error: Request failed with status code 500`; see `FLY_OPTIMIZER_WAKE_500_BUG.md` | Both failed pairs remain quarantined. Unchanged retry study `6a5dd72aea0d6db55c694eeb` completed 112/112, proving recovery at the same workload. | RECOVERED; upstream root cause open |
| F2 fold-1 materialized replay diverges from study | Study fold-1 OOS is −13.2106%, $15,307.50 sold, 96 null gates; exact May 12–31 materialized replay `6a5de246ea0d6db55c696248` is −11.2575%, $14,950 sold, 120 null gates with the same $15.60 fees; see `F2_FOLD1_MATERIALIZATION_REPLAY_FIDELITY_BUG.md` | Fold-1 study economics are quarantined. Fresh materialized replay is used for attribution and promotion decisions. | OPEN certification-fidelity bug |

## Post-fix engine sanity (S0; does not count toward certification)

- Typed one-axis/three-value direct-OpenOption sweep preview: PASS; 2 disjoint anchored folds, 8
  planned units, no gene warnings.
- Walk-forward smoke: study `6a5da1d09dffb90d2c07de8a`, root optimizer
  `6a5da1d09dffb90d2c07de8e`; direct-OpenOption evaluation and fold-winner persistence now work.
- Dead-name check: F2 seed over 2022-01-03 through 2022-01-14, backtest
  `6a5da1e355ac577a49d16806`; COMPLETE with zero trades, 15,855 null-gated evaluations, and no SNDK
  signal/resolution/order/no-signal events. PASS: no fabricated SNDK reading.
- Winner persistence: fold 0 selected individual `6a5da25d65eabcf7514eeb6f` materialized as
  ChatPortfolio `6a5da266627ac9b74ecee32f`; direct inspection confirms four one-leg outright-long
  MU/SNDK call/put entries at the selected 5% OTM value. PASS.
- Window fidelity: **FAIL**. Fold 0 OOS study statistics show +44.030125% and $435.09 fees; exact
  standalone replay `6a5da27655ac577a49d1684a` shows +49.24125% and $18.20 fees. The $416.89 fee
  delta exactly equals the 5.211125 percentage-point return delta on $8,000. Validation also diverges
  in fees, sold dollars, and trade path. See `WALK_FORWARD_OPTION_FEE_FIDELITY_BUG.md`.
- S0 result: **BLOCKED/FAIL**. Study `6a5da1d09dffb90d2c07de8a` and all of its fold results are
  diagnostic-only. No post-fix strategy result is trusted until a new study passes exact replay
  parity under a single explicit option fee contract.

### Fresh post-fee-fix S0 retest — PASS

- Study `6a5dc4c82ee25ecab46ba437`; root sweep `6a5dc4c92ee25ecab46ba43e`;
  COMPLETE, 8/8 units, two disjoint anchored folds, aggregate present.
- Fold 0 winner `6a5dc5b3ea0d6db55c693bfe`: validation replay
  `6a5dc5c3814d31180a1c2d39` and OOS replay `6a5dc5e62ee25ecab46ba4a2` match the study exactly.
  Validation −30.15125%, Sortino −2.28420, maxDD 62.07735%, fees $22.10; OOS +49.24125%,
  Sortino 6.19235, maxDD 57.42776%, fees $18.20.
- Fold 1 winner `6a5dc63cea0d6db55c693c56`: validation replay
  `6a5dc64aea0d6db55c693c6d` and OOS replay `6a5dc64e2ee25ecab46ba4f7` match the study exactly.
  Validation +19.24813%, Sortino 3.38499, maxDD 30.72820%, fees $29.90; OOS +68.21000%,
  Sortino 10.26241, maxDD 32.04373%, fees $18.20.
- Persistence: PASS; every completed fold has a real `selectedChatPortfolioId`.
- Dead-name retest: `6a5dc675ea0d6db55c693c9c`, 2022-01-03 through 2022-01-14;
  COMPLETE with zero trades/fees, 15,855 null-gated evaluations, and no SNDK signal,
  resolution, order, or no-signal events. PASS.
- Residual observability note: fold and standalone `nullGatedEvaluations` counts differ by 24 while
  every economic statistic matches exactly. This does not block S0 but should not be used as a
  cross-surface equality metric.
- **S0 overall: PASS. Strategy iteration may resume from fresh post-fix IDs.**

## Verdict

**ACTIVE — campaign-level null retracted. Nothing is deployed.**

The block below is retained as the terminal result for **Family 1: shared one-ticket impulse**, not as
proof that the user's SNDK/MU idea is impossible. The strategy-bakeoff verdict-integrity rule forbids
a campaign-level no-winner conclusion before multiple genuinely distinct mechanisms receive
certification. Attempt 7 is therefore reopened for a put-first shock / delayed-call-continuation
family and at least one additional outright-long calls-and-puts family.

### Family 1 terminal result — shared one-ticket impulse

The strongest longer-DTE research book is `6a5ce9c814879ee3b06ddbf4`: 3–10 DTE, 10% OTM,
one-contract outright-long MU/SNDK calls and puts, one global ticket, call daily ROC >1%, intraday
impulse/VWAP entries, +75% TP, −50% SL, and minute-360 flatten. Its exact continuous backtest
`6a5cec614c459b8ce9c04f32` returned +201.30% with Sortino 4.41 and maxDD 39.14% over
2026-01-02 through 2026-07-10. That is only 44.65% of the +450.85% buy-and-hold baseline, its
drawdown is worse than baseline 34.46%, and one SNDK put contributes about 74% of net trade P&L.

It does rip in the fresh July partition (+129.71% versus baseline −8.07%) and both calls and puts make
money, but it fails the campaign's full-period return, drawdown, and concentration requirements. The
10–21 DTE search winner fails two of three validation partitions; 21–45 DTE fails two of three and
often trades only one name. Symmetric daily regime gating, a looser call gate, and independent
underlying slots all fail. No longer-DTE variant tested here is suitable for the live $8,000 portfolio.

The next stage changes the mechanism rather than tuning Family 1 further. It keeps the existing risk
mandate: $8,000, MU/SNDK only, outright-long calls and puts, no spreads or short legs, intraday flat,
and automatic approval off.

## Multi-family certification ledger

| Family | Mechanism | Seed | Systematic search | Validation/certification | Status |
|---|---|---|---|---|---|
| F1 | Shared one-ticket impulse | `6a5ce9c814879ee3b06ddbf4` | 27-cell explicit grid; DTE optimizer bug documented | May/June/July/full + event audit | EXHAUSTED; local null only |
| F2 | Put-first shock, delayed call continuation | `6a5cf368392c6f50da48e7d6` | 27 cells: DTE 1/3–10/10–21 × strike 5/10/15% OTM × TP 75/150/300 | Study `6a5dd72aea0d6db55c694eeb`; robust key `adad9e44d767d2fba5a230a090db75ab68ec91c3c656d190811580e80b9d12d1`; 3–10 DTE, 15% OTM, TP75; OOS −11.33/−13.21/+33.27/+68.87%; min validation Sortino −1.94 | ATTEMPT 1 KILL — binding gate: min validation Sortino; family not exhausted |
| F3 | Opening-gap fade with VWAP reversal | `6a5ddb43814d31180a1c462a`; refinement `6a5dde0f814d31180a1c4894` | Two fresh 27-cell searches: DTE 1/3–10/10–21 × strike 5/10/15% OTM × TP 75/150/300 | Attempt 1 study `6a5ddba7814d31180a1c469e`; attempt 2 study `6a5dde44814d31180a1c48d3`; both have four negative validation folds and three negative OOS folds | EXHAUSTED; lowering the gap threshold worsened the same mechanism; local null only |

### F2 certification attempt 1 — terminal result

Fresh study `6a5dd72aea0d6db55c694eeb` and root optimizer
`6a5dd72bea0d6db55c694ef5` completed 112/112 units across four anchored folds. The same candidate won
every fold and the cross-fold robust selection: 3–10 DTE, 15% OTM, TP +75%, key
`adad9e44d767d2fba5a230a090db75ab68ec91c3c656d190811580e80b9d12d1`.

Validation returns were +3.00%, −6.84%, −16.65%, and +12.99%; validation Sortinos were +0.89,
−1.10, −1.94, and +1.49. OOS returns were −11.33%, −13.21%, +33.27%, and +68.87%, with OOS
max drawdowns 24.24–31.44%. Two folds explicitly failed the configured selection floors. The single
binding certification gate is cross-fold minimum validation Sortino (−1.94 versus required +0.50).
The two late bull OOS windows rip, so the mechanism remains economically interesting, but its regime
instability forbids promotion. This kills F2 attempt 1 only; it does not exhaust F2 or the campaign.

Fresh event-enabled exact-window replays used backtests `6a5de2492ee25ecab46bcf29`,
`6a5de246ea0d6db55c696248`, `6a5de1e22ee25ecab46bce51`, and
`6a5de1e6814d31180a1c53eb`. Across those materialized paths, MU puts lost about $1,000; SNDK puts
lost about $1,608 in the first two folds and only became strongly positive because one July 2 trade
made about $8,749. Calls were sparse but net positive (about +$2,231 combined). This concentration
supports one coherent attempt-2 change: require negative one-day ROC confirmation on put entries,
mirroring the positive one-day ROC gate already applied to calls. Calls, timing, exits, contract
count, global slot, and the qualifying sweep grid remain unchanged.

### F3 mechanism and structure freeze

F3 seed `6a5ddb43814d31180a1c462a` is a genuinely different mean-reversion mechanism. Calls require a
negative opening gap of at least 1% followed by a price cross above that underlying's VWAP; puts
require a positive opening gap of at least 1% followed by a price cross below VWAP. Entries are
limited to minute 30–180 and share the global one-position gate. The persisted field audit confirms
MU conditions bind MU and SNDK conditions bind SNDK.

The seed contains exactly four OpenOption entries: one long call and one long put for each of MU and
SNDK, each one leg, one contract, 3–10 DTE, 10% OTM. It keeps TP +75%, SL −50%, minute-360 flatten,
and `automaticOrderApproval:false` on all seven strategies. `build_portfolio` returned valid with no
issues before persistence. `get_sweep_surface` confirms DTE, strike distance, and take-profit are
applicable. The exact-calendar qualifying preview compiled 27 exhaustive cells over the same four
anchored folds as F2, 112 planned units, 165.95 tokens, and no gene warnings. Fresh study
`6a5ddba7814d31180a1c469e` / root optimizer `6a5ddba7814d31180a1c46a2` completed 112/112 units.

#### F3 certification attempt 1 — terminal result

Study `6a5ddba7814d31180a1c469e` completed 112/112 units. The robust key
`2f03d9b939405c6c08adf033240643a94bb8e058f41a83cebc74311446cb7b04` resolves to 1 DTE,
15% OTM, TP +150%; TP was economically non-binding. Validation returns were −0.89%, −1.71%,
−4.02%, and −3.28%, and every fold explicitly failed the floors. OOS returns were −0.56%, −2.47%,
+0.57%, and −0.96%; the last two OOS folds traded only one underlying. The binding gate is minimum
validation Sortino, −4.88 versus required +0.50.

The losses and drawdowns were small, but dollars sold and option fees show the 1% gap plus exact VWAP
cross was too sparse to capture the bull tape. F3 attempt 2 therefore changes only the gap magnitude
to 0.25%; it does not alter reversal direction, timing, position gating, exits, or sweep axes.

#### F3 certification attempt 2 — shallow-gap refinement

Clean seed `6a5dde0f814d31180a1c4894` passed `build_portfolio`, persisted-structure audit, and
`get_sweep_surface`. Its only mechanism change is call gap ≤ −0.25% and put gap ≥ +0.25% on each
strategy's own fixed underlying. All four entries remain single-leg outright-long one-contract calls
and puts with approval off. The exact-calendar 27-cell/four-fold preview again produced 112 units,
165.95 tokens, and no warnings. Study `6a5dde44814d31180a1c48d3` / root optimizer
`6a5dde44814d31180a1c48d9` completed 112/112 units. The dominant robust key
`19f5b81d9d2ee9de60ac4c073e98b364f0851142a4412e98b4d3ead3d53c72c3` resolves to 1 DTE,
15% OTM, TP +75%. Validation returns were −1.24%, −1.91%, −4.30%, and −3.55%; all four folds
failed the configured floors and the minimum validation Sortino was −8.32 versus required +0.50.
OOS returns were −0.75%, −2.55%, +0.57%, and −2.97%, with three of four OOS folds negative and
some folds still participating in only one name.

The shallower gap increased weak entries without repairing robustness. F3 is therefore exhausted as
a local mechanism family after two coherent fresh certifications. This is not a campaign-level null:
F2 remains alive because it delivered +33.27% and +68.87% in its late bull OOS folds. The next F2
change will be chosen from fresh event-level attribution of all four materialized F2 fold winners,
not from another blind threshold adjustment.

### F2 certification attempt 2 — bearish-confirmed puts

Clean seed `6a5de30eea0d6db55c696294` passed `build_portfolio`, persistence audit, and
`get_sweep_surface`. Calls retain the one-day ROC > +1 confirmation; the only mechanism change is a
one-day ROC < −1 confirmation on each fixed-underlying put. It still contains exactly four
OpenOption entries—one long call and one long put for MU and SNDK—each one leg, one contract, with
all seven strategies set to `automaticOrderApproval:false`.

The typed qualifying preview compiled the frozen DTE 1/3–10/10–21 × strike 5/10/15% OTM × TP
75/150/300 grid across the same four anchored folds: 27 exhaustive cells, 112 planned units, 165.95
tokens, and no gene warnings. Study `6a5de4582ee25ecab46bd02a` / root optimizer
`6a5de4582ee25ecab46bd030` completed 112/112 units. Per-fold OOS returns were −6.50%, −60.91%,
+2.31%, and +115.18%; OOS Sortinos were −1.85, −12.41, +1.65, and +16.16; max drawdowns were
32.73%, 70.48%, 42.74%, and 17.54%. Winners were unstable across folds. Two folds were explicitly
uncertified, and the cross-fold robust candidate—3–10 DTE, 15% OTM, TP +300%, key
`27110c9ae9e5a519d142b9365717c2bab442c1357d7b1708f5879763a195b018`—had validation
returns +1.41%, +7.85%, −20.56%, and −15.70%, with minimum validation Sortino −2.92.

Attempt 2 is **KILL**. The single binding gate remains cross-fold minimum validation Sortino, and the
−60.91% May OOS / 70.48% drawdown independently forbids promotion. The daily bearish put gate made
July more convex but removed useful June put participation and did not control May. The failed
strike-distance gene-intent preview produced no study and no evaluations; it is another reproduction
of the already-open compiler-path bug.

F2 attempt 3 returns to the attempt-1 put logic and changes only put timing: wait until minute 60–150
instead of minute 15–60. Event attribution shows the weak put entries clustered in the opening hour
and were generally held into closing losses; delaying requires downside persistence before buying
puts while preserving both directions and the same intraday-flat risk mandate.

Clean seed `6a5de7f5814d31180a1c5a2a` passed `build_portfolio`, persistence audit, and
`get_sweep_surface`; every entry is still one long leg and one contract with approval off. Exploratory
full-period backtest `6a5de809ea0d6db55c696796` returned +98.59%, Sortino 3.02, and max drawdown
53.73%; this is search evidence only and is not a certification result. The qualifying preview again
compiled 27 cells, four anchored folds, 112 units, 165.95 tokens, and no gene warnings. Study
`6a5de8ad814d31180a1c5a93` / root optimizer `6a5de8ae814d31180a1c5a97` completed 112/112 units.

#### F2 certification attempt 3 — terminal result

Study `6a5de8ad814d31180a1c5a93` completed 112/112 units. OOS returns were −10.76%, −27.94%,
+75.71%, and +68.71%; OOS Sortinos were −3.49, −6.91, +9.69, and +12.75. The dominant fold
candidate was stable in the first three folds, but three folds were explicitly uncertified. The
cross-fold robust key `46ba10f9010eeef3a4e8890afe5f4302537da3a504854959e77aadc4fdbdeb57`
had validation returns −0.63%, −11.85%, −36.29%, and −61.26%, with minimum Sortino −3.32.

Attempt 3 is **KILL** on cross-fold minimum validation Sortino. F2 is exhausted after three coherent
fresh certifications. It demonstrates the desired June/July convexity but cannot survive the earlier
regimes; this is a local family result, not a campaign-level impossibility claim.

### F4 certification attempt 1 — persistent daily regime, affordable convexity

F4 removes the five-minute shock-cross trigger. Calls require one-day ROC > +5% and price above VWAP;
puts require one-day ROC < −5% and price below VWAP; both enter only at minute 60–150 and retain the
global one-position gate and minute-360 flatten. Event attribution on the initial 15% OTM structure
showed puts net positive but SNDK calls swinging roughly −$1,866 to +$2,936 per trade—too large for
an $8,000 account.

Fresh affordability screening found 3–10 DTE / 25% OTM seed `6a5ded802ee25ecab46bd968` at +45.40%,
Sortino 3.11, and max drawdown 26.85% over the exploratory full period. Same-day 25/35/50% OTM
variants all lost money; 3–10 DTE at 35/50% OTM returned only +3.54%/−10.35%. F4 therefore promotes
the affordable neighborhood, not those points.

The qualifying preview compiled DTE 3–10/10–21/21–45 × strike 20/25/30% OTM × TP 75/150/300:
27 cells, four anchored folds, 112 units, 165.95 tokens, no warnings. Study
`6a5dee5bea0d6db55c696d7b` / root optimizer `6a5dee5bea0d6db55c696d7f` completed 112/112 units.

#### F4 certification attempt 1 — terminal result

OOS returns were −5.19%, 0.00%, 0.00%, and +25.01%. All four folds were uncertified, and the
cross-fold robust candidate had minimum validation Sortino −4.13. The persistent ±5% daily regime
was too sparse outside the final bull window. A coherent threshold-3% refinement was screened as a
new artifact (`6a5df0092ee25ecab46bdb20`); its fresh exploratory full backtest
`6a5df014814d31180a1c5fe0` returned only +7.46%, Sortino 0.68, and maxDD 38.34%, so it was rejected
at search rather than spending a certification touch. F4 is a local mechanism rejection.

### Additional distinct-family search rejections

- F5 normalized opening-drive continuation: +0.5% from open lost 62.67% with 74.24% drawdown;
  +1% lost 3.12% with 11.66% drawdown; +2% produced no trades. The earlier raw
  `PriceChangeSinceOpen` screen was quarantined after its unit mismatch was identified.
- F6 daily mean reversion: the three coherent ROC/VWAP variants lost 42.83%, 23.36%, and 12.16%,
  with best drawdown still 29.94%. Rejected at search.
- F7 per-underlying independent slots (`6a5df2c0ea0d6db55c69709f`) lost 93.53% with 95.19%
  drawdown in fresh backtest `6a5df2d6ea0d6db55c6970ab`. The single global ticket is therefore a
  risk control, not merely a capital bottleneck.

### Fresh AA1 reconstruction — current leading candidate

The historical AA1 structure was rebuilt into new artifact `6a5df3f12ee25ecab46bde3f`; no old
backtest ID was reused. Persisted audit confirms four OpenOption entries: one single-leg outright-long
call and put on each of MU and SNDK, one contract each, exact 0–0 DTE, calls 4% OTM, puts 3% OTM,
global open-option count below one, and approval off on all seven strategies.

Fresh full-period current-engine backtest `6a5df4192ee25ecab46bde54` returned +347.80%, Sortino
6.84, and maxDD 22.38%. The separately rebuilt control returned +450.85%, Sortino 5.85, and maxDD
34.46%. AA1 therefore captures 77.14% of baseline return while improving Sortino and reducing
drawdown by 12.08 percentage points. This clears the campaign's alternate full-path search bar but
is not certified yet. Fixed-configuration walk-forward study `6a5df458814d31180a1c62ea` is the
next gate; no optimization is permitted until that exact structure's OOS behavior is known.

#### AA1 fixed-certification result and concentration rejection

Fixed study `6a5df458814d31180a1c62ea` completed 12/12 units. Validation was positive in all four
folds. OOS returns were +4.46%, −13.22%, +12.92%, and +231.80%, with median +8.69% and worst
drawdown 32.57%. Exact event replays matched every OOS economic statistic. The final OOS window,
however, contained a +$19,626.20 SNDK put; the other three OOS windows traded only MU. AA1 remains
useful as an overlay mechanism but is rejected as a standalone finalist because of name and
single-trade concentration.

### F8 and call-sleeve diagnostics

F8 combined 3–10 DTE impulse calls with positive-gap/VWAP-failure puts in clean portfolio
`6a5df609814d31180a1c63bd`. Fresh event backtest `6a5df61aea0d6db55c69744a` lost 88.13% with
90.21% drawdown. F8 is exhausted locally.

Four clean call-only diagnostic artifacts isolated 0DTE/3–10 DTE and impulse/persistent entries.
Their full returns were −22.07%, −45.34%, −27.63%, and −86.38%. This proved that the earlier
positive observed call attribution was selection-by-competition from puts occupying the global
ticket, not durable standalone call alpha.

### F9 regime-aligned VWAP re-entry

F9 replaced five-minute shock entries with daily-regime VWAP re-entry: calls require one-day ROC
above +1% and a cross above VWAP; puts require one-day ROC below −1% and a cross below VWAP.
The 0DTE seed `6a5df758814d31180a1c64c2` returned +238.14%, Sortino 4.41, maxDD 46.29%; the
3–10 DTE seed `6a5df75c2ee25ecab46be011` returned +191.05% with disqualifying 57.09% drawdown.

Full event run `6a5df790814d31180a1c64e6` showed calls lost $1,513.99 combined, while one July 2
SNDK put earned $19,766.20. A bounded near-ATM 0DTE/1DTE surface and four direction-specific
call/put strike cells did not improve the frontier: the highest return, +318.85%, carried 81.18%
drawdown; the lowest-risk tested refinement still had only +177.29% return and 45.50% drawdown.
F9 is exhausted locally.

## Certified finalist — 80% MU/SNDK core plus intraday AA1 overlay

The winning architecture preserves the thesis exposure instead of forcing intraday options to
replace overnight stock gains. Portfolio `6a5df976ea0d6db55c697601` buys 40% MU and 40% SNDK
fractional-share cores and reserves 20% initial cash for the AA1 overlay. The overlay contains exactly
four OpenOption entries: one single-leg outright-long 0DTE call and put for each name, one contract,
global open-option count below one, TP +100%, SL −50%, and minute-360 flatten. All nine strategies
have `automaticOrderApproval:false`; no spread or short leg exists.

Fresh continuous event backtest `6a5dfa70ea0d6db55c69766f` returned +717.73%, Sortino 8.65,
and maxDD 16.41%, versus +450.85%, Sortino 5.85, and maxDD 34.46% for newly rebuilt control
`6a5df3ed2ee25ecab46bde2f` / `6a5df416814d31180a1c62a2`. The 70% core sibling returned
+671.49% with 15.87% drawdown. The frozen 80% book was selected before certification.

Fixed-config walk-forward study `6a5df9f92ee25ecab46be1a5` completed 12/12 units with no
optimization. Validation returns were +63.56%, +148.77%, +141.77%, and +185.75%. OOS returns
were +45.97%, +4.29%, +27.22%, and +26.04%; median OOS was +26.63%, every OOS Sortino was
positive, worst OOS drawdown was 23.83%, both names participated in every fold, and no fold had an
unmet constraint. Matching stock-control OOS returns were +50.59%, +21.34%, +17.44%, and −16.40%,
so the finalist beat two of four and stayed positive in all four.

The full event ledger contains two stock fills and 19 complete option round trips (38 option fills).
Both names, calls, and puts filled. Option P/L was +$27,824.05: SNDK calls −$423.80, MU calls
−$845.65, MU puts +$156.20, and SNDK puts +$28,937.30. The largest trade was the July 2 SNDK
put at +$19,626.20. Removing that trade arithmetically lowers full return to approximately +472.40%,
still above the +450.85% control; removing the top three put wins lowers it below the control. This
concentration caveat is binding disclosure, not hidden by the headline.

After design freeze, the only untouched data available was July 13–17—far short of the required
126-day lockbox. Single-touch tail run `6a5dfab92ee25ecab46be1f3` returned +0.90% versus −16.60%
for control `6a5dfabe2ee25ecab46be1fb`, with a 31.00% versus 22.21% drawdown. The tail contained
one MU put round trip and no call fill. It is a useful fresh confirmation, **not** a formal lockbox.

### Final research verdict

**PASS as an outstanding research finalist; NOT DEPLOYED; NOT FORMAL-LOCKBOX CERTIFIED.** The
portfolio beats the fresh control by 266.88 percentage points on the continuous path, improves
Sortino by 2.80, and cuts drawdown by 18.05 points. Its fixed OOS path is positive in all four folds
and participates in both names. The solution is a hybrid: the stock core supplies persistent bull
exposure, while calls and puts remain intraday-flat. It is not a pure all-cash daytrading book, calls
were a small economic drag in the tested span, and option alpha is concentrated in SNDK puts. Those
limitations must be accepted explicitly before any later deploy authorization.

## Paper deployment

- Deployed from frozen chat finalist `6a5df976ea0d6db55c697601` through the paper-only deploy path.
- New active paper portfolio ID: `6a5e1f9d814d31180a1c8768`.
- Initial value/cash/buying power: $8,000; no initial positions or manual reconciliation orders were
  created during deployment.
- `get_portfolio` verifies all nine deployed strategies, real strategy IDs, exact conditions/actions,
  four one-leg outright-long 0DTE call/put entries, and `automaticOrderApproval:false` throughout.
- Read-only reconcile preview produced the expected single-tick core target: buy 3.642448 MU and
  2.296755 SNDK for an estimated $6,400 debit, leaving 20% cash. No reconcile orders were created;
  a subsequent `get_portfolio` still showed $8,000 cash and no positions.
- `fetch_portfolios` corrupts only the compact strategy summaries into blank IDs and ` when condition`
  names; see `FETCH_PORTFOLIOS_DEPLOYED_STRATEGY_SERIALIZATION_BUG.md`. The full persisted record is
  intact, so this is logged as an observability/serialization issue rather than deployment failure.
