# Diagnose: RebalanceOption `totalBudget` may not cap cumulative deployment

## One-line
A RebalanceOption strategy with `totalBudget = 40% of portfolio` deployed **~96% of NAV in option
premium at cold start (over 3 daily rebalance ticks)**. If `totalBudget` is meant to cap deployed
capital, this is a bug — and it likely emerged with the recent **affordability-backfill** change.

## Expected vs observed
- **Expected:** at each rebalance, total *new + existing* option premium deployed should not exceed
  `totalBudget` (40% of NAV ≈ $11.6k on a $29k book). Per-name is `12% of portfolio`.
- **Observed (cold start, $29k):** 10 long-call positions opened across 3 consecutive days totaling
  **~$27.8k entry premium ≈ 96% of NAV** — ~2.4× the 40% cap. These are freshly opened (no time to
  appreciate), so this is **cost-basis over-deployment, not mark-to-market drift.**

## Reproduction
- Portfolio: `6a450132bcd19f94d5aaba82` (RebalanceOption, `totalBudget` 40% of portfolio,
  `perNameAllocation` 12% of portfolio, 21-name universe, 7-rung deep-OTM LEAP ladder, TP +250%).
- Backtest: `6a454fb583e9fc112c231a19` — 2026-06-24→2026-07-01, `initial_value` 29000, `generate_events`.
- Filled opens (premium = price×100):
  - 6/24: OSCR 3×$11.11=$3,333 · OKTA $3,030 · DUOL $3,096 · HOOD $2,939  (day total ≈ $12.4k ≈ 43% NAV)
  - 6/25: ANET $3,143 · NET $3,333 · XOM $2,107 · GLD $2,941            (day total ≈ $11.5k)
  - 6/26: AVGO $2,904 · COP $983                                        (day total ≈ $3.9k)
  - **Sum ≈ $27.8k / $29k ≈ 96%.**

## Leading hypothesis (verify, don't assume)
Each **daily rebalance tick deploys ~40% of NAV again without subtracting already-open option
exposure**, so deployment stacks past the cap. Prime suspect: the **backfill loop** (new: "if a name
can't afford 1 contract, advance to the next ranked name") — it may size successive names against a
*fresh* 40% budget rather than **decrementing the remaining budget as each fill is committed**.
Supporting signal: the SAME book PRE-backfill (`6a45013c`, 10-wk, $29k) sat at **median deployment 47% /
max 59%** — i.e., budget looked roughly respected before the change; the jump to ~96% coincides with
backfill.

## Alternatives to rule out (so this isn't a false alarm)
1. **Metric definition.** If "deployment" = position *market value* / NAV, values >40% are expected as
   LEAPs appreciate and would NOT be a bug. — Argued against here because the 96% is *entry cost within
   3 days*, before any appreciation.
2. **By design.** If `totalBudget` is intended as *per-tick new-money* (not a standing exposure cap),
   then daily stacking is "working as designed" — but then the 40/60/80 budget gene is nearly
   non-differentiating and should be documented as such.

## Where to look
- The RebalanceOption budget accounting: does it compute `remainingBudget = totalBudget − currentOpenOptionCost`
  before sizing, and does it **decrement `remainingBudget` after each fill within a single rebalance pass**?
- The **backfill loop** specifically: when it skips an unaffordable name and moves to the next, does it
  carry the running spent/remaining tally, or re-read the full 40%?
- Whether the budget check uses **gross NAV each tick** vs. cash/buying-power net of open positions.

## Diagnostic checks
1. Single-tick backtest ($X initial); assert `Σ entry premium ≤ 0.40 × NAV` on the first rebalance.
2. Multi-tick: confirm whether deployment monotonically stacks each tick (points to per-tick reset).
3. A/B the backfill flag off vs on, same seed/window; compare peak entry-cost deployment.

## Impact on prior results (why this blocks conclusions)
If confirmed, all Ep-11/attempt2 backtests + sweeps ran at **higher-than-configured leverage** →
**returns and drawdowns both inflated**, and the `totalBudget` sweep gene is likely non-differentiating.
The OOS certs (Option 2 12%, full sweep, SelectTop sweep) should be **re-validated after the fix**.
