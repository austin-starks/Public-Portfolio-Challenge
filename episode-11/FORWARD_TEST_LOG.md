# Episode 11 forward test log: Public Portfolio Challenge: Semis + Biotech

**Live target:** `6a8cb433e3971b7c87943f11`, Public `5OH79160`, `initialValue` $13,500
**Strategy set:** the 26-company allocator deployed 2026-08-26 CT (2026-08-27 02:05 UTC). Rules:
[`LIVE_ALLOCATOR_RUNBOOK.md`](LIVE_ALLOCATOR_RUNBOOK.md).
**Public page:** [nexustrade.io/shared-portfolio/6a8cb4ebc57fd738a24f1a41](https://nexustrade.io/shared-portfolio/6a8cb4ebc57fd738a24f1a41)

This log records facts read from the account. It does not invent fills or back-fill P&L.

---

## Entry 1: read 2026-10-02 (latest close: 2026-10-01)

### Sources

- Orders: `query_portfolio_events` on `6a8cb433e3971b7c87943f11`, `event_types: ["Order"]`,
  2026-08-24 → 2026-10-03 (83 order events across both pages). Times are UTC.
- Positions and marks: `GET /api/share-portfolio/portfolio/6a8cb4ebc57fd738a24f1a41/performance-export`,
  `asOf` 2026-10-02 17:48:49 UTC.
- Account value series: `GET /api/share-portfolio/portfolio/6a8cb4ebc57fd738a24f1a41/history`
  (598 snapshots, 2026-08-25 13:32 UTC → 2026-10-02 17:48 UTC).
- SPY: daily regular-session bars from Robinhood, raw and dividend-adjusted.
- Strategy and approval settings: `get_portfolio 6a8cb433e3971b7c87943f11`, read 2026-10-02.

### Before the allocator (sector-gated book, for context)

| Time (UTC) | Order | Result | Strategy |
| --- | --- | --- | --- |
| 2026-08-25 13:30:01 | Buy 1 QGEN 2027-12-17 $45 call, limit $4.10 | Pending User Approval, then resubmitted | `6a8cfa84c45529b8680b71a7` (legacy XBI-gated biotech sleeve) |
| 2026-08-25 13:37:57 | Buy 1 ADPT 2027-04-16 $30 call, limit $4.30 | **Canceled** | same |
| 2026-08-25 13:38:00 | Buy 1 QGEN 2027-12-17 $45 call, limit $5.90 | **Filled $5.90** | same |

The allocator kept this QGEN call when it replaced the strategy set.

### Every live order since the allocator went live

| Time (UTC) | Order | Result | Strategy |
| --- | --- | --- | --- |
| 2026-09-01 13:30:14 | Buy 1 NVDA 2027-12-17 $400 call, limit $7.15 | **Filled $7.05** | allocator `…d8d8` |
| 2026-09-01 13:30:17 | Buy 1 SDGR 2027-11-19 $20 call, limit $5.80 | **Filled $5.80** | allocator `…d8d8` |
| 2026-09-01 13:30:04 | Buy 1 BMY 2027-12-17 $70 call, limit $7.90 | **Canceled** (no reason in the event) | allocator `…d8d8` |
| 2026-09-08 13:30:11 | Buy 1 MRK 2027-12-17 $230 call, limit $5.05 | **Filled $5.05** | allocator `…d8d8` |
| 2026-09-08 13:30:15 | Buy 1 BMY 2027-12-17 $72.50 call, limit $7.10 | **Filled $6.25** | allocator `…d8d8` |
| 2026-09-14 14:26:32 | Sell 1 NVDA 2027-12-17 $400 call, limit $5.70 | **Filled $5.70** | NVDA company exit `…d947` |
| 2026-09-15 14:00:06 | Buy 1 NVDA 2027-12-17 $380 call, limit $7.20 | **Filled $7.20** | allocator `…d8d8` |
| 2026-09-15 14:52:17 | Sell 1 NVDA 2027-12-17 $380 call, limit $6.90 | **Filled $6.90** | NVDA company exit `…d947` |
| 2026-09-15 14:52:23 to 14:52:37 | Three more sells of the same NVDA $380 call | **Canceled** by the broker: "The order quantity entered exceeds the amount you have available to close." | NVDA company exit `…d947` |
| 2026-09-22 14:00:08 | Buy 1 NVDA 2028-01-21 $400 call, limit $8.25 | **Filled $8.25** | allocator `…d8d8` |
| 2026-09-22 14:00:08 | Buy 5 RXRX 2028-01-21 $4 calls, limit $1.55 | **Filled $1.55** | allocator `…d8d8` |
| 2026-09-23 14:10:04 | Sell 1 BMY 2027-12-17 $72.50 call, limit $4.75 | **Filled $4.75** | BMY company exit `…d942` |
| 2026-09-29 14:00:11 | Buy 7 PACB 2028-01-21 $1 calls, limit $1.10 | **Filled $1.03** | allocator `…d8d8` |
| 2026-10-01 19:17:17 | Sell 1 QGEN 2027-12-17 $45 call, limit $3.40 | **Filled $3.40** | QGEN company exit `…d91f` |

Strategy IDs are abbreviated from `6a8f9b244945cfc21aa3d…`. The events list only the filled price
and do not show option fees. Cash reconciles to these fills: $13,500 minus $3,971 of net fill cash
is $9,529, against $9,529.42 of cash reported on 2026-10-02.

### Closed trades (gross, per the fills above)

| Contract | Bought | Sold | Gross P&L |
| --- | ---: | ---: | ---: |
| QGEN 2027-12-17 $45 call | $590 (2026-08-25) | $340 (2026-10-01) | **-$250** |
| NVDA 2027-12-17 $400 call | $705 (2026-09-01) | $570 (2026-09-14) | **-$135** |
| NVDA 2027-12-17 $380 call | $720 (2026-09-15) | $690 (2026-09-15) | **-$30** |
| BMY 2027-12-17 $72.50 call | $625 (2026-09-08) | $475 (2026-09-23) | **-$150** |
| **Total realized** | | | **-$565** |

### Open positions (marks at 2026-10-02 17:48 UTC, intraday)

| Contract | Qty | Cost | Mark | P&L | Return | Bought |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| SDGR 2027-11-19 $20 call | 1 | $580 | $1,500 | **+$920** | +158.6% | 2026-09-01 |
| PACB 2028-01-21 $1 call | 7 | $721 | $1,204 | **+$483** | +67.0% | 2026-09-29 |
| RXRX 2028-01-21 $4 call | 5 | $775 | $810 | **+$35** | +4.5% | 2026-09-22 |
| NVDA 2028-01-21 $400 call | 1 | $825 | $835 | **+$10** | +1.2% | 2026-09-22 |
| MRK 2027-12-17 $230 call | 1 | $505 | $302 | **-$203** | -40.2% | 2026-09-08 |
| **Total** | | **$3,406** | **$4,651** | **+$1,245** | | |

Cash $9,529.42. Cash plus listed marks is $14,180.42; the same API response reports `currentValue`
$14,205.42. The response does not explain the $25 difference.

SDGR and PACB are the two largest gains. Codex removed SDGR from the universe on 2026-08-25 and
restored it on 2026-08-26; PACB was removed on 2026-08-24 and restored on 2026-08-26 (see
[`CODEX_CAMPAIGN_LOG_20260824T134240Z.md`](CODEX_CAMPAIGN_LOG_20260824T134240Z.md)).

### Return vs SPY as of the 2026-10-01 close

| Measure | Value |
| --- | ---: |
| Account value, last snapshot of 2026-10-01 (19:55 UTC, 3:55 PM ET) | **$14,244.42** |
| Account return from the $13,500 deposit | **+5.51%** |
| SPY total return, 2026-08-25 open ($766.16) → 2026-10-01 close ($763.99), dividend included | **-0.04%** |
| SPY price-only return, same window | -0.28% |
| Excess over SPY total return | **+5.55 points** |
| Max drawdown, 13-minute snapshots through 2026-10-01 | **5.92%** ($13,735.06 on 2026-09-04 → $12,922.11 on 2026-09-14) |
| Lowest value vs deposit | -4.28% ($12,922.11, 2026-09-14 15:27 UTC) |

**Measurement method.**

- **Start:** the $13,500 deposit. The first snapshot is $13,500.00 at 2026-08-25 13:32 UTC (9:32 AM
  ET), before the QGEN fill, so SPY is measured from the same session's open.
- **End:** the last account snapshot of the 2026-10-01 session against SPY's 2026-10-01 close. The
  account snapshot is five minutes before the bell; no later snapshot exists for that session.
- **SPY dividend:** $1.888834 per share, ex-date 2026-09-18. Both figures are inferred from
  Robinhood's bars: the dividend-adjusted series sits exactly $1.888834 below the raw series on every
  session before 2026-09-18 and equals it from 2026-09-18 onward. The dividend is added to the ending
  price; it is not reinvested.
- **Window sensitivity:** measured from SPY's 2026-08-24 close ($763.47) instead of the 2026-08-25
  open, SPY total return is +0.32%.
- **Why not the share page headline.** The public page reported +6.73% vs SPY +0.21% at
  2026-10-02 17:48 UTC. Its portfolio baseline is the first afternoon snapshot ($13,310.02 at
  2026-08-25 19:32 UTC), which leaves out $189.98 of day-one loss from the QGEN fill and mark. Its
  SPY series ended at 2026-09-28. The figures in this entry use the deposit and matched dates instead.
- **Scope:** about five weeks and 26 trading sessions. This is a forward record, not evidence of an edge.

### Daily record (last account snapshot per session vs SPY total return from the 2026-08-25 open)

| Session | Last snapshot (UTC) | Account | vs $13,500 | SPY close | SPY TR |
| --- | --- | ---: | ---: | ---: | ---: |
| 2026-08-25 | 19:32 | $13,310.02 | -1.41% | 765.91 | -0.03% |
| 2026-08-26 | 19:57 | $13,335.02 | -1.22% | 766.08 | -0.01% |
| 2026-08-27 | 13:41 | $13,360.02 | -1.04% | 771.10 | +0.64% |
| 2026-08-28 | 18:19 | $13,355.02 | -1.07% | 769.35 | +0.42% |
| 2026-08-31 | 15:19 | $13,310.02 | -1.41% | 767.05 | +0.12% |
| 2026-09-01 | 19:59 | $13,255.06 | -1.81% | 761.78 | -0.57% |
| 2026-09-02 | 19:58 | $13,572.06 | +0.53% | 765.16 | -0.13% |
| 2026-09-03 | 19:58 | $13,580.06 | +0.59% | 773.17 | +0.91% |
| 2026-09-04 | 19:58 | $13,619.06 | +0.88% | 770.19 | +0.53% |
| 2026-09-08 | 19:56 | $13,285.10 | -1.59% | 765.96 | -0.03% |
| 2026-09-09 | 19:58 | $13,378.10 | -0.90% | 762.40 | -0.49% |
| 2026-09-10 | 19:55 | $13,148.10 | -2.61% | 757.83 | -1.09% |
| 2026-09-11 | 19:59 | $13,077.10 | -3.13% | 764.29 | -0.24% |
| 2026-09-14 | 19:20 | $12,987.11 | -3.80% | 760.88 | -0.69% |
| 2026-09-15 | 19:59 | $13,198.14 | -2.24% | 757.39 | -1.14% |
| 2026-09-16 | 19:53 | $13,189.14 | -2.30% | 754.05 | -1.58% |
| 2026-09-17 | 19:59 | $14,038.14 | +3.99% | 762.60 | -0.46% |
| 2026-09-18 | 19:55 | $13,799.14 | +2.22% | 761.69 | -0.34% |
| 2026-09-21 | 19:59 | $13,835.14 | +2.48% | 773.50 | +1.20% |
| 2026-09-22 | 19:57 | $14,020.26 | +3.85% | 773.38 | +1.19% |
| 2026-09-23 | 19:58 | $13,814.27 | +2.33% | 767.81 | +0.46% |
| 2026-09-24 | 19:59 | $13,779.27 | +2.07% | 767.18 | +0.38% |
| 2026-09-25 | 19:58 | $13,567.27 | +0.50% | 771.35 | +0.92% |
| 2026-09-28 | 19:50 | $13,781.27 | +2.08% | 765.61 | +0.17% |
| 2026-09-29 | 19:58 | $13,829.41 | +2.44% | 764.20 | -0.01% |
| 2026-09-30 | 19:57 | $14,228.41 | +5.40% | 762.63 | -0.21% |
| 2026-10-01 | 19:55 | $14,244.42 | +5.51% | 763.99 | -0.04% |

The history endpoint writes a snapshot when the value changes, so some sessions end early in the day.

### Approval state at this read

- Portfolio policy `automatedApproval.enabled: true`, `maxAutomatedTradesPerDay: 25`, updated
  2026-09-14 23:06 UTC by the owner account. At deployment on 2026-08-26 it was off.
- All 29 strategies `automaticOrderApproval: false`.
- How each individual order above was approved is not recorded in the events read for this entry.

### Observations

- The allocator has bought 6 of its 26 names so far (NVDA, SDGR, BMY, MRK, RXRX, PACB). The QGEN
  call came from the earlier sector-gated book. The one allocator order that did not fill was the
  BMY $70 call on 2026-09-01.
- NVDA's company exit closed an NVDA call on two consecutive sessions (2026-09-14 and 2026-09-15).
  On 2026-09-15 the entry filled at 14:00 UTC and the exit filled at 14:52 UTC, which is the
  intraday whipsaw named in the runbook's known constraints.
- Every order event in this window carries one of the strategy IDs listed above.
