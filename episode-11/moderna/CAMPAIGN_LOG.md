# Episode 11 — Moderna / AI-biotech campaign note

**Book:** neoantigen / mRNA value chain (Moderna / AI-biotech)
**Live target:** `6a5e20a3ea0d6db55c69a171` — **Public Portfolio Challenge: Biotech** (Public `5OH86568`)
**Status as of 2026-08-23 CT:** KEEP design-frozen and cloned to live. No option positions. No staged
option order IDs. No live P&L headline. Orders still require Austin’s UI approval when the chain is
live.
**Runbook:** [`RUNBOOK.md`](RUNBOOK.md)
**Methodology parent:** [`episode-10/BAKEOFF_RUNBOOK.md`](../../episode-10/BAKEOFF_RUNBOOK.md)

This note records facts that already happened. It is not a reconstructed bakeoff and it does not
invent fills.

---

## Thesis (fixed)

Sector re-rating after the **2026-08-19** Moderna/Merck **intismeran autogene + Keytruda** Phase 3
melanoma readout. Universe = neoantigen / mRNA value chain. **`MRNA` required in universe, not
required as a sleeve.** High beta is the intent.

**Owner override:** deploy bar is a very good Challenge-class book. It is **not** Episode 10 Gate 4
vs Baseline C (`+59.33%` / Sortino `3.02`). KEEP’s certified assembled-OOS mean (`+32.223%` /
Sortino `1.734`) would miss that C bar; that is expected under the override, not a quiet rewrite of
Episode 10.

---

## Frozen constants

| Role | ID / value |
| --- | --- |
| Live target | `6a5e20a3ea0d6db55c69a171` — **Public Portfolio Challenge: Biotech**, Public `5OH86568`, Public brokerage, `initialValue` 5500, cash **$5,494.51** |
| Paper KEEP (inactive) | `6a8a7c0a14da9860bfda5254` |
| Chat | `6a8a7c13e718a0c3b750d77a` |
| Selecting study | `6a8a7a9f2229e2cd48bfa2b7` (`crossFoldRobustSelection`, not fold argmax) |
| Canonical watchlist | `6a88fe991037666dfebd096c` |
| Do not mutate | `69a7dc7acdb6bf6a4681d36c` (**Public Portfolio Challenge: Original** / Baseline C) |
| Do not mutate | `6a45f218e6b1f2131d1f26be` (**Public Portfolio Challenge: Semis**) |
| Lockbox | 2026-04-14 → 2026-08-18 (single touch; already used) |
| WF span | 2022-01-01 → 2026-04-14 · 4 folds · 252-day OOS · validation 50% · anchored · Day · certification sweep |

**Frozen 20:** MRNA MRK BNTX PSNL RXRX SDGR ADPT GH NTRA VCYT ILMN TWST QGEN TXG PACB TMO DHR A TECH BMY

---

## KEEP (design freeze)

Knobs: budget **75** / SelectTop **20** / roll DTE **90** / TP **80** / Δ~**0.50** / **365–730** LEAPs.

Paper display name (field-read, inactive): `E11 S5 robust assembled paper — neighborhood 75/20/DTE90/TP80`.

### S5 certified assembled OOS — MEAN OF 4 FOLDS, NOT YTD

| Fold | OOS window | Return |
| --- | --- | ---: |
| F0 | 2023-07-12 → 2024-03-19 | +26.407% |
| F1 | 2024-03-20 → 2024-11-26 | +25.437% |
| F2 | 2024-11-27 → 2025-08-05 | +56.296% |
| F3 | 2025-08-06 → 2026-04-14 | +20.751% |
| **Aggregate** | mean of 4 folds | **+32.223%** / Sortino **1.734** / worst DD **44.28** |

Selection provenance: study `6a8a7a9f2229e2cd48bfa2b7`, **`crossFoldRobustSelection`**.

---

## S6 lockbox (one touch)

Window **2026-04-14 → 2026-08-18**, capital **$5,494.51**, Day. Do not re-run as research.

| Book | Return | Sortino | maxDD | Backtest |
| --- | ---: | ---: | ---: | --- |
| KEEP | +62.966% | 4.247 | 24.879% | `6a8a884a6b55968aac525c62` |
| SPY B&H | +11.292% | 3.499 | 4.294% | `6a8a8871bbb5a31396fcd854` |
| ARKG B&H | +50.099% | 5.164 | 13.480% | `6a8a8871bbb5a31396fcd8a1` |

KEEP breadth **17/20**. `NTRA`, `TECH`, `TMO`: zero-fill + rejection. Median deploy **15.44%**,
never ≥ 40%.

KEEP beat SPY and ARKG on lockbox **return**. ARKG’s lockbox Sortino (5.164) is higher than KEEP’s
(4.247). Those are the numbers; this note does not invent a Sortino win vs ARKG.

---

## 2026 YTD-to-08-18 (not a clean holdout)

January–April overlaps F3. Not lockbox. Not assembled-OOS.

KEEP **+53.269%** / Sortino **2.404** / maxDD **24.093** — `6a8a888a6b55968aac525e3d` — vs SPY
**+11.848%** vs ARKG **+45.479%**.

Only those YTD figures were recorded. This note does not invent SPY/ARKG YTD Sortino or drawdown.

---

## Failed neighborhoods (already known)

Do not re-run as if unknown.

| Neighborhood | Assembled result |
| --- | --- |
| TP60 | +9.48% / 0.66 |
| Later-roll 180 + Δ0.55 | −26.97% |
| Challenge-shape transplant | +18.62% / 0.99 |
| KEEP + SMA100 / ROC63 flatten | +2.03% / 0.27 |
| Wave-3 OTM / high-beta / regime | all KILL |

---

## Live S8 — 2026-08-23 CT

Owner signed off: clone KEEP onto live `5OH86568` and stage for UI approval.

| Step | Fact |
| --- | --- |
| Clone | `clone_strategies_to_portfolio` source `6a8a7c0a14da9860bfda5254` → target `6a5e20a3ea0d6db55c69a171` |
| Strategies copied | 3 |
| Cash | still **$5,494.51** |
| Dust | tiny BTC remains (not an options book; not a P&L headline) |
| Automated approval | **off** |
| Sunday reconcile | `fresh_deploy` produced **no option opens** (empty target / no fresh market data) |
| Staged option orders | **none invented; none recorded** |
| Approval | still requires Austin’s UI when the chain is live |

### Field read of the live target after clone (2026-08-23)

`get_portfolio 6a5e20a3ea0d6db55c69a171` confirmed: live, name `Public Portfolio Challenge: Biotech`,
Public / `5OH86568`, `initialValue` 5500, cash **$5,494.51**, buying power **$5,494.51**,
`automatedApproval.enabled: false`, three strategies with `automaticOrderApproval: false`, no
option holdings. Cloned strategy IDs on the live book:

| Live strategy ID | Role (from stored name / audit) |
| --- | --- |
| `6a8a893447c400d0bd89c3e7` | RebalanceOption — Δ0.5 365–730 long call, frozen 20, SelectTop 20, totalBudget 75 |
| `6a8a893447c400d0bd89c3ec` | CloseOption — P/L ≥ 80% |
| `6a8a893447c400d0bd89c3f1` | CloseOption — DTE ≤ 90 |

Paper source `6a8a7c0a14da9860bfda5254` remains **paper** and **inactive**.

---

## Honest caveats

- **No live options P&L.** The account has not opened the KEEP option book. Do not report dust or
  cash as strategy performance.
- **Lockbox is spent.** 2026-04-14 → 2026-08-18 was the single touch. Further design work needs a
  new holdout.
- **YTD is contaminated** by F3 overlap. Do not use it as the certification headline.
- **Gate 4 vs C was overridden**, in writing, before deploy. Episode 10’s published C bar is
  unchanged.
- **Other Episode 11 books**, if they exist or return, are siblings. This folder does not replace
  them.
