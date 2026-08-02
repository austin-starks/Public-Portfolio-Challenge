# SNDK/MU Weekly Options Daytrade — Deploy-Readiness Verdict

## Decision

**NO DEPLOY. No tested options-only family is eligible for a pristine holdout or live capital.**

This is not a claim that profitable SNDK/MU daytrading is mathematically impossible forever. It is
the narrower decision that a deploy-ready winner cannot be established from the currently available
data and engine:

1. Three distinct mechanism families completed mandatory systematic search and matched-calendar
   walk-forward certification.
2. Every family underperformed the same-$8,000 share benchmark in all four OOS folds.
3. The remaining two momentum attempts failed the search layer and were not promoted.
4. All available 2025-04-01 through 2026-07-17 history has already been inspected, so no sufficiently
   long, globally pristine single-touch lockbox remains.

## Fixed contract

- Initial value: **$8,000** for strategy and benchmark.
- Strategy instruments: MU and SNDK options only.
- Allowed exposure: outright long calls and outright long puts.
- No stock actions, short option legs, or overnight holdings.
- Engine interval: Minute.
- Transaction fee: engine default option fee of $0.65 per contract.
- Benchmark: 50/50 MU/SNDK buy-and-hold shares, same initial value.

## Mandatory search ledger

| Family / attempt | Seed | Search | Result |
|---|---|---|---|
| Directional momentum | `6a63a3479925d1bb4e64d687` | `6a63a8e937f23e31d00b2f17` | KILL — 0/27 variants positive in both active train and validation windows |
| Mean reversion | `6a63a94d8b861d24bd40dba5` | `6a63a9a98b861d24bd40dc02` | KILL — all seven nonnegative-both rows were zero-trade artifacts |
| Long volatility | `6a63a9758b861d24bd40dbc2` | `6a63a9a337f23e31d00b2fc3` | PROMOTE to cert only — best stable row +0.04% train / +1.17% validation but below Sortino floor |
| Momentum attempt 2: opening range | `6a63abd28b861d24bd40e10a` | `6a63abfa37f23e31d00b351c` | KILL — 0/27 variants profitable in validation |
| Momentum attempt 3: prior-day trend | `6a63acce37f23e31d00b3607` | `6a63acef8b861d24bd40e2f5` | KILL — every active variant failed at least one split |

Every systematic search used the same 27-cell grid:

- DTE bracket: 0-0, 1-3, 4-7
- Entry cooldown: 0, 1, 3 days
- Take-profit: 75%, 150%, 250%

The strike-distance axis was excluded because the compiler emitted `NoChange` for every requested
value; see `STRIKE_DISTANCE_SWEEP_COMPILER_BUG.md`.

## Matched-calendar OOS verdict

OOS windows:

1. 2025-07-21 through 2025-09-04
2. 2025-09-04 through 2025-10-19
3. 2025-10-19 through 2025-12-03
4. 2025-12-03 through 2026-01-17

| Family | Study | OOS returns by fold | Mean OOS | Mean Sortino | True worst DD | Versus shares |
|---|---|---:|---:|---:|---:|---|
| Directional momentum | `6a63aa2d8b861d24bd40dc95` | +0.25%, -2.56%, +0.44%, -1.10% | -0.75% | -1.78 | 8.71% | Lost 4/4 |
| Mean reversion | `6a63aab98b861d24bd40deb7` | -0.46%, -1.84%, -4.38%, +3.37% | -0.82% | -2.50 | 9.66% | Lost 4/4 |
| Long volatility | `6a63aab437f23e31d00b3331` | -2.73%, -1.73%, -0.27%, -5.39% | -2.53% | -2.21 | 14.73% | Lost 4/4 |
| 50/50 MU/SNDK shares | `6a63ab4f2c927d110892567f` | +16.25%, +112.35%, +26.99%, +81.71% | +59.32% | +7.54 | 31.08% | Benchmark |

The engine's known `oosMaxDrawdown.worst` reducer reports the minimum fold drawdown. “True worst
DD” above is calculated as `max(perFold)` rather than trusting that field.

## Certification gates

- **Return floor:** FAIL for all three families on mean OOS return.
- **Sortino floor (>= 0.5):** FAIL for all three families.
- **Benchmark outperformance:** FAIL in 12/12 family-fold comparisons.
- **Cross-fold stability:** FAIL; `winnerStableAcrossFolds` was false for every family.
- **Selection floors:** momentum missed in 4/4 folds; mean reversion in 3/4; long volatility in 3/4.
- **Breadth:** OOS selected variants generally traded both names, so breadth does not rescue the
  failed return and benchmark gates.
- **Pristine lockbox:** NOT AVAILABLE. The previously favorable 2026 tail was already inspected and
  is quarantined; using it again would be data reuse, not certification.

## What would be required before deployment

A future candidate must be frozen before new data arrives, paper-observed without parameter changes,
and then evaluated once on a sufficiently long untouched forward window. It must beat the same-$8,000
50/50 share benchmark, post nonnegative returns and Sortino >= 0.5 in every required gate, trade both
underlyings, remain intraday-only, and reproduce exactly. Until then, creating live orders would not
be evidence-based deployment.
