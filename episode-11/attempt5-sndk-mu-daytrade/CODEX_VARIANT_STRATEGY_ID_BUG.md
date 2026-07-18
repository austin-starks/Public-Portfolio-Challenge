# Diagnose: portfolio variant persists blank strategy IDs

## One-line

`create_portfolio_variant` validated and persisted a six-strategy 0DTE portfolio, but every strategy was returned with an empty `strategyId`, preventing safe strategy-level edits and making the variant unsuitable as a deploy source.

## Expected vs observed

- **Expected:** A successfully persisted portfolio variant should assign a non-empty strategy ID to each copied strategy, matching the behavior of structured `create_portfolio`.
- **Observed:** Variant C2 `6a5b2e05595ed3a6ef3b3ea7` returned six strategies with `strategyId: ""` through `fetch_portfolios`, even though the variant response reported `validation: ok`. A later attempt to replace the misleading close-strategy label could not resolve a target strategy ID.

## Reproduction

- Source portfolio: `6a5a825ed6bfadbd6146935d` (`CODEX SNDK + MU 0DTE Two-Sided Momentum C1`; six strategies with real IDs).
- Dry-run patch: replace `/strategies/4/action/triggers/0/minPnlPercent` from 100 to 250 and remove `/strategies/4/action/triggers/1`; result `validation: ok`.
- Persisted variant: `6a5b2e05595ed3a6ef3b3ea7`; result `validation: ok`.
- Read-back: `fetch_portfolios` returned `strategyId: ""` for all six strategies.
- Control: the same finished strategy objects passed through `build_portfolio` and structured `create_portfolio` as C3 `6a5b2e63595ed3a6ef3b3ede`; the builder generated real strategy IDs.

## Leading hypothesis (verify, don't assume)

**Hypothesis:** the variant persistence path deep-copies canonical strategies after stripping `_id`, but does not run the same strategy-ID assignment step used by structured portfolio creation.

## Alternatives to rule out

1. **Read-model omission.** The IDs might exist in storage but be omitted by `fetch_portfolios`. Against this: `get_portfolio` and `conditionFieldAudit` also omitted strategy IDs for C2, and `replaceStrategy` could not be constructed from any returned identifier.
2. **By design for chat variants.** Against this: source C1 and canonical chat portfolio C3 both expose non-empty strategy IDs, so blank IDs are not normal for chat portfolios.

## Where to look

- The `create_portfolio_variant` persistence step after RFC6902 patch application.
- The canonical strategy normalization/ID assignment shared by `build_portfolio` and `create_portfolio` but apparently skipped by the variant path.
- The `fetch_portfolios` projection as a secondary check.

## Diagnostic checks

1. Create a one-strategy variant with a no-op name-only change and assert the persisted strategy ID is non-empty.
2. A/B the same source through `create_portfolio_variant` and structured `create_portfolio`; compare stored strategy IDs and `conditionFieldAudit.strategyId`.
3. Confirm that `replaceStrategy` works immediately on the newly created variant without an alternate lookup path.

## Impact on prior results

C2 and minute backtest `6a5b2e185e9beacc0a1765bf` are quarantined. The config was rebuilt as canonical C3 `6a5b2e63595ed3a6ef3b3ede`, and all conclusions must use C3 plus its independent minute backtest `6a5b2e6b595ed3a6ef3b3eef`. No earlier Episode 10/11 campaign result is invalidated by this issue.
