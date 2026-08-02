# Episode 11 Attempt 8 — SNDK + MU Options-Only Concurrency Retest

**Started:** 2026-07-20
**Capital:** $8,000 fixed cold-start capital
**Intended target:** `MU + SNDK Live Trading Portfolio`
**Status:** PAPER RESEARCH FINALIST — accelerated live-readiness remains unproven; no orders staged

## Mandate

Build and certify an outstanding intraday strategy on MU and SNDK using only outright long calls and
puts. Stock actions, debit or credit spreads, short option legs, and overnight option exposure are
forbidden. The active hybrid paper portfolio `6a5e1f9d814d31180a1c8768` remains unchanged as a separate
benchmark; it is not an eligible Attempt 8 candidate.

## Hard constraints

- Universe exactly `MU` and `SNDK`.
- Every entry is one single-leg long call or long put, allocated as an explicit contract count.
- No stock Buy/Sell actions, multi-leg structures, spreads, or short option legs.
- Both names and both option types must be present in persisted structure and fresh fill evidence.
- Initial value is exactly $8,000; all options close before the bell.
- Every strategy keeps `automaticOrderApproval: false`.
- Global concurrent option positions are a controlled search axis: 1, 2, and 3.
- No paper/live deployment, reconciliation, or staged orders without new explicit authorization.

## Fresh-evidence rule

All earlier artifacts are inspiration or incumbents only. Attempt 8 creates new portfolio artifacts and
current-engine runs. Search results may kill or promote a candidate but cannot certify one. Any promoted
configuration must receive fixed-configuration walk-forward evidence and a fill/concentration audit.

## Frozen first-stage concurrency experiment

The seed mechanism is the current-engine AA1 impulse family: exact 0DTE, 4% OTM calls, 3% OTM puts,
price/VWAP direction, five-minute ROC crossing +/-0.75%, a +1% daily ROC gate on calls, one contract,
100% take profit, 50% stop loss, and minute-360 flatten. Only the global `OptionPositionCount` ceiling
changes between variants.

| Candidate | Global ceiling | Purpose |
|---|---:|---|
| C1 | `< 1` | Fresh incumbent control |
| C2 | `< 2` | Permit two simultaneous option positions |
| C3 | `< 3` | Stress-test additional concurrency and affordability |

## Evaluation contract

- Full continuous path: 2026-01-02 through 2026-07-10 from one $8,000 start.
- Primary baseline: fresh 50/50 MU/SNDK buy-and-hold, +450.85%, Sortino 5.85, maxDD 34.46%.
- Promotion favors return, positive Sortino, drawdown no worse than the baseline, real calls-and-puts
  participation, and less dependence on a single outlier trade.
- The final verdict requires fixed walk-forward OOS evidence; full-period resubstitution is insufficient.

## Campaign ledger

| Time | Stage | Artifact | Result | Status |
|---|---|---|---|---|
| 2026-07-20 | Reset | This log | Options-only mandate and 1/2/3-slot screen frozen | ACTIVE |
| 2026-07-20 | Paper state | Hybrid `6a5e1f9d814d31180a1c8768` | Reactivated and left unchanged | SEPARATE BENCHMARK |
| 2026-07-20 | Structure | C1 `6a5e281e2ee25ecab46c2203`; C2 `6a5e28272ee25ecab46c2213`; C3 `6a5e282fea0d6db55c69b2a6` | All valid and persisted: 4 single-leg long entries, 1 contract, exact 0DTE, no stock actions, approvals off | PASS |
| 2026-07-20 | Full screen | C1 BT `6a5e285d2ee25ecab46c2294` | +347.80%, Sortino 6.84, maxDD 22.38% | RISK LEADER; PROMOTE |
| 2026-07-20 | Full screen | C2 BT `6a5e2861814d31180a1ca3cd` | +377.48%, Sortino 5.58, maxDD 44.20% | RETURN LEADER; DD FAIL VS BASELINE |
| 2026-07-20 | Full screen | C3 BT `6a5e28642ee25ecab46c229c` | Identical to C2 | REDUNDANT — per-name spread caps limit realized concurrency to two |
| 2026-07-20 | Event audit | C1 event BT `6a5e28f42ee25ecab46c22df` | 19 trades; calls −$1,269.45; puts +$29,093.50; largest trade +$19,626.20 | CONCENTRATION/CALL-EDGE FAIL |
| 2026-07-20 | Event audit | C2 event BT `6a5e292dea0d6db55c69b37d` | 37 trades; calls −$1,262.85; puts +$31,461.25; largest trade +$19,626.20 | CONCENTRATION/CALL-EDGE FAIL |
| 2026-07-20 | Sweep preview | C2 call-only 3-axis request | All axes correctly rejected: compiler cannot target nested call-only thresholds or option-type-specific legs | CAPABILITY LIMIT; EXPLICIT GRID USED |
| 2026-07-20 | Explicit call grid | 27 valid immutable portfolios / 27 completed search BTs | Cross {0.5,0.75,1.0} × daily ROC {0,1,2} × call OTM {2,4,6}; best +131.85%, Sortino 6.72, DD 19.17% | SEARCH COMPLETE; ROBUST REGION PROMOTED |
| 2026-07-20 | Call-grid validation | 5 neighboring cells × May/June/July | May −8.08% to +11.37%; June −10.63% to −27.14%; July +289.24% to +295.42% | FAMILY KILL — weak May/June and July tail dependence |
| 2026-07-20 | Asymmetric DTE screen | Calls 1–7 `6a5e2eb9c0ccd581202564be`; 8–14 `6a5e2ebeca725b4a5d9cd3ae`; 15–30 `6a5e2ec5ca725b4a5d9cd3c2` | Search +136.79% / +141.94% / +18.15% | 1–7 PROMOTE; 8–14 RISK FAIL; 15–30 KILL |
| 2026-07-20 | 1–7 DTE validation | May `6a5e2f21e52c3fd9a4c9bb77`; June `6a5e2f24ca725b4a5d9cd405`; July `6a5e2f28c0ccd581202564f9` | +1.17%, +163.11%, +290.15% | FIRST POSITIVE 3/3 OOS SURVIVOR |
| 2026-07-20 | Full/event audit | Portfolio `6a5e2eb9c0ccd581202564be`; BT `6a5e2f73e52c3fd9a4c9bbd6` | +657.36%, Sortino 6.46, maxDD 37.45%; 108 trades; calls +$20,005.50, puts +$32,583.35 | RETURN/SORTINO PASS; DD 2.99pp WORSE THAN BASELINE — EXIT TUNING REQUIRED |
| 2026-07-20 | Exit grid | 27 valid immutable portfolios / 27 completed search BTs | Stop {35,42.5,50} × flatten {300,330,360} × TP {100,150,250}; stop/TP non-binding, flatten controls surface | F300 PROMOTED |
| 2026-07-20 | Exit OOS | F300 portfolio `6a5e3103ca725b4a5d9cd55c` | May +95.71%, June +138.70%, July +284.01% | PASS 3/3 |
| 2026-07-20 | Full finalist | F300 BT `6a5e3394e52c3fd9a4c9c582` | +569.09%, Sortino 5.49, maxDD 32.12% vs baseline +450.85%, 5.85, 34.46% | PASS — +118.24pp return and 2.34pp lower DD |
| 2026-07-20 | Fixed WF cert | Study `6a5e340bca725b4a5d9cdbaf` | OOS +22.87%, +98.56%, +38.55%, +408.75%; min Sortino 4.00; 0 unmet constraints | PASS 4/4 |
| 2026-07-20 | Exact event rerun | BT `6a5e34ade52c3fd9a4c9c651` | Reproduced +569.09%, DD 32.12%; 108 trades; calls +$20,554.50, puts +$24,972.35; largest trade 37.46% of P&L | PASS WITH CONCENTRATION WATCH |
| 2026-07-20 | Paper deploy | Source `6a5e3103ca725b4a5d9cd55c` → paper `6a5e3bbfc0ccd58120257cc8` | Active, $8,000 cash, 7 strategies, option-only field audit passed, approvals off, no positions/orders staged | DEPLOYED |

## Certified finalist

Portfolio `6a5e3103ca725b4a5d9cd55c` is the Attempt 8 options-only finalist:

- Two global concurrent option positions maximum (`OptionPositionCount < 2`).
- MU and SNDK long calls: one contract, one leg, 4% OTM, nearest 1–7 DTE.
- MU and SNDK long puts: one contract, one leg, 3% OTM, exact 0DTE.
- Calls require price above VWAP, five-minute ROC crossing above +0.75%, and one-day ROC above +1%.
- Puts require price below VWAP and five-minute ROC crossing below −0.75%.
- Entry window minute 15–150; all positions flatten at minute 300.
- Take profit +150%; stop loss −42.5%; both were non-binding on the training exit surface.
- Every strategy has `automaticOrderApproval: false`; there are no stock actions, spreads, short legs,
positions, staged orders, or reconciliations on the source chat portfolio. Its exact clone is active as
paper portfolio `6a5e3bbfc0ccd58120257cc8`.

## Remaining risk disclosure

The largest trade contributes 37.46% of exact-run P&L, so concentration is material but no longer a
majority of total P&L. MU calls remain slightly negative (−$477) while SNDK calls are strongly positive
(+$21,031.50). This is a certified research finalist, not permission to replace or deploy over the active
hybrid paper benchmark. The paper clone has no positions yet and will evaluate future signals with
automatic approvals disabled.

## Bug ledger

### Accelerated live-readiness audit — 2026-07-20

The owner requested an immediate deploy-readiness decision without waiting for forward paper fills. The
frozen finalist was therefore tested on the only completed post-freeze sessions not used by the original
January 2–July 10 search: July 13–17.

| Test | Artifact | Result | Gate |
|---|---|---|---|
| $8k post-freeze holdout | `6a5e41a3ca725b4a5d9cedef` | +9.62%, Sortino 6.83, maxDD 28.86%; one MU put; SNDK zero fills | POSITIVE BUT INSUFFICIENT — one genuinely unseen round trip |
| Exact rerun, alternate baseline | `6a5e41a6c0ccd58120258458` | Exact identity at 0 bps; +9.62% vs SNDK −24.0% and MU −8.3% | REPRO PASS; realized breadth 1/2 |
| $25k fixed-capital breadth diagnostic | `6a5e4284c0ccd581202586bb` | −0.35%, Sortino 0.45, maxDD 12.41%; both names filled | DIAGNOSTIC ONLY — not comparable to the $8k deploy path |
| Fold-0 standalone replay | `6a5e421be52c3fd9a4c9daf1` | +22.8675%, Sortino 3.9972, maxDD 28.6113% | EXACT MATCH to study |
| Fold-2 standalone replay | `6a5e4221c0ccd58120258561` | +38.5544%, Sortino 4.4172, maxDD 39.0047% | EXACT MATCH to study |
| July-20 partial-session request | `6a5e41a9c0ccd5812025845d` | Engine returned July-17 market data only; zero strategy evaluations/resolutions | NOT CURRENT-DAY EVIDENCE |

The $8k result is positive but too thin to certify by itself. SNDK had 33 resolution attempts, including
two `cannotAfford` rejections and 29 `noDteWindow` rejections, and no fill. One rejected SNDK contract
had estimated max loss of about $7,901.94 against $7,800 effective buying power. The $25k run kept the
same fixed signals and one-contract actions, but the additional buying power admitted a SNDK contract
that the $8k path rejected and changed the return denominator. It is therefore a useful capital-sensitivity
and breadth diagnostic, not an apples-to-apples holdout and not evidence that the $8k strategy failed.

**Accelerated verdict: NOT YET PROVEN for live money; paper only.** Withdraw the earlier claim that the
$25k loss rejects the $8k strategy. The clean post-freeze $8k evidence is +9.62%, but consists of one MU
put round trip; the requested July-20 run contained no current-session strategy data; and the authored
P/L exits remain unvalidated. The four favorable fixed walk-forward folds support historical stability,
but their dates were already touched by the January–July strategy search, so they are not a pristine
post-design lockbox.

### ⚠️ BUG/ISSUE — walk-forward worst-drawdown aggregation

Study `6a5e340bca725b4a5d9cdbaf` stores OOS max drawdowns of 28.6113%, 34.3711%, 39.0047%, and
37.3025%, but reports aggregate `oosMaxDrawdown.worst = 28.6113`. The worst drawdown is 39.0047%.
Standalone replays above confirm the per-fold values. See `WALK_FORWARD_WORST_DRAWDOWN_BUG.md`.

### ⚠️ BUG/ISSUE — P/L close triggers did not bind

In post-freeze holdout `6a5e41a3ca725b4a5d9cedef`, the MU put entered at $1.9125, marked above
$11 during the next sampled hour (well above the +150% take-profit), and exited only through the
minute-300 flatten at $9.625. The full event audit likewise attributed every paired exit to the
minute-300 strategy, including trades ending below −42.5%. Until minimally reproduced and fixed, the
+150% take-profit and −42.5% stop-loss must not be treated as live risk controls. See
`PNL_CLOSE_TRIGGER_NONBINDING_BUG.md`.
