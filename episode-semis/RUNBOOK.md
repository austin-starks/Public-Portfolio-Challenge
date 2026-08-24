# Semiconductors — S13 A

> **Paste this whole file into a fresh LLM session** with the NexusTrade MCP server connected.
> Follow top to bottom. Do not ask clarifying questions. The one interactive point is live-order
> approval, which only Austin can do in the UI — you must never approve orders yourself.
>
> **This is not a new bakeoff.** S13 A is design-frozen and **now running** on the live Semis book.
> G3 was replaced. Do not invent a replacement book. Do not invent a 95% stock hybrid. Do not
> re-touch the lockbox.

---

## Owner's thesis (READ FIRST — fixed priors, not things to re-litigate)

Challenge-family semiconductor book: a **fixed conviction universe** plus **single-name momentum**,
expressed as **percent-debit call verticals**. This is not a stock book and it is not a 95% stock
hybrid.

- Frozen 7: `NVDA` `TSM` `AVGO` `AMAT` `LRCX` `ANET` `MRVL`. Do not add, drop, or substitute names.
- Two **isolated** sleeves (`positionScope=strategy`). Do not merge them into one sleeve.
- The bar is **SMH**, not Episode 10 Gate 4 vs Baseline C (`+59.33%` / Sortino `3.02`).
- Ship if walk-forward mean beats SMH **32.535**, lockbox is at least SMH **~20.8**, fills are real,
  and there is no disaster fold. Deploy **≥10%** is enough. The observed 13–31% band is accepted.
- `LRCX` often `cannotAfford`. That is a known live fact, not a reason to change the universe.

This is why the book is what it is: Challenge-shape options on a frozen AI-semis chain, measured
against SMH on the same four ET folds as SMH Baseline D.

---

## Inherited methodology (do not re-litigate)

Gates, selection, posture, and lockbox discipline are inherited from
[`episode-10/BAKEOFF_RUNBOOK.md`](../episode-10/BAKEOFF_RUNBOOK.md). If this file and that file
disagree on *method*, that file wins. If they disagree on *this book's priors*, this file wins.

Non-negotiable inherited rules:

1. **Search may KILL or PROMOTE. Only certification issues a verdict.**
2. **Search ends on or before 2026-04-17.** Do not train knobs on the lockbox.
3. **Lockbox is exam-only and single-touch.** This book's lockbox has already been touched.
   Looking again and then iterating burns it.
4. **Measure the assembled deploy-shape book directly** on each fold's OOS window.
5. **Verify at field level** (`conditionFieldAudit`), never by `strategy.name` or `condition.name`.
6. **Do not approve orders.** Stage only. Austin approves in the UI. Auto-approve stays **false**.
7. **Do not mutate** the incumbent Challenge book or Biotech KEEP (IDs below).

Episode 10 Gate 4 vs Baseline C remains the *published Challenge incumbent bar*. It is **not** this
book's deploy bar. Do not "fail" S13 A for missing `+59.33%` / Sortino `3.02`. Do not quietly move
those numbers either — name the SMH bar.

---

## Specialized FIXED priors

| Role | Value |
| --- | --- |
| Live target | `6a45f218e6b1f2131d1f26be` — **Public Portfolio Challenge: Semis** (Public `5OH79160`), Public brokerage, `initialValue` **8000** |
| What is live | **S13 A** (G3 was replaced) |
| Chat source | `6a8b9a85d287103ac48dcb14` — `SEMIS S13 A CHEAP15 M63 DTE45 20260823` |
| Canonical watchlist | `6a890a9c0c5e08a7b308164b` — `SEMIS AI 20260822 freeze` |
| Do **not** mutate | `69a7dc7acdb6bf6a4681d36c` (**Public Portfolio Challenge: Original**) |
| Do **not** mutate | `6a5e20a3ea0d6db55c69a171` (**Public Portfolio Challenge: Biotech** / KEEP) |
| Search window | walk-forward search **≤ 2026-04-17** |
| Fold calendar | same **4 ET folds** as SMH Baseline D |
| Lockbox (already touched) | **2026-04-17 → 2026-08-23**, exam-only |
| Auto-approve | **false** (book policy and every strategy) |
| Reconcile | Monday **9am CT** queues tickets. Do not approve them. |

### Frozen 7 (do not change)

`NVDA` `TSM` `AVGO` `AMAT` `LRCX` `ANET` `MRVL`

---

## Design freeze — S13 A

Do not re-sweep these knobs. They are the selected neighborhood, not a suggestion.

Two isolated sleeves, both `positionScope=strategy`:

| Sleeve | Per-name | Structures | DTE | First-fire / when |
| --- | ---: | --- | --- | --- |
| **LEAP** | 12% | percent-debit call verts **20/25**, then **10/25** | 365–730 | `Or(DaysSince ≥ 99999, DaysSince ≥ 63)` **AND** `VIX < 35` |
| **Cheap** | 15% | percent-debit call verts **20/25** only | 90–180 | same 63-day first-fire + `VIX < 35` |

Shared pipeline and exits (both sleeves):

| Knob | Frozen value |
| --- | --- |
| Filter | `Price > SMA100` **AND** `ROC63 > 0` |
| SelectTop | **7** by `ROC126` |
| Take-profit | **300** |
| Time exits | DTE **≤ 21**, and DTE **22–45** |
| Per-name flatten | `Price < SMA100` **AND** `ROC63 < 0` |

Field-read live strategy IDs (cloned from the chat source; do not treat names as source of truth):

| Live strategy ID | Role |
| --- | --- |
| `6a8b9b3cd287103ac48dcf58` | LEAP sleeve — 12%/name, 20/25 then 10/25, 365–730, `positionScope=strategy` |
| `6a8b9b3cd287103ac48dcf5d` | Cheap sleeve — 15%/name, 20/25 only, 90–180, `positionScope=strategy` |
| `6a8b9b3cd287103ac48dcf62` | CloseOption — P/L ≥ 300% |
| `6a8b9b3cd287103ac48dcf67` | CloseOption — DTE ≤ 21 |
| `6a8b9b3cd287103ac48dcf6c` | CloseOption — DTE 22–45 |
| `6a8b9b3cd287103ac48dcf71` … `6a8b9b3cd287103ac48dcf8f` | Per-name flatten on the frozen 7 |

### Certified assembled OOS vs SMH — mean of 4 ET folds, search ≤ 2026-04-17

Same four ET folds as SMH Baseline D. Headline = that mean. Do not substitute lockbox or YTD.

| Fold | S13 A | SMH |
| --- | ---: | ---: |
| F0 | **57.305** | 44.807 |
| F1 | **58.852** | 7.403 |
| F2 | **66.861** | 20.765 |
| F3 | **69.058** | 57.166 |
| **Mean** | **63.019** | **32.535** |

All four folds beat SMH. No disaster fold.

---

## What is already done (do not redo)

### Search / certify

S13 A cleared the SMH bar on the search-window folds above (mean **63.019** vs **32.535**). G3 is
not the live object. Do not restore G3. Do not invent a stock hybrid to "improve" deploy.

### Lockbox (ONE TOUCH — burned if you iterate)

Window: **2026-04-17 → 2026-08-23**, exam-only. Do not train knobs on this window.

| Book | Return |
| --- | ---: |
| S13 A | **+44.432** |
| SMH | **+20.797** |

Lockbox ≥ SMH ~20.8. Deploy in the **13–31%** band is accepted. Deploy **≥10%** is enough to ship.
`LRCX` often `cannotAfford`.

### Live clone (2026-08-23 night CT)

Owner signed off: S13 A is **now running** on Public `5OH79160`. G3 was replaced.

- Chat source `6a8b9a85d287103ac48dcb14` → live target `6a45f218e6b1f2131d1f26be`
- Field-read name: `Public Portfolio Challenge: Semis`
- Cash **$8,000**. No option positions at the 2026-08-23 night CT field-read.
- `automatedApproval.enabled: false`. Every strategy `automaticOrderApproval: false`.
- Monday **9am CT** reconcile queues tickets. **Do not approve them.**
- **Do not invent staged option order IDs.** Log only IDs the tools return.

There is **no invented live P&L** in this campaign. Cash with no option holdings is not a
performance headline.

---

## Remaining work (only this)

1. **Do not mutate S13 A, Biotech KEEP, or Original.**
2. **Do not re-touch the lockbox.** It is exam-only.
3. Monday 9am CT reconcile may queue tickets. Austin approves (or declines) in the UI. You may
   *inspect* pending orders and field-audit clone parity. You may not approve.
4. If reconcile returns order IDs, log the real ones. If it returns none, write that — do not
   fabricate IDs.
5. Log any later live fills, rejects, `cannotAfford` (especially `LRCX`), or empty-chain events in
   [`CAMPAIGN_LOG.md`](CAMPAIGN_LOG.md). Do not back-fill a P&L you did not read from the account.

---

## Working rules

- One log: [`CAMPAIGN_LOG.md`](CAMPAIGN_LOG.md) in this folder. Append facts. Do not invent IDs.
- Search-layer numbers are not a verdict. This campaign’s verdict already rests on the four-fold
  SMH comparison + the single lockbox touch + the SMH deploy bar.
- Biotech KEEP lives in [`episode-11/moderna/`](../episode-11/moderna/). Leave that body intact.
- Headline = mean of the four search-window folds vs SMH, then the lockbox row. Never YTD as if it
  were holdout. Never train on the lockbox.
