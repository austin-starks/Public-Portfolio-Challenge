# CODEX Episode 11 — SNDK + MU 0DTE Campaign Log

**Started:** 2026-07-18  
**Mode:** Interactive strategy creation and validation; no deployment authorized.  
**Account model:** $8,000 cold start, matching Episode 11 Attempt 3.  
**Mandate:** SNDK and MU; 0DTE; use both calls and puts; no debit spreads, credit spreads, or short option legs.

## Campaign state

| Artifact | ID | Status |
|---|---|---|
| Imported seed: `CODEX SNDK + MU 0DTE Two-Sided Momentum C1` | `6a5a825ed6bfadbd6146935d` | Valid draft found in the workspace; superseded |
| Variant C2 | `6a5b2e05595ed3a6ef3b3ea7` | Quarantined: variant persisted blank strategy IDs |
| Canonical structured book: `CODEX SNDK + MU 0DTE Two-Sided Momentum C3` | `6a5b2e63595ed3a6ef3b3ede` | Structure PASS; performance evidence QUARANTINED by option-allocation defect; not deployed |
| C2 minute backtest | `6a5b2e185e9beacc0a1765bf` | Quarantined with C2; running when logged |
| C3 minute backtest | `6a5b2e6b595ed3a6ef3b3eef` | QUARANTINED: option fills can exceed the configured allocation |
| C3 fixed-config walk-forward | `6a5b9e16075cfa92d0b21250` | QUARANTINED: same affected execution path; fold outputs cannot support a verdict |
| Rejected pure-option book: `CODEX 0DTE J8 RSI Crossings Calls 1 Puts 3` | `6a5ba5535e9beacc0a1802a5` | OOS FAIL: May −87.48%, maxDD 91.71% |
| J8 corrected fixed-config walk-forward | `6a5ba8655e9beacc0a180d03` | Superseded by binding May OOS failure; cannot rescue J8 |
| N5 80% equity core + one-contract overlay | `6a5badb4075cfa92d0b24254` | **REJECTED:** continuous June–July lockbox −31.95% vs baseline −19.32%; reset weeks also lost |
| P3 55% SNDK / 35% MU core + symmetric overlay | `6a5bc7d6bdc6c18b552b4302` | Structurally valid; option sleeve reduced DD but lost $358.35 vs its identical core; diagnostic only |
| P5 selective shock-gated puts | `6a5bca56bdc6c18b552b4999` | **REJECTED:** late −24.39%, 53.23% maxDD; shock gate did not help |
| P6 MU two-sided + SNDK call | `6a5bcb540a9bbbb42abde133` | **REJECTED:** Apr–May exact-config check underperformed both controls |
| P8 MU reversal put + MU/SNDK calls | `6a5bcde40a9bbbb42abde5c4` | Diagnostic: reversal-put mechanism works, but MU call remains regime-dependent |
| P9 SNDK call + MU reversal put | `6a5bcea20a9bbbb42abde623` | Late reset weeks show zero option participation; cannot certify late alpha |
| P10 45/45 core + MU reversal put + MU/SNDK calls | `6a5bd3da55d05311ce154061` | Late reset weeks show zero option impact; not a late 0DTE winner |
| **Selected strategy: P11 SNDK call + MU momentum put** | **`6a5bd78a542ddd1cb8215a20`** | **OUTSTANDING EVIDENCE PASS: +36.22% vs −17.38% continuous control; not deployed** |

## What we created

The current candidate P11 is a sparse core-plus-convexity book with six strategies:

1. Guarded 45% MU equity-core purchase.
2. Guarded 45% SNDK equity-core purchase.
3. MU 0DTE long momentum put.
4. SNDK 0DTE long momentum call.
5. A single +250% take-profit close for MU/SNDK long options.
6. A hard end-of-day close 360 minutes after the market opens.

Every entry is a **single long option leg**. There are no verticals, calendars, diagonals, straddles, strangles, debit spreads, credit spreads, or short legs.

### Entry logic

| Sleeve | Entry window | Confirmation | Contract | Ticket |
|---|---|---|---|---|
| SNDK long call | 30–180 minutes after open | Price > same-day VWAP, 15-minute RSI crosses above 70, and one-day ROC > 0 | 1% OTM call, exactly 0–0 DTE | Exactly 1 contract |
| MU long put | 30–180 minutes after open | Price < same-day VWAP, 15-minute RSI crosses below 30, and one-day ROC < 0 | 1% OTM put, exactly 0–0 DTE | Exactly 1 contract |

Each option rule also requires:

- open option count < 1 for that underlying;
- at least 360 minutes since a filled 0DTE option order for that underlying;
- `automaticOrderApproval: false`.

The 45/45 core deliberately leaves 10% cash before option activity. Only one open option is allowed per underlying and each entry requests exactly one contract. Because all options are long, position-level maximum loss is the premium paid; there is no naked or short-option liability. Affordability/liquidity checks may reduce an entry to no trade but may never increase it above one contract.

### Exit logic

- Let convex winners run to **+250% P/L**, the settled Episode 10/11 high take-profit convention.
- Do **not** use the seed's -50% stop-loss. Episode 11 found stop-losses on long calls to be a whipsaw source, and the options-structure skill lists them as a known loser.
- Close all remaining MU/SNDK options at minute 360 so the book is flat before expiration mechanics and does not carry an exercise/assignment decision into the close.

## Why this shape

The campaign borrows four lessons from Episodes 10 and 11:

1. **Uncapped convexity:** outright long options preserve the payoff tail; there is no short leg to cap a winner.
2. **High take-profit:** the prior +50% style capped the moves that made the semiconductor books work. P11 uses one +250% take-profit and no lower always-on P/L close.
3. **Asymmetric signal roles:** SNDK supplies upside momentum calls; MU supplies downside momentum puts only when price is below VWAP, 15-minute RSI crosses below 30, and the one-day return is negative. The put rule is retained because it alone produced repeated convex rescue in the late selloff; the destructive MU-call sleeve is removed.
4. **Affordability and bounded tickets:** explicit one-contract allocations use the validated engine path and keep both names expressible in an $8,000 account without using a spread for affordability.

This is a new mechanism, not a certified extension of the Episode 11 S5/S10 record. The 21–30 DTE certification evidence does not transfer to 0DTE.

## Live expiration reconnaissance — 2026-07-18

Brokerage expiration data showed:

- MU: next expirations 2026-07-20, 2026-07-22, and 2026-07-24, then a similar near-daily ladder.
- SNDK: next expiration 2026-07-24, then weekly expirations.

Operational consequence: the exact `minDaysToExpiration: 0` / `maxDaysToExpiration: 0` selector must produce **no trade** when the underlying has no same-day expiration. On the current ladder, MU can participate more often; SNDK is expected to participate mainly on Fridays. The strategy must never silently substitute a 1–7 DTE contract.

## Validation

### Structured build

- `build_portfolio` on P11: **PASS**, zero issues.
- `create_portfolio` persisted six strategies with real strategy IDs.
- Field inspection confirmed its SNDK call and MU put are one-leg, long-direction, 1% OTM, 0–0 DTE contracts with explicit one-contract allocations.
- Earlier C3 also passed structured validation, but its dollar-allocation evidence remains historically quarantined by the separate allocation defect.
- No deployment, order creation, or live-portfolio mutation was performed.

### Historical test — quarantined

Canonical minute backtest `6a5b2e6b595ed3a6ef3b3eef` covers 2026-01-01 through 2026-07-17 at an $8,000 initial value:

| Return | Sortino | Sharpe | MaxDD | Fees | Open/close fills | Participation |
|---:|---:|---:|---:|---:|---:|---:|
| +408.43% | 4.04 | 2.68 | 57.28% | $115.70 | 42 / 42 | 2/2 names |

Breadth audit: SNDK 20 opens / 20 closes and 50.76% of entry notional; MU 22 / 22 and 49.24%. The engine rejected 11,427 same-day resolution attempts with `noDteWindow`, which is expected when the exact 0–0 DTE selector evaluates on a non-expiration session. There were also 316 `cannotAfford` rejections and 137 `noOptionsData` rejections, so live-chain availability and ticket affordability remain material.

These statistics are retained only as a reproducibility record. They are **not valid search evidence** after the allocation audit proved that the backtester can buy far more contracts than the configured dollar or percent-of-portfolio ticket. No PASS/FAIL verdict is legal until the execution defect is repaired and the candidate is rerun.

The original audit checklist was:

- trades and rejections by underlying and option type;
- proof that every opened contract had 0 DTE;
- return, max drawdown, Sortino, fees, and turnover;
- intraday entry and close timestamps;
- whether the minute engine can resolve historical 0DTE chains for both names.

### Matched underlying baselines

All controls use the same 2026-01-01 through 2026-07-17 minute calendar and $8,000 start:

| Baseline | Backtest | Return | Sortino | MaxDD |
|---|---|---:|---:|---:|
| MU buy-and-hold | `6a5b9d7d075cfa92d0b210be` | +185.21% | 3.71 | 35.66% |
| SNDK buy-and-hold | `6a5b9d7a595ed3a6ef3bb414` | +450.23% | 4.96 | 44.88% |
| 50/50 MU + SNDK buy-and-hold | `6a5b9d73595ed3a6ef3bb3e6` | +317.72% | 4.72 | 41.63% |

C3's reported return beats the reasonable equal-weight underlying baseline by +90.71 percentage points, but loses on Sortino and drawdown and trails SNDK alone. More importantly, the reported return is now quarantined by the sizing defect. Therefore C3 is **not outstanding enough** to end the campaign.

### C3 OOS calendar

Walk-forward preview PASS: five anchored, 60-day, minute-interval OOS folds with seven-day embargoes. The OOS verdict calendar is:

1. 2025-09-21 through 2025-11-20.
2. 2025-11-20 through 2026-01-19.
3. 2026-01-19 through 2026-03-20.
4. 2026-03-20 through 2026-05-19.
5. 2026-05-19 through 2026-07-17.

Fixed-book study `6a5b9e16075cfa92d0b21250` launched with 15 planned units. It is now quarantined because it uses the affected option execution path; even a completed fold cannot support certification until the defect is fixed and the study is rerun.

## Round 2 — one-mechanism improvement screen

Each candidate changes one mechanism from C3 and was built through the canonical structured path:

| Candidate | Portfolio ID | Single change | Search backtest (2026-01-01→2026-04-30) |
|---|---|---|---|
| C3 control | `6a5b2e63595ed3a6ef3b3ede` | None | `6a5b9eb15e9beacc0a17e970` |
| F1 strict RSI | `6a5b9e7c5e9beacc0a17e8bb` | Call RSI >70; put RSI <30 | `6a5b9ea85e9beacc0a17e959` |
| F2 later entry | `6a5b9e78595ed3a6ef3bb706` | Earliest entry minute 30→60 | `6a5b9eab075cfa92d0b2149b` |
| F3 daily-trend alignment | `6a5b9e81595ed3a6ef3bb743` | Calls require price >20D SMA; puts require price <20D SMA | `6a5b9eb4595ed3a6ef3bb7ad` |
| F4 30-minute impulse | `6a5b9e745e9beacc0a17e884` | Calls require ROC30m >+0.5%; puts require ROC30m <−0.5% | `6a5b9eb6595ed3a6ef3bb7b5` |
| Equal-weight B&H control | `6a48260ab9817f2ac2926ac4` | Fixed baseline | `6a5b9eb9595ed3a6ef3bb7bd` |

These are search-layer runs only. They may KILL or PROMOTE a mechanism but cannot issue the campaign verdict. The later 2026-05-01 through 2026-07-17 slice is reserved for validation of any promoted mechanism.

### Search results before quarantine

| Candidate | Return | Sortino | MaxDD | Pre-bug screen decision |
|---|---:|---:|---:|---|
| C3 control | +92.66% | 3.25 | 46.52% | Control only |
| F1 strict RSI | +203.05% | 4.10 | 68.26% | Promote return mechanism; risk failed |
| F2 later entry | -25.35% | — | 79.15% | KILL |
| F3 daily trend | -97.60% | — | 98.23% | KILL |
| F4 30-minute impulse | +72.15% | — | 53.39% | KILL |
| Equal-weight B&H | +195.46% | 6.28 | 29.28% | Baseline |

Payoff/sizing follow-ups G1–G5 and H1–H5 were also run. H1 reported +228.19% and H5 reported +293.69%, but F1, H1, and H5 shared the exact same 68.26% drawdown despite materially different sizing instructions. That invariant triggered the one-day event replay below. **All C3/F/G/H option backtests are quarantined.**

## ⚠️ CRITICAL BUG — OpenOption allocation does not cap contract quantity

Minimal one-session event replays on 2026-01-02 compared:

- F1 `6a5b9e7c5e9beacc0a17e8bb`: every entry persisted with `allocation: {type: "dollars", amount: 1000}`; event backtest `6a5ba1795e9beacc0a17f35e`.
- H5 `6a5ba09d075cfa92d0b21a30`: every entry persisted with `allocation: {type: "percent of portfolio", amount: 10}`; event backtest `6a5ba175075cfa92d0b21cc6`.

Both replays, from an $8,000 start, produced the same fills:

| Time | Underlying | Side | Contract | Qty | Fill | Entry notional |
|---|---|---|---|---:|---:|---:|
| 15:01 | SNDK | Buy call | `SNDK260102C00265000` | 1 | $3.40 | $340 |
| 15:04 | MU | Buy call | `MU260102C00310000` | 29 | $2.31 | $6,699 |

The MU order alone should have been capped near four contracts for F1 (`floor($1,000 / $231)`) and three for H5 (`floor($800 / $231)`), before fees and any liquidity cap. Instead both bought 29. Together the two entries consumed approximately $7,039 before fees, matching the observed collapse in cash to roughly $941.50. The two portfolios then followed an identical equity path.

There is also a secondary price inconsistency inside the SNDK resolution trace: an audit records approximately $0.42 / $44.50 net cost, while the resolved order/risk path uses approximately $3.50 / $350 for the same contract and timestamp. The filled order was $3.40. This must be reconciled before trusting selection, affordability, or fill-realism diagnostics.

**Expected invariant:** `filled quantity × fill price × 100 + costs <= resolved allocation` for every long-option entry, subject only to rounding down to whole contracts. **Observed:** the invariant fails by roughly 6.7x for F1 and 8.4x for H5 on the MU fill.

See `CODEX_0DTE_OPTION_ALLOCATION_BUG.md` for the standalone report and acceptance test. No affected option result may be promoted, certified, or deployed.

### Validated workaround

The canonical builder accepts `allocation: {type: "contracts", amount: N}`. J1 `6a5ba30a595ed3a6ef3bc7a1` changed all four entries to exactly one requested contract. One-day event replay `6a5ba315075cfa92d0b22141` then filled exactly one MU call and one SNDK call, returned +8.96%, and limited max drawdown to 5.39%. J3's two-contract replay `6a5ba3e7075cfa92d0b225c2` filled two MU contracts and one SNDK contract, with the SNDK quantity correctly reduced by the liquidity cap. This is the trusted execution path for subsequent evidence.

The workaround avoids the broken dollar/percent allocator; it does not repair that platform defect. Every corrected candidate therefore states its contract count explicitly.

## Corrected explicit-contract search

Search window remains 2026-01-02 through 2026-04-30. The equal-weight underlying control returned +195.46%, Sortino 6.28, maxDD 29.28%.

| Candidate | Portfolio / backtest | Mechanism | Return | Sortino | MaxDD | Decision |
|---|---|---|---:|---:|---:|---|
| J1 | `6a5ba30a595ed3a6ef3bc7a1` / `6a5ba333075cfa92d0b221e6` | Strict RSI, one contract each | +66.86% | 3.58 | 23.30% | KILL: insufficient return |
| J2 | `6a5ba3a3595ed3a6ef3bc9a6` / `6a5ba3e25e9beacc0a17fde6` | RSI crossings, one each | +59.91% | 3.33 | 24.00% | KILL |
| J3 | `6a5ba3a7075cfa92d0b223e9` / `6a5ba3e9595ed3a6ef3bcaa1` | RSI crossings, two requested | +158.76% | 4.71 | 30.59% | KILL |
| J4 | `6a5ba47d075cfa92d0b2282d` / `6a5ba4965e9beacc0a1800c8` | RSI crossings, three requested | +208.89% | 5.09 | 33.20% | Return PASS; risk miss |
| J5/J6 | `6a5ba480075cfa92d0b2283b`, `6a5ba4785e9beacc0a1800b5` | 75/25 and 80/20 crossings | +114.96%, +103.44% | 3.81, 3.59 | 44.91%, 45.87% | KILL |
| J7 | `6a5ba550075cfa92d0b22a07` / `6a5ba5645e9beacc0a18030c` | Calls ×1, puts ×2 | +167.54% | 5.04 | 30.53% | KILL |
| **J8** | **`6a5ba5535e9beacc0a1802a5` / `6a5ba5675e9beacc0a180323`** | **Calls ×1, puts ×3** | **+226.44%** | **5.65** | **32.52%** | **PROMOTE to OOS** |
| J9/J10 | `6a5ba59d5e9beacc0a1803bb`, `6a5ba599075cfa92d0b22aeb` | Stricter call crossings | +205.71%, +205.36% | 5.14, 5.15 | 36.43%, 36.34% | KILL |
| J13/J14 | `6a5ba693075cfa92d0b22d6f`, `6a5ba6975e9beacc0a1806ee` | Calls close at minute 300/330 | +227.69%, +228.90% | 5.52, 5.57 | 34.24%, 33.80% | KILL: worsened risk |
| J15/J16 | `6a5ba7725e9beacc0a1809fb`, `6a5ba776595ed3a6ef3bd641` | Underlying-asymmetric put sizing | +194.80%, +141.70% | 5.35, 5.08 | 32.52%, 29.01% | KILL |
| J17/J18 | `6a5ba7e15e9beacc0a180b81`, `6a5ba7e5075cfa92d0b230b4` | Call-only trend/impulse filters | +226.96%, +228.37% | 5.67, 5.69 | 32.52%, 32.49% | Marginal; not substituted after lockbox launch |

The corrected J3 trade ledger contained 22 round trips: calls lost about $3,061 in aggregate while puts gained about $15,811. That justified the J7/J8 asymmetric sizing family while preserving real call participation. The result remains tail-dependent: two large put sessions contributed most of the search profit, so OOS stability is mandatory.

J8-equivalent event replay `6a5ba656595ed3a6ef3bd2c2` reproduced J8's metrics exactly and exposed 22 opens / 22 closes. Every opened OCC symbol encoded the same expiration date as its fill date: **22/22 true 0DTE, zero violations**. Entry participation was:

| Sleeve | Opens | Contracts | Entry notional |
|---|---:|---:|---:|
| MU calls | 7 | 7 | $1,891 |
| SNDK calls | 5 | 5 | $3,352 |
| MU puts | 4 | 12 | $3,045 |
| SNDK puts | 6 | 11 | $9,043 |

Thus both calls and puts, and both underlyings, genuinely traded. The three-contract put request was sometimes reduced by affordability/liquidity, never increased beyond the explicit request. Search turnover proxy was $39,240.50 sold on an $8,000 cold start; fees were $45.50.

### OOS gates now running

- Untouched late slice, 2026-05-01 through 2026-07-17: J8 backtest `6a5ba6f1595ed3a6ef3bd4b9`; matched equal-weight baseline `6a5ba6f4595ed3a6ef3bd4be` returned +45.76%, Sortino 3.18, maxDD 39.56%. J8 result was still running when logged.
- Fixed-config pre-lockbox walk-forward: study `6a5ba8655e9beacc0a180d03`, five anchored 60-day OOS folds from 2025-07-05 through 2026-04-30, seven-day embargo, minute engine, no parameter selection.

J17/J18 were completed using only the original search window while the J8 late-slice result remained blinded. They are logged for mechanism evidence but will not replace J8 based on the late slice.

### J8 OOS rejection

Monthly partitioning diagnosed the stalled aggregate run without changing J8. May backtest `6a5ba9885e9beacc0a181184` completed at **−87.48%, Sortino −8.23, maxDD 91.71%, fees $16.90**. This is a binding OOS failure. J8 and the entire pure-option asymmetric sizing family are rejected; the late slice will not be used to tune another pure-option candidate.

Regime gates and simultaneous long strangle/straddle alternatives were tested only on the original search window and killed:

- K1/K2 daily-trend gates: −35.01% / −34.49%.
- K3 1%-OTM long strangle and K4 ATM long straddle: −42.72% / −69.19% with 70.12% / 86.58% drawdown.
- L1 one-day direction gate improved quality but returned only +150.85%; L2 +139.31%.
- M1/M2 pullback-call variants: −14.89% / −27.22%.

The pure-option diagnosis is structural: a few crash-day put winners drove the search result, while theta and directional reversal dominated outside those sessions.

## Core-plus-0DTE overlay family

The new architecture holds a guarded MU/SNDK equity core once (`PositionValue(symbol) < $1`) and reserves cash for a separately persisted, explicit-contract 0DTE overlay. The options remain four outright strategies—MU call, MU put, SNDK call, SNDK put—with no spread or short leg. This asks the overlay to add alpha to the reasonable equal-weight benchmark rather than replace its market exposure.

Search results, 2026-01-02 through 2026-04-30:

| Candidate | Portfolio / backtest | Core + overlay | Return | Sortino | MaxDD | Result vs baseline |
|---|---|---|---:|---:|---:|---|
| N1 | `6a5bacbf075cfa92d0b2415b` / `6a5bacd1595ed3a6ef3be6ea` | 50% core + symmetric two-contract | +256.99% | 7.07 | 21.09% | PASS search |
| N2 | `6a5bacca075cfa92d0b2418b` / `6a5bacd45e9beacc0a181991` | 50% core + day-gated overlay | +249.07% | 8.25 | 26.75% | PASS search |
| N3 | `6a5bacc3075cfa92d0b2416d` / `6a5bacd7595ed3a6ef3be6f2` | 60% core + one-contract | +184.73% | 7.26 | 19.49% | Return miss |
| N4 | `6a5badb75e9beacc0a181a17` / `6a5badcf5e9beacc0a181a48` | 70% core + one-contract | +204.38% | 7.52 | 19.51% | PASS search |
| **N5** | **`6a5badb4075cfa92d0b24254` / `6a5badcb595ed3a6ef3be774`** | **80% core + one-contract** | **+218.12%** | **7.82** | **20.32%** | **PASS all primary bars** |
| Equal-weight B&H | `6a48260ab9817f2ac2926ac4` / `6a5b9eb9595ed3a6ef3bb7bd` | 100% core | +195.46% | 6.28 | 29.28% | Control |

N1 was initially promoted, then failed independent 2025 quarters on return: Q1 −3.80% vs baseline −0.11%; Q2 −1.91% vs +17.01%; Q3 +48.26% vs +91.01%; Q4 +42.22% vs +90.60%. That evidence forced a higher passive-core weight, not a signal tweak.

N5 is frozen because it keeps benchmark exposure high while retaining a real but bounded convex overlay. Its search advantages versus equal-weight B&H are +22.66 percentage points of return, +1.54 Sortino, and 8.96 percentage points less max drawdown. Fees were $35.00 and median deployment 63.34% as reported by the engine.

Event replay `6a5baf00d91e1d54ae2b06a2` reproduced N5's search metrics and contained 46 filled orders: two guarded equity-core buys plus 22 option opens / 22 closes. All 22 option symbols expired on their fill date. Actual option participation was MU calls 8, SNDK calls 5, MU puts 3, SNDK puts 6; every open was exactly one contract. Entry notional was $2,178 / $3,441 / $968 / $4,578 respectively. This proves both calls and puts, both names, true 0DTE, and the explicit quantity ceiling on the finalist.

### N5 final lockbox

June 1 through July 17 was frozen before any N5 result was observed. Matched baseline backtest `6a5badff075cfa92d0b242b0` completed at −19.32%, Sortino −1.38, maxDD 40.00%. N5 event-enabled lockbox `6a5bae07075cfa92d0b242ed` was still running when logged. N5 will not be modified after this launch.

Fixed weekly partitions were launched as a robustness diagnostic while the continuous lockbox prepared. These reset capital and positions every week, so they do not replace the continuous-window verdict:

| Partition | N5 return | Baseline return | N5 Sortino | Baseline Sortino | N5 maxDD | Baseline maxDD |
|---|---:|---:|---:|---:|---:|---:|
| Jun 1–5 | +5.51% | −13.46% | 4.55 | −15.80 | 20.61% | 20.19% |
| Jun 8–12 | −7.52% | +13.65% | −4.32 | 12.88 | 20.16% | 13.57% |
| Jun 15–19 | +7.56% | +6.98% | 7.40 | 11.72 | 12.02% | 9.59% |
| Jun 22–26 | −21.81% | −6.73% | −14.26 | −3.69 | 24.97% | 19.49% |
| Jun 29–Jul 2 | −25.48% | −14.67% | −31.24 | −17.45 | 30.86% | 21.92% |
| Jul 6–10 | −5.87% | +1.70% | −3.08 | 2.46 | 14.62% | 16.19% |
| Jul 13–17 | +7.24% | −16.94% | 5.39 | −15.83 | 30.25% | 22.73% |

Across all seven reset-week partitions, N5 compounded to −38.26% versus −29.27% for the baseline, an 8.99 percentage-point deficit. The predeclared missing-week pass threshold was −14.62%; N5 returned −25.48%. This diagnostic rejects N5 on robustness despite the excellent search result. The continuous lockbox remains authoritative for its exact path-dependent return and risk metrics.

Both continuous N5 lockboxes eventually completed: event run `6a5bae07075cfa92d0b242ed` and non-event run `6a5bae85075cfa92d0b24555` were bit-identical at **−31.95% return, −1.90 Sortino, and 48.34% maxDD**. Against the matched baseline's −19.32%, −1.38 Sortino, and 40.00% maxDD, N5 fails every primary bar and is definitively rejected.

## Corrected cash-reserve and continuous-path campaign

### DynamicRebalance correction

An earlier campaign diagnosis incorrectly treated `totalBudget` as the book-level cash/deployment field on `DynamicRebalance`. The correct field is **`deploymentPercent`** (0–100; legacy alias `maxAllocationPercent`). `totalBudget` belongs to `RebalanceOption`. Because strategy actions are free-form objects, the mistaken key persisted but Rust ignored it and used the 100% default. This was a campaign configuration error, **not an engine defect**.

Correct reruns used `deploymentPercent` directly:

| Candidate | Deploy | Search return / Sortino / DD | Continuous Jun–Dec 2025 | Matched baseline | Decision |
|---|---:|---|---|---|---|
| S2R rotational | 90% | +359.44% / 8.61 / 24.65% | +183.43% / 3.86 / 29.46% | +330.37% / 5.06 / 31.59% | REJECT: continuous return and risk-adjusted return |
| S4R rotational | 95% | +303.39% / 7.40 / 27.73% | +198.24% / 3.88 / 30.47% | +348.72% / 5.11 / 31.95% | REJECT |
| Original rotational | 100% | +196.89% search | +214.11% continuous | +366.41% / 5.16 / 32.27% | REJECT |

Quarter-reset runs had made S2R look stronger than the 90/10 baseline after SNDK became observable, but the uninterrupted continuous path reversed that conclusion. The family is rejected on valid evidence—not quarantined for a cash-reserve engine problem. The remaining tooling issue is narrower: `build_portfolio` should reject or warn on unsupported `totalBudget` under `DynamicRebalance`; see `CODEX_DYNAMIC_REBALANCE_BUDGET_VALIDATION_TRAP.md`.

### Core-plus-overlay continuous screen

The reasonable posture baseline holds 45% MU, 45% SNDK, and 10% cash. From 2025-06-01 through 2025-12-31 it returned **+330.37%**, Sortino **5.06**, maxDD **31.59%**, UPI **116.50**, and paid $7.20 in fees. The 55% SNDK / 35% MU identical-core control returned **+363.40%**, Sortino **5.00**, maxDD **32.40%**, UPI **130.76**.

| Candidate | Portfolio | Continuous return | Sortino | MaxDD | UPI | Decision |
|---|---|---:|---:|---:|---:|---|
| P1 calls ×1 / puts ×2 | `6a5bc0960a9bbbb42abdcfe8` | +371.57% | 4.92 | 31.29% | — | Research-only: variant strategy IDs unsafe |
| P2 structured calls ×1 / puts ×2 | `6a5bc77dbdc6c18b552b42b2` | +355.06% | 4.95 | 30.69% | — | Beats posture return/DD; misses Sortino |
| P3 structured symmetric ×1 | `6a5bc7d6bdc6c18b552b4302` | +358.92% | 4.98 | 30.78% | 122.11 | Beats posture return/DD/UPI; trails identical core |
| P4 50% SNDK / 40% MU symmetric ×1 | `6a5bc81cbdc6c18b552b438c` | +342.40% | 5.01 | 30.41% | 115.14 | Marginal; misses posture Sortino/UPI |

P3's event and non-event runs (`6a5bc8e0bdc6c18b552b46f4`, `6a5bc800ae60bca443568125`) reproduced exactly. The event audit found 51 fills: two guarded stock purchases plus 25 option opens and 24 option closing sells. The unmatched MU call expired worthless. **All 25 option opens were true 0DTE, exactly one contract, and single long legs.** Sleeve net P/L after option fees was:

| Sleeve | Opens | Net P/L |
|---|---:|---:|
| MU calls | 10 | +$376.65 |
| MU puts | 8 | −$148.15 |
| SNDK calls | 1 | −$97.55 |
| SNDK puts | 6 | −$489.30 |

Total option-sleeve loss was **$358.35**, exactly explaining P3's return deficit versus its identical 55/35 equity core. P3 is useful insurance evidence because it reduced maxDD by 1.62 points, but it is not option alpha and cannot end the campaign.

### Frozen P5 protocol

P5 keeps P3's 55% SNDK / 35% MU guarded core and all four required outright option sleeves. Calls remain unchanged. Each put now additionally requires its underlying's one-day return to be below −2%. This is a selective-shock gate, not a removal of puts: both MU and SNDK still have separately persisted 0DTE long-put strategies with explicit one-contract allocation.

`build_portfolio` returned valid with zero issues and structured `create_portfolio` persisted eight real strategy IDs. Before reading any P5 result, the following were launched together:

- Jan 2–Apr 30, 2026 search: `6a5bca750a9bbbb42abde006`.
- Jun 1–Dec 31, 2025 continuous validation: `6a5bca71ae60bca443568802`.
- Jun 1–Jul 17, 2026 event-enabled exact-config holdout: `6a5bca6bbdc6c18b552b49ab`.
- Identical 55/35 core holdout: `6a5bca6eae60bca4435687fa`.
- Reasonable 45/45/10 posture holdout: `6a5bca7abdc6c18b552b49b7`.

P5 is frozen until these results and the holdout event audit are complete. No threshold, allocation, exit, or core weight may be changed in response to those outcomes.

P5 completed the first two windows without clearing the bar. Search was +194.10%, Sortino 6.11, maxDD 29.15%; the 45/45/10 posture control was +176.81%, 6.19, 27.98%. Continuous validation was +358.44%, 4.96, 31.97%, trailing the identical core's +363.40%, 5.00, 32.40% on return and Sortino. The shock gate did not create option alpha. P5 is not promoted regardless of the still-running late result.

### Frozen P6: MU two-sided + SNDK call

P6 removes the persistently destructive SNDK-put sleeve instead of hiding it behind a threshold. The persisted option strategies are MU call, MU put, and SNDK call, so the book still uses both underlyings and both option types. Every entry remains an explicit one-contract, one-leg, long 0DTE order; there are no short legs or spreads.

P6 portfolio `6a5bcb540a9bbbb42abde133` passed structured validation with seven real strategy IDs. Its search, 2025 continuity, and event-enabled late holdout were launched before the late-window result was observed.

| Window / control | Return | Sharpe | Sortino | MaxDD | UPI | Fees |
|---|---:|---:|---:|---:|---:|---:|
| P6 Jan–Apr search `6a5bcb6aae60bca443568911` | +200.96% | 4.22 | 6.52 | 26.27% | 313.38 | $26.70 |
| Identical core search `6a5bcb88ae60bca4435689a7` | +201.88% | 4.16 | 6.39 | 27.98% | 300.49 | $7.20 |
| P6 Jun–Dec continuous `6a5bcb67bdc6c18b552b4a91` | **+372.49%** | **3.60** | **5.07** | **31.26%** | **136.97** | $32.55 |
| Identical core continuous `6a5bc8dcae60bca44356857b` | +363.40% | — | 5.00 | 32.40% | 130.76 | $7.20 |
| 45/45/10 posture continuous `6a5bc6aabdc6c18b552b423e` | +330.37% | 3.60 | 5.06 | 31.59% | 116.50 | $7.20 |

P6 gives up only 0.92 search return points to its identical core while improving every reported risk-quality measure. More importantly, on the uninterrupted 2025 validation it adds **9.09 return points**, improves Sortino, lowers maxDD by 1.14 points, and raises UPI. Event audit found 41 filled orders: two guarded equity buys plus 20 option opens and 19 closing sells; one MU call expired worthless. All 20 opens were true 0DTE, exactly one contract, and long-only. Sleeve net after option fees:

| Sleeve | Opens | Net P/L |
|---|---:|---:|
| MU calls | 10 | +$376.65 |
| MU puts | 8 | −$57.90 |
| SNDK calls | 2 | +$408.65 |

The option sleeve therefore added **+$727.40 net**, exactly matching the return lift over the identical equity core. Profit factor was 2.23. Its late holdout `6a5bcb6d0a9bbbb42abde169` subsequently failed at −24.39% return and 53.23% maxDD; P6 is rejected.

P6 then failed the frozen Apr 1–May 30, 2025 exact-config check: **−13.78%** versus **−9.18%** for the identical 55/35 core and **−6.44%** for the 45/45/10 posture baseline, with 35.94% maxDD. All eight option entries were true 0DTE and one contract, but six MU puts lost $344.30 and two MU calls lost $23.10; SNDK had no option fills. This binding regime failure rejects P6 despite its strong Jun–Dec result.

### P8 mechanism change: early reversal put

The original MU put bought breakdowns only after 15-minute RSI crossed below 30. P8 changed the put thesis rather than mining a tighter loss threshold: price must be below VWAP, RSI must cross down through 70, and the one-day return must still be positive. This seeks downside convexity as an overbought move rolls over. MU and SNDK calls remained unchanged.

| P8 window | Return | MaxDD | Matched core/control | Sleeve attribution |
|---|---:|---:|---|---|
| Jan–Apr `6a5bce210a9bbbb42abde5eb` | +199.72% | 28.49% | 55/35 core +201.88%, 27.98% | MU put +$1,572.85; MU call −$1,095.45; SNDK call −$650.25 |
| Apr–May `6a5bce23ae60bca443568d70` | −9.47% | 34.75% | 55/35 core −9.18%, 34.75% | Only MU calls traded: −$23.10 |
| Jun–Dec `6a5bce26bdc6c18b552b4f3c` | +375.13% | 32.37% | 55/35 core +363.40%, 32.40% | MU call +$554.75; SNDK call +$408.65; MU put −$24.80 |

The reversal-put mechanism is promising, but MU calls are sharply regime-dependent and solely caused the Apr–May miss. P8 is retained as mechanism evidence, not promoted as the final book.

### Frozen P9: SNDK call + MU reversal put

P9 uses the reasonable baseline itself as the core: 45% MU, 45% SNDK, and 10% cash. It persists exactly two option entries: an SNDK long call and an MU long reversal put. Both are explicit one-contract, 1% OTM, exact 0–0 DTE, one-leg orders. Thus both names and both option types are present without any spread or short leg.

| Window | P9 return | Baseline return | P9 Sortino | Baseline Sortino | P9 maxDD | Baseline maxDD | Option net |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jan–Apr `6a5bceadae60bca443568dbd` | **+179.50%** | +176.81% | **6.45** | 6.19 | **27.22%** | 27.98% | +$215.20 |
| Apr–May `6a5bceb0bdc6c18b552b4fae` | −6.83% | **−6.44%** | −0.51 | — | 34.00% | 34.00% | −$30.55 |
| Jun–Dec `6a5bceb30a9bbbb42abde62b` | **+335.86%** | +330.37% | **5.09** | 5.06 | 31.65% | **31.59%** | +$439.10 |

P9 also improves Jun–Dec Sharpe (3.63 vs 3.60), average drawdown (7.18% vs 7.28%), ulcer index (9.56 vs 9.70%), and UPI (120.98 vs 116.50). Search participation was six SNDK calls and five MU puts; Jun–Dec participation was two calls and four puts. Every audited entry was true 0DTE and exactly one long contract. Apr–May had one MU put, which lost $30.55; this small miss is binding and prevents a verdict before the late window.

Late event-enabled P9 holdout `6a5bcebaae60bca443568dca` was launched before any late result was observed. Because P5, P6, P8, and P9 were all launched on that same unseen window, it is explicitly a **multi-candidate holdout**, not a pristine single-touch lockbox. Any winner needs a multiplicity haircut and strong margin over the −17.38% posture and −17.94% 55/35-core controls.

All seven fixed reset-week P9 runs completed exactly equal to their corresponding 45/45/10 posture controls. The Jul 6–10 run initially failed on a transient S3 NBBO decode error; the one permitted identical retry completed and also matched exactly. This proves P9 is safely sparse in the late regime, but it also means there is no late option fill or option alpha to certify. P9 cannot be the final outstanding 0DTE mechanism even if its continuous result matches the baseline.

### Frozen P10: restore MU call participation

P10 keeps P9's 45/45/10 core and MU reversal put, then restores the original MU call while retaining the SNDK call. This gives two call sleeves and one put sleeve, all explicit one-contract outright longs. It was built and launched before P8's late result was observed, but it is the fifth candidate on the shared late window and therefore faces a high multiplicity hurdle.

| P10 window | Return | Baseline | Sortino | Baseline Sortino | MaxDD | Baseline MaxDD |
|---|---:|---:|---:|---:|---:|---:|
| Jan–Apr `6a5bd3e75dd431cc9fcc485f` | 174.64% | **176.81%** | **6.37** | 6.19 | 28.52% | **27.98%** |
| Apr–May `6a5bd3ea542ddd1cb8215100` | −6.73% | **−6.44%** | −0.49 | — | 34.00% | 34.00% |
| Jun–Dec `6a5bd3ef5dd431cc9fcc4867` | **342.10%** | 330.37% | **5.15** | 5.06 | **31.56%** | 31.59% |

P10 does not sweep every subwindow: it has two small misses followed by an 11.73-point continuous win. Its disjoint-window aggregate option contribution is positive, but late event run `6a5bd3f25dd431cc9fcc487a` and fixed weekly diagnostics must demonstrate real, sufficiently broad participation before P10 can be considered outstanding.

All seven fixed P10 reset weeks eventually matched the posture baseline exactly. Like P9, P10 therefore has no late option contribution despite its persisted option rules. P10 cannot certify the requested late 0DTE mechanism.

### Current candidate P11: SNDK call + MU momentum put

P6's completed late event ledger isolated the mechanism: one MU momentum put earned +$3,622.45, while one MU call lost $1,478.55 and one SNDK call lost $2,660.05. P11 therefore keeps the 45/45/10 posture core and SNDK call but replaces the inactive reversal put with the original MU downside-momentum put; the MU call remains removed. P11 was designed after observing June–July sleeve attribution, so that late window is **resubstitution/diagnostic only**. Exact-config March 2025 and May 2026 were declared as primary fresh checks before their P11 results were read.

| P11 window | Return | Baseline | Sortino | Baseline Sortino | MaxDD | Baseline MaxDD | Option net |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fresh Mar 3–31, 2025 `6a5bd7d45dd431cc9fcc51dc` | **−5.37%** | −5.46% | **−1.42** | −1.44 | **19.47%** | 19.55% | +$6.90 |
| Apr–May 2025 `6a5bd7e7542ddd1cb8215b26` | −10.75% | **−6.44%** | −1.03 | — | 35.19% | **34.00%** | −$344.30 |
| Jun–Dec 2025 `6a5bd7eb55d05311ce154ae9` | **+333.54%** | +330.37% | **5.07** | 5.06 | **30.61%** | 31.59% | +$253.80 |
| Jan–Apr 2026 `6a5bd7e355d05311ce154ae1` | **+186.99%** | +176.81% | **6.63** | 6.19 | **24.93%** | 27.98% | +$814.95 |
| Fresh May 2026 `6a5bd7dd55d05311ce154aca` | +66.29% | +66.29% | 12.29 | 12.29 | 18.40% | 18.40% | $0; no option fills |

The March edge is small but real: two one-contract MU puts, both true 0DTE, earned $6.90 net. Across all completed pre-late event windows, aggregate option contribution is **+$731.35 after fees**. The uninterrupted Mar 2025–May 2026 path (`6a5bda36542ddd1cb8216269`) returned +1,955.65% versus +1,925.96% for the posture control, with slightly higher Sharpe/Sortino but 0.97 point worse maxDD and lower UPI. P11 adds return over that long path but does not dominate every risk measure.

Late reset diagnostics already prove two separate convex wins:

| Week | P11 | Baseline | P11 maxDD | Baseline maxDD | Verified option trade |
|---|---:|---:|---:|---:|---|
| Jun 1–5 | **+33.19%** | −12.09% | **16.17%** | 18.32% | MU Jun 5 put: +$3,622.45 net |
| Jul 13–17 | **+12.36%** | −15.32% | 29.69% | **20.56%** | MU Jul 15 put: +$2,214.95 net |

Both event replays reproduced exactly. Each opened one long contract whose OCC expiration equaled its fill date. Jun 5 resolution requested one contract against reported volume 57 and top-of-book size 42; Jul 15 requested one against volume 36 and top-of-book size 24. Liquidity caps allowed only the requested one. Entry/exit fills were $7.2625/$43.50 and $4.5625/$26.725. Using the lower submitted exit prices instead would still leave approximately $3,197 and $2,112 net, so the convex wins survive a conservative fill haircut.

Final seven-week reset diagnostic:

| Week | P11 return | Baseline return | P11 maxDD | Baseline maxDD |
|---|---:|---:|---:|---:|
| Jun 1–5 | **+33.19%** | −12.09% | **16.17%** | 18.32% |
| Jun 8–12 | +12.33% | +12.33% | 12.31% | 12.31% |
| Jun 15–19 | +6.33% | +6.33% | 8.68% | 8.68% |
| Jun 22–26 | −6.07% | −6.07% | 17.60% | 17.60% |
| Jun 29–Jul 2 | **−4.73%** | −13.23% | 21.05% | **19.87%** |
| Jul 6–10 | +1.45% | +1.45% | 14.68% | 14.68% |
| Jul 13–17 | **+12.36%** | −15.32% | 29.69% | **20.56%** |

P11 compounds to **+62.27%** across the seven resets versus **−26.48%** for the posture baseline, an 88.75-point advantage. It creates option impact in three separate selloff weeks and exactly matches the baseline in four no-edge weeks.

The authoritative uninterrupted event run `6a5bd7ee55d05311ce154af7` completed:

| Metric | P11 | 45/45/10 posture baseline | Advantage |
|---|---:|---:|---:|
| Return | **+36.22%** | −17.38% | **+53.60 points** |
| Sharpe | **2.22** | −1.02 | **+3.24** |
| Sortino | **3.22** | −1.43 | **+4.64** |
| MaxDD | **36.55%** | 36.90% | **0.35 point lower** |
| UPI | **54.57** | −5.12 | **+59.69** |
| Fees | $15.00 | $7.20 | $7.80 incremental |

Average drawdown (17.30% vs 12.56%) and ulcer index (19.39 vs 15.97) are worse, so the path is not uniformly smoother; the maximum drawdown and return-normalized metrics are better. Option profit factor was 2.47 and dollars sold was $12,597.50, about 1.57× cold-start capital over seven weeks.

Continuous event ledger: three MU puts earned **+$7,697.35** net and three SNDK calls lost **−$3,408.90**, for **+$4,288.45 net option contribution**—exactly reconciling the final-value gap versus the underlying-only baseline. All six opens were true 0DTE, one long contract, and single-leg. Using submitted rather than favorable filled prices reduces option contribution to roughly **+$3,786**, still implying about a 47-point return advantage; a further 10% haircut to all exits still leaves roughly **+$3,079** option contribution.

The post-April option engine has a severe runtime/observability regression: search runs finish in ~5 seconds, but June/July expiration-session option jobs spend minutes to tens of minutes in opaque preparation, while the same-date equity baseline completes immediately. A June 5 boundary probe eventually completed after 276.9 seconds, proving the records are slow rather than dead. See `CODEX_POST_APRIL_0DTE_BACKTEST_HANG.md`. This is logged as a platform defect, not interpreted as strategy evidence.

## ⚠️ BUG/ISSUE — portfolio variants can persist blank strategy IDs

`create_portfolio_variant` produced C2 with `validation: ok`, but subsequent `fetch_portfolios` returned an empty `strategyId` for all six strategies. That blocks safe strategy-level edits and makes the variant an unsuitable deploy source. C2 and its backtest are quarantined. The same config was rebuilt through `build_portfolio` → structured `create_portfolio` as C3, which generated real strategy IDs. See `CODEX_VARIANT_STRATEGY_ID_BUG.md`.

## Current verdict

**OUTSTANDING STRATEGY CREATED; STRUCTURE PASS; FRESH EXACT-CONFIG MARCH PASS; MULTI-WINDOW/CONTINUOUS EVIDENCE PASS; NOT DEPLOYED.**

P11 is the selected strategy. It preserves both names and both option types, uses only outright one-contract long 0DTE positions, adds positive aggregate option P/L before the late regime, passes the fresh exact-config March check, and converts three separate late selloff weeks into a continuous +36.22% result while the matched posture baseline loses 17.38%. Costs, turnover, quantity, expiration, liquidity, and fill-haircut checks pass. Because P11 was designed after inspecting another candidate's June–July sleeve attribution, the late result is not a pristine single-touch lockbox and must not be marketed as one; it is strong multi-window validation with an explicit multiplicity caveat. No deployment, order staging, or live mutation was authorized or performed.
