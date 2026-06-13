# CURSOR Campaign Log — Episode 10 Walk-Forward Options Campaign
**Run start:** 2026-06-13T16:52:24Z  
**Agent:** CURSOR  
**Runbook:** episode-10/RUNBOOK.md

---

## Fixed constants (frozen at S0)

| Parameter | Value |
|-----------|-------|
| initial_value | 25000 |
| lockbox_width_days | 126 |
| WF span | 2022-01-01 → 2026-02-08 |
| fold_count | 4 |
| oos_width_days | 252 |
| validation_percent | 50 |
| engine_kind (cert) | sweep |
| baseline_symbol | SPY |

## Baseline C (incumbent — FROZEN bar)

| Fold | OOS window | Return | Sortino | maxDD | Breadth |
|------|------------|--------|---------|-------|---------|
| 0 | 2023-05-07 → 2024-01-14 | +24.17% | 1.47 | 17.06% | 10 |
| 1 | 2024-01-14 → 2024-09-22 | +8.78% | 0.64 | 18.47% | 9 |
| 2 | 2024-09-22 → 2025-06-01 | +66.87% | 5.60 | 16.56% | 9 |
| 3 | 2025-06-01 → 2026-02-08 | +137.51% | 4.37 | 17.35% | 7 |
| **Aggregate** | | mean +59.33% / min +8.78% | mean 3.02 / min 0.64 | worst 18.47% | |

---

## Stage S0 — Engine Sanity ✅ PASS

| Check | Result | Evidence |
|-------|--------|----------|
| WF sweep smoke | PASS | Study `6a2d8adb08bb1349f5b63dfc` COMPLETE, 2 folds, aggregate OOS mean +10.99% |
| Window fidelity | PASS | Fold 0 val: WF 10.65% vs standalone 10.93%; OOS: WF 4.12% vs standalone 4.70%; maxDD exact match |
| Persistence | PASS | `selectedChatPortfolioId` present both folds (`6a2d8af6e5a40a29b74c66dd`, `6a2d8b1bdaff5c67a9715e95`) |
| SNDK dead-name | PASS | 2022 backtest: SNDK zero resolution attempts, zero fills, no fabricated prices |

---

## Stage S1 — Baselines

### Baseline A (Equity B&H) — chatPortfolioId `6a2d8ae1daff5c67a9715e21`
Study `6a2d8ae6e5a40a29b74c66b4` COMPLETE

| Fold | OOS Return | OOS Sortino | OOS maxDD |
|------|------------|-------------|-----------|
| 0 | +42.35% | 3.80 | 9.69% |
| 1 | +41.00% | 2.78 | 17.96% |
| 2 | +25.33% | 1.46 | 30.64% |
| 3 | +51.92% | 3.52 | 11.06% |
| **Agg** | **mean +40.15%** | **mean 2.89** | **worst 9.69%** |

### Baseline B (original 95% budget) — chatPortfolioId `6a2d8ae408bb1349f5b63e09`
Study `6a2d8ae6daff5c67a9715e29` COMPLETE — agg OOS mean +76.99% return, mean 2.23 Sortino.

Full-span posture audit: **median deploy 63.77%** → exceeds 55% cap.

### Stage S1.5 — AUTO-RELAX Baseline B ✅ FIRED

Original B: totalBudget 95%, median deployment 63.77%, 34% days >70% outside regime.

**Posture-matched B (46% budget):** chatPortfolioId `6a2d8c3108bb1349f5b64033`, median deploy **35.04%**.  
WF study `6a2d8c35daff5c67a9716096` COMPLETE — agg OOS mean **+54.59%** return, mean **1.87** Sortino.

---

## Consolidated target block (frozen)

- **Return:** aggregate OOS ≥ max(A +10pp, SPY +10pp) AND > posture-matched B AND > C (+59.33%)
- **Sortino:** aggregate ≥ 1.9; every fold ≥ 0.9; beat B per-fold where B ≥9 breadth; beat C per-fold AND aggregate (>3.02)
- **Drawdown:** OOS maxDD ≤ 55% every fold
- **Posture:** median deployment ≤ 55%; >70% only in opportunity regime (SPY < 0.92 × 252d max)

---

## Search layer

| ID | Type | Seed | Status |
|----|------|------|--------|
| `6a2d8b3108bb1349f5b63e7b` | systematic_sweep | Family A `6a2d8afc08bb1349f5b63e2c` | RUNNING (27 evals) |

---

## Certification ledger

| Family | Seed id | get_sweep_surface ✓ | gene_intents axes | Study id | crossFoldRobustSelection | Assembled book | OOS gate | Verdict |
|--------|---------|---------------------|-------------------|----------|--------------------------|----------------|----------|---------|
| A — Momentum long calls/verticals | `6a2d8afc08bb1349f5b63e2c` | ✓ | SelectTopLimit × BuyingPowerPct × TakeProfitPct × RollTriggerDte (3×3×3×3) | `6a2d8b3108bb1349f5b63e7e` | pending | — | pending | RUNNING |
| B — Regime-switch long/flat | `6a2d8b3c08bb1349f5b63ea2` | pending | SelectTopLimit × BuyingPowerPct × TakeProfitPct × RollTriggerDte | `6a2d8b4c08bb1349f5b63ed6` | pending | — | pending | RUNNING |
| C — Credit put spreads | `6a2d8b87daff5c67a9715f3c` | pending | SelectTopLimit × BuyingPowerPct × RollTriggerDte | `6a2d8b91daff5c67a9715f5e` | pending | — | pending | RUNNING |
| Incumbent (Baseline C seed) | `6a2d8af4e5a40a29b74c66d8` | ✓ | SelectTopLimit × BuyingPowerPct × TakeProfitPct × RollTriggerDte | `6a2d8b49e5a40a29b74c6799` | pending | — | pending | RUNNING |

---

## Portfolio IDs (this run only)

| Label | chatPortfolioId |
|-------|-----------------|
| S0 Smoke | `6a2d8acedaff5c67a9715e0d` |
| Baseline A | `6a2d8ae1daff5c67a9715e21` |
| Baseline B (original) | `6a2d8ae408bb1349f5b63e09` |
| Baseline B (posture-matched 55%) | `6a2d8b9ddaff5c67a9715f6c` |
| Baseline B (posture-matched 46%) | `6a2d8c3108bb1349f5b64033` |
| Incumbent seed | `6a2d8af4e5a40a29b74c66d8` |
| Family A seed | `6a2d8afc08bb1349f5b63e2c` |
| Family B seed | `6a2d8b3c08bb1349f5b63ea2` |
| Family C seed | `6a2d8b87daff5c67a9715f3c` |

---

## Next steps (in flight)

1. Complete Baseline B original + posture-matched WF scoring
2. Await 4 certification studies (~729 tokens each)
3. Apply crossFoldRobustSelection → assemble deploy books → gate
4. Lockbox single-touch on finalist
5. Deploy sign-off (discover live target via fetch_portfolios)

## Incumbent assembled book (crossFoldRobustSelection)

- **candidateKey:** `9c122dbef4d20934db5623eabee62f26c24be4ab8993b7ffbfd3065df7538f46`
- **chatPortfolioId:** `6a2d8cf5daff5c67a97161ad`
- **Params:** top-8 both sleeves, 45% buying power, roll DTE 60, TP 100%
- **Cert study:** `6a2d8b49e5a40a29b74c6799` COMPLETE

### Direct OOS measurement (assembled book)

| Fold | OOS window | Return | Sortino | maxDD | Breadth | vs C return | vs C Sortino |
|------|------------|--------|---------|-------|---------|-------------|--------------|
| 0 | 2023-05-08 → 2024-01-15 | +39.59% | 2.03 | 20.54% | **8/20** | ✓ +24.17% | ✓ 1.47 |
| 1 | 2024-01-15 → 2024-09-23 | +312.26% | 11.39 | 16.64% | 9/20 | ✓ +8.78% | ✓ 0.64 |
| 2 | 2024-09-23 → 2025-06-02 | +170.99% | 4.06 | 46.03% | **8/20** | ✓ +66.87% | ✗ 5.60 |
| 3 | 2025-06-02 → 2026-02-08 | +140.26% | 4.30 | 21.43% | **7/20** | ✓ +137.51% | ✗ 4.37 |
| **Agg** | | **mean +165.8%** | **mean 5.45** | worst 20.54% | | ✓ +59.33% | ✓ 3.02 |

**Gate 1 FAIL:** breadth < 9/20 on folds 0, 2, 3 (binding constraint).  
**Gate 4 partial FAIL:** Sortino below C on folds 2–3.  
**Not deploy-ready** — lockbox not touched.

## Failed certifications (fold-0 NoEligibleCandidate)

- Family A Attempt 1 `6a2d8b3108bb1349f5b63e7e` — plain momentum seed
- Family A Attempt 2 `6a2d8c3adaff5c67a97160a5` — regime-gated seed
- Family B Attempt 1 `6a2d8b4c08bb1349f5b63ed6` — opportunity-only seed
- Family C Attempt 1 `6a2d8b91daff5c67a9715f5e` — credit put spreads

## Family A Attempt 3 (incumbent seed, wider top-K) — study `6a2d8d42daff5c67a9716259` COMPLETE

- **crossFoldRobustSelection candidateKey:** `a463eff25001b4d780c091712ed79192a7d07a7d4d27d50195d0fd7806649938`
- **Assembled book:** `6a2d8f6ee5a40a29b74c6d91` — top-14 both sleeves, 50% BP, TP 100%, roll DTE 60

### Direct OOS (assembled book)

| Fold | Return | Sortino | maxDD | Breadth | Gate 1 | Gate 4 vs C |
|------|--------|---------|-------|---------|--------|-------------|
| 0 | +31.17% | 1.57 | 28.37% | **6/20** | FAIL | ✓ |
| 1 | +149.56% | 6.83 | 19.07% | **8/20** | FAIL | ✓ |
| 2 | +202.91% | 4.35 | 44.01% | **8/20** | FAIL | ✗ Sortino 5.60 |
| 3 | +172.93% | 5.51 | 24.19% | **7/20** | FAIL | ✓ |
| **Agg** | **mean +139.1%** | **mean 4.56** | | | **FAIL** | partial |

**Fold-3 winner variant** (`6a2d8f5bdaff5c67a97166cf`, top-14/50%/TP200%/roll45): folds 1–3 pass breadth (9–10 names) but fold 0 still **6/20**; fold 3 Sortino 3.99 < C 4.37.

**Kill reason:** Gate 1 — breadth < 9/20 on every OOS segment when measured on assembled deploy book (binding: LEAP affordability + Greek filters block fills on eligible names).

## Incumbent Cert Attempt 2 — study `6a2d8f8008bb1349f5b64789` COMPLETE

- **crossFoldRobustSelection:** `c5e258dad64adc9f26161449cf956caf4ddbf6d08b7d4cdc62efb12fbef47691`
- **Assembled book:** `6a2d90b708bb1349f5b6499b` — top-16 both sleeves, 50% BP, TP 100%, roll DTE 60

| Fold | Return | Sortino | Breadth |
|------|--------|---------|---------|
| 0 | +42.3% | 2.10 | **8/20** |
| 1 | +149.6% | 6.83 | **8/20** |
| 2 | +202.9% | 4.35 | **8/20** |
| 3 | +251.2% | 5.42 | **7/20** |

**Kill:** Gate 1 (breadth < 9 every fold).

## Family B Attempt 2 — study `6a2d8f8d08bb1349f5b647c6` COMPLETE

- **crossFoldRobustSelection:** `978de53514c9a092a21f29ccf6257d8821a7d4c4bdcac7e1a4a02867c6e48114`
- **Assembled book:** `6a2d90f4daff5c67a9716ab1` — top-14, 50% BP, TP 100%, roll DTE 45
- WF cert agg OOS: mean +206.1% return, mean 5.03 Sortino

| Fold | Return | Sortino | Breadth |
|------|--------|---------|---------|
| 0 | +31.3% | 1.57 | **6/20** |
| 1 | +159.4% | 6.94 | **8/20** |
| 2 | +202.9% | 4.35 | **8/20** |
| 3 | +172.9% | 5.51 | **7/20** |

**Kill:** Gate 1 (breadth < 9 every fold on assembled book).

## Additional errors (this session)

| Study | Error |
|-------|-------|
| Family A Attempt 4 `6a2d8fa2e5a40a29b74c6e5d` | NoEligibleCandidate fold 0 |
| Family C Attempt 2 `6a2d8fa208bb1349f5b64808` | TakeProfitPct gene mismatch (credit book has no TP close) |
| Family C Attempt 3 `6a2d90bedaff5c67a97169df` | NoEligibleCandidate fold 0 |

## Binding constraint (campaign-wide)

**Gate 1 — breadth:** Regime-switched LEAP books (top-8 through top-16, 45–50% BP) consistently fill only 6–8/20 names on direct OOS backtests. Breadth audit shows Greek-filter rejections and `cannotAfford` on high-priced names (LLY, META). Increasing top-K does not fix fold-0 early-window participation.

**Verdict:** Campaign IN PROGRESS — 4 complete regime-switched certs, **zero gate-passing finalists**. Plain momentum and credit families failed certification. Lockbox untouched. No deploy sign-off.

---

## Session 2 — New mechanism seeds + certifications (2026-06-13T17:21Z)

### New seeds created

| Family | Seed | chatPortfolioId | Fold-0 OOS smoke (2023-05-08→2024-01-15) |
|--------|------|-----------------|---------------------------------------------|
| C v2 — credit puts + ROC126 | `6a2d9182daff5c67a9716b6d` | **13/20 names**, +6.1% return |
| D — calendar calls ROC63 | `6a2d918408bb1349f5b64b69` | **0/20 names** (no fills — seed broken) |
| A v2 — vertical-only momentum | `6a2d9188daff5c67a9716b89` | **15/20 names**, +3.3% return |

### Certifications in flight

| Study | Family | Status |
|-------|--------|--------|
| `6a2d9193e5a40a29b74c72ae` | C v2 credit | RUNNING (fold 0 optimizing) |
| `6a2d919508bb1349f5b64b9b` | D calendar | RUNNING |
| `6a2d9196daff5c67a9716bb9` | A v2 vertical momentum | RUNNING |
| `6a2d9195e5a40a29b74c72b9` | Incumbent Attempt 3 (lower alloc) | COMPLETE — gates evaluated (see below) |
| `6a2d93dce5a40a29b74c75da` | A v2 Attempt 6 | RUNNING (fold 0) |

---

## Session 3 — Assembled-book gate evaluation (2026-06-13T17:32Z)

### Family C v2 — study `6a2d9193e5a40a29b74c72ae` COMPLETE → **KILL Gate 1 + Gate 2**

- **crossFoldRobustSelection:** `801b54d2f599d98233e4801cd9e5489ffe643307609c6b73ab619b358798d137`
- **Assembled book:** `6a2d933608bb1349f5b64e9c` — top-14 credit puts, 5% BP, TP 50%, roll DTE 7
- WF cert agg OOS: mean **+8.7%** return, mean **0.90** Sortino

**Direct OOS (assembled book):**

| Fold | Return | Sortino | Breadth | top-5 share | Gate flags |
|------|--------|---------|---------|-------------|------------|
| 0 | +4.35% | 0.21 | 14/20 | 67.1% | top-5 >60%; rejections: ANET,AVGO,GS,LLY,OSCR |
| 1 | +10.41% | 0.95 | 14/20 | 64.5% | top-5 >60%; rejections: ANET,GS,LLY,META |
| 2 | +5.61% | 0.52 | 14/20 | 65.7% | top-5 >60%; rejections: DUOL,GS,LLY,META,OSCR,SNDK |
| 3 | +2.54% | 0.02 | 14/20 | — | Sortino <0.9 |
| **Agg** | **mean +5.7%** | **mean 0.43** | all ≥9 | all folds top-5 >60% | |

**Kill:** Gate 1 (top-5 concentration >60% every fold; `namesWithRejectionsAndZeroFills` non-empty). Gate 2 (agg Sortino 0.43 ≪ 1.9). Gate 4 (agg +5.7% vs C +59.33%).

**Remedy note:** Credit v2 solved breadth count (14/20) but not concentration or return vs C. Do not raise deployment — book is already low-posture (median deploy ~−3%).

---

### Incumbent Attempt 3 — study `6a2d9195e5a40a29b74c72b9` COMPLETE → **KILL Gate 4**

- **crossFoldRobustSelection:** `4ada0f15103050cb5a02dabb9c6306a4e55f29a1c3a35b3273ee680cb591abaf`
- **Assembled book:** `6a2d93e2e5a40a29b74c75f3` — top-16 LEAP, **5% BP** (down from 45–55%), TP 150%, roll DTE 33
- WF cert agg OOS: mean **+24.4%** return, mean **1.50** Sortino
- **Key finding:** Lower per-name allocation (5% vs 45–55%) **breaks the Gate-1 breadth ceiling** — first regime-switched cert with direct OOS breadth ≥16 every fold.

**Direct OOS (assembled book):**

| Fold | Return | Sortino | Breadth | vs C return | vs C Sortino |
|------|--------|---------|---------|-------------|--------------|
| 0 | +38.77% | 2.32 | **17/20** | beats +24.17% | beats 1.47 |
| 1 | +53.64% | 2.84 | **17/20** | beats +8.78% | beats 0.64 |
| 2 | +22.18% | 1.25 | **16/20** | loses vs +66.87% | loses vs 5.60 |
| 3 | +21.04% | 1.25 | **16/20** | loses vs +137.51% | loses vs 4.37 |
| **Agg** | **mean +33.9%** | **mean 1.91** | all ≥16 | loses vs +59.33% | loses vs 3.02 |

Gate 1 breadth count: **PASS** (16–17/20 all folds). Minor flags: `namesWithRejectionsAndZeroFills` (ANET/AVGO etc.), SNDK zero attempts — not binding vs Gate 4.  
Gate 2 Sortino floor: **PASS** (agg 1.91 ≥ 1.9; all folds ≥ 0.9).  
Gate 5 maxDD: **PASS** (worst 23.4%).  
Gate 6 posture: **PASS** (fold-3 median deploy 21.4%, max 32.8%).

**Kill:** Gate 4 — assembled-book agg OOS +33.9% / Sortino 1.91 **does not beat frozen Baseline C** (+59.33% / 3.02); folds 2–3 lose C on both return and Sortino.

**Remedy note:** Breadth fix (lower BP) trades away C-level convexity. Do not revert to high-BP configs — those fail Gate 1. Need a distinct mechanism or structure change, not allocation tuning alone.

---

### Additional session 3 status

| Study | Family | Status |
|-------|--------|--------|
| `6a2d919508bb1349f5b64b9b` | D calendar | ERROR fold 0 (NoEligibleCandidate) |
| `6a2d9196daff5c67a9716bb9` | A v2 Attempt 5 | ERROR fold 1 (NoEligibleCandidate) |
| `6a2d93dce5a40a29b74c75da` | A v2 Attempt 6 | RUNNING |

## Updated binding constraint

1. **High-BP regime-switched LEAP:** Gate 1 breadth (6–8/20 direct OOS) — unchanged.
2. **Low-BP regime-switched LEAP (Attempt 3):** Gate 1 breadth **solved** (16–17/20), but **Gate 4 vs C fails** — cannot match incumbent return/Sortino bar with deployable breadth.
3. **Credit v2:** Gate 1 count OK (14/20) but concentration + return/Sortino fail.

**Verdict:** Campaign IN PROGRESS — **6+ complete certifications**, **zero gate-passing finalists**. Lockbox untouched. No deploy sign-off.

---

## Session 4 — Next-wave certifications (2026-06-13T17:45Z)

### Family A Attempt 6 — ERROR (fold 0)
- Study `6a2d93dce5a40a29b74c75da` — NoEligibleCandidate on fold 0 validation (same failure mode as Attempts 5/6).

### New certifications launched

| Study | Family | Seed | Grid | Status |
|-------|--------|------|------|--------|
| `6a2d96e2daff5c67a97174e7` | Incumbent Attempt 4 | `6a2d8af4e5a40a29b74c66d8` | top 12/14/16 × BP 6/7/8 × TP 100/150/200 × roll 45/60 | RUNNING (fold 0 optimizing) |
| `6a2d96e2daff5c67a97174dc` | A v2 Attempt 7 | `6a2d9188daff5c67a9716b89` | top 10/12/14 × BP 4/5/6 × roll 33/45/60 (no TP gene) | RUNNING (fold 0 optimizing) |
| `6a2d96ee08bb1349f5b65596` | D Attempt 2 (CODEX diagonal) | `6a2d905908bb1349f5b648f7` | incl. TP gene | **ERROR** — TP gene mismatch |
| `6a2d974edaff5c67a97175fe` | D Attempt 3 (CODEX diagonal) | `6a2d905908bb1349f5b648f7` | BP 20/35/55 × top 8/10/12 × roll 30/45/60 × DTE brackets | RUNNING (queued) |

### Attempt 4 rationale
Attempt 3 (5% BP) fixed Gate-1 breadth (16–17/20) but **KILL Gate 4** (+33.9% vs C +59.33%). Attempt 4 probes **6–8% BP** — the Pareto frontier between Attempt 3 (breadth) and high-BP configs (return, 6–8/20 breadth).

### Best candidate so far (direct OOS, assembled book)
**Incumbent Attempt 3** book `6a2d93e2e5a40a29b74c75f3`: agg **+33.9% / Sortino 1.91**, breadth **16–17/20**, passes Gates 1/2/5/6, **fails Gate 4 vs C**.

### Next actions (auto-continue)
1. Poll Attempt 4 → assembled book → direct OOS gates (priority).
2. Poll Attempt 7 / D Attempt 3 for certification completion or ERROR.
3. If Attempt 4 completes: compare breadth vs Attempt 3 on same direct-OOS protocol.
4. Lockbox remains **untouched** until a gate-clean finalist exists.
