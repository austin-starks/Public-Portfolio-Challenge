# Episode 11: live Semis + Biotech allocator

> **Paste this whole file into a fresh LLM session** with the NexusTrade MCP server connected.
> Follow top to bottom. Do not ask clarifying questions. You audit, measure and log. You never
> approve orders, never change approval settings and never edit the live strategy set.
>
> **This is not a new bakeoff.** The allocator is design-frozen and live. Do not invent a replacement
> book. Do not re-run the rejected constructions listed below as if they were unknown.

---

## Thesis and universe (READ FIRST: fixed priors, not things to re-litigate)

The thesis brief is Austin's: after the **2026-08-19** Moderna/Merck intismeran autogene + Keytruda
Phase 3 melanoma readout, personalized oncology becomes a recurring sequencing, compute and
manufacturing workload, so both the neoantigen/mRNA chain and AI infrastructure benefit.

**Who decided what.**

- **Grok Bot** researched and froze the company names: 20 biotech names and 7 semiconductor names
  ([`GROK_BOT_CAMPAIGN_LOG.md`](GROK_BOT_CAMPAIGN_LOG.md)). Austin did not pick the companies.
- **Codex** designed the live construction on 2026-08-26 and deployed it at Austin's direction
  ([`CODEX_CAMPAIGN_LOG_20260824T134240Z.md`](CODEX_CAMPAIGN_LOG_20260824T134240Z.md)).
- **Austin** set the experiment, directed the redesign and authorized the live replacement.

The live universe is Grok Bot's 27 names minus PSNL (Tempus agreed to acquire Personalis on
2026-08-21). Do not add, drop, or substitute names in this book. A different universe is a new
sibling book with its own record.

### Frozen 26 (do not change)

| Thesis bucket (explanation only, not separate cash queues) | Names |
| --- | --- |
| Therapy platforms and oncology partners | `MRNA` `MRK` `BNTX` `BMY` |
| Computational drug discovery | `RXRX` `SDGR` |
| Precision-oncology diagnostics | `ADPT` `GH` `NTRA` `VCYT` |
| Measurement infrastructure | `ILMN` `TWST` `QGEN` `TXG` `PACB` |
| Diversified life-science tools | `TMO` `DHR` `A` `TECH` |
| AI compute and custom silicon | `NVDA` `AVGO` `MRVL` |
| Semiconductor manufacturing and equipment | `TSM` `AMAT` `LRCX` |
| AI networking | `ANET` |

There is no special MRNA allocation, no special ANET allocation and no XBI or SMH gate.

---

## Fixed IDs

| Role | Value |
| --- | --- |
| Live target | `6a8cb433e3971b7c87943f11`, **Public Portfolio Challenge: Semis + Biotech**, Public `5OH79160`, `initialValue` 13500, frequency `Constant` |
| Public share page | `6a8cb4ebc57fd738a24f1a41` |
| Validated source (cloned to live) | `6a8f7ea36c9d5ad71a63775d` |
| Certified source | `6a8f7c8c6c9d5ad71a636b36` |
| Walk-forward study | `6a8f7ca76c9d5ad71a636c07` |
| Full event replay | `6a8f7dd2f68259010d956f8d` |
| Current executable replay (2026-08-25 snapshot) | `6a8f7dd5f68259010d956f8e` |
| Post-deploy reconciliation | `6a8f9b603a0c760d5849f380` |
| Live notepad | `6a8f92a2af3e2e9df8c56ea4`, "Episode 11 deployed redesign and reconciliation" |
| Allocator (RebalanceOption) | `6a8f9b244945cfc21aa3d8d8` |
| Global exit: gain ≥ 300% | `6a8f9b244945cfc21aa3d8dd` |
| Global exit: ≤ 180 DTE | `6a8f9b244945cfc21aa3d8e2` |
| Company exits (26) | `6a8f9b244945cfc21aa3d8e7` through `6a8f9b244945cfc21aa3d965`; examples: QGEN `…d91f`, BMY `…d942`, NVDA `…d947` |
| Legacy sector-gated book (paper) | `6a8f9b0ec67c177db82d5b0f` |
| Do **not** mutate | `69a7dc7acdb6bf6a4681d36c` (Original Challenge) |
| Do **not** mutate | Grok Bot paper controls (shared `6a8d07f817356dfe9cc71f11`, `6a8d07fc17356dfe9cc71fc9`) |
| Do **not** mutate | `6a5e20a3ea0d6db55c69a171` (historical Biotech book) and `6a45f218e6b1f2131d1f26be` (historical Semis book) |

Verify strategies at field level (`conditionFieldAudit`), never by `strategy.name`.

---

## Exact rules (as deployed 2026-08-26 CT)

| Component | Rule |
| --- | --- |
| Starting capital | $13,500 |
| Security held | Single-leg long call only. No stock, no spreads, no short legs. |
| Company entry filter | Underlying above its own 100-day SMA **and** its own 63-day return above zero |
| Candidate ordering | Highest 126-day return |
| Allocation weight | 63-day return divided by 63-day price volatility |
| Cadence | At least 7 days since the last RebalanceOption order |
| Broad stress gate | VIX below 35 |
| Sector gates | None |
| Per-company cap | 6% of current portfolio value |
| Per-rebalance budget | 45% of current portfolio value |
| New-cycle gate | Do not start another rebalance cycle when option gross exposure is 39% or higher |
| Expiry at entry | 270 to 730 DTE, middle of the available range |
| Strike ladder | 0%, 10%, 20%, 35%, 50%, 75%, then 100% OTM; first executable structure |
| Execution filter | Maximum 20% bid-ask spread |
| Profit exit | Close at a 300% option gain |
| Time exit | Close at 180 DTE remaining |
| Company exit | Close when the stock is below its own 100-day SMA **or** its 63-day return is below zero |
| Position scope | Portfolio-wide |
| Orders | Limit orders at the current quote, good for the day |

The 39% gate blocks new entry cycles. It is not a forced deleveraging rule; existing calls can
appreciate past it without being sold for that reason.

---

## Certification evidence (do not re-run as if unknown)

Five non-overlapping OOS folds at $13,500, study `6a8f7ca76c9d5ad71a636c07`:

| OOS window | Return | Sortino | Max DD | Median deployment |
| --- | ---: | ---: | ---: | ---: |
| 2022-11-08 → 2023-07-18 | +42.87% | 3.26 | 15.01% | 28.30% |
| 2023-07-18 → 2024-03-26 | +25.00% | 1.99 | 15.33% | 14.17% |
| 2024-03-26 → 2024-12-03 | -2.22% | -0.31 | 21.64% | 19.42% |
| 2024-12-03 → 2025-08-12 | +9.95% | 0.62 | 22.47% | 22.76% |
| 2025-08-12 → 2026-04-20 | +65.40% | 5.61 | 8.09% | 25.38% |

Gate: a majority of profitable folds with acceptable risk. Austin set this on 2026-08-26 ("we do NOT
need to be profitable 5/5 folds"). Result: 4 of 5, median +25.00%, median Sortino 1.99, worst OOS
drawdown 22.47%.

Full replay 2022-03-07 → 2026-04-20: +252.37%, Sortino 2.02, max drawdown 29.79%, median deployment
30.53%, 20 of 26 names traded, 496 option fills, longest underwater 573 days.

**No untouched lockbox.** The only valid combined-book lockbox (a different three-sleeve design) lost
44.15% on 2026-04-20 → 2026-08-24. The universe was frozen with August 2026 knowledge. The forward
test is the only clean evidence for this book.

### Rejected constructions (already known)

| Construction | Why it was rejected |
| --- | --- |
| XBI-gated biotech + SMH-gated semis (ran live Aug 24 to Aug 26 CT) | Sector ETFs vetoed company signals; SMH blocked a selected ANET entry on 2026-08-26 |
| Eight separate thesis-bucket sleeves | Worst OOS drawdown 33.43%; lower gates (40%, 32%) made it worse |
| Six-sleeve Candidate F with MRNA core | Anchored OOS mean +8.98%; Austin rejected it |
| MRNA and ANET "core" sleeves | Withdrawn; no conviction hierarchy was ever given |
| Stock-led portfolio | Rejected by Austin; this is an options portfolio |
| Nearest-expiration 120–270 DTE | -32.31% OOS fold |

### Known constraints

- At $13,500, a 6% cap is about $810 per company. Expensive long-dated calls (ANET's audited contract
  cost about $2,225) are rejected rather than oversized. Zero fills on a name are expected behavior.
- Entry and company exit use complementary rules. A name that crosses its 100-day SMA or 63-day
  return intraday can be bought and closed on the same day (NVDA, 2026-09-15).

---

## What is already done (do not redo)

- 2026-08-27 02:04 UTC: legacy six-strategy book preserved as paper `6a8f9b0ec67c177db82d5b0f`.
- 2026-08-27 02:05 UTC: live set replaced with 29 strategies matching `6a8f7ea36c9d5ad71a63775d`.
- 2026-08-27 02:05 UTC: reconciliation at NAV $13,335.02 produced zero orders; QGEN call preserved.
- Live orders and results since then: [`FORWARD_TEST_LOG.md`](FORWARD_TEST_LOG.md).

### Approval state (field-read 2026-10-02)

- Portfolio policy: `automatedApproval.enabled: true`, `maxAutomatedTradesPerDay: 25`, last updated
  2026-09-14 23:06 UTC by the owner account.
- All 29 strategies: `automaticOrderApproval: false`.
- At deployment on 2026-08-26 both levels were off. Do not change either setting.

---

## Remaining work (only this)

1. **Do not mutate** the live strategy set, approval settings, or any book in the do-not-mutate rows.
2. **Do not approve orders.**
3. Read orders with `query_portfolio_events` (`event_types: ["Order"]`, a recent `start_date`) and
   append every filled or canceled order to [`FORWARD_TEST_LOG.md`](FORWARD_TEST_LOG.md) with the
   strategy ID that produced it. Use only IDs and prices the tool returns.
4. Measure performance from the **$13,500 deposit** using the last value snapshot of each session from
   `/api/share-portfolio/portfolio/6a8cb4ebc57fd738a24f1a41/history`. Compare with SPY total return
   (price plus dividends) between the 2026-08-25 open and the same close. Do not quote the share page's
   headline return as the account return; that baseline starts after day-one fill costs.
5. Do not back-fill a P&L you did not read from the account.

## Working rules

- One forward log: [`FORWARD_TEST_LOG.md`](FORWARD_TEST_LOG.md). Append facts. Do not invent IDs.
- Backtest numbers above are research evidence, not live performance.
- Other Episode 11 books are siblings. Leave them intact.
