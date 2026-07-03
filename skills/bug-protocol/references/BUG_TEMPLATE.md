# Diagnose: <one-line bug title — component + suspected wrong behavior>

## One-line
<Single sentence: what happened, the magnitude, and why it matters if the suspected behavior is real.
State the leading suspect if one already stands out (e.g. "likely emerged with the recent X change").>

## Expected vs observed
- **Expected:** <what the config/contract says should happen, with the numeric target derived from the
  config — e.g. "deployed premium ≤ totalBudget (40% of NAV ≈ $11.6k on a $29k book)">
- **Observed:** <what actually happened, with hard numbers and why it's not explainable by normal drift
  — e.g. "10 opens across 3 days totaling ~$27.8k ≈ 96% of NAV; freshly opened, so cost-basis
  over-deployment, not mark-to-market">

## Reproduction
- Portfolio: `<id>` (<one-line config: structure, budget, per-name, universe, TP>).
- Backtest / study: `<id>` — <window>, `initial_value` <X>, <flags e.g. generate_events>.
- <The specific rows/events/fills that show the bug, with dates and dollar amounts.>

## Leading hypothesis (verify, don't assume)
<The mechanism you believe is wrong, labeled as a hypothesis. Name the prime suspect code path.
Include any supporting signal — e.g. "the same book PRE-change sat at median deployment 47%, so the
jump coincides with change Y.">

## Alternatives to rule out (so this isn't a false alarm)
1. **Metric definition.** <Could the "wrong" number be correct under a different definition, e.g.
   market value vs cost basis? Argue for/against.>
2. **By design.** <Could this be intended behavior that's merely undocumented / non-differentiating?
   If so, what should be documented?>

## Where to look
- <The specific accounting/loop/field the maintainer should inspect first.>
- <The second-most-likely location.>

## Diagnostic checks
1. <A minimal single-tick assertion that would confirm/deny — e.g. "assert Σ entry premium ≤ 0.40×NAV
   on the first rebalance">.
2. <A multi-tick or A/B check that isolates the suspected cause (flag off vs on, same seed/window).>

## Impact on prior results (why this blocks conclusions)
<Which prior backtests/studies are now suspect, in which direction they're biased (returns and/or
drawdowns inflated/deflated), which sweep genes may be non-differentiating, and what must be re-run
after the fix.>
