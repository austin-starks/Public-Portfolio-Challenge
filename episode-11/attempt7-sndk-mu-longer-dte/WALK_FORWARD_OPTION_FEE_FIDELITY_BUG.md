# Diagnose: walk-forward option fees diverge from standalone backtests

## Resolution status — 2026-07-20

**CLOSED by the shipped fee-contract fix.** Fresh study `6a5dc4c82ee25ecab46ba437`
completed both folds and persisted winners. Independent validation/OOS replays of both winners match
all economic statistics—including return, Sortino, drawdown, sold dollars, and fees—to full precision.
Only the diagnostic `nullGatedEvaluations` counter differs between fold execution and standalone
replay; fills and economics do not.

## One-line

The post-fix walk-forward path evaluates and materializes direct-OpenOption winners, but its fold
replays use the optimizer's default **0.3% of option notional** fee model while ordinary backtests use
**$0.65 per contract**; on fold 0 OOS this reports $435.09 instead of $18.20 in fees and changes the
$8,000 book's return from +49.2411% to +44.0301%, so walk-forward and standalone results are not
comparable.

## Expected vs observed

- **Expected:** replaying a fold's persisted `selectedChatPortfolioId` over the fold's exact date
  window, interval, $8,000 initial value, and empty initial positions should reproduce the fold's
  trades, fees, return, and drawdown within rounding tolerance.
- **Observed, fold 0 OOS (2026-06-01 through 2026-06-20):** the study reports +44.030125%, Sortino
  5.84947, max drawdown 58.3422%, and $435.09 fees. Standalone replay reports +49.24125%, Sortino
  6.19235, max drawdown 57.4278%, and $18.20 fees. `dollarsSold` ($76,142.50), average trade P&L,
  win rate, and profit factor match exactly. The $416.89 fee delta is exactly 5.211125% of the $8,000
  initial value, which exactly explains the return delta.
- **Observed, fold 0 validation (2026-05-02 through 2026-05-31):** the study reports -30.5589%,
  Sortino -2.50078, max drawdown 61.8762%, $46,642.50 sold, and $280.962 fees. Standalone replay
  reports -30.15125%, Sortino -2.28420, max drawdown 62.0773%, $50,357.50 sold, and $22.10 fees.
  Here the different fee drag also changes capital availability and the realized trade path.

## Reproduction

- Seed portfolio: `6a5cf368392c6f50da48e7d6` (`$8,000`; MU/SNDK; four outright-long,
  one-leg call/put entries; 3-10 DTE; one contract; intraday exits; no spreads; automatic approval
  off).
- Walk-forward study: `6a5da1d09dffb90d2c07de8a`; root sweep
  `6a5da1d09dffb90d2c07de8e`; Minute; global 2026-01-02 through 2026-07-10; two anchored folds;
  one exhaustive strike-distance gene (5%/10%/15% OTM).
- Fold 0 selected portfolio: `6a5da266627ac9b74ecee32f`; persisted with 5% OTM on all four legs
  and the expected $8,000 initial value.
- Standalone validation replay: `6a5da2749dffb90d2c07defb`.
- Standalone OOS replay: `6a5da27655ac577a49d1684a`.

## Leading hypothesis (verify, don't assume)

The two execution surfaces have incompatible default option fee contracts:

- `server/src/models/optimization/index.ts` initializes `Optimizer.feeConfig.Option` to
  `{ amount: 0.3, type: percent }`.
- `server/src/models/walkForward/rootOptimizerFactory.ts` creates the root optimizer without
  overriding that fee model.
- `app/src/model/optimizer/walk_forward/oos_promote.rs` passes `self.fee_config` into the fold
  training/validation/OOS backtest work.
- `app/src/model/fee_config/mod.rs` defines the ordinary `FeeConfig::default()` option fee as
  `$0.65 per contract`.

The OOS study fee also fingerprints the optimizer model: $435.09 / 0.003 = $145,030 of inferred
gross option turnover, plausible for the reported $76,142.50 of closing sales plus opening buys.

## Alternatives to rule out (so this isn't a false alarm)

1. **Different portfolio genome.** Ruled down: the fold persisted a real ChatPortfolio and direct
   inspection confirms all four legs use the selected 5% OTM value. The OOS sold dollars and
   trade-quality statistics match exactly.
2. **Date-boundary or warmup mismatch.** Ruled down for the OOS fee/return discrepancy by the exact
   match in sold dollars, average trade P&L, win rate, and profit factor. Date/state differences
   remain worth checking for the validation trade-path divergence after fee parity is restored.
3. **Intended optimizer conservatism.** If 0.3%-of-notional is intentional, it must be explicit in
   the study request/result and standalone replay must accept the same frozen fee config. A hidden
   surface-specific default cannot satisfy the S0 fidelity contract.

## Where to look

- Unify the option fee default at the TypeScript `Optimizer` / walk-forward root factory boundary,
  or persist an explicit study fee config and expose it in study results/materialized replays.
- Add a parity assertion around `promote_individual_oos_in_process` using the same persisted
  portfolio, window, initial capital, fee config, slippage config, and initial-position policy as
  ordinary `backtest_portfolio`.

## Diagnostic checks

1. Run the fold 0 OOS promotion and standalone replay with an explicitly identical fee config. Assert
   exact parity for `totalFees`, ending equity, percent change, filled contract count, and fill IDs.
2. A/B the current defaults on the same OOS window: 0.3%-of-notional should reproduce $435.09;
   $0.65-per-contract should reproduce $18.20. Then repeat validation and assert the trade paths also
   converge.

## Impact on prior results (why this blocks conclusions)

Old study `6a5da1d09dffb90d2c07de8a` remains a diagnostic artifact only. Its fold returns,
drawdowns, ranking, and selected genome are not certifiable because fee drag can change both scores
and whether this capital-constrained portfolio can open later trades. The pre-fix 0-evaluation sweep
IDs remain quarantined. After the fee contract is fixed, rerun Stage S0 from a new study ID, replay
every selected fold portfolio independently. That requirement passed in fresh study
`6a5dc4c82ee25ecab46ba437`; F2 systematic search may resume from new IDs.
