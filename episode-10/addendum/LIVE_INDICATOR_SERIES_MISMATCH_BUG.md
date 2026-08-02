# Investigate: live `100 Day SMA` / `63 Day ROC` do not reproduce from the EOD screener

**Found:** 2026-07-24

**Status:** open investigation; mismatch confirmed, root cause not confirmed

**Severity:** high for live-versus-backtest parity; no current exit decision changed

**Live portfolio:** `69a7dc7acdb6bf6a4681d36c` (`Public Portfolio Challenge`)

**Primary live event:** `2026-07-24T19:55:08.498Z`

## One-line summary

The deployed strategy engine and the SQL stock screener agree that none of the five current
underlyings should exit, but their numerical SMA100 and ROC63 values differ materially; more
importantly, consecutive live audits imply that the engine's reported `100 Day SMA` contains
exactly 213 effective samples, which is inconsistent with the expected 100 unique daily closes
unless the live contract intentionally averages multiple observations per day.

## What the strategy contract says

Each held ticker has a dedicated `CloseOption` strategy:

```text
underlying price < its 100 Day SimpleMovingAverage
AND
63 Day PriceRateOfChange < 0
```

Both predicates must be true. The relevant live strategy IDs are:

| Ticker | Strategy ID |
|---|---|
| COP | `6a63a9082c927d1108925211` |
| HOOD | `6a63a9072c927d11089251ee` |
| LLY | `6a63a9082c927d11089251f3` |
| OSCR | `6a63a9082c927d1108925216` |
| XOM | `6a63a9082c927d110892520c` |

The portfolio's `conditionFieldAudit` confirms `window.length: 100`, `interval: Day` for
`SimpleMovingAverage`, and `window.length: 63`, `interval: Day` for `PriceRateOfChange`.

## Expected versus observed

- **Expected:** the live evaluator and a point-in-time EOD reproduction should use a documented,
  reproducible daily price series. If `100 Day SMA` means the conventional 100-session SMA, it
  should average 100 unique session closes. ROC63 should compare the current/as-of price with the
  corresponding close 63 unique sessions earlier.
- **Observed:** the live engine and `financials.sec_stock_price_metrics` produce materially different
  SMA100 and ROC63 values. The live SMA also reacts to intraday price changes as though it averages
  213 observations.

The screener is one completed session behind the live event, so exact equality is not expected.
That timing difference does not explain the 213-sample response observed entirely within successive
live events.

## Reproduction A: authoritative live condition audit

Run:

```json
{
  "tool": "query_portfolio_events",
  "arguments": {
    "portfolio_id": "69a7dc7acdb6bf6a4681d36c",
    "start_date": "2026-07-24T19:54:30Z",
    "event_types": ["NoSignal"],
    "include_noise_events": true,
    "include_condition_audit": true,
    "collapse_repeats": false,
    "page": 1,
    "page_size": 10,
    "raw": false
  }
}
```

At `2026-07-24T19:55:08.498Z`, the engine recorded:

| Ticker | Live price | Live SMA100 | Live ROC63 | Price below SMA? | ROC negative? | Combined exit? |
|---|---:|---:|---:|---|---|---|
| COP | 120.0900 | 115.7131 | -0.3072% | no | yes | **no** |
| HOOD | 94.6300 | 91.3052 | 28.5035% | no | no | **no** |
| LLY | 1194.1650 | 1072.0626 | 12.1282% | no | no | **no** |
| OSCR | 28.1900 | 24.6745 | 24.5141% | no | no | **no** |
| XOM | 156.3450 | 147.2234 | 0.9198% | no | no | **no** |

This event is a valid engine audit, not an inferred calculation. It contains each base condition's
`lhsValue`, `rhsValue`, comparison, and `isTrue`.

## Reproduction B: completed-session SQL screener

The screener queried the latest completed session, `2026-07-23`, from
`financials.sec_stock_price_metrics`:

```sql
WITH LatestDate AS (
  SELECT MAX(date::DATE) AS max_date
  FROM financials.sec_stock_price_metrics
  WHERE ticker IN ('COP', 'HOOD', 'LLY', 'OSCR', 'XOM')
),
PriceHistory AS (
  SELECT
    p.ticker,
    p.date::DATE AS session_date,
    CAST(p.closingPrice AS DOUBLE) AS close,
    AVG(CAST(p.closingPrice AS DOUBLE)) OVER (
      PARTITION BY p.ticker
      ORDER BY p.date::DATE
      ROWS BETWEEN 99 PRECEDING AND CURRENT ROW
    ) AS sma100,
    LAG(CAST(p.closingPrice AS DOUBLE), 63) OVER (
      PARTITION BY p.ticker
      ORDER BY p.date::DATE
    ) AS close_63_ago,
    COUNT(*) OVER (
      PARTITION BY p.ticker
      ORDER BY p.date::DATE
      ROWS BETWEEN 99 PRECEDING AND CURRENT ROW
    ) AS history_depth
  FROM financials.sec_stock_price_metrics p
  WHERE p.ticker IN ('COP', 'HOOD', 'LLY', 'OSCR', 'XOM')
    AND p.date::DATE >= (SELECT max_date FROM LatestDate) - INTERVAL 200 DAY
)
SELECT
  ph.ticker,
  ph.session_date,
  ph.close,
  ph.sma100,
  ((ph.close - ph.sma100) / NULLIF(ph.sma100, 0)) * 100 AS pct_dist_sma100,
  ((ph.close / NULLIF(ph.close_63_ago, 0)) - 1) * 100 AS roc63_pct,
  (ph.close < ph.sma100) AS closeBelowSma100,
  (((ph.close / NULLIF(ph.close_63_ago, 0)) - 1) < 0) AS roc63Negative,
  (ph.close < ph.sma100
    AND ((ph.close / NULLIF(ph.close_63_ago, 0)) - 1) < 0) AS thesisExit
FROM PriceHistory ph
JOIN LatestDate ld ON ph.session_date = ld.max_date
WHERE ph.history_depth >= 100
ORDER BY ph.ticker ASC;
```

The screener returned:

| Ticker | EOD close | EOD SMA100 | EOD ROC63 | Combined exit? |
|---|---:|---:|---:|---|
| COP | 120.2000 | 118.4690 | -1.9576% | no |
| HOOD | 101.5800 | 85.7813 | 14.8705% | no |
| LLY | 1185.8700 | 1032.6883 | 28.6919% | no |
| OSCR | 28.9200 | 21.0984 | 75.9124% | no |
| XOM | 156.8900 | 150.6360 | 4.9431% | no |

## Cross-source magnitude

`Delta` below is live engine minus EOD screener. The dates differ by one session.

| Ticker | Live price delta | SMA delta | SMA delta | ROC delta |
|---|---:|---:|---:|---:|
| COP | -0.09% | -2.7559 | -2.33% | +1.65 pp |
| HOOD | -6.84% | +5.5240 | +6.44% | +13.63 pp |
| LLY | +0.70% | +39.3743 | +3.81% | -16.56 pp |
| OSCR | -2.52% | +3.5761 | +16.95% | -51.40 pp |
| XOM | -0.35% | -3.4126 | -2.27% | -4.02 pp |

The sources agree on the sign of ROC63 for all five names and agree that no combined exit is due.
They do not closely reproduce the numeric indicator values.

## Strongest diagnostic clue: the live SMA has an effective sample count of 213

The live evaluator emitted successive audits at `19:54:52` and `19:55:08`. Over those 16 seconds,
the historical window should be fixed; only the current live price changed.

For a simple arithmetic mean in which only one observation changes:

```text
delta SMA = delta current price / N
therefore N = delta current price / delta SMA
```

Applying that identity:

| Ticker | Price at 19:54:52 | Price at 19:55:08 | SMA at 19:54:52 | SMA at 19:55:08 | Implied N |
|---|---:|---:|---:|---:|---:|
| COP | 120.0600 | 120.0900 | 115.7130049 | 115.7131458 | 213.0000 |
| HOOD | 94.4800 | 94.6300 | 91.3045355 | 91.3052398 | 213.0000 |
| LLY | 1193.9200 | 1194.1650 | 1072.0614825 | 1072.0626328 | 213.0000 |
| OSCR | 28.1850 | 28.1900 | 24.6744601 | 24.6744836 | 213.0000 |
| XOM | 156.3300 | 156.3450 | 147.2232862 | 147.2233566 | 213.0000 |

The exact same `N = 213` across five unrelated tickers is unlikely to be market drift or rounding.
It strongly suggests a shared history-buffer/window implementation containing 213 effective
observations.

This does **not** by itself prove the engine is mathematically wrong. It could mean that `100 Day`
is implemented as a 100-calendar-day duration containing multiple samples per day. If so, that
contract must be made explicit, and live/backtest parity must be proven because a conventional
100-day SMA means 100 daily closes.

## Ranked hypotheses

### H1 — multiple observations per session enter the live `Day` window

**Likelihood: high.**

The live history builder may be passing every timestamp within a 100-day duration to an unweighted
mean instead of resampling to one close per market session. Duplicate hydration rows, intraday
snapshots, or multiple vendor partitions could produce approximately two observations per session.
The exact 213-sample response across all names is the strongest support.

### H2 — `window.length: 100, interval: Day` means a duration, not 100 daily bars

**Likelihood: high or equivalent to H1.**

The implementation may intentionally select all observations newer than `now - 100 days`.
If the source has multiple observations per day, the mean is internally consistent but the UI name
and backtest comparison are misleading. The investigator must establish the intended contract before
calling this a defect.

### H3 — live and screener use different price sources or adjustment policies

**Likelihood: medium-high.**

The screener uses `financials.sec_stock_price_metrics.closingPrice`. The live event embeds a
real-time `marketData.prices` value and may hydrate history from another table, cache, vendor, or
split-adjusted series. This can explain the cross-source level differences and ROC reference prices,
but not by itself the live `N = 213`.

### H4 — the current quote is appended repeatedly rather than replaced

**Likelihood: medium.**

A constant-frequency portfolio is evaluated repeatedly. If every evaluation appends a new live
observation to a shared historical array/cache, the buffer may accumulate duplicate current-session
points. Check whether the sample count grows during the session. A stable 213 over the sampled
events would favor a pre-existing multi-row history rather than unbounded accumulation.

### H5 — corporate-action adjustment differences

**Likelihood: low-to-medium.**

Adjusted versus unadjusted closes can materially alter long-window indicators. It is unlikely to
produce the same 213-sample response across every ticker, but it must be ruled out when comparing
the live source with `closingPrice`.

### H6 — the screener SQL is not actually one row per ticker/session

**Likelihood: low but easy to test.**

The SQL uses row windows. Duplicate `(ticker, date)` rows would make `ROWS BETWEEN 99 PRECEDING`
different from 100 unique sessions. Verify row uniqueness before treating the screener as the
canonical reproduction.

## Additional data-quality signal

The same live event formatter reported several `price_below_same_snapshot_low` or
`price_above_same_snapshot_high` warnings in embedded fundamentals. For example, OSCR's embedded
`closingPrice` was below the same snapshot's `lowestPrice`. These warnings may reflect asynchronously
assembled fields rather than the indicator history itself, but they strengthen the case for tracing
source provenance instead of assuming every embedded field belongs to one coherent market bar.

## Where to look first

1. The live indicator resolver for `SimpleMovingAverage` and `PriceRateOfChange`, especially the
   translation of `{length: 100, interval: "Day"}` into a query or history slice.
2. The live portfolio hydration path that assembles price history for constant-frequency
   evaluation. Log source table/vendor, timestamps, adjustment flag, and number of rows.
3. Resampling and de-duplication before indicator evaluation:
   - Is there exactly one observation per ticker and market session?
   - Are current quotes appended, replaced, or cached?
   - Are premarket, regular-session, and after-hours points mixed?
4. The backtest indicator path. Determine whether backtests use daily bars while live evaluation uses
   raw timestamped observations.
5. The screener table:
   - uniqueness of `(ticker, date)`;
   - adjusted versus unadjusted field choice;
   - split/dividend normalization;
   - source coverage for the exact 100/63-session windows.

## Minimal diagnostic checks

1. **Dump the exact live vector.** For COP at `2026-07-24T19:55:08.498Z`, persist every
   `(timestamp, price, source, adjustment)` consumed by SMA100 and ROC63.
2. **Count rows and sessions.** Report total rows, distinct UTC dates, distinct exchange sessions,
   and rows per session. Confirm or reject the inferred count of 213.
3. **Offline recomputation.** Compute the arithmetic mean of that exact vector and the ROC reference
   point; verify they equal `115.71314577917538` and `-0.30715514468266825%`.
4. **Current-quote injection test.** Hold history fixed, perturb the current COP quote by exactly
   `$1.00`, and assert the SMA changes by the documented weight:
   - `$0.01` if it is a 100-observation SMA with one current observation;
   - about `$0.00469484` if 213 observations are intentionally present.
5. **After-close parity test.** After the 2026-07-24 session is complete, compare live, backtest, and
   SQL values using the same as-of timestamp and the same explicit series.
6. **Deployment-frequency A/B.** Evaluate the same immutable strategy once under `Constant` and once
   under `OpenClose`. The indicator values should match at the same timestamp.
7. **Uniqueness query.** For all five tickers, assert `COUNT(*) = COUNT(DISTINCT date)` in the
   screener window and inspect any duplicates.
8. **Backtest/live parity fixture.** Feed a synthetic series of exactly 100 unique daily closes into
   both evaluators. Require identical SMA100 and ROC63 values.
9. **Session-growth check.** Re-query the live audit later the same day and infer `N` again. If `N`
   increases with every evaluation, the current quote is being appended repeatedly.

## Acceptance criteria

The issue is resolved when:

1. `100 Day SMA` and `63 Day ROC` have a documented definition: calendar duration versus unique
   sessions, current-bar inclusion, regular-hours policy, and adjustment policy.
2. Live evaluation, backtest evaluation, and the supported SQL reproduction use the same canonical
   series or explicitly disclose why they differ.
3. If the intended contract is conventional daily technicals, SMA100 consumes exactly 100 unique
   session closes and ROC63 uses the close exactly 63 unique sessions earlier.
4. Event audits expose enough provenance to reproduce an indicator: source/as-of timestamp,
   observation count, and preferably the first/last history timestamps.
5. Regression tests cover duplicate timestamps, multiple intraday points, the current quote, splits,
   and constant-frequency repeated evaluation.

## Impact and quarantine boundary

- The five current holdings are **not** due for a thesis exit under either source. The latest live
  event emitted zero close orders for them.
- The live event audit is authoritative for what the deployed engine will do. Do not use screener
  SMA/ROC values as exact live thresholds until this is resolved.
- DTE180 and TP250 are unaffected by this particular mismatch; the same live event independently
  audited those triggers and emitted no close orders.
- The prior GLD live thesis exit should be retrospectively checked against a canonical 100-session
  daily series. This document does not claim that sale was wrong.
- Fixed-book OOS certification is not automatically quarantined because its historical evaluator may
  use a separate daily-bar path. However, live-versus-backtest parity remains unproven. If the
  backtest and live resolvers consume different window semantics, the deployment claim must be
  narrowed and the affected strategy rerun after parity is restored.

## Questions the investigation LLM must answer

1. What exact ordered price vector produced COP SMA100 `115.71314577917538`?
2. Why does the intraday derivative imply 213 observations for all five tickers?
3. Does `Day` mean one session bar or a wall-clock duration?
4. Does the live path resample/de-duplicate before computing indicators?
5. Which source and adjustment policy feed live, backtest, and screener calculations?
6. Can the live and historical evaluators produce identical values from one frozen fixture?
7. Did the same semantics govern the GLD exit and the certified historical runs?

## Required output from the investigation

Return:

1. confirmed root cause with code/data-path evidence;
2. exact before/after vectors for one ticker;
3. whether this is a calculation defect, source mismatch, or undocumented contract;
4. affected surfaces: live, paper, reconcile, backtest, walk-forward, and screener;
5. regression tests added;
6. whether any live exits or certification runs require replay or quarantine.
