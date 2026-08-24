# Semiconductors — S13 A campaign note

**Book:** frozen AI-semis conviction universe, Challenge-family percent-debit call verticals
**Live target:** `6a45f218e6b1f2131d1f26be` — **Public Portfolio Challenge: Semis** (Public `5OH79160`)
**Status as of 2026-08-23 night CT:** **NOW RUNNING S13 A**. G3 was replaced. Auto-approve still
false. Monday 9am CT reconcile queues tickets. No option positions at the field-read. No invented
live P&L.
**Runbook:** [`RUNBOOK.md`](RUNBOOK.md)
**Methodology parent:** [`episode-10/BAKEOFF_RUNBOOK.md`](../episode-10/BAKEOFF_RUNBOOK.md)

This note records facts that already happened. It is not a reconstructed bakeoff and it does not
invent fills. It does not invent a stock hybrid.

---

## Thesis (fixed)

Challenge family: **fixed conviction universe + single-name momentum** as **percent-debit call
verticals**, not 95% stock.

**Deploy bar:** walk-forward mean **> SMH 32.535**, lockbox **≥ SMH ~20.8**, real fills, no disaster
fold. Deploy **≥10%** is enough. Observed **13–31%** is accepted. This is **not** Episode 10 Gate 4
vs Baseline C (`+59.33%` / Sortino `3.02`).

---

## Frozen constants

| Role | ID / value |
| --- | --- |
| Live target | `6a45f218e6b1f2131d1f26be` — **Public Portfolio Challenge: Semis**, Public `5OH79160`, Public brokerage, `initialValue` **8000**, cash **$8,000** at the 2026-08-23 night CT field-read |
| What is live | **S13 A** (G3 replaced) |
| Chat source | `6a8b9a85d287103ac48dcb14` — `SEMIS S13 A CHEAP15 M63 DTE45 20260823` |
| Canonical watchlist | `6a890a9c0c5e08a7b308164b` — `SEMIS AI 20260822 freeze` |
| Do not mutate | `69a7dc7acdb6bf6a4681d36c` (**Public Portfolio Challenge: Original**) |
| Do not mutate | `6a5e20a3ea0d6db55c69a171` (**Public Portfolio Challenge: Biotech** / KEEP) |
| Search | walk-forward **≤ 2026-04-17** · same 4 ET folds as SMH Baseline D |
| Lockbox | 2026-04-17 → 2026-08-23 (exam-only; already used) |
| Auto-approve | **false** |
| Reconcile | Monday 9am CT queues tickets |

**Frozen 7:** NVDA TSM AVGO AMAT LRCX ANET MRVL

---

## S13 A (design freeze)

Two isolated sleeves, `positionScope=strategy`:

- **LEAP 12%/name:** percent-debit 20/25 then 10/25, 365–730 DTE, `Or(DaysSince ≥ 99999, ≥ 63)` AND `VIX < 35`
- **Cheap 15%/name:** 20/25 only, 90–180 DTE, same 63-day first-fire + `VIX < 35`

Shared: Filter `Price > SMA100` AND `ROC63 > 0`, SelectTop 7 `ROC126`, TP **300**, DTE ≤ 21, DTE
22–45, per-name flatten `Price < SMA100` AND `ROC63 < 0`.

Chat display name (field-read, inactive draft): `SEMIS S13 A CHEAP15 M63 DTE45 20260823`.

### Certified assembled OOS vs SMH — MEAN OF 4 ET FOLDS, SEARCH ≤ 2026-04-17

| Fold | S13 A | SMH |
| --- | ---: | ---: |
| F0 | 57.305 | 44.807 |
| F1 | 58.852 | 7.403 |
| F2 | 66.861 | 20.765 |
| F3 | 69.058 | 57.166 |
| **Mean** | **63.019** | **32.535** |

All four folds beat SMH. No disaster fold.

---

## Lockbox (one touch — exam only)

Window **2026-04-17 → 2026-08-23**. Do not train knobs on this window. Do not re-run as research.

| Book | Return |
| --- | ---: |
| S13 A | +44.432 |
| SMH | +20.797 |

Lockbox ≥ SMH ~20.8. Deploy **13–31%** accepted; **≥10%** is enough to ship. `LRCX` often
`cannotAfford`.

---

## Live — 2026-08-23 night CT

Owner signed off: S13 A is live on `5OH79160`. G3 was replaced.

| Step | Fact |
| --- | --- |
| Source | chat `6a8b9a85d287103ac48dcb14` |
| Target | live `6a45f218e6b1f2131d1f26be` |
| Name | `Public Portfolio Challenge: Semis` |
| Cash | **$8,000** |
| Option holdings | **none** at this field-read |
| Automated approval | **off** |
| Strategy approval | every strategy `automaticOrderApproval: false` |
| Next reconcile | Monday 9am CT queues tickets |
| Approval | still requires Austin’s UI |

### Field read of the live target (2026-08-23 night CT)

`get_portfolio 6a45f218e6b1f2131d1f26be` confirmed: live, name `Public Portfolio Challenge: Semis`,
Public / `5OH79160`, `initialValue` 8000, cash **$8,000**, buying power **$8,000**,
`automatedApproval.enabled: false`, twelve strategies, no option holdings. Sleeves are isolated
(`positionScope=strategy`). Cloned strategy IDs on the live book:

| Live strategy ID | Role (from stored fields / audit) |
| --- | --- |
| `6a8b9b3cd287103ac48dcf58` | RebalanceOption — LEAP 12%/name, 20/25 then 10/25, 365–730, frozen 7, SelectTop 7 |
| `6a8b9b3cd287103ac48dcf5d` | RebalanceOption — Cheap 15%/name, 20/25 only, 90–180, frozen 7, SelectTop 7 |
| `6a8b9b3cd287103ac48dcf62` | CloseOption — P/L ≥ 300% |
| `6a8b9b3cd287103ac48dcf67` | CloseOption — DTE ≤ 21 |
| `6a8b9b3cd287103ac48dcf6c` | CloseOption — DTE 22–45 |
| `6a8b9b3cd287103ac48dcf71` | Flatten NVDA — Price < SMA100 AND ROC63 < 0 |
| `6a8b9b3cd287103ac48dcf76` | Flatten TSM |
| `6a8b9b3cd287103ac48dcf7b` | Flatten AVGO |
| `6a8b9b3cd287103ac48dcf80` | Flatten AMAT |
| `6a8b9b3cd287103ac48dcf85` | Flatten LRCX |
| `6a8b9b3cd287103ac48dcf8a` | Flatten ANET |
| `6a8b9b3cd287103ac48dcf8f` | Flatten MRVL |

Chat source `6a8b9a85d287103ac48dcb14` remains a **chat** draft.

An older notepad on this portfolio (`S10 Convertible Ladder`) describes a prior MU/SNDK config. It
is **not** S13 A. Do not treat it as the live method.

---

## Honest caveats

- **No live options P&L.** The account has not opened the S13 A option book as of the 2026-08-23
  night CT field-read. Do not report cash as strategy performance.
- **Lockbox is spent.** 2026-04-17 → 2026-08-23 was the single exam-only touch. Further design work
  needs a new holdout. Do not train knobs on it.
- **SMH is the bar**, in writing, before deploy. Episode 10’s published C bar is unchanged.
- **`LRCX` often cannotAfford.** Expected. Not a universe change.
- **Biotech KEEP** stays in [`episode-11/moderna/`](../episode-11/moderna/). This folder does not
  replace or rewrite it.
