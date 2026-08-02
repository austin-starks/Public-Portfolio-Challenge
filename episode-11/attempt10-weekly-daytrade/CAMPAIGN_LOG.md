# CODEX Attempt 10 — SNDK/MU Weekly Options Daytrade

## Verdict

FAIL / QUARANTINED. This candidate is not eligible for deployment.

The 2026-01-16 through 2026-07-17 backtest beat an equal-weight MU/SNDK share buy-and-hold control
from the same $8,000 initial value, but that interval overlapped prior research and was not a
globally pristine holdout. More importantly, the exact fixed configuration underperformed the
same-capital share control in all four earlier walk-forward OOS folds. The favorable 2026 tail is
research evidence only and cannot override the failed multi-regime certification.

## Frozen contract

- Initial value: $8,000 for candidate and share control.
- Candidate assets: options on MU and SNDK only; no stock actions.
- Structures: one-leg, one-contract outright long calls and puts.
- Calls: nearest 1-7 DTE, 4% OTM.
- Puts: exact 0 DTE, 3% OTM.
- Entries: minutes 15-150; VWAP posture plus a 5-minute ROC cross at +/-0.75%.
- Calls additionally require 1-day ROC > 1%.
- Portfolio cap: fewer than two open option positions.
- Same-underlying cooldown: 360 minutes.
- Exits: +150% P/L, -42.5% P/L, or mandatory minute-300 flatten.
- Fees: engine default $0.65 per option contract.
- Candidate portfolio: `6a63a3479925d1bb4e64d687`.

## Engine sanity

- Current-engine S0 sweep study: `6a63a060e490b0ae31ed3517` — COMPLETE, 2/2 folds.
- Fold winners persisted as real chat portfolios.
- Standalone validation/OOS reruns matched the study statistics exactly.
- Dead-name probe: `6a63a0139925d1bb4e64d36a` — 2022 SNDK produced 0 trades,
  0 deployment, and no fabricated SNDK price exposure.
- Known reducer defect remains: `aggregate.oosMaxDrawdown.worst` selects the minimum fold drawdown.
  See `WALK_FORWARD_WORST_DRAWDOWN_REDUCER_BUG.md`.

## ⚠️ BUG/ISSUE — strike-distance sweep compiler

Two `systematic_sweep` previews on portfolio `6a63a3479925d1bb4e64d687` accepted explicit 0%, 3%,
and 6% OTM strike-distance values but compiled every value as `NoChange`. Affected strike-distance
sweeps are quarantined because their advertised variants may be duplicates. The active three-family
bakeoff excludes that axis. See `STRIKE_DISTANCE_SWEEP_COMPILER_BUG.md`.

## Search ledger

The following mechanisms failed and are not finalists:

- Time-flatten-only inherited momentum shape: walk-forward `6a63a0da9925d1bb4e64d43c`,
  mean OOS return -5.69%, profitable in 1/4 folds.
- Full exit-grid control: walk-forward `6a63a1418851af28134e05c2`,
  mean OOS return -3.34%, profitable in 2/4 folds.
- Put daily-trend-gate variants V1-V4: continuous returns ranged from -22.50% to -51.48%
  versus +520.21% for the same-$8k share control on 2025-04-01 through 2026-01-15.
- Weekly cadence/SMA regime variants W1-W6: continuous returns ranged from -16.14% to -51.66%
  on the same screen window.

The failed screens are search evidence only. They are included to document what was rejected, not
as OOS certification evidence.

## Quarantined same-capital tail comparison

Window: 2026-01-16 through 2026-07-17.

| Metric | Options finalist | 50/50 MU/SNDK shares |
|---|---:|---:|
| Backtest | `6a63a3618851af28134e0763` | `6a63a365e490b0ae31ed3712` |
| Return | +283.34% | +179.33% |
| Excess return | +104.01 pp | — |
| Sortino | 4.21 | 4.11 |
| Sharpe | 2.84 | 2.59 |
| Max drawdown | 40.67% | 37.94% |
| Fees | $146.90 | $7.99 |

Independent candidate rerun `6a63a4928851af28134e081c` was identical at
`tolerance_bps: 0`: same statistics and no tape divergence.

## Event and structure audit

- Event summary: 135,120 events and 226 filled option orders.
- SNDK: 58 buys and 58 sells; MU: 55 buys and 55 sells.
- All observed option orders had quantity 1 and `totalLegs: 1`.
- Raw fills contained both calls and puts.
- EOD posture had 0% deployment on all 155 observations.
- Parsed paired spread groups had 109 same-day round trips and 0 overnight round trips; the
  aggregate EOD posture independently confirms no overnight holdings.
- 14 limit opens expired unfilled; they were not counted as trades.
- The configuration contains no Buy/Sell stock action and no short option leg.

## Caveats

- Fixed-config walk-forward `6a63a1418851af28134e05c2` underperformed the equal-weight share
  control in 4/4 OOS folds. Candidate OOS returns were +0.04%, +6.44%, -10.48%, and -9.36%;
  corresponding share-control returns were +13.24%, +119.63%, +29.18%, and +67.18%.
- The tail was reserved from this attempt's walk-forward work, but earlier campaigns had inspected
  overlapping 2026 data. It is therefore not a globally pristine single-touch lockbox.
- SNDK option liquidity remains a material live risk. Backtest fills use engine execution and
  slippage assumptions; they are not brokerage fills.
- No portfolio was deployed and no brokerage order was created.

## Continued deploy-readiness bakeoff

The campaign continued after the false PASS was corrected. Three distinct options-only families each
completed a 27-cell systematic search and a four-fold matched-calendar sweep certification at the
fixed $8,000 capital base:

- Directional momentum study `6a63aa2d8b861d24bd40dc95`: mean OOS -0.75%, lost to shares 4/4.
- Mean reversion study `6a63aab98b861d24bd40deb7`: mean OOS -0.82%, lost to shares 4/4.
- Long volatility study `6a63aab437f23e31d00b3331`: mean OOS -2.53%, lost to shares 4/4.
- Same-calendar 50/50 MU/SNDK share benchmark `6a63ab4f2c927d110892567f`: mean OOS +59.32%.

Two further momentum attempts were killed at the search layer:

- Opening-range continuation search `6a63abfa37f23e31d00b351c`: 0/27 variants profitable in
  validation.
- Prior-day trend search `6a63acef8b861d24bd40e2f5`: every active variant failed at least one
  development split; the seven nonnegative-both rows were zero-trade artifacts.

The authoritative decision and per-fold table are in `DEPLOY_READINESS_VERDICT.md`.

## Post-fix Stage S0 retest

After NexusTrade commit `4d8efc5aa2`, the campaign reran the two reported defects:

- Typed strike sweep `6a63bad571ca2cdf1a36d34c` completed all three variants. Materialized
  portfolios were inspected at the option-leg field level and contained distinct 0%, 3%, and 6%
  OTM selectors across both calls and puts on both MU and SNDK.
- The natural-language strike compiler still emitted an all-`NoChange` axis and was rejected. Only
  the explicit typed sweep path is currently usable.
- Fresh two-fold study `6a63bb35eb51c44c87cf2b73` completed, but the connected service still
  reported the smaller drawdown as `aggregate.oosMaxDrawdown.worst`: 6.2835% instead of the correct
  19.7949%.
- Focused source regressions passed: 46/46 TypeScript tests and 1/1 Rust test.

The source is fixed, but the connected research service is not yet running the corrected aggregate.
Stage S0 therefore remains failed and all new certification work stays quarantined.

### Confirmed deployment gap

A second fresh study, `6a63bc48ed8ac595f3f10d98`, again selected the smaller fold drawdown:
2.0041% instead of 6.8471%. Read-only fleet inspection then identified the exact stale runtimes:

- Rust backtesting and optimizer fleets:
  `deployment-01KYADD64CB7NCZ5A63PMV9DY9`,
  digest `sha256:a898cd58eeabc27589e580b0eb94f622de34173cf4a19973d18e1362fbe44ba5`.
  Its build timestamp predates fix commit `4d8efc5aa2` by approximately three hours.
- TypeScript web and worker fleets: image tag `bf7f147efc`, also before `4d8efc5aa2`.

Required service remediation before Stage S0 can pass:

1. Green-gated Rust deployment (`make deploy-rust`).
2. Green-gated TypeScript deployment (`make deploy-ts`).
3. Publish the corrected sweep-gene production prompt/schema with
   `server/src/scripts/agent/publishSweepGeneHardening.ts --run`.
4. Rerun the natural-language strike preview and a fresh two-fold reducer study.

These production mutations were not performed by this campaign.

### Post-deployment Stage S0 result

The runtime deployment subsequently completed:

- TypeScript web/workers: `a54fc9e9bb`.
- Rust backtesting/optimizer:
  `deployment-01KYAV33F5EZRYQ03MYQ197N71`,
  digest `sha256:fbe8d7f3f88524ffcd89841b52b6c6d272a6ee2f2202f243f2c74957696393c9`.

Fresh reducer study `6a63c757a6248fba1267bf85` and fresh typed-sweep study
`6a63c7af1e2c5df8d028e807` both returned
`aggregate.oosMaxDrawdown.worst === max(perFold)`. The typed sweep completed 2/2 folds and
persisted real fold winners.

The production natural-language strike prompt remains stale, but the explicit typed config
continues to materialize verified 0%, 3%, and 6% selectors. Stage S0 is PASS for the typed research
path; every strike-aware search below must use that path.
