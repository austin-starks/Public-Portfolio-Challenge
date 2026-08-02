# Diagnose: walk-forward aggregate selects the best drawdown as `worst`

## One-line

Study `6a5e340bca725b4a5d9cdbaf` reports 28.6113% as the worst OOS drawdown although one fold reached
39.0047%, understating the deploy-facing risk summary by 10.3934 percentage points.

## Expected vs observed

- **Expected:** `oosMaxDrawdown.worst` equals the maximum of the per-fold maximum-drawdown values:
  39.0047%.
- **Observed:** the field equals the minimum, 28.6113%.

## Reproduction

- Portfolio: `6a5e3103ca725b4a5d9cd55c`, Attempt 8 fixed options-only finalist.
- Study: `6a5e340bca725b4a5d9cdbaf`.
- Per-fold OOS maxDD: 28.6113%, 34.3711%, 39.0047%, 37.3025%.
- Standalone fold-0 replay: `6a5e421be52c3fd9a4c9daf1`, 28.6113%.
- Standalone fold-2 replay: `6a5e4221c0ccd58120258561`, 39.0047%.

## Leading hypothesis (verify, don't assume)

Hypothesis: the aggregate reducer uses `min` for both the favorable and adverse drawdown rollups, or
the display layer treats a numerically smaller drawdown as the worst observation.

## Alternatives to rule out (so this isn't a false alarm)

1. **Metric definition.** Per-fold fields are all positive maximum-drawdown magnitudes, so the largest
   value is the worst loss under the displayed definition.
2. **By design.** If `worst` intends “lowest numeric value,” the label is unsafe and contradicts the
   deploy-risk meaning used by certification.

## Where to look

- The walk-forward aggregate reducer that builds `oosMaxDrawdown`.
- The API serializer/display mapper for the `worst` field.

## Diagnostic checks

1. Assert `worst === Math.max(...perFold)` for positive drawdown magnitudes.
2. Add a fixture `[10, 40, 25]` and require `worst = 40`.

## Impact on prior results (why this blocks conclusions)

Per-fold statistics remain usable and were independently reproduced, but aggregate deploy summaries
may understate drawdown. Recompute the worst fold directly from `perFold` until the reducer is fixed.
