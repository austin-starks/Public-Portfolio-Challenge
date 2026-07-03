# Episode 11 / Attempt 3 — SNDK / MU Short-DTE Campaign Log

**Mode:** Interactive discovery (NOT a runbook). Back-and-forth exploration with the human in the loop.
**Started:** 2026-07-03
**Account:** "Experimental Public Portfolio" — `6a45f218e6b1f2131d1f26be`, LIVE on Public brokerage, **$8,000 cash**, zero strategies, clean slate.
**Mandate:** SNDK + MU, short-DTE, high-risk/high-reward. Technicals, fundamentals, and unstructured data all in play.

## Initial prompt (verbatim)

> https://nexustrade.io/portfolio/6a45f218e6b1f2131d1f26be
>
> i want to create a SNDK / MU trading strategy. I only have $8000. i prefer short DTE high-risk, high-reward strategies. Create an agent (with create_agent) that can make this work. Feel free to use technicals, fundamentals, or even unstructured data. keep a CAMPAIGN_LOG.md
>
> this one is NOT a "Runbook". it's an interactive back and forth discovery. Use all of nexustrade's MCP (or create_agent) or both for discovery, testing, and analysis

---

## Hard constraints carried in (options-structure-rules skill)

- Any debit/vertical spread must expire in **≤ ~30 DTE** (short-dated verticals are *candidates*, not banned — but a thin, uncapped-share sleeve failed cert before; width and sleeve share must be instrumented).
- Long-dated (≥120 DTE) = outright calls only. Probably irrelevant here given the mandate is short-DTE.
- Watch the take-profit convexity-cap footgun: no stacked "always" TP closes where the lowest binds first.
- Turnover/fee guardrail matters for short-DTE books — fee churn killed the prior ≤30-DTE sleeve.

## Discovery — 2026-07-03

### Chain reconnaissance (15-DTE monthly, 2026-07-17, live broker data)

| | SNDK | MU |
|---|---|---|
| Spot | $1,762.07 | $977.00 |
| ATM IV | ~122% | ~107% |
| ATM call (mid) | ~$171 ($17.1k/contract) | ~$72 ($7.2k/contract) |
| Furthest listed strike | $2,110 (+20%, 0.26Δ, $5,955) | $1,170+ (+20%, 0.22Δ, $2,345) |
| Weeklies | Yes (8/15/22/29 DTE all listed) | Yes (same ladder) |

**Key finding — affordability wall:** Both underlyings are huge-dollar stocks with ~110%+ IV. On $8k:
- SNDK outright calls are essentially **infeasible** (even +20% OTM at 15 DTE ≈ $6k/contract — one ticket = 75% of the account).
- MU outright calls are marginal: ~0.25Δ ($1,150) ≈ $2.8k/contract.
- **Debit spreads are the only structure that gives both names simultaneous participation.** All ≤30 DTE, so spread-shape compliant. Examples at mid:
  - MU 1050/1150 (15 DTE): ~$25.50 debit → $2,550 risk, $10k width ≈ **2.9:1**
  - SNDK 1950/2100 (15 DTE): ~$37.05 debit → $3,705 risk, $15k width ≈ **3:1**
  - Wide + OTM keeps the reward convex while capping each ticket at ~⅓ of the account.

### Working thesis for structure

2-name book, one wide OTM call debit spread per name (15–30 DTE), signal-gated entries (momentum / news / alt-data), hard per-ticket dollar cap (~$2.5–3.5k ≈ ⅓ of account), single high TP, no stop-loss on longs (known loser). Fee/turnover instrumentation from day one.

### Open questions for the agent / next iterations

1. What entry signal actually works on these two names — price momentum, IV regime, news flow, WSB mentions?
2. 8 vs 15 vs 29 DTE — where does theta bleed vs. gamma payoff net out?
3. One name at a time (concentrate) or both simultaneously (split $8k)?
4. Put spreads too, or calls only? (Mandate says high-risk/high-reward, not long-only.)

### Fundamental / news picture (agent's Stock News Querier, 2026-07-03)

- **MU:** Record FQ3-26 — $41.46B rev (+346% YoY, ~17% beat), EPS $25.11 vs $20.78 est, 84.9% GM; guided FQ4 to ~$50B/$31 EPS. 16 Strategic Customer Agreements lock ≥$100B revenue through 2030 ($22B deposits). BUT: −19.6% off the $1,255 high after the July-1 "Meta Shock" (Meta selling "excess" AI compute → KOSPI −7.9%, SK Hynix −14.6%), a June-25 price-fixing class action, CEO selling $45M stock, and Michael Burry short from $1,051.87. Cantor PT $2,000; consensus PT $1,454, 88% buy.
- **SNDK:** Best S&P 500 performer H1 2026 (~+800%) on NAND shortage; Q1 EPS $23.41 vs $14.17 est, rev +251%. Extremely volatile: −20% (Jun 22–24), +24% single-session bounce, −14% Jul 2. BofA PT $2,500 (Jul 1), China Renaissance $3,169. NAND tightness projected through 2027.
- **Read-through:** Both names are in a violent post-blowoff pullback with intact fundamental theses — exactly the regime where short-DTE spreads either print or get vaporized. Dip-buy entries (bounce confirmation) look more promising than breakout entries at these IVs.

### ⚠ Engine-prior warning (from agent's knowledge-base lookup)

Platform priors claim short-DTE OTM **delta-based** strike selection historically produced 58.8–76.7% entry rejections (noValidDelta) on semis and NaN percentChange validation errors in sweeps. If the subagent backtests come back empty/degenerate, this is the first suspect — prefer **percent-OTM (distanceType=percent/dollars)** strike selection over delta-based, and treat any "no fills" result as an instrumentation problem before a strategy verdict (bug-protocol applies).

## Actions

- **2026-07-03:** Chain recon complete (above). Launched Aurora agent `6a47f7e590561bf0c2399251` (planning: gemini-3-flash-preview, execution: deepseek-v4-flash, 30 iters, automated). Its plan: verify tickers → news catalysts → two optionsStrategy subagents (7–14 DTE vs 21–30 DTE, ⅓-account sizing) → compare backtests, report drawdown + fees.

## Subagent results — 2026-07-03

### Subagent A (`…e59a`, tasked 7–14 DTE) — produced the candidate
- 7–14 DTE **fixed-strike** spreads deadlocked (no executable strike pairs) → pivoted to **delta-based** selection at 21–45 DTE.
- **Winner: "Semiconductor Momentum Spreads V2"** (chat portfolio `6a47f966443f7c0ef055106d`, backtest `6a47f972443f7c0ef05513dc`):
  - Per name (MU, SNDK): open 40Δ long / 20Δ short call vertical, 21–45 DTE, $2,667/ticket, entry RSI(14) > 50, max 1 open vertical per name (OptionSpreadCount gate). Exit: P/L ≥ +50% or DTE ≤ 5. No stop-loss.
  - Backtest 2024-01-01→2026-07-03, $8k, vs SPY: **+960.4% total, −48.1% maxDD, Sortino 3.21, Sharpe 1.51, 65.4% win rate, +19.3% avg trade, ~$2,051 fees**. Median deployment only **5.15%** — mostly cash, episodic strikes.
- Config verified via `get_portfolio`: matches the report. Two issues found:
  1. **DTE 21–45 violates the ≤~30-DTE spread rule** (and MU legs carried a fallback `expirationRange.maxDte: 60`).
  2. Skepticism: the +960% is likely concentrated in SNDK's H1-2026 +800% run — in-sample hero, no OOS evidence yet.

### Subagent B (`…e59c`, tasked 21–30 DTE) — verdict DISCARDED
- Reported **zero trades across 93 variants** and declared the structure "mathematically inconsistent with $8k."
- **Its premises were wrong**: it believed SNDK was delisted (used WDC as proxy) and priced MU like a ~$100 stock ($750–1,000 per 0.30Δ contract). Live chain shows MU $977 / SNDK $1,762 with $2.3–3.7k spreads clearly buildable. Verdict rejected; its "strike-pair deadlock" mechanics note is retained as a real risk (matches Subagent A's fixed-strike failure).
- Possible platform/data issue worth watching: two different data paths gave subagents different SNDK listing histories (spin-off Feb 2025 vs "delisted"). Not loudly-declarable yet — could be model hallucination rather than platform data.

### Compliance patch — V2c
- Cloned winner → **"Semiconductor Momentum Spreads V2c (21-30 DTE compliant)"** (`6a47fb55b8a1214d21f428ac`): all legs' expirationSelector max 45→30, MU fallback expirationRange maxDte 60→30.
- Backtest `6a47fb5ebfe7b4bb6c3a0bdc` (2024-01-01→2026-07-03, $8k, baseline **MU** buy-and-hold — SPY is the wrong bar for a two-semi book) — **COMPLETE**:

| Metric | V2 (21–45 DTE, non-compliant) | **V2c (21–30 DTE, compliant)** |
|---|---|---|
| Total return | +960.4% | **+825.9%** |
| Max drawdown | −48.1% | −49.6% |
| Sortino / Sharpe | 3.21 / 1.51 | 2.88 / 1.40 |
| Win rate | 65.4% | 65.3% |
| Avg trade return | +19.3% | +19.2% |
| Total fees | ~$2,051 | $1,906 |
| Median deployment | 5.15% | 5.30% |
| Names traded | 2 | 2 |

- **Read:** tightening to the compliant 21–30 DTE window costs ~134pts of total return but preserves the character of the strategy (same win rate, same avg trade, same drawdown). The edge is not living in the 31–45 DTE tail → **V2c is the working candidate**.
- **Caveats standing:** (1) median deployment ~5% means the book is in cash ~95% of the time — returns are episodic lottery hits, and a fixed-window backtest can't distinguish skill from the SNDK H1-2026 supercycle; (2) `dollarsSold` $1.1M on an $8k book = enormous turnover — fee drag is survivable ($1.9k) but slippage on 100%+-IV wings is unmodeled; (3) no OOS evidence — this is a discovery artifact, not a certified strategy.

## Entry-gate check ("can we enter the play right now?") — 2026-07-03

Human's requirement: the strategy must be enterable NOW. Two gates checked against the live tape:

1. **Signal gate — NOT live today.** RSI(14) at the 2026-07-02 close: **MU 48.5, SNDK 46.8** — both just under the >50 trigger after the −20%/−25% five-session Meta-Shock selloff (MU $1,213→$976, SNDK $2,335→$1,745). One solid bounce day flips both. The RSI>50 gate is doing its job: it demands bounce confirmation instead of knife-catching.
2. **Affordability gate — V2c HARD-FAILS at today's chain.** 22-DTE 40Δ/20Δ debit at mid: **MU $3,620, SNDK $7,400** vs the $2,667 ticket. The backtest filled when these were $100–600 stocks; after the 3–10× run-up the fixed dollar ticket no longer buys a 40Δ/20Δ structure. Classic affordability-ladder trap — the incumbent config is structurally dead at current prices.

**What $2,667 buys today (22 DTE, at mid):** MU long 30Δ $1,150 / short 12Δ $1,350 = $2,605 debit (~6.7:1 max); SNDK long 25Δ $2,220 / short 17Δ $2,420 = $2,650 (~6.5:1 max).

### V3 — "Semiconductor Momentum Spreads V3 (30d/15d affordable)"

Cloned V2c → `6a47fd429abb2b74b1e33003`, strike deltas 0.40/0.20 → **0.30/0.15**, all else identical. Backtest `6a47fd4f9abb2b74b1e33032` (same window/baseline):

| Metric | V2c (40Δ/20Δ) | V3 (30Δ/15Δ) |
|---|---|---|
| Total return | +825.9% | +605.4% |
| Max drawdown | −49.6% | **−65.1%** ⚠ near the −70% bound |
| Sortino / Sharpe | 2.88 / 1.40 | 2.12 / 1.21 |
| Win rate | 65.3% | 65.0% |
| Avg trade return | +19.2% | +24.2% |
| Fees | $1,906 | $2,263 |
| Median deployment | 5.3% | 4.7% |
| Enterable at today's chain | **NO** | **YES** |

**Verdict on the entry requirement:** V3 satisfies affordability now; the RSI>50 signal fires on the first bounce day (both names are within ~2–3 RSI points). Entry is achievable — proceeding to OOS certification per the human's conditional approval ("if we can, we can oos cert").

## OOS certification — launched 2026-07-03

- Walk-forward study **`6a47fde3bfe7b4bb6c3a0e1c`** on V3 (`6a47fd429abb2b74b1e33003`): validation mode, anchored, 5 folds, 2022-01-01→2026-07-03, oos_width 252d, embargo 14d, `inner_mode: backtest_only` (fixed book). Cost 20 tokens. Preview verified: spans 2022 bear; fold-3 OOS (2025-02-15→2025-10-25) contains April-2025; fold-4 OOS is 2025-10-25→2026-07-04 (the SNDK supercycle + Meta-Shock end).
- Pre-flight: no LaunchAgent; spread-shape compliant (all verticals 21–30 DTE); single close rule (P/L≥50% OR DTE≤5) — no stacked-TP cap.
- **Known read-with-care:** SNDK lists 2025-02-24, so folds 0–2 are effectively MU-only for the SNDK sleeve (engine must show zero SNDK fills there, per engine-sanity — if it shows SNDK trades pre-listing, that's a bug-protocol stop).
- Deviation from the challenge-book template: spot-checks and deployment math at **$8k** (this account), not the $25k challenge base.

## ⚠️ BUG/ISSUE — walk-forward participation gate (2026-07-03)

- **Symptom:** study `6a47fde3bfe7b4bb6c3a0e1c` completed with ALL 5 folds `NO_SIGNAL` — "Training window had zero participation; fold excluded from selection scoring" — and `foldsComplete: 0`, **no OOS statistics at all**. But each fold's own training stats show real trading (dollarsSold ≈ $54k, fees ≈ $367, winRate ≈ 64%). Contradiction between the gate and the tape.
- **Hypothesis (labeled as such):** the fold gate reads `participationRate`, which is structurally 0 for direct-OpenOption books (`universeSize: 0` — participation is a rebalance-universe concept). Even the +605% full-window backtest reports `participationRate: 0`.
- **Blocks:** any formal walk-forward certification of direct-OpenOption-shaped books (this whole attempt's candidate family).
- **Hand-off doc:** `PARTICIPATION_GATE_BUG.md` (this directory). Study quarantined as a verdict-less run.

## OOS certification verdict — **FAIL** (2026-07-03)

Two independent grounds:

1. **Formal:** the study produced zero OOS folds (bug above). Per protocol, an empty validation aggregate is reported, not papered over — no cert can issue from this run.
2. **Substantive (bug-independent):** the fold *training* windows told the real story, confirmed by a standalone spot-check `6a47fed11c3d3a5e304a0df1` — **V3 over 2022-01-01→2024-01-01: −99.97%, maxDD 99.98%, profit factor 0.91** (64% win rate; the +50%-TP winners never cover the full-debit losers + churn outside a supercycle tape). Fold validation windows: −0.5%, −73.6%, +94.3%, −60.1%, −47.7% (maxDD up to 80%). The +605% headline is **2024+ AI-memory-supercycle beta**, not an all-weather edge. RSI(14)>50 short-DTE OTM spreads on MU in 2022–2023 chop = theta annihilation.

**Conclusion: V3 (and by extension V2c/V2) is NOT deployable on OOS evidence.** The "can we enter right now" requirement is met mechanically (V3 fills at today's chain), but the certification the human conditioned deployment on has failed.

### Paths forward (human decision)
- **(a) Regime-condition the entry** — e.g. underlying > long SMA or a memory-sector health gate — then re-sweep (structural change ⇒ sweep-reoptimization discipline) and re-cert. Caveat: 200D-SMA-style gates are on the known-losers list for the LEAP challenge book; different book, but prior is negative.
- **(b) Re-express as a RebalanceOption universe book** (SNDK+MU universe, rank/rotate) — sidesteps the participation-gate bug AND gets the certifiable shape; re-cert there.
- **(c) Accept regime dependence explicitly** — deploy small, thesis-scoped (NAND shortage through 2027 per BofA), with a hard human kill-switch. Honest but uncertifiable; not recommended as "certified."
- **(d) Stand down** on short-DTE for this account until a signal with pre-2024 evidence exists.

## Round 2 — post-engine-fix dive (2026-07-03, human fixed the participation gate)

### ✅ Bug fix verified end-to-end
Rerun study **`6a480c9490a070a491e5c0b3`** (identical params to the quarantined study): **all 5 folds COMPLETE with real OOS statistics**. The participation-gate fix works. PARTICIPATION_GATE_BUG.md can be marked resolved.

### V3 formal certification verdict: **FAIL** (now with real fold evidence)
Per-fold OOS: **−57.8%** (dd 70.5%) / **+133.7%** (dd 28.9%) / **−55.3%** (dd 75.2%) / **−61.0%** (dd 87.1%) / **+338.4%** (dd 52.1%). Median OOS **−55.3%**; mean +59.6% is carried entirely by the two supercycle folds. 3/5 folds deeply negative. Matches the substantive kill-window evidence exactly.

### Round-2 candidates & triage (kill window 2022→2024 · supercycle 2024→2026-07)

| Candidate | ID | 2022–23 | 2022–23 maxDD | 2024–26 | 2024–26 maxDD | Verdict |
|---|---|---|---|---|---|---|
| V4a = V3 + 200d SMA gate | `6a480c9990a070a491e5c0cc` | **−14.6%** | **86.3%** ⚠ | +600.4% | 64.9% | Gate rescues terminal P&L but interim dd 86% — fails risk tolerance |
| V4b = V3 + 50d SMA gate | `6a480c9a90a070a491e5c0e3` | **−101.1%** ⚠⚠ | 100% | +636.9% | 59.8% | DEAD. Also breached physical floor (see issue below) |
| R1 = rotation universe book | `6a480cd4f14bdc40fb63fbff` | **−46.4%** | 66.9% | +357.2% | **76.4%** | Best kill-window dd; supercycle dd breaches 70% |

R1 confirms the rotation shape reports participation properly (universeSize 2, participationRate 0.5–1.0) — certifiable shape.

### ⚠️ ISSUE #2 — physical-floor breach (engine self-flagged)
Backtest `6a480ca7f14bdc40fb63fbc6` (V4b, 2022→2024) reported **percentChange −101.14%** with engine validationWarning: *"below physical floor of −100.5%; likely unbounded short or negative position value."* A long-debit-spread book cannot lose more than 100% of NAV. Engine's own validator caught it, so this is a known-suspect run, quarantined; V4b is dead on the merits regardless. Not writing a separate bug doc unless it recurs on a surviving candidate.

### Diagnosis after round 2
The killer is **re-entry churn**, not the absence of a regime gate: RSI>50 as a *level* keeps the book perpetually armed, so it re-buys spreads through every bear rally (V4a still took 86% interim dd in 2023 chop). Round 3 tests entry-frequency fixes:
- **V5** (`6a480d85b9817f2ac2924092`): entry = RSI(14) **CrossAbove** 50 (fires once per swing, not continuously).
- **R2** (`6a480d8890a070a491e5c942`): rotation with RSI filter raised to **60** + cadence 5→**10 days**.

## Round 3 results (2026-07-03)

| Candidate | 2022–23 | maxDD | 2024–26 | maxDD | Read |
|---|---|---|---|---|---|
| V5 CrossAbove-50 (`6a480d85…`) | −89.2% | 98.3% | +201.3% | 54.1% | DEAD — cross-entry doesn't fix the OpenOption book |
| **R2** RSI>60 + 10d cadence (`6a480d88…`) | −54.0% | 76.7% | **+533.7%** | **48.4%** | Best risk-adjusted bull book (Sortino 2.23, win 69%, participation 1.0) |
| R3 two-sided ±momentum (`6a480e1b…`) | −75.0% | 82.5% | +246.2% | 67.7% | DEAD — put side buys spreads at local bottoms in a chop-bear; double theta whipsaw |

**Family finding after 10 candidates:** No configuration of "short-DTE OTM directional spreads on SNDK/MU with momentum entries" survives 2022–23 within a −70% dd tolerance — level entries, cross entries, 50d/200d gates, rotation shape, higher RSI bar, slower cadence, and two-sided all tested. The family is a leveraged bet on the memory cycle; short DTE pays theta continuously for that bet.

**R2 formal cert launched anyway** (`6a480e83f14bdc40fb64023d`, same 5-fold anchored config): the anchored calendar absorbs 2022 into training — all OOS folds start 2023+, so R2 could legitimately clear more folds than V3's 2/5. This is the last verdict in the funnel.

## Benchmark comparison — R2 vs buy-and-hold (backtested with dividends, $8k, 2026-07-03)

| Book | 2022→now | maxDD | Sortino | 2024→now | maxDD | 2022–23 | maxDD |
|---|---|---|---|---|---|---|---|
| **R2 (certified)** | **+468.1%** | 76.7% | 1.51 | **+533.7%** | 48.4% | −54.0% | 76.7% |
| SPY B&H | +64.3% | 26.5% | 1.01 | +61.0% | 20.2% | +2.2% | 26.5% |
| QQQ B&H | +82.2% | 36.3% | 0.97 | +77.1% | 24.1% | +3.6% | 36.3% |
| TQQQ B&H | +79.8% | 81.1% | 0.77 | +204.3% | 60.1% | −38.8% | 81.1% |
| SPXL B&H | +90.3% | 66.3% | 0.76 | +168.1% | 51.3% | −27.4% | 66.3% |

Read: R2's risk profile is leveraged-ETF-class (maxDD between SPXL and TQQQ; worse than both in the 2022–23 bear), but its realized return is ~5–6× the 3x ETFs on the full cycle with a *higher* Sortino (1.51 vs 0.76–0.77). Caveat: the comparison window contains the memory supercycle — R2's outperformance is partly idiosyncratic sector tailwind that SPY/QQQ structurally can't capture. Baseline portfolio IDs: SPY `6a481f8090a070a491e5eb5f`, QQQ `6a481f82b9817f2ac2925fc2`, TQQQ `6a481f84f14bdc40fb641a21`, SPXL `6a481f85b9817f2ac2925fc7`.

## Deep research — SNDK & MU future (2026-07-03)

- Aurora research agent `6a482180b9817f2ac2926426` produced a ~92k-char Deep Research report (in agent conversation `6a48217b3ac8f15fea0ca17c`): supercycle thesis, HBM/NAND supply-demand through 2028, Meta-Compute scare, valuations, bull/bear, catalysts. Its conclusion: "cautiously optimistic — the supercycle has several years yet to run," with 2028–29 oversupply as the main structural risk.
- Claude-side web sweep (5 searches) key facts: NAND undersupplied through 2027 (BofA, Citi PT $2,500; Deutsche Bank sees tightness possibly to 2028); MU HBM sold out through 2026, 16 SCAs ≈ $100B locked, HBM TAM >$100B in 2027; Meta Compute (Jul 1) = first hyperscaler admitting "excess capacity" — MU −10.6% that day; CXMT at ~350 kwspm exiting 2026 (≈ MU's ~385) with commodity-DRAM price pressure; SK Hynix Nasdaq listing ~Jul 10 (~$29B raise, possible flow competition); Kioxia/SanDisk capex +40% YoY (supply discipline eroding at the margin); MU trailing P/E >40 but ~10× forward, PEG ~0.13; SNDK consensus Strong Buy (18/21), some FV models say MU ~65% above fair value.
- Synthesis + 12-month view written in chat (2026-07-03): constructive on both with violent volatility expected; MU preferred on quality (contracted revenue, HBM moat), SNDK higher-octane but thinner moat; regime-end markers to watch = hyperscaler capex language, CXMT commodity pricing, 2027–28 fab ramps, Kioxia/Samsung capex acceleration.

- **Candidate:** V2c `6a47fb55b8a1214d21f428ac` (chat portfolio, not deployed).
- Open decisions for the human: (a) walk-forward OOS cert before any deploy? (b) add a put-spread leg for two-sided high-risk? (c) alt-data entry (WSB mentions) vs RSI? (d) deploy sizing — 2×$2,667 tickets leaves ~$2.7k cash buffer.

## The benchmark that matters — R2 vs B&H of the underlyings (2026-07-03)

B&H portfolio IDs: MU `6a48260790a070a491e5f61e`, SNDK `6a48260990a070a491e5f623`, 50/50 `6a48260ab9817f2ac2926ac4`. All $8k, dividends included. SNDK lists 2025-02-24, so the apples-to-apples window is 2025-03-01→now.

| Book | 2022→now | maxDD | 2024→now | maxDD | 2025-03→now | maxDD | Sortino (25-03→) |
|---|---|---|---|---|---|---|---|
| R2 (certified spreads) | +468% | 76.7% | +534% | 48.4% | **+343%** | 43.4% | 3.06 |
| B&H MU | **+948%** | **59.0%** | +1,063% | 59.0% | +919% | 38.0% | 4.39 |
| B&H SNDK | — | — | — | — | **+3,490%** | 48.3% | 5.15 |
| B&H 50/50 | — | — | +1,069% | 59.0% | **+2,204%** | 43.1% | 5.09 |

**Finding: buy-and-hold dominated R2 on this tape — decisively.** Full-cycle, B&H MU beat R2 on BOTH return (+948 vs +468) and drawdown (59% vs 77%). In the SNDK era, 50/50 B&H returned 6.4× R2 at the SAME drawdown (43%). Mechanism: (1) the +50% take-profit truncates exactly the tail moves that made these stocks; (2) median deployment ~0.4–5% — the spread book sits mostly in cash while B&H compounds at ~100% deployment. R2 is capital-efficient per deployed dollar but massively under-invested in a monster bull.

**Honest framing:** the OOS cert proved R2's *mechanism* is positive in every regime since 2023 — it did NOT prove it beats owning the underlyings; the certification bar was absolute (return>0, Sortino≥0.5), not relative to underlying B&H. On this tape, the simplest expression of the memory thesis (own the shares) crushed the options expression. R2's remaining case is regime insurance (goes flat when RSI<60 while B&H eats the full bust) — and even that insurance was imperfect (R2 2022–23: −54%).

## Beat-B&H iteration (2026-07-03, human mandate: "beat buy and hold in many ways")

Diagnosis of R2's loss to B&H: (1) ~5% median deployment, (2) +50% TP truncates tails, (3) short leg caps convexity.

### Round 1 (triage: 2022–23 kill / 2024→ / SNDK-era)
| Candidate | ID | 2022–23 | 2024→ | SNDK era | Verdict |
|---|---|---|---|---|---|
| S1 hybrid 60% shares + R2 spreads | `6a4829fd…` | −10.1% / 49.5dd | +1,105% / 58.9dd | +2,196% / 42.7dd | ≈B&H (overlay starved: share re-buys soak buying power) |
| S2 R2 with TP 50→150 | `6a4829f1…` | −72.3% / 84.7dd | **−13.9%** / 78.9dd | +212% / 67.9dd | DEAD — capped spreads round-trip through theta without the +50 harvest |
| S4 uncapped 30Δ calls, TP250, 33/67 %NAV | `6a482a03…` | −42.4% / 90.1dd | **+2,342%** / 79.2dd | **+3,267%** / 42.8dd | Breakthrough — convexity cap was the killer |

### Round 2
| Candidate | ID | 2022–23 | 2024→ | SNDK era |
|---|---|---|---|---|
| **S5 = S4 + per-candidate Price>200d-SMA filter** | `6a482abcd89cad8e9a8aa809` | **+81.9%** / 55.9dd | **+3,109%** / 70.8dd | **+3,270%** / 43.3dd (Sortino 5.23) |
| S6 hybrid 50% shares + call overlay | `6a482ac7…` | −14.1% / 52.8dd | +1,113% / 59.2dd | +2,162% / 43.4dd (overlay starved again — engine note: repeated %-of-portfolio Buy strategies consume all buying power, starving RebalanceOption budgets) |

**S5 beats B&H on return in ALL three windows** (incl. the bear: +82% vs MU's ~−10%), beats 50/50 at equal dd in the SNDK era, ≈ ties B&H-SNDK-alone with lower dd/higher Sortino. Caveats: 2022–23 result is few-trade (~$24.5k sold); candidate #10+ on the same tape → selection bias; verdict deferred to walk-forward `6a482b5eaaf11ccf36fde8f5` + full-cycle backtest `6a482b5dd89cad8e9a8aaa10`.

### Human feedback (2026-07-03, durable): ~50% TP/SL is disproven — never use it. Saved to persistent memory. S5's TP+250 aligns with the episode-10 settled family.

### S5 verdict — CERTIFIED, and it beats B&H (2026-07-03)

- Walk-forward `6a482b5eaaf11ccf36fde8f5`: **5/5 OOS folds positive — +99.0% / +100.4% / +106.4% / +670.9% / +743.1%** (median +106%/fold), worst OOS dd 48.9%, Sortino 2.6–18.1, win rate 84–99.9%, winner stable.
- Full cycle 2022→2026-07 (`6a482b5dd89cad8e9a8aaa10`): **+5,492%** ($8k → ~$447k), maxDD 68.4%, Sortino 2.72, win 92.1%, PF 4.99, fees $901.

Scorecard vs B&H ("beat it in many ways"):
| Dimension | S5 | Best B&H | Winner |
|---|---|---|---|
| Full-cycle return | +5,492% | +948% (MU) | **S5 (5.8×)** |
| 2024→ return | +3,109% | +1,069% (50/50) | **S5 (2.9×)** |
| SNDK-era return | +3,270% | +3,490% (SNDK alone) / +2,204% (50/50) | ≈tie vs SNDK, **S5** vs 50/50 |
| SNDK-era dd / Sortino | 43.3% / 5.23 | 48.3% / 5.15 (SNDK) | **S5** |
| Bear 2022–23 | +81.9% | ~−10% (MU) | **S5** |
| Full-cycle Sortino | 2.72 | 1.87 (MU) | **S5** |
| Full-cycle maxDD | 68.4% | 59.0% (MU) | B&H (the one loss) |

**S5 config** (`6a482abcd89cad8e9a8aa809`): RebalanceOption MU+SNDK; pipeline Filter[price>200d SMA] → Filter[RSI(14)>60] → SelectTop-2 by 63d ROC; outright long 30Δ calls 21–30 DTE (20Δ fallback rung); 33% NAV per name / 67% total budget; exit +250% P/L or DTE≤5. No spreads, no low TP, no stop-loss — consistent with options-structure-rules (outright calls, short-dated) and the no-low-TP rule.

**Standing caveats:** (1) S5 is candidate ~12 evaluated on this same tape — the design was chosen after seeing full-window results, so the anchored folds are not a substitute for a true untouched holdout; all historical data is now burned, the only clean OOS is the future. (2) 92% win rate / +238% avg trade are supercycle-flattered; mid-price fills at 100%+ IV understate slippage. (3) Full-cycle maxDD 68% is the price of the returns — B&H MU is gentler on that one axis.

## Round 4 — "try even harder, comfort-focused, $8k-aware" (2026-07-03)

Prior-attempt mining (episode-10 + e11 attempt1/2) verdicts applied: TP+250 ✓, 63d ROC ✓, expensive→cheap template ladder ✓, percent-OTM rungs for affordability ✓. **LEAPs verified impossible on $8k** for these names (MU 350-DTE +100% OTM ≈ $14.9k/contract at ~100% IV) — the certified 365–730 DTE family cannot be expressed here; short/medium DTE is forced, not chosen.

| Candidate | ID | 2022–23 | 2024→ | SNDK era | Full cycle | Verdict |
|---|---|---|---|---|---|---|
| S7 40% budget / 20% name | `6a482ce1…` | +79.1 / 37.4dd | +717.7 / 51.3dd | +654.0 / 53.0dd | — | DEAD: small tickets can't afford 30Δ rung; loses return AND comfort |
| S8 ladder (36–60d +40/+60% OTM rungs + 21–30d floor) | `6a482ce53ad7b39b18a25555` | −38.1 / 39.2dd | **+3,576.9 / 51.4dd** | **+3,933.1 / 39.2dd** (beats B&H SNDK on every axis) | **+3,511.7 / 68.3dd** | **cert FAIL** — fold-0 OOS −31.8% (deep rungs die in moderate-momentum tape). Study `6a482d8d3ad7b39b18a25725`: [−31.8, +11.3, +12.1, +201.4, +2,280.3] |
| S9 = S8 with deep rungs gated on ROC63>40 | `6a482da1…` | +81.9 / 55.9dd | +1,089.0 / 70.8dd | +1,071.9 / 39.9dd | — | Dominated: bear = S5, bulls ≪ S8 |

**Final standing: S5 (`6a482abcd89cad8e9a8aa809`) remains the only strict 5/5-certified B&H-beater.** S8 documented as the non-certified aggressive variant (blowoff-regime specialist). ~18 candidates evaluated total this campaign; selection-bias caveat stands — forward performance is the only clean test remaining.

## Round 5 — S10 "Convertible Ladder" (SNDK inclusion mandate, 2026-07-03)

Human requirement: must hold SNDK too, not just MU; test primarily on 2026 data with intraday backtests. Human's structural idea: debit spreads whose short leg gets bought back on strength.

**S10** (`6a4838694ed7c21e3f3adb74`) = S5 brain + 4-rung affordability ladder (expensive→cheap): 30Δ call → 20Δ call → 25Δ/15Δ vertical (~$2,980 SNDK today) → 20Δ/10Δ vertical (~$1,915 SNDK today ✓), plus two leg-buyback strategies: when a name's vertical P/L ≥ +75%, CloseOption closeScope=leg buys back ONLY the short leg → spread converts to uncapped call (then governed by TP+250/DTE≤5). Verticals all 21–30 DTE (spread-shape ✓). At today's chain: MU fills R1 ($2.6k), SNDK fills R4 ($1.9k) — both names participate.

- Daily backtests: **identical to S5 to the decimal** (+3,109% / +3,270% / +81.9%) — at historical prices the outright rungs always filled first, so the new machinery activates only when affordability forces it (i.e., now). No historical behavior change.
- **Certified**: study `6a4839686d6c7f417c89843e` — 5/5 folds, OOS mean +344.0%, exactly matching S5's study. S10 formally inherits the certified record.
- 2026-YTD Minute-interval runs: B&H 50/50 = +424.1% / 29.3dd (done); S10 (`6a4838786d6c7f417c898269`) and S5 (`6a4838796d6c7f417c898275`) Minute runs slow — watching for a possible hang (updatedAt frozen at 22:38, timeElapsed reset; potential issue #3 if it persists).

### Round-5 close-out (2026-07-03)

- ⚠️ **ISSUE #3 (loudly declared): Minute-interval backtests hang on options books.** Both S10/S5 Minute runs (`6a4838786d…`, `6a4838796d…`) stuck RUNNING 20+ min with frozen updatedAt + reset timeElapsed; equity Minute control completed in 12s. Hand-off doc: `MINUTE_OPTIONS_HANG_BUG.md`. Intraday validation blocked until fixed; Day-interval used as fallback.
- **2026 YTD (Day, fallback)**: S10 `6a483d0e7169075c691e51e6` = **+573.2%, dd 49.9%, Sortino 6.29, win 91.6%, both names traded, participation 1.0, median deployment 10.7%** — vs B&H 50/50 YTD +424.1% / dd 29.3 (Minute run). S10 wins return + Sortino; B&H shallower dd in this half-year.
- **DEPLOY CANDIDATE: S10** (`6a4838694ed7c21e3f3adb74`) — certified 5/5 (study `6a4839686d…`, identical to S5's folds), includes SNDK via affordable vertical rungs + short-leg-buyback conversion, entry gates currently dark (RSI ~48 < 60 → no orders until confirmed bounce). Awaiting explicit human "deploy + clean up" to run the gated deploy flow.

## Round 6 — weighting experiments (alt-data-indicators discipline, 2026-07-03)

Verification per skill: `WsbMentions21_Full` (`6a45fa78…`) = 7,228 pts, dense MU+SNDK daily coverage 2021-12→**2025-12-31**, lookahead-safe (post-date stamped, dual-build verified). 2026 missing from Reddit lake; live scrape 403 → the known WSB freshness deploy-blocker stands: stale data may not drive a live book.

| Variant | Tilt | Result |
|---|---|---|
| S11 (`6a483f0d…`) | rank = ROC63 × (1+log10(1+SMA21(WSB mentions))) — proven anchor shape | **Exact no-op**: identical to S10 to the decimal in 2024→ and 2026 YTD. On a 2-name equal-weight book the rank only orders funding, and both names always fund. Confirmed graceful degradation across the 2026 data cliff (kept trading). Not wired further. |
| S12 (`6a483f48…`) | rank = ROC63 ÷ peRatioTTM (fresh, deployable) | Cert `6a483fc61dac39edf8fea6a5`: 5/5 positive, folds 0–3 identical to S10, **fold 4 strictly worse** (+573.3/52.3dd vs S10's +743.1/48.9dd; mean +310 vs +344). De-prioritizing expensive SNDK in a supercycle is backwards. REJECTED. |

**Weighting verdict:** on this 2-name book, rank tilts are either no-ops or harmful; the meaningful "weight by something" levers would be static sleeves (unequal per-name sizing) — not pursued, since the deep-research tilt (favor MU quality) would have cut the SNDK-driven returns. **S10 stands unchanged as the deploy candidate.** Fundamental probe artifact: valid Fundamental metrics enumerated (peRatioTTM, psRatioTTM, epsActual, totalRevenue, …) via build_portfolio validation.

Minute-run status: both 2026-YTD Minute options runs still RUNNING and healthy (fleet logs show active HEAVY workers; updatedAt now advancing). MINUTE_OPTIONS_HANG_BUG.md downgraded to a status-reporting issue (frozen updatedAt/timeElapsed during prep).
