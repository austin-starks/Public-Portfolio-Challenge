# Resolved diagnosis: sweep preview stamps MU, runtime late-binds each OpenOption underlying

## One-line

An F2 systematic-sweep preview compiled a requested per-strategy underlying gap filter into
`Abs(MU Gap Percentage)` under selector `All`, which looks cross-bound in the preview but is safely
late-bound to each fixed-underlying OpenOption strategy during Rust materialization.

## Expected vs observed

- **Expected:** each OpenOption strategy's added normalized gap filter binds to that strategy's own
  `builder.underlyingSymbol`: MU for MU calls/puts and SNDK for SNDK calls/puts.
- **Observed in preview:** both `Gap <= 2%` and `Gap <= 4%` gene values contain a shared condition
  whose `GapPercentage.targetAsset.symbol` is `MU`; the gene selector is `All`.
- **Observed in runtime code:** `apply_condition_to_matching_strategies` resolves an asset separately
  from each action via `action_condition_asset`; fixed-underlying OpenOption actions return their own
  `builder.underlying_symbol`. `PartialCondition::to_condition` then calls `Condition::with_asset`.
  That recursively reaches `AbsoluteValue`, then its child `GapPercentage`, whose `with_asset` arm
  overwrites `target_asset`. MU strategies therefore bind MU and SNDK strategies bind SNDK.

## Reproduction

- Portfolio: `6a5cf368392c6f50da48e7d6` (F2 put-first shock / delayed-call continuation; four outright-long
  MU/SNDK call/put entries; 3–10 DTE; one contract; global ticket; intraday flat).
- Tool: `systematic_sweep` with `preview_only: true`, search window 2026-01-02 through 2026-04-30.
- Gene intent: apply to every OpenOption strategy `No extra filter`, own-underlying absolute
  `GapPercentage <= 2%`, or own-underlying absolute `GapPercentage <= 4%`.
- Compiled gene: `scope: Strategy`, `field: EntryCondition`, `selector: All`; both Condition values
  explicitly target MU. No evaluations were launched.

## Verified mechanism

Create Sweep Gene emits one shared condition and the LLM fill commonly stamps the first ticker. Rust
materialization intentionally treats that condition as a template and late-binds it per matching
fixed-underlying OpenOption strategy through `action_condition_asset → to_condition → with_asset`.

## Alternatives to rule out (so this isn't a false alarm)

1. **Display-only serialization.** Confirmed: runtime rebinding occurs even though the preview does
   not expose the late-bound result.
2. **By design.** Cross-asset filters are valid in general, but the user's intent explicitly requested
   each strategy's underlying. The compiler must either generate per-strategy genes or reject the
   intent rather than silently substitute a cross-asset filter.

## Remaining product issue

- Preview/rendering should communicate that the condition is a per-strategy late-bound template, or
  show a materialized example per matched strategy. The current preview looks unsafe and caused a
  false-positive campaign bug report.

## Diagnostic checks

1. Add a Rust regression that materializes one shared `AbsoluteValue(GapPercentage(MU))` condition
   across MU and SNDK OpenOption strategies and asserts required fields/targets are MU and SNDK.
2. Add preview metadata such as `assetBinding: perMatchedStrategy` and render the resolved targets.

## Impact on prior results (why this blocks conclusions)

No performance result was invalidated. Fixed-underlying OpenOption sweeps using this late-binding path
do not have cross-asset eligibility from the preview's stamped ticker. This report is closed as a
preview clarity/observability issue, not a runtime correctness bug.
