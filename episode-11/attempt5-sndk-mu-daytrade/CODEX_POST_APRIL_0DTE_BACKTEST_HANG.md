# Diagnose: post-April 2026 expiration-day 0DTE minute prep is extremely slow and opaque

> **Classification note:** Episode 11 Attempt 3 previously proved a similar apparent "hang" was active multi-GiB feeder preparation, not a dead worker. Without worker logs, the current jobs must be treated as slow/opaque rather than declared dead. The actionable defect is the lack of phase/progress visibility; the sharp expiration-day slowdown remains a performance issue to profile.

## One-line

Corrected explicit-contract 0DTE books complete January–April 2026 minute backtests in roughly 5–15 seconds, but jobs touching June/July 2026 expiration sessions remain `RUNNING` for minutes, including one-week partitions, with no phase or progress field.

## Expected vs observed

- **Expected:** Runtime should scale roughly with the number of minute bars. A one-week run should finish faster than a four-month run with the same portfolio.
- **Observed:** Four-month search runs repeatedly completed in about five seconds. Full/late corrected option runs remained running for 10–26+ minutes. Seven one-week N5 partitions were all still running after 25–40 seconds at their first poll. The matched stock-only baseline completed immediately.

## Reproduction

Portfolio N5 `6a5badb4075cfa92d0b24254` uses an 80% MU/SNDK stock core and four explicit-contract 0DTE entries.

- Control: 2026-01-02 through 2026-04-30, backtest `6a5badcb595ed3a6ef3be774`, COMPLETE in ~5.05 seconds.
- Lockbox with events: 2026-06-01 through 2026-07-17, `6a5bae07075cfa92d0b242ed`, still RUNNING after 110 seconds at the recorded poll.
- Lockbox without events: same dates, `6a5bae85075cfa92d0b24555`, still RUNNING after the initial poll.
- Stock-only matched baseline: `6a5badff075cfa92d0b242b0`, COMPLETE immediately.

Weekly partitions, all fixed N5 config:

| Window | Backtest |
|---|---|
| 2026-06-01→06-05 | `6a5baeac075cfa92d0b2457c` |
| 2026-06-08→06-12 | `6a5baeb0595ed3a6ef3bea7e` |
| 2026-06-15→06-19 | `6a5baeb3075cfa92d0b24581` |
| 2026-06-22→06-26 | `6a5baeb6595ed3a6ef3bea83` |
| 2026-06-29→07-02 | `6a5baebc595ed3a6ef3bea9a` |
| 2026-07-06→07-10 | `6a5baec15e9beacc0a181f1d` |
| 2026-07-13→07-17 | `6a5baec4595ed3a6ef3bebe2` |

## Scope

The slowdown is isolated to option data preparation/resolution: the same-date equity baseline is fast. It is not caused only by event generation because the non-event lockbox is also slow. May alone can complete quickly (`6a5ba9885e9beacc0a181184`, ~5.05 seconds), narrowing the suspect boundary toward June 2026 option-chain data volume or its storage path.

## Leading hypotheses — verify, do not assume

1. The June/July chain surface contains much more intraday contract data and triggers an unindexed resolution scan per minute.
2. A post-May expiration-calendar/data anomaly causes repeated resolver retries or a large rejection loop.
3. Recent-date data takes a different hot/cold storage path with pathological latency.

## Diagnostic checks

1. Profile one fixed strategy over 2026-05-29, 2026-06-01, and 2026-06-05 to find the first slow date.
2. Log resolver attempts, contracts scanned, query latency, and retry counts per underlying/minute.
3. Compare MU-only, SNDK-only, and stock-only versions over the same week.
4. Verify indexes used by expiration/DTE, underlying, timestamp, and strike-distance filters.
5. Add a runtime regression: a five-session run must not take longer than the four-month control by more than a declared tolerance.

### Boundary probe

- Monday 2026-06-01, N5 backtest `6a5baf99d91e1d54ae2b089f`: COMPLETE in roughly two wall-clock seconds; no option sells and 44 null-gated evaluations.
- Friday 2026-06-05, N5 backtest `6a5baf9d612dc791de158de4`: eventually COMPLETE after 276.90 reported seconds, +8.97%; it was still RUNNING after 25 seconds at the first substantive poll.

This sharply narrows the slowdown to sessions with a same-day expiration/chain rather than June market bars generally. It also confirms the worker is progressing, consistent with Attempt 3's multi-GiB-prep diagnosis. Prioritize contract resolution and historical quote lookup on expiration sessions, and expose prep bytes/files completed so callers can distinguish slow progress from a dead job.

## Campaign impact

The strategy remains frozen and jobs are allowed to finish; no result is inferred from runtime. Certification cannot complete until the lockbox returns metrics and its event audit proves true-0DTE calls/puts, quantities, costs, and fills.

## Additional hard failure — S3 NBBO decode

P9 fixed weekly diagnostic `6a5bcfb70a9bbbb42abde6c3` (2026-07-06 through 2026-07-10) failed after 155.75 seconds with the exact error:

```text
Backtest failed: nbbo batch 2026-07-10: External: Generic S3 error: error decoding response body
```

This is a platform/data-path failure before strategy statistics were produced. It must not be counted as a P9 PASS or FAIL. The identical frozen request may be retried once to distinguish a transient object-body/network decode from a deterministic corrupt NBBO batch. If it repeats, the Jul 6–10 slice is blocked pending inspection of the 2026-07-10 NBBO object, response headers/content encoding, checksum, and retry/error instrumentation. No alternative quote source or substitute date is authorized.

The one permitted identical retry, `6a5bd0d55dd431cc9fcc419f`, completed in 191.15 seconds and exactly matched the stock-only posture control at +1.45% return, 2.28 Sortino, and 14.68% maxDD. This makes the S3 decode error transient, but still actionable: the batch path needs bounded retry with object/key context and decode diagnostics so a temporary response-body failure does not fail the whole backtest after minutes of preparation.
