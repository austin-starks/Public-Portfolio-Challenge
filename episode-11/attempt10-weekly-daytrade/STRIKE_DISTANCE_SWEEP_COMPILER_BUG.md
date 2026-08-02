# Diagnose: sweep compiler emits NoChange for every strike-distance value

## One-line

The `systematic_sweep` gene compiler accepted explicit 0%, 3%, and 6% OTM strike-distance values
but emitted `NoChange` for every value, which would make the advertised strike grid
non-differentiating.

## Expected vs observed

- **Expected:** Three distinct `OptionLeg.StrikeDistance` mutations representing 0%, 3%, and 6% OTM.
- **Observed:** All requested values were labeled correctly but serialized with `"type": "NoChange"`.
  The preview reported three or four theoretical variants even though none would mutate the seed.

## Reproduction

- Portfolio: `6a63a3479925d1bb4e64d687` (MU/SNDK outright long calls and puts, $8,000 initial value).
- Tool: `systematic_sweep`, `preview_only: true`, Minute interval, 2025-04-01 through 2025-10-18.
- Reproduced with both:
  - `Strike distance percent OTM on all option legs: 0, 3, 6`
  - `Set every option leg strike distance to exactly 0 percent OTM, 3 percent OTM, or 6 percent OTM`

## Leading hypothesis (verify, don't assume)

Hypothesis: the Create Sweep Gene compiler lacks a numeric mutation representation for
`OptionLeg.StrikeDistance` and silently falls back to `NoChange` while retaining the requested
labels.

## Alternatives to rule out (so this isn't a false alarm)

1. **Selector semantics.** Confirm whether `OptionLeg` requires a selector narrower than `All`.
2. **Compound value type.** Strike distance may require a structured percent-distance value rather
   than `Numeric`; if so, compilation should reject the intent instead of emitting `NoChange`.

## Where to look

- Create Sweep Gene handling for `scope=OptionLeg`, `field=StrikeDistance`.
- Sweep validation that counts distinct mutations and planned evaluations.

## Diagnostic checks

1. Compile 0%, 3%, and 6% OTM and assert that all three values are mutating and distinct.
2. Materialize a three-cell test and verify each option leg's stored `strikeSelector.distance`.

## Impact on prior results (why this blocks conclusions)

Any sweep using this compiled strike-distance axis may report fake grid breadth and duplicate
backtests. No strike-distance result from this compiler path should support selection until the
materialized option-leg fields are verified. This campaign excluded the axis and substituted DTE,
entry cooldown, and take-profit.

## 2026-07-24 post-fix verification

- Source fix: NexusTrade commit `4d8efc5aa2` rejects all-`NoChange` strike axes and includes a
  publisher for the corrected Create Sweep Gene instructions.
- Focused TypeScript tests passed: 46/46 across `sweep.test.ts` and
  `test-walkForwardAggregate.ts`.
- The connected natural-language compiler still rejected the 0%/3%/6% intent because it emitted
  only `NoChange` values. The corrected prompt path is therefore not service-verified.
- The typed `sweep_config` path did pass:
  - Sweep `6a63bad571ca2cdf1a36d34c` completed 3/3 exhaustive evaluations.
  - Materialized portfolios `6a63bb0171ca2cdf1a36d35e`,
    `6a63bb0171ca2cdf1a36d361`, and `6a63bb0171ca2cdf1a36d364`.
  - Field-level inspection showed every MU/SNDK call and put leg at exactly 0%, 6%, and 3% OTM,
    respectively.

**Status:** typed runtime mutation verified; natural-language compiler remains stale in the
connected service. Strike-aware research may use only the explicit typed config and must verify
materialized fields.

### Runtime diagnosis

- A second compiler retest again rejected the intent after producing only `NoChange` values.
- The connected `nexustrade-web` and `nexustrade-workers` fleets were running Git-tagged image
  `bf7f147efc`, which precedes source fix commit `4d8efc5aa2`.
- The corrected production prompt/schema publisher is
  `server/src/scripts/agent/publishSweepGeneHardening.ts`; it is dry-run by default and requires
  explicit `--run` to write NexusGenAI production.

The remaining gap is deployment/prompt publication, not the typed mutation engine.

## Post-deployment status

- TypeScript web and workers are deployed at `a54fc9e9bb`.
- The natural-language compiler still emits an all-`NoChange` strike axis, proving the production
  prompt/schema publisher was not run or did not take effect.
- The explicit typed `sweep_config` path remains verified before and after deployment, including
  real 0%, 3%, and 6% materialized selectors.

**Status:** natural-language convenience path OPEN; typed strike research path PASS. The campaign
uses only typed strike configs and performs field-level winner verification.
