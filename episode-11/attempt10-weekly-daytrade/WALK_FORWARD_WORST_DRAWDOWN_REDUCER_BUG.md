# Diagnose: walk-forward aggregate worst drawdown selects the best fold

## One-line

Current walk-forward studies report `aggregate.oosMaxDrawdown.worst` as the minimum per-fold
drawdown instead of the maximum, materially understating worst-fold risk.

## Expected vs observed

- **Expected:** `worst = max(perFold)` because max drawdown is a positive loss magnitude.
- **Observed:** S0 study `6a63a060e490b0ae31ed3517` had per-fold values
  `[4.1359%, 4.2598%]` but reported `worst: 4.1359%`. Candidate study
  `6a63a0da9925d1bb4e64d43c` had `[1.3638%, 9.7256%, 23.7808%, 15.7000%]` but
  reported `worst: 1.3638%`.

## Reproduction

- Portfolio: `6a63a0be9925d1bb4e64d409`.
- Study: `6a63a0da9925d1bb4e64d43c` — 2025-04-01 through 2026-01-15,
  initial value $8,000, four fixed-config minute folds.
- Read `aggregate.oosMaxDrawdown.perFold` and compare its maximum with `worst`.

## Leading hypothesis (verify, don't assume)

Hypothesis: the aggregate reducer uses a minimum comparator for max-drawdown magnitudes, possibly
reusing logic intended for signed returns.

## Alternatives to rule out

1. **Metric definition.** Per-fold max drawdowns are persisted as positive percentages, so the
   smallest value is unambiguously the least severe drawdown.
2. **By design.** A field named `worst` cannot reasonably mean the smallest positive loss magnitude.

## Where to look

- Walk-forward aggregate construction for `oosMaxDrawdown.worst`.
- Shared metric-direction metadata used by min/max reducers.

## Diagnostic checks

1. Assert `worst === Math.max(...perFold)` for positive max-drawdown magnitudes.
2. Add a fixture with per-fold values `[5, 20, 10]` and require `worst === 20`.

## Impact on prior results

Any verdict that quoted only `aggregate.oosMaxDrawdown.worst` may understate risk. Per-fold return
and drawdown values remain usable; until fixed, compute worst drawdown directly as
`max(perFoldOOSMaxDrawdown)`.

## 2026-07-24 post-fix verification

- Source fix: NexusTrade commit `4d8efc5aa2` changes both the TypeScript and Rust reducers to use
  the maximum per-fold drawdown magnitude.
- Focused source tests passed:
  - TypeScript: `test-walkForwardAggregate.ts` and `sweep.test.ts` — 46/46 tests.
  - Rust: `worst_oos_max_drawdown_is_largest_fold_magnitude` — 1/1 test.
- Fresh connected-service study: `6a63bb35eb51c44c87cf2b73`.
- Fresh fold drawdowns: `[6.2835109451%, 19.7949433201%]`.
- Fresh service output: `worst: 6.2835109451%`.
- Correct value: `19.7949433201%`.

**Status:** fixed and tested in source, but not verified in the connected research service. Stage S0
remains failed until a fresh service study returns `worst === max(perFold)`.

### Runtime diagnosis

- Second fresh connected-service study: `6a63bc48ed8ac595f3f10d98`.
- Fold drawdowns: `[2.0040685474%, 6.8470597277%]`.
- Service again reported `worst: 2.0040685474%`; correct is `6.8470597277%`.
- All `nexustrade-backtesting` and `nexustrade-optimizer` machines were pinned to image
  `deployment-01KYADD64CB7NCZ5A63PMV9DY9`
  (`sha256:a898cd58eeabc27589e580b0eb94f622de34173cf4a19973d18e1362fbe44ba5`).
- The image ULID timestamp is `2026-07-24T15:55:19.564Z`, about three hours before the fix commit
  at `2026-07-24T18:57:33Z`.

This proves the connected Rust workers have not received the source fix; it is not a flaky
reproduction.

## Post-deployment closure

- Deployed Rust image:
  `deployment-01KYAV33F5EZRYQ03MYQ197N71`
  (`sha256:fbe8d7f3f88524ffcd89841b52b6c6d272a6ee2f2202f243f2c74957696393c9`).
- Fresh fixed-book study `6a63c757a6248fba1267bf85` correctly reported
  `worst: 6.8470597277%` for fold drawdowns `[2.0040685474%, 6.8470597277%]`.
- Fresh typed-sweep study `6a63c7af1e2c5df8d028e807` correctly reported
  `worst: 19.7949433201%` for `[6.2835109451%, 19.7949433201%]`.

**Status:** CLOSED. The connected reducer now passes Stage S0.
