# Episode 11 — Moderna / AI-biotech book

> **Paste this whole file into a fresh LLM session** with the NexusTrade MCP server connected.
> Follow top to bottom. Do not ask clarifying questions. The one interactive point is live-order
> approval, which only Austin can do in the UI — you must never approve orders yourself.
>
> **This is not a new bakeoff.** KEEP is design-frozen. Do not invent a replacement book. Do not
> re-run failed neighborhoods as if they were unknown. Do not touch the lockbox again.

---

## Owner's thesis (READ FIRST — fixed priors, not things to re-litigate)

Sector re-rating after the **2026-08-19** Moderna/Merck **intismeran autogene + Keytruda** Phase 3
melanoma readout. The universe is the **neoantigen / mRNA value chain**.

- **`MRNA` is required in the universe.** It is **not** required as a sleeve. High beta is the intent.
- Do not add, drop, or substitute names. Do not spend effort questioning the picks.
- **Owner override:** the deploy bar is **not** Episode 10 Gate 4 vs Baseline C
  (`+59.33%` / Sortino `3.02`). The bar is a **very good Challenge-class book**.

This is why the book is what it is: a high-beta LEAP expression on a frozen neoantigen/mRNA chain,
risk-shaped by the inherited Episode 10 methodology except for that owner-override bar.

---

## Inherited methodology (do not re-litigate)

Gates, selection, posture, and lockbox discipline are inherited from
[`episode-10/BAKEOFF_RUNBOOK.md`](../../episode-10/BAKEOFF_RUNBOOK.md). If this file and that file
disagree on *method*, that file wins. If they disagree on *this book's priors*, this file wins.

Non-negotiable inherited rules:

1. **Search may KILL or PROMOTE. Only certification issues a verdict.**
2. **Select with `aggregate.crossFoldRobustSelection`** (minimax validation Sortino). Do **not**
   deploy a per-fold validation argmax.
3. **Measure the assembled deploy-shape book directly** on each fold's OOS window. Fold-winner
   numbers for a different object are not the headline.
4. **Lockbox is single-touch.** This book's lockbox has already been touched. Looking again and
   then iterating burns it.
5. **Verify at field level** (`conditionFieldAudit`), never by `strategy.name` or `condition.name`.
6. **Do not approve orders.** Stage only. Austin approves in the UI when the chain is live.
7. **Do not mutate** the incumbent Challenge book or **AI Semis Live** (IDs below).

Episode 10 Gate 4 vs Baseline C remains the *published Challenge incumbent bar*. It is **not** this
book's deploy bar. Do not "fail" KEEP for missing `+59.33%` / Sortino `3.02`. Do not quietly move
those numbers either — name the override.

---

## Specialized FIXED priors

| Role | Value |
| --- | --- |
| Live target | `6a5e20a3ea0d6db55c69a171` — **Public Portfolio Challenge: Biotech** (Public `5OH86568`), Public brokerage, `initialValue` 5500, certified at cash **$5,494.51** |
| Paper KEEP (inactive) | `6a8a7c0a14da9860bfda5254` |
| Chat | `6a8a7c13e718a0c3b750d77a` |
| Study that selected KEEP | `6a8a7a9f2229e2cd48bfa2b7` via **`crossFoldRobustSelection`**, not fold argmax |
| Canonical watchlist | `6a88fe991037666dfebd096c` |
| Do **not** mutate | `69a7dc7acdb6bf6a4681d36c` (incumbent Challenge / Baseline C) |
| Do **not** mutate | `6a45f218e6b1f2131d1f26be` (**AI Semis Live**) |
| Lockbox (already touched) | 2026-04-14 → 2026-08-18 |
| Walk-forward span | 2022-01-01 → 2026-04-14 |
| `fold_count` | 4 |
| `oos_width_days` | 252 |
| `validation_percent` | 50 |
| Calendar | anchored |
| `interval` | Day |
| Certification engine | sweep (`engine_kind: sweep`, `certification: true`) |

### Frozen 20 (do not change)

`MRNA` `MRK` `BNTX` `PSNL` `RXRX` `SDGR` `ADPT` `GH` `NTRA` `VCYT` `ILMN` `TWST` `QGEN` `TXG` `PACB` `TMO` `DHR` `A` `TECH` `BMY`

`MRNA` stays in the universe. It does not have to be a live sleeve.

---

## Design freeze — KEEP

Do not re-sweep these knobs. They are the selected neighborhood, not a suggestion:

| Knob | Frozen value |
| --- | --- |
| Total budget | 75 |
| SelectTop | 20 |
| Roll DTE | 90 |
| Take-profit | 80 |
| Delta | ~0.50 |
| DTE family | 365–730 LEAPs |

Certified assembled OOS — **mean of 4 folds, not YTD**:

| Fold | OOS window | Return |
| --- | --- | --- |
| F0 | 2023-07-12 → 2024-03-19 | **+26.407%** |
| F1 | 2024-03-20 → 2024-11-26 | **+25.437%** |
| F2 | 2024-11-27 → 2025-08-05 | **+56.296%** |
| F3 | 2025-08-06 → 2026-04-14 | **+20.751%** |
| **Aggregate** | mean of 4 folds | **+32.223%** / Sortino **1.734** / worst DD **44.28** |

Headline = that aggregate. Do not substitute 2026 YTD.

---

## Failed neighborhoods (do not re-run as if unknown)

These already ran. Re-running them as a "fresh search" is invalid.

| Neighborhood | Assembled result | Disposition |
| --- | --- | --- |
| TP60 | +9.48% / Sortino 0.66 | KILL |
| Later-roll 180 + Δ0.55 | −26.97% | KILL |
| Challenge-shape transplant | +18.62% / Sortino 0.99 | KILL |
| KEEP + SMA100 / ROC63 flatten | +2.03% / Sortino 0.27 | KILL |
| Wave-3 OTM / high-beta / regime | (all KILL) | KILL |

If a later campaign wants a new family, it is a **new sibling folder** with a new lockbox, not a
mutation of KEEP and not a second touch of 2026-04-14 → 2026-08-18.

---

## What is already done (do not redo)

### S5 — assembled OOS

KEEP selected from study `6a8a7a9f2229e2cd48bfa2b7` by `crossFoldRobustSelection`. Per-fold table
above. Paper book `6a8a7c0a14da9860bfda5254` is the frozen assembled object.

### S6 — lockbox (ONE TOUCH — burned if you iterate)

Window: **2026-04-14 → 2026-08-18**, `initial_value` **$5,494.51**, Day.

| Book | Return | Sortino | maxDD | Backtest |
| --- | ---: | ---: | ---: | --- |
| KEEP | **+62.966%** | **4.247** | **24.879%** | `6a8a884a6b55968aac525c62` |
| SPY B&H | +11.292% | 3.499 | 4.294% | `6a8a8871bbb5a31396fcd854` |
| ARKG B&H | +50.099% | 5.164 | 13.480% | `6a8a8871bbb5a31396fcd8a1` |

KEEP lockbox breadth **17/20**. `NTRA`, `TECH`, `TMO` were zero-fill + rejection. Median deploy
**15.44%**, never ≥ 40%.

### 2026 YTD-to-08-18 (NOT a clean holdout)

January–April overlaps F3. Do not present this as lockbox or as assembled-OOS.

KEEP **+53.269%** / Sortino **2.404** / maxDD **24.093** — `6a8a888a6b55968aac525e3d` — vs SPY
**+11.848%** vs ARKG **+45.479%**.

### S8 — live clone (2026-08-23 CT)

Owner signed off: clone KEEP onto live `5OH86568` and stage for UI approval.

- `clone_strategies_to_portfolio` source `6a8a7c0a14da9860bfda5254` → target `6a5e20a3ea0d6db55c69a171`
- 3 strategies copied
- Cash still **$5,494.51**
- Tiny BTC dust remains
- Automated approval **off**
- Sunday `fresh_deploy` reconcile produced **no option opens** (empty target / no fresh market data)
- **Do not invent staged option order IDs.** Orders still require Austin’s UI approval when the
  chain is live.

There is **no invented live P&L** in this campaign. Cash plus dust is not a performance headline.

---

## Remaining work (only this)

1. **Do not mutate KEEP, Public Portfolio Challenge: Biotech rules, Challenge, or AI Semis Live.**
2. **Do not re-touch the lockbox.**
3. When the options chain is live, Austin approves (or declines) orders in the UI. You may
   *inspect* pending orders and field-audit clone parity. You may not approve.
4. If reconcile is re-run on a market-open session, log the real order IDs the tool returns. If it
   returns none, write that — do not fabricate IDs.
5. Log any later live fills, rejects, or empty-chain events in
   [`CAMPAIGN_LOG.md`](CAMPAIGN_LOG.md). Do not back-fill a P&L you did not read from the account.

---

## Working rules

- One log: [`CAMPAIGN_LOG.md`](CAMPAIGN_LOG.md) in this folder. Append facts. Do not invent IDs.
- Search-layer numbers are not a verdict. This campaign’s verdict already rests on the certified
  assembled OOS + the single lockbox touch + the owner override of Gate 4 vs C.
- Other Episode 11 books are siblings. Leave them intact.
- Headline = mean of the four S5 folds, then the S6 lockbox row. Never YTD as if it were holdout.
