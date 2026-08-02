# Diagnose: option P/L close triggers do not bind despite threshold-crossing marks

## One-line

The Attempt 8 +150% take-profit and −42.5% stop-loss generated no paired exits in audited runs; a fresh
MU put marked far above +150% but remained open until the minute-300 flatten.

## Expected vs observed

- **Expected:** an open option closes when its P/L reaches +150% or −42.5%.
- **Observed:** in `6a5e41a3ca725b4a5d9cedef`, an MU put bought at $1.9125 was marked around
  $11.35 at the 15:00 history sample, yet it closed only at minute 300 for $9.625. Across the exact
  full event rerun `6a5e34ade52c3fd9a4c9c651`, every paired exit was attributed to the minute-300
  flatten, including trades with terminal returns beyond −42.5%.

## Reproduction

- Portfolio: `6a5e3103ca725b4a5d9cd55c`; TP +150%, SL −42.5%, flatten minute 300.
- Fresh holdout: `6a5e41a3ca725b4a5d9cedef`, 2026-07-13 through 2026-07-17, $8,000,
  minute interval, events enabled.
- Trade: `MU260715P00920000`, buy $1.9125 at 14:07Z; sampled position value $1,135 at 15:00Z;
  sell $9.625 at 18:31Z via strategy `6a5e3103ca725b4a5d9cd55b` (minute-300 flatten).

## Leading hypothesis (verify, don't assume)

Hypothesis: `CloseOption` P/L trigger evaluation is not receiving the same current option mark used by
portfolio history, or the trigger comparison is skipped until the unconditional flatten action runs.

## Alternatives to rule out (so this isn't a false alarm)

1. **Metric definition.** Confirm whether the trigger uses executable liquidation value rather than
   history mark. Even with a spread haircut, the sampled increase is far above +150%.
2. **By design.** Confirm whether action-level P/L triggers are evaluated only after a separate
   strategy condition changes. The persisted strategy condition is `always`, so that behavior would
   contradict the authored rule.

## Where to look

- `CloseOption` action trigger evaluation and its option-price source.
- Event-loop ordering between position marking, close evaluation, and order emission.

## Diagnostic checks

1. Replay the single MU trade and assert a close order is emitted on the first executable mark at or
   above 2.5 times entry premium.
2. Run the same trade with only the TP strategy active, then only the flatten strategy active, and
   compare close timestamps and evaluation rows.

## Impact on prior results (why this blocks conclusions)

The historical performance is effectively a minute-300 flatten strategy. TP/SL grid labels are not
validated risk controls, and any conclusions attributing robustness to those thresholds must be
quarantined until a minimal reproduction passes.
