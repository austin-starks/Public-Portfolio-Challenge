# Episode 11 Attempt 6 — SNDK + MU Fresh 0DTE Retest

**Started:** 2026-07-19
**Capital:** $8,000 fixed cold-start capital
**Intended live portfolio:** `MU + SNDK Live Trading Portfolio`
**Status:** BLOCKED / NULL — research complete on current evidence; no deployment or orders authorized

> **Continuation:** Attempt 6 remains the immutable pure-options null. After the user allowed longer
> DTE and continued iteration, the active successor campaign moved to
> [`../attempt7-sndk-mu-longer-dte/CAMPAIGN_LOG.md`](../attempt7-sndk-mu-longer-dte/CAMPAIGN_LOG.md),
> which now records a certified 80% stock-core plus intraday 0DTE calls-and-puts research finalist.

## One-line mandate

Create an outstanding intraday-only SNDK/MU strategy that buys outright 0DTE calls and puts, never
uses a debit spread, credit spread, short option leg, or overnight option hold, and on the updated
minute engine performs at least near a reasonable equal-weight MU/SNDK buy-and-hold baseline while
materially outperforming it in bull regimes.

## Evidence reset

Every result produced before this attempt is **UNVERIFIED / QUARANTINED** because the intraday minute
engine changed. Episode 10 and Episode 11 are used only for experimental design, field-shape examples,
and known failure modes. No prior return, drawdown, Sortino, trade count, fill, or certification verdict
is an incumbent bar. All claimed performance in this log must come from a newly completed Attempt 6
run on the current engine.

Prior structures may be re-created as fresh seeds, but their old IDs and metrics do not count as
evidence. In particular, old direct-option allocation defects, variant-ID defects, hanging jobs, and
misleading hold-to-expiry ledger statistics remain risks to re-check rather than assumed current bugs.

## Hard constraints

- Universe is exactly `MU` and `SNDK`.
- Options are exactly `0–0 DTE`; no substitution into 1–7 DTE.
- Entries are single-leg `OpenOption` actions with one **long call** or one **long put**.
- No `OpenOption` action may contain more than one leg; every leg direction must be `long`.
- Calls and puts must both participate in completed fresh-engine evidence; a dormant decorative sleeve
  does not satisfy the mandate.
- Use explicit contract allocation, initially one contract, until fill-time dollar caps are proven on
  the current engine.
- Flat all options before the close; no exercise/assignment or overnight exposure.
- `automaticOrderApproval: false` on every strategy.
- No deployment, reconciliation, or order creation without a later explicit human instruction.

## Baselines and success bars

Primary baseline: a newly created 50/50 MU/SNDK buy-and-hold control starting from the same $8,000,
tested on exactly the same calendars. Because buy-and-hold uses permanent exposure and the candidate is
intraday-only, this is deliberately a demanding baseline, not an easy cash benchmark.

Secondary diagnostics:

1. MU buy-and-hold and SNDK buy-and-hold separately.
2. An equal-weight underlying intraday control if the engine exposes an equivalent executable shape.
3. Cash at 0% as a floor, never as the headline baseline.

Predeclared campaign PASS requires all of the following:

1. Fresh completed minute-engine results only; `RUNNING`, `PENDING`, `ERROR`, quarantined, or old runs
   never count.
2. Positive return in a majority of independent validation partitions, positive aggregate Sortino,
   and no physical-floor or NaN anomalies.
3. Final full-period return at least 80% of equal-weight MU/SNDK buy-and-hold, **or** materially better
   risk-adjusted performance with no worse max drawdown and at least 65% of baseline return.
4. On predeclared bull partitions, return at least 1.25× the equal-weight baseline with positive option
   alpha after fees. “Ripping” means outperformance, not merely a large absolute return in a rising tape.
5. Max drawdown no worse than the equal-weight baseline and preferably below 35%; any drawdown above
   50% is an automatic risk FAIL for an $8,000 live account.
6. Both names trade, both calls and puts fill and close, every opened OCC contract expires on its entry
   date, and every entry is exactly one long leg.
7. Event-level quantity, premium, cash, and fees reconcile. One contract costing more than available
   cash or any quantity above the requested contract cap is a blocking execution failure.

The 80% return bar is the literal “at least close to buy-and-hold” interpretation. It will not be
quietly weakened after results are observed.

## Frozen evaluation design

Minute-data availability will be verified before finalizing dates. The intended current-data campaign
shape is:

- **Search:** 2026-01-02 through 2026-04-30.
- **Validation 1:** 2026-05-01 through 2026-05-29.
- **Validation 2:** 2026-06-01 through 2026-06-30.
- **Fresh confirmation:** 2026-07-01 through the latest complete session with historical option data.
  The current probe established 2026-07-10 as usable and 2026-07-17 as unavailable, so the current
  endpoint is 2026-07-10 unless a later session is proven usable.
- **Full continuous path:** 2026-01-02 through the latest complete session, with one $8,000 start and
  no partition resets.

Partition resets are diagnostics; only the continuous path answers compounding and survival. Because
the earlier Episode 11 logs already exposed some dates to the researcher, these windows are not called
an untouched lockbox. They are a fresh-engine OOS-style retest with frozen rules and honest provenance.

## Candidate families

At least three genuinely different intraday mechanisms must receive fresh completed evidence before a
null verdict is legal:

| Family | Call mechanism | Put mechanism | One-change thesis | Status |
|---|---|---|---|---|
| A — trend continuation | Above VWAP + RSI/30-minute impulse confirmation | Below VWAP + inverse confirmation | Capture expansion after direction confirms | KILLED |
| B — failed-move reversal | Reclaim VWAP after an early washout | Lose VWAP after an early squeeze | Buy convexity on intraday reversal, not persistent levels | KILLED |
| C — five-minute impulse | 5-minute ROC crosses above +0.75% while above VWAP | 5-minute ROC crosses below −0.75% while below VWAP | Trade discrete intraday impulses with one ticket/day | RESEARCH LEADER; NOT CERTIFIED |
| G — P11 structural retest | SNDK RSI/VWAP call | MU RSI/VWAP momentum put | Fresh-engine retest of the old shape without importing its metrics | KILLED |
| M — two-strike long barbell | Independent 2% and 4% OTM long calls | Independent 2% and 4% OTM long puts | Increase convex participation without any short leg or defined-risk spread | KILLED ON RISK |
| O — later flatten | C structure, flat at minute 360 | C structure, flat at minute 360 | Preserve late-session 0DTE gamma while remaining intraday | RESEARCH LEADER; NOT CERTIFIED |
| P/Q — daily regime gates | Require positive daily ROC for calls | Require negative/shock daily ROC for puts | Filter intraday impulses by the prior daily regime | KILLED IN SEARCH |
| R/T — asymmetric moneyness | Move SNDK or calls farther OTM | Keep the put convexity sleeve closer | Reduce one-contract premium risk without spreads | KILLED IN VALIDATION |
| U — asymmetric exact grid | 4%/5%/6% OTM calls | 3%/4%/5% OTM puts | Exhaustive call/put/exit re-sweep | KILLED IN VALIDATION |
| V/W — one-ticket exact grid | One open option position across the book | One open option position across the book | Prevent paired-name loss concentration | RISK LEADER; NOT CERTIFIED |
| X/Y — same-day stock delta | Daily or impulse-only intraday MU/SNDK stock sleeve | V/W outright put overlay retained | Add broad bull delta without overnight holdings | KILLED ON FEES / NO ALPHA |
| Z/AA–AD — call-edge retests | RSI breakout, daily-gated impulse, sustained impulse, and late continuation | V3 one-ticket 3% put engine fixed | Find positive bull-call alpha without disturbing downside convexity | KILLED; AA1 IS FINAL RISK LEADER |

Search may KILL or PROMOTE. It may not issue the final verdict. Parameters on a promoted exact design
must be re-swept or exhaustively hand-gridded on that same structure, then frozen for validation.

## Engine-sanity gate

Before trusting performance:

1. Structured `build_portfolio` must accept a minimal one-call/one-put book.
2. A small completed minute backtest must produce signals/orders without hanging.
3. Persisted `conditionFieldAudit` and raw actions must match the requested fields.
4. Event replay must prove same-day OCC expirations, one requested contract, long-only one-leg shape,
   same-day closes, and cash/fill reconciliation.
5. A repeat run must reproduce exactly or within an explicitly explained market-data revision.

Any contradiction triggers the bug protocol and quarantines affected runs.

## Campaign ledger

| Time | Stage | Artifact | Result | Evidence status |
|---|---|---|---|---|
| 2026-07-19 | Reset | This log | Mandate, gates, and evaluation design frozen | VALID |
| 2026-07-19 | S0 build | Portfolio `6a5c5dd3e0fad1524c18389f` | Six strategies persisted; four one-leg long 0DTE entries; two timed exits; field audit matched | VALID |
| 2026-07-19 | S0 data boundary | Backtest `6a5c5ddee0fad1524c1838a5` | Signals fired on 2026-07-17, but MU and SNDK both rejected `No options data available` | DATA-LIMITED; no performance evidence |
| 2026-07-19 | S0 execution | Backtest `6a5c5e33e0fad1524c1838f8` | 2026-07-10 completed; both names and both directions opened and closed | VALID ENGINE PROBE; excluded from candidate evidence |
| 2026-07-19 | Baseline | Portfolio `6a5c5e0504196c7dbc7edf7a` | Fresh 50/50 MU/SNDK buy-and-hold control created at $8,000 | VALID |
| 2026-07-19 | Baseline | Backtest `6a5c5ee404196c7dbc7ee118` | Full path +450.85%, Sortino 5.85, maxDD 34.46% | VALID PRIMARY BAR |
| 2026-07-19 | Attribution | Backtest `6a5c67be38b89b14af44ac94` | C full event replay reproduced +277.38%; 44 opens and 44 closes reconciled | VALID, but fails campaign bars |
| 2026-07-19 | Final research leader | Portfolio `6a5c6978ce63c9f6e4113c29` | Same C entries, one contract, 4% OTM, flat at minute 360 | STRUCTURE PASS; PERFORMANCE FAIL |
| 2026-07-19 | Exact re-sweep | 27 explicit U portfolios/backtests | Calls 4/5/6%, puts 3/4/5%, exits 330/345/360; all 27 completed | VALID SEARCH SURFACE; no robust validation winner |
| 2026-07-19 | Risk-control leader | Portfolio `6a5c729c6ca2e2e52402baec` | 4% calls, 3% puts, minute-360 flatten, global option-position count below one | STRUCTURE PASS; BULL GATE FAIL |
| 2026-07-19 | Risk-control full path | Backtest `6a5c735438b89b14af44c88c` | +342.82%, Sortino 6.73, maxDD 22.69% | VALID; 76.04% of baseline with better risk |
| 2026-07-19 | Risk-control event replay | Backtest `6a5c78e8ce63c9f6e4115e86` | Exact metric reproduction; 22 opens / 22 closes; all one-contract true 0DTE | VALID EVENT EVIDENCE; attribution still put-dominated |
| 2026-07-19 | Final risk leader | Portfolio `6a5c7a964412b1d5eedba11e` | V3 plus +1% one-day ROC gate on calls | STRUCTURE PASS; BULL GATE FAIL |
| 2026-07-19 | Final full path | Backtest `6a5c7b2b4412b1d5eedba299` | +347.80%, Sortino 6.84, maxDD 22.38% | VALID; 77.14% of baseline with better risk |
| 2026-07-19 | Final event replay | Backtest `6a5c7bb34412b1d5eedba307` | Exact reproduction; 19 opens / 19 closes; all one-contract true 0DTE | VALID; calls still net negative |

## Candidate certification ledger

| Family | Seed ID | Structure audit | Search backtest(s) | Validation backtest(s) | Full path | PROMOTE / KILL |
|---|---|---|---|---|---|---|
| A | `6a5c5eb7e0fad1524c183971` | PASS: four one-leg long 0DTE entries, one contract, no spreads | `6a5c5ed804196c7dbc7ee089`: +26.92%, DD 20.73% | May −5.06%; June −42.26% / DD 58.46%; July +34.92% | `6a5c5f6704196c7dbc7ee1bb`: +14.52%, DD 61.98% | KILL |
| B | `6a5c5eba188cf942854b038d` | PASS: four one-leg long 0DTE entries, one contract, no spreads | `6a5c5eda188cf942854b04c4`: −3.94%, Sortino −2.48 | Not promoted | Not run | KILL |
| C | `6a5c5ebee0fad1524c183982` | PASS: four one-leg long 0DTE entries, one contract, no spreads | `6a5c5ede04196c7dbc7ee10c`: +36.08%, DD 19.29% | May +6.68%; June −15.98% / DD 55.13%; July +250.61% | `6a5c5f72188cf942854b07eb`: +277.38%, DD 46.67% | FAIL: 61.52% of baseline and worse risk |
| G | `6a5c6368e0fad1524c1844ba` | PASS: MU put + SNDK call; one long 0DTE contract each | +10.19%, DD 25.05% | May −24.21%; June +18.29%; July +70.58% | `6a5c63a204196c7dbc7eebb9`: +74.85%, DD 41.87% | KILL |
| M | `6a5c673f38b89b14af44ac65` | PASS shape: independent outright 2%/4% long options; no short leg | +112.70%, DD 28.00% | May +29.76%; June +6.44% / DD 69.02%; July +121.15% | `6a5c677bce63c9f6e4113966`: +270.05%, DD 49.19% | KILL: automatic risk fail |
| O | `6a5c6978ce63c9f6e4113c29` | PASS: four one-leg long 0DTE entries; flat at minute 360 | `6a5c69966ca2e2e52402a4bf`: +79.62%, DD 15.07% | May +8.91%; June −31.01% / DD 62.84%; July +285.67% | `6a5c69eb6ca2e2e52402a5cb`: +343.19%, DD 44.36% | BEST RETURN; FAIL risk and validation |
| P | `6a5c6b8c6ca2e2e52402a88c` / `…a8b2` / `…a89f` | PASS: symmetric daily ROC gates at 0/1/2% | −7.63% / −13.64% / −18.67% | Not promoted | Not run | KILL |
| Q | `6a5c6c606ca2e2e52402acc9` / `…baf5` / `…4b45` | PASS: put-only daily shock gates at 0/1/2% | −14.89% / −21.27% / −26.08% | Not promoted | Not run | KILL |
| R | `6a5c6cd3ce63c9f6e4114c21` / `…4c56` / `…4d9d` | PASS: MU 4% OTM, SNDK 5/6/8% OTM | +74.12% / +68.11% / +48.63% | Best 5%: May +5.32%; June −26.53%; July +252.23% | Not promoted | KILL: June risk remains |
| S | `6a5c6d856ca2e2e52402b14f` / `…bd6a` / `…bd8d` | PASS: entry floors 20/25/30 minutes | +92.62% / +63.22% / +36.47% | Every setting lost 48–53% in June | Not run | KILL: later resolution did not avoid bad days |
| T | `6a5c6e32ce63c9f6e4114f15` / `…be59` / `…4f28` | PASS: calls 5/6/8%, puts 4% | +84.87% / +91.43% / +93.36% | 5% calls: May +0.04%; June −22.08%; July +274.04% | `6a5c6eee6ca2e2e52402b2b3`: +336.87%, DD 41.65% | KILL: misses return/risk bars |
| U | 27 explicit variants rooted at O | PASS: exhaustive C4/5/6 × P3/4/5 × E330/345/360 | Top adjacent E360 cells: +94.49% / +100.23% / +106.95% | C4/P3: May +2.82%; June −27.14% / DD 65.25%; July +317.79% | Not promoted | KILL: validation auto-risk fail |
| V3 | `6a5c729c6ca2e2e52402baec` | PASS: C4/P3/E360 plus global `OptionPositionCount < 1` | `6a5c72d0ce63c9f6e4115675`: +107.86%, DD 18.23% | May −9.78% / DD 23.16%; June +4.69% / DD 26.99%; July +240.06% / DD 31.55% | `6a5c735438b89b14af44c88c`: +342.82%, Sortino 6.73, DD 22.69% | RISK LEADER; FAIL bull gate |
| W | 27 explicit variants rooted at V3 | PASS: exhaustive C2/3/4 × P2/3/4 × E330/345/360 | C2/P3/E360 +125.36%, DD 17.98%; C3/P3/E360 +123.80%, DD 18.09% | C2: −9.55% / +11.44% / −26.58%; C3: −2.46% / +3.15% / −22.05% | Not promoted | KILL: only one profitable validation partition |
| X/Y | `6a5c773dce63c9f6e4115be7` / `6a5c78056ca2e2e52402c253` families | PASS: stock entry ends before exit; options remain V3 outright book | Daily core best +24.38%; sparse bull delta best +108.13% vs V3 +107.86% | Not promoted | Not run | KILL: fees / no incremental alpha |
| Z | `6a5c7a2e4412b1d5eedba06c` family | PASS: RSI-70 / VWAP / positive-day calls at 1/2/3% OTM; V3 puts fixed | +95.26% / +97.22% / +98.67%, DD 18.20% | Not promoted | Not run | KILL: dominated by V3 |
| AA1 | `6a5c7a964412b1d5eedba11e` | PASS: V3 plus calls require one-day ROC > +1% | `6a5c7aa75423eef2bb277106`: +109.54%, DD 18.20% | May −6.45% / DD 20.32%; June +4.69% / DD 26.99%; July +240.03% / DD 31.55% | `6a5c7b2b4412b1d5eedba299`: +347.80%, Sortino 6.84, DD 22.38% | FINAL RISK LEADER; FAIL bull gate |
| AB | `6a5c7b634412b1d5eedba2c4` / `6a5c7b605423eef2bb2771c6` / AA1 | PASS: AA1 calls at 2/3/4% OTM | +105.24% / +107.84% / +109.54% | Not promoted | Not run | KILL: closer calls monotonically worse |
| AC | `6a5c7c14a698a7cfe9fd90b9` family | PASS: 15-minute call ROC cross at 1.5/2/2.5% | +105.40% / +105.48% / +106.31% | Not promoted | Not run | KILL: sustained-call family dominated |
| AD | `6a5c7c72af2d2a418d3f8c60` family | PASS: late calls, minutes 240–300, 30-minute ROC 0.5/1/1.5% | +99.79% / +99.93% / +100.09% | Not promoted | Not run | KILL: late continuation dominated |

## Bug / issue ledger

| Issue | Minimal repro | Expected | Observed | Impact | Status |
|---|---|---|---|---|---|
| Historical option data unavailable on 2026-07-17 | `6a5c5ddee0fad1524c1838a5` | Same-day chains resolve on a listed expiry | Four signaled attempts rejected `No options data available` | Campaign endpoint clipped to last proven session; no claim beyond 2026-07-10 | OPEN DATA LIMITATION |
| Requested two-contract allocation filled only one on late dates | Portfolio `6a5c614604196c7dbc7ee959`, event run `6a5c618b04196c7dbc7ee9f4` | Persisted `{type: contracts, amount: 2}` should fill two when cash/liquidity permit or emit a clear cap audit | SNDK Jul 2 and Jul 10 entries filled quantity 1; late-window metrics matched the one-contract book | Two-contract sizing branch cannot be used as certified evidence without an explicit cap reason | OPEN ENGINE ISSUE |
| Intraday stock exit generated pathological churn | Portfolio `6a5c641fe0fad1524c1845eb`, backtest `6a5c642704196c7dbc7eecfb` | Buy 25% MU/SNDK once, sell each sleeve once after minute 330 | $3.09M dollars sold and $6,179 fees from $8,000 in one search run | Stock-participation architecture quarantined; no performance inference | OPEN ENGINE ISSUE |
| Moneyness changes which later direction can fill | Clean controls `6a5c68ed6ca2e2e52402a34c` and `6a5c68eace63c9f6e4113b5b`; event runs `6a5c68f638b89b14af44aef7` / `6a5c68f938b89b14af44aefd` | Same entry conditions should generate the same signals; different strikes may legitimately change resolution/fills | Both saw the early SNDK call signal; the 2% call filled and blocked the later put, while the 4% call did not become a position and the later put filled | Not a signal bug, but proves the large 4% result is materially liquidity/path dependent | RESOLVED AS EXECUTION PATH DEPENDENCE |
| Call-only / put-only strike sweep axes fail compilation | `systematic_sweep` preview on `6a5c6e32ce63c9f6e4114f15` with three declared axes | Compiler should materialize call strike, put strike, and timed-exit genes or reject before partial planning | Both strike intents failed with `strike target requires StrikeSelector values`; only the third axis was kept | Automated partial sweep would look complete; U and W were run as explicit 27-cell grids instead | OPEN SWEEP-COMPILER DEFECT |
| Intraday core re-entered after its own exit | H stock buy allowed any time after minute 15 and sell began at minute 330 | Once-per-day same-day stock round trip | Flattening made the buy condition true again after minute 330, causing the old $3.09M churn | Root cause isolated; corrected 15–30 entry window removed the loop, though fee drag still killed X | RESOLVED IN X |

## Fresh baseline table

| Window | 50/50 MU/SNDK B&H | MaxDD | AA1 final risk leader | MaxDD | Relative result |
|---|---:|---:|---:|---:|---|
| Jan 2–Apr 30 | +191.54% | 28.99% | +109.54% | 18.20% | 57.2% of baseline; smoother, but not bull outperformance |
| May 1–29 | +71.81% | 19.40% | −6.45% | 20.32% | Binding rising-tape miss |
| Jun 1–30 | +21.51% | 19.74% | +4.69% | 26.99% | Positive and much safer than O, but only 21.8% of baseline return |
| Jul 1–10 | −8.07% | 24.35% | +240.03% | 31.55% | Strong convex win, but not a bull partition |
| Jan 2–Jul 10 continuous | +450.85% | 34.46% | +347.80% | 22.38% | 77.14% of baseline; alternative risk clause passes, bull clause fails |

## Parameter and mechanism evidence

- The exhaustive C sweep `6a5c6004e0fad1524c183ef9` evaluated 27 combinations across 2%/4%/6% OTM, 50%/100%/150% take-profit, and no/20-day/50-day regime gates. Every populated validation result in the leading ranked rows was negative; lower rows without validation statistics were not treated as evidence. The sweep produced no robust winner.
- Fresh exact variants showed 2% OTM (`6a5c6095188cf942854b0a81`) was positive in every reset partition and returned +143.62% full path, but still had 44.98% maxDD and captured only 31.86% of the baseline return. Three percent returned +98.89%; five percent +46.56% in search; six percent +13.88% full. There was no monotonic free lunch from deeper strikes.
- A 2%-call/4%-put hybrid (`6a5c65ddce63c9f6e41137a7`) was positive in every reset partition but returned only +115.40% full with 44.69% maxDD. Event replay proved that its more liquid early calls filled and consumed the one-position slot before later put signals.
- Stop triggers at −25%, −35%, and −50% produced identical search metrics, so they did not provide an effective intraday loss-control lever in these runs. Earlier timed exits at minutes 240/270/300 sharply reduced return. Minute 360 improved the full return; minute 375 deteriorated in search.
- Daily regime gating was not a free risk filter. Symmetric 0/1/2% daily ROC gates lost 7.63–18.67% in search, and put-only shock gates lost 14.89–26.08%; the profitable search puts were being removed.
- The explicit U surface was smooth in search but not in validation. Later exits helped every strike pair, while 3% puts led search; the resulting C4/P3/E360 cell then suffered 65.25% June drawdown. Search smoothness did not license promotion.
- Global `OptionPositionCount < 1` was the first effective risk control. V3 changed June from O's −31.01% / 62.84% DD to +4.69% / 26.99% DD and reduced full maxDD from 44.36% to 22.69%, but it also concentrated the book further into whichever contract filled first.
- The W re-sweep proved that closer 2%/3% calls increased search return but filled early enough to consume the one-ticket slot before July's later puts. Both adjacent closer-call finalists lost July and failed the majority-validation rule.
- Correcting the stock-core entry window removed the pathological re-entry loop. Even so, a daily 15%/25%/35% per-name core returned only 24.38%/22.76%/20.88% in search after $372/$602/$825 of fees. Sparse impulse-only stock delta returned 108.13%/108.04%/107.74%, effectively no better than V3's 107.86% while adding fees.
- A positive one-day call gate at 0/1/2% returned 109.16%/109.54%/107.09% in search. The +1% cell AA1 modestly improved every full-path risk metric and May versus V3, but did so by avoiding losing calls rather than discovering a bullish edge.
- With the +1% daily gate fixed, closer 2%/3% calls returned 105.24%/107.84% versus 109.54% for 4% calls. Replacing the five-minute call with a 15-minute sustained impulse returned 105.40–106.31%; moving calls to minutes 240–300 returned 99.79–100.09%. All were dominated without opening validation.

## Full event attribution for C

Backtest `6a5c67be38b89b14af44ac94` exactly reproduced the non-event full result and produced 88 filled orders: 44 one-contract opens and 44 closes. All entries were same-day OCC contracts. Net sleeve P/L after entry and exit fees was:

| Sleeve | Round trips | Net P/L |
|---|---:|---:|
| SNDK puts | 9 | +$19,117.05 |
| MU puts | 11 | +$3,190.45 |
| SNDK calls | 13 | +$558.10 |
| MU calls | 11 | −$674.80 |

The result is therefore dominated by a small number of SNDK put convex wins, especially Jul 2. Calls did participate and SNDK calls were net positive, but this is not broad, stable bull-market outperformance: the strongest reset win occurred while the underlying baseline fell.

## Full event attribution for V3

Backtest `6a5c78e8ce63c9f6e4115e86` exactly reproduced V3's non-event +342.82% result and produced 44 filled orders: 22 opens and 22 closes. Every open was quantity one, every OCC expiration matched the fill date, and there were no unmatched positions. Net sleeve P/L after both-side option fees was:

| Sleeve | Round trips | Net P/L |
|---|---:|---:|
| SNDK puts | 4 | +$28,937.30 |
| MU puts | 6 | +$156.20 |
| MU calls | 10 | −$991.75 |
| SNDK calls | 2 | −$675.85 |

Both names and both option types therefore participate physically, but the event evidence rejects a bull-outperformance claim. Calls lose $1,667.60 in aggregate while four SNDK puts create more than the entire net profit. V3 is a materially safer downside-convex strategy, not the requested bull-market ripper.

## Full event attribution for AA1

Backtest `6a5c7bb34412b1d5eedba307` exactly reproduced AA1's +347.80% non-event result and produced 38 filled orders: 19 opens and 19 closes. All opened contracts were one long leg, quantity one, and true 0DTE. Net sleeve P/L after both-side fees was:

| Sleeve | Round trips | Net P/L |
|---|---:|---:|
| SNDK puts | 4 | +$28,937.30 |
| MU puts | 6 | +$156.20 |
| MU calls | 8 | −$845.65 |
| SNDK calls | 1 | −$423.80 |

The daily gate avoided three losing calls and raised net option P/L to $27,824.05, but calls still lost $1,269.45. AA1 improves risk and return by declining bad call trades; it does not create positive call alpha or bull-partition outperformance.

### S0 execution audit

The forced probe on 2026-07-10 is deliberately not a candidate. It opened one MU call and one SNDK
call at minute 60, closed them at minute 90, opened one MU put and one SNDK put at minute 120, and
closed them at minute 150. Raw events showed:

- each buy used a one-leg `OpenOption` action with `direction: long`;
- each selected OCC expiration was exactly `2026-07-10` (0 DTE);
- requested and final quantity were exactly one contract;
- the risk audit reserved the resolved contract cost and reported no unhedged short contracts;
- both names and both option types completed round trips; and
- the run lost 6.60% with 12.05% max drawdown, which illustrates why a forced execution probe is not
  strategy evidence.

Probe backtests on 2026-07-02 (`6a5c5e3604196c7dbc7edfb0`) and 2026-06-26
(`6a5c5e3a04196c7dbc7edfb7`) also completed with two-name participation. Their returns are excluded
from candidate evidence.

## Final verdict

**NULL / NOT OUTSTANDING / NOT DEPLOYED.** The best fresh current-engine design is AA1, portfolio `6a5c7a964412b1d5eedba11e`. It is a genuine risk improvement: +347.80% full return, Sortino 6.84, and 22.38% max drawdown versus +450.85%, Sortino 5.85, and 34.46% max drawdown for 50/50 buy-and-hold. It clears the campaign's alternative 65%-of-baseline risk clause and has two profitable validation partitions. It still fails the independently binding bull-regime clause: search returned +109.54% versus +191.54% for the baseline, May lost 6.45% while the baseline gained 71.81%, June earned only 4.69% versus 21.51%, and the calls lost $1,269.45 in the full event ledger. Its +240.03% July reset occurred while the baseline fell 8.07% and was driven by SNDK puts, so it cannot honestly be labeled a bull-market ripper.

There is no honest live-ready winner from this attempt. The same blocker survived repeated independent mechanism families: available 0DTE call entries on MU/SNDK produced negative aggregate call alpha, while the only near-baseline return came from a handful of SNDK put fills in falling tapes. The corrected same-day stock sleeves proved that broad intraday delta cannot cheaply recreate the overnight buy-and-hold path: the daily core paid hundreds of dollars in turnover fees, while sparse bull-delta entries added no return over the option-only book. The one-contract minimum remains coarse for an $8,000 account, and no allowed sizing, timing, regime, moneyness, concurrency, or same-day delta branch satisfied the frozen bull bar. The campaign is therefore blocked/null rather than weakened after seeing results. No deployment, reconciliation, staged order, or live mutation was performed.
