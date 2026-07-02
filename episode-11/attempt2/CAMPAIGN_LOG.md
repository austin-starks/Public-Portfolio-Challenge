# Episode 11 / Attempt 2 — Participation Repair Campaign Log

Goal: live book only buys OSCR → restore actual cross-watchlist participation at a similar-ish
validated gain to v3. Driven autonomously by Claude Code through Stages A–D (Stage E deploy gated).

Today: 2026-07-01. Capital base: $25,000 cold-start. Universe (21): ANET DUOL HOOD LLY GS META TSM
AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD MU SNDK SPCX.

---

## Stage A — Reproduce collapse + true fixed-$25k breadth  ✅

**Live config = v3 confirmed** (7-rung deep-OTM outright-call ladder ATM/+10/+20/+35/+50/+75/+100 @
365–730 DTE, per-name 5%, total budget 40%, 63D-ROC rank, TP 250%, `automaticOrderApproval:false`).

**Live-collapse evidence (OptionResolutionAttempt, 2026-06-29):** rebalance targeted 7 names (SPCX, MU,
DDOG, SNDK, OSCR, OKTA, AMAT); **6 rejected "cannot afford even 1 contract" (alloc 5% ≈ $1.2–1.45k),
only OSCR resolved** (~$1,205). That's the single-name book, live.

**Fixed-$25k breadth of v3 is an illusion:**
- Existing v3 12mo breadth backtest `6a39ae235346252f5d06637f`: participation 0.90 / 19-of-21 —
  BUT per-name shows 1–3 fills amid **hundreds of `cannotAfford`** (APP 481 rejects / **0 fills**,
  SNDK 336/1, MU 239/2, LLY 203/2, NET 161/1, DUOL 150/1, AVGO 146/1). "19 names" = cumulative
  lucky single entries over 12mo at rising NAV, not simultaneous cold-start breadth.
- Fresh v3 12mo @ $25k `6a44f570926676a04c795b8e`: +241.2% / DD 11.5% / Sortino 6.48 / participation
  0.90 / 19 names / **median deployment 41.8%** (compounds to ~$85k → late breadth is NAV-driven).

**Root cause:** at $25k, 5%/name affords only the cheapest LEAP (OSCR); budget is stranded on
unaffordable top-weighted names (engine does not backfill). Structural, not a data glitch.

---

## Stage B — Fixes (sweep + hand-built variant)

### Sweep engine OUTAGE (blocker for the sizing/convexity sweep) ⚠️
Three `engine_kind:sweep` walk-forward studies all **ERROR at unitsDone:0** with identical
`Failed to load optimizer after claim: BSON error … invalid type: unit value, expected a map`:
- `6a44f60a926676a04c795d44` (sizing sweep, cert, custom fitness) — ERROR
- `6a44f66dbcd19f94d5aaa82f` (same, no custom fitness) — ERROR
- `6a44f6a0bcd19f94d5aaa8bc` (minimal 2-gene, no cert, smoke test) — ERROR
→ Engine-side sweep bug, independent of config. Sizing/convexity re-optimization (levers A/D)
**cannot run until the sweep engine is fixed.** `backtest_only` cert path is unaffected (below).

### Lever E — wide ≤30 DTE debit-spread backstop (hand-built, per Austin's steer) ✅ built
Variant `6a44f651bcd19f94d5aaa7d1` = v3 + appended structure rung "Wide call debit spread (≤30 DTE)"
(long ATM / short +25% OTM, 7–30 DTE, tried only after all 7 LEAP rungs) + a CloseOption to exit
verticals at maxDte 4 (avoid pin). Spread-shape compliant (long-dated = outright calls; the only
vertical is ≤30 DTE).

**Fixed-$25k breadth (12mo `6a44f672bcd19f94d5aaa857`): participation 1.00 / 21-of-21 / median
deployment 61.9%.** Every premium name now fills via the backstop (LLY 18, MU 31, NET 21, DUOL 17,
SNDK 48, APP 31, META 8, AMAT 8); `namesWithRejectionsAndZeroFills: []`. Return +818% / DD 28.3% /
Sortino 5.69 / fees $456 (vs v3 $34 — higher churn, but far from v2's $1.5–8.9k/fold theta-bleed).
⚠️ 12mo is a bull window — OOS cert (2022 + Apr-2025) is the real test (v2 died there). RUNNING.

---

## Performance bar (v3, certified PASS attempt1)
OOS folds all 5 positive: mean +110% / median +108% / min +62.2% · Sortino min 3.34 · maxDD worst 28.6%.

## Stage C — Certification (walk-forward BLOCKED → fixed-window stress backtests)

### Walk-forward orchestrator is FULLY down ⚠️
`backtest_only` walk-forward ALSO errors identically (`6a44f6df…` variant, `6a44f6e3…` v3 — both
engineKind "Parameter", both `Failed to load optimizer after claim` at unit 0). So **no walk-forward
cert of any kind runs right now** — not sweep, not backtest_only. True OOS certification (train/val/
embargo) is BLOCKED on the engine. Plain `backtest_portfolio` is unaffected → used for fixed-window
stress tests over the exact regimes that killed v2 (2022 bear, Apr-2025). These are FULL-SAMPLE fixed
backtests, NOT walk-forward OOS — optimistic, and the comparison (not the absolute level) is the signal.

### Fixed-$25k stress comparison — v3 vs debit-spread variant (E)
| Window | Metric | v3 (deep-OTM only) `…700e` | Variant + wide ≤30DTE spread `…7d1` |
|---|---|---|---|
| **Full cycle** 2022-01→2026-07 | Return / maxDD / Sortino / fees | +1,613% / **35.6%** / 3.51 / $123 | +1,869% / **47.6%** / 2.84 / $970 |
| | id | `6a44f734…a31` | `6a44f72e…a16` |
| **2022 bear** 2022-01→2023-01 | Return / maxDD / Sortino | **−10.3%** / 28.1% / −0.37 | **−28.0%** / 36.3% / −1.06 |
| | id | `6a44f730…a1e` | `6a44f72a…f1a` |
| **Apr-2025** 2025-01→2025-10 | Return / maxDD / Sortino | +132% / **37.6%** / 4.68 | +167% / **53.0%** / 3.25 |
| | id | `6a44f732…a26` | `6a44f72c…a08` |
| **12mo bull** 2025-07→2026-07 | Return / maxDD | +241% / 11.5% | +818% / 28.3% |
| **Cold-start breadth** (12mo) | participation / med. deploy | 0.90 (illusory*) / 41.8% | **1.00 (real) / 61.9%** |

\* v3's 0.90 = cumulative lucky single entries amid hundreds of `cannotAfford`; variant's 1.00 = every
name actually funds via the ≤30DTE backstop, `namesWithRejectionsAndZeroFills: []`.

---

## VERDICT (Stage D)

**The mechanism Austin asked for WORKS for participation, and beats v2 decisively — but it is a
higher-drawdown book, not a risk-neutral fix, and it is NOT yet certified (engine outage).**

- **Participation: SOLVED.** Wide ≤30 DTE debit-spread backstop → 21/21 names actually fund at
  cold-start $25k (vs live = OSCR-only, vs v3 = 1–2 real names + breadth illusion).
- **Gain: ≥ similar.** +1,869% full cycle vs v3 +1,613%; higher in every sub-window.
- **Risk: materially worse, consistently.** maxDD +12pp full cycle (47.6 vs 35.6), bear −28% vs −10%,
  Apr-2025 DD 53% vs 38%; Sortino lower everywhere (2.84 vs 3.51). Fees 8× ($970 vs $123) but far from
  v2's $1.5–8.9k/fold — the *wide, pin-managed* spread avoids v2's theta-bleed collapse (v2 was
  −63→−76% in 2022 / 61.6% DD Apr-25; this variant −28% / 53%).

**Two hard caveats:**
1. **NOT certified.** Walk-forward engine (sweep AND backtest_only) is down — these are full-sample
   fixed backtests, optimistic vs true OOS. Re-run the walk-forward cert when the engine is back.
2. **Knobs are inherited (amber).** TP 250 / 5%/name / 40% budget / 63D rank carried from v3, NOT
   re-swept on the new debit-spread structure (standing rule #1). The width (+25%), sleeve DTE, and
   pin-close (maxDte 4) are hand-set. The sizing/width/share-cap sweep (levers A/D/E-tuning) is the
   blocked step that would properly co-optimize DD down.

**Recommendation:** the debit-spread backstop is the right direction for real participation and is
production-plausible, but before deploy it needs (a) walk-forward OOS certification once the engine is
restored, and (b) a sweep of spread width / sleeve share / per-name size to pull the 47% full-cycle DD
back toward v3's 35%. NO deploy yet (Stage E gated).

## Stage C (redo, engine restored) — TRUE walk-forward OOS certs ✅

Both `backtest_only` walk-forward certs COMPLETED (fixed book, 5 anchored folds, 2022→2026-07,
`winnerStableAcrossFolds: true` both).

| OOS aggregate (held fixed) | v3 (deep-OTM) `6a44f941…` | Debit-spread variant (E) `6a44f93d…` |
|---|---|---|
| %chg per fold | 108 / 148 / 65 / 120 / 104 | 104 / 237 / 117 / 119 / 333 |
| %chg mean / median / **min** | +109% / +108% / **+64.8%** | +182% / +119% / **+104%** |
| Sortino mean / **min** | 5.63 / **3.51** | 4.12 / **2.92** |
| maxDD mean / **worst-fold** | 20.5% / **30.4%** | 36.6% / **48.3%** |
| OOS participation (names) | 0.71–0.86 (15–18) | 0.90–1.00 (19–21) |
| Verdict (all folds +, Sortino≥0.5) | **PASS** | **PASS** |

**Both certify.** The variant's every OOS fold is positive with **higher min return (+104% vs +64.8%)
and higher mean (+182% vs +109%)** and more names — but **~1.6–1.8× the OOS drawdown** (worst fold
48.3% vs 30.4%) and lower risk-adjusted Sortino (min 2.92 vs 3.51). "Similar-ish gain" is met/exceeded;
the price is drawdown.

### DD-taming sweep — first attempt ERRORED, and the error is a finding
`6a44f94b…` (certification:true) died at fold 0: *"no individual passes fold selection constraints on
validation statistics (every candidate violated at least one configured floor)."* Fold-0 validation =
**2022-07→2023-01 (deep bear)**, and **no sizing candidate (4–8% alloc, 24–40% budget) could clear the
%chg≥0 / Sortino≥0.5 floor there.** ⇒ the variant's bear fragility is **structural, not a tuning miss** —
sizing alone can't make the short-dated sleeve certify through the 2022 bear.
Relaunched as `6a44fa58…` (no hard floors, rank by maxDrawdown/Sortino) to still surface the *lowest-DD*
sizing — RUNNING.

### DD-taming sweep (no-floor) COMPLETE — `6a44fa58…` — sizing CANNOT tame the DD
Swept alloc {4,6,8}% × budget {20,30,40}% × TP {150,250}, ranked by DD/Sortino, 5 folds.
`winnerStableAcrossFolds: false`. Best-per-fold OOS aggregate: **%chg mean +133% / min +33.9% ·
Sortino mean 3.50 / min 1.83 · maxDD mean 34.6% / worst-fold 43.9%.** Cross-fold robust (maximin
Sortino) pick = 8%/40%/TP150 (`6a44fb2a…f3`), min-fold Sortino 1.90.
→ Even the tamest sizing leaves OOS DD ~35% mean / ~44% worst — barely below the base variant
(36.6/48.3) and still far above v3 (20.5/30.4), while return drops (+133% vs +182%). **The drawdown is
structural to the short-dated sleeve, not a sizing miss** (confirmed twice: the cert-floor sweep
couldn't clear the 2022-bear floor at any sizing; the no-floor sweep can't get DD near v3 at any sizing).

---

## FINAL VERDICT (Stage D)

**Your instinct was right — the wide ≤30-DTE debit-spread backstop is the mechanism that gives real
cross-watchlist participation, and it CERTIFIES out-of-sample. But it is a higher-drawdown book, and
that drawdown is structural (sizing can't remove it) — so the choice is a risk-appetite call, not a
free lunch.**

| | v3 (live/deep-OTM) | Debit-spread variant (E) | Variant, tamest sizing |
|---|---|---|---|
| Real cold-start participation | **1 name (OSCR)** live / illusory 0.90 | **21/21 (1.00)** | ~20/21 |
| OOS return mean / min | +109% / +65% | +182% / +104% | +133% / +34% |
| OOS Sortino min | 3.51 | 2.92 | 1.83 |
| OOS maxDD mean / worst | 20.5% / 30.4% | 36.6% / 48.3% | 34.6% / 43.9% |
| OOS cert (folds +, Sortino≥0.5) | PASS | PASS | PASS (no-floor rank) |

**Recommendation:** two honest paths, pick by risk appetite —
1. **Breadth-max:** deploy the debit-spread variant `6a44f651…7d1` (or tamer 6%/30%/TP250) — full
   participation + higher return, accept ~44–48% OOS drawdowns. Needs a re-sweep on its OWN structure
   before deploy to de-amber the inherited knobs (spread width, sleeve DTE aren't sweepable → hand-set).
2. **Risk-controlled:** keep v3's deep-OTM structure and just raise per-name allocation so it funds
   ~4–6 real names at cold-start (fewer than 21, but genuine multi-name at v3-like ~30% DD). This is the
   lever-A sizing sweep on v3 — NOT yet run (it was the one blocked by the earlier engine outage).

NO deploy performed. Stage E remains gated on explicit "deploy + clean up".

## OPTION 2 COMPLETE (autonomous) — v3 sizing sweep `6a44fc7c…` — the standout path

Lever A on v3's deep-OTM structure (outright calls only; only per-name allocation moves). Swept
alloc {8,12,16}% × budget {40,60,80}% × TP {150,250}, 5 folds, ranked DD/participation/Sortino.
**Dominant + robust config: per-name 12% / budget 40% / TP 250% / top-21** (`9fd23458`; only change
vs live is 5%→12% alloc). `winnerStableAcrossFolds: false` (concentration shifts by regime).

OOS aggregate (best-per-fold): %chg [87,159,205,154,273] **mean +176% / min +87%** · Sortino
[4.20,4.70,4.92,4.83,5.72] **mean 4.87 / min 4.20** · maxDD [19,25,40,37,35] **mean 31% / worst 40%** ·
participation **13–18 names (0.62–0.86)**, deployment ~85–97%.

### Three-way OOS comparison (all certify; all folds positive)
| | v3 as-is (5%/name) | **v3 sizing 12% (opt 2)** | Debit-spread variant (opt 1) |
|---|---|---|---|
| Real cold-start participation | 1 (OSCR) live | **13–18 names** | **19–21 names** |
| OOS return mean / min | +109% / +65% | **+176% / +87%** | +182% / +104% |
| OOS Sortino min | 3.51 | **4.20 (best)** | 2.92 |
| OOS maxDD mean / worst | 20.5% / 30.4% | 31% / 40% | 36.6% / 48.3% |
| Structure | outright calls | **outright calls (clean)** | + short-dated verticals |
| Provenance | live | 1 knob (amber-lite) | hand-built sleeve (amber) |

**Updated recommendation:** **Option 2 (per-name 12%) is the best risk-adjusted path** — near-variant
return (+176%), the **highest OOS Sortino of all three (min 4.20)**, moderate DD (worst 40% vs the
variant's 48%), genuine multi-name participation (13–18), and it stays 100% outright-calls (no
theta-bleed sleeve, spread-shape clean, only ONE knob changes from the live book). The debit-spread
variant wins on raw breadth (19–21) and slightly higher return, but at worse Sortino and drawdown.
Fold winners materialized: opt-2 robust pick `6a44fd86…9f6`. Neither deployed — Stage E still gated.

---

## Option 2 fixed-config OOS cert — CORRECTION to the "4.20 Sortino" above
Backtest_only cert of the exact 12% config (`6a4509aa…`): OOS %chg [134,147,205,78,273] mean +167% /
**min +78%** · Sortino [6.09,5.03,4.92,2.49,5.72] **min 2.49** · maxDD mean 31% / **worst 46%** · 14–17
names. ⇒ The "min Sortino 4.20 / DD 40%" in the table above were the sweep's *per-fold-optimized*
numbers (optimistic); the **deployable fixed config is min Sortino 2.49 / worst DD 46%**. Held-fixed,
Option 2 does NOT clearly beat the debit-spread variant. Config verified by field (per-name 12%, budget
40%, TP 250, top-21, all outright LEAPs). Deploy portfolio built + renamed: `6a450c04bcd19f94d5aae3d7`.

## DEPLOY attempt + halt (only-SPCX reconcile)
Cloned Option 2 onto LIVE `69a7dc7a…` (strategies replaced; nothing staged). **Reconcile target came
back a SINGLE SPCX $300 LEAP** (would sell OSCR+LLY for −$1,685 to buy one contract). Investigated via
the (now-exposed) reconcile events:
- Cause: rebalance picks **top-3 by 63D ROC = SPCX, MU, DDOG**; MU ($30.6k) & DDOG unaffordable at 12%;
  reconcile is a **single tick** (no backfill pre-fix) → only SPCX cleared. Not an SPCX fault.
- **My errors (retracted):** (1) claimed reconcile "generates no events" — false, it does, just wasn't
  exposed (Austin fixed exposure). (2) called the SPCX contract "impossible data" off the event
  snapshot's `SPCX=$21.98`; **live SPCX is $172.10** (get_options_chain) → the $300 strike (+74% OTM)
  at $28 is legitimate. Real oddity for Austin's events work: event payload stamped $21.98 vs live $172.
- Reconcile is now **blocked by auto-mode** (live mutation; deploy approval superseded). Nothing staged.

## Affordability BACKFILL engine fix (Austin) — VERIFIED ✅
Engine change: if a name can't afford 1 contract, **skip to the next ranked name** (lever B from the
runbook). Verified on a cold-start $29k single-tick events backtest (`6a454fb5…`): Option 2 opened
**~10 names in 3 days** (OSCR, OKTA, DUOL, HOOD, ANET, NET, XOM, GLD, AVGO, COP) vs **1 (SPCX-only)**
pre-fix. Pricey names still unaffordable (MU/SNDK/LLY/APP) are correctly skipped. **5%/name is now
viable** (was the broken OSCR-only case).
⚠️ Observation (flagged, not diagnosed): that tick deployed ~96% of NAV over 3 days, above the 40%
`totalBudget` — possibly per-tick stacking; worth an engine look.

## FULL SWEEP post-backfill (`6a454eee…`, alloc 5/8/12/16 × budget 40/60/80 × TP 150/250/400 × top 11/21)
OOS: %chg mean **+120% / min +55%** (all folds +) · Sortino mean 4.66 / **min 2.52** · maxDD mean 27.6%
/ **worst 44.8%** · 13–19 names · winner UNSTABLE (winners span 5–16%). Val≈OOS on return (~+120% both)
→ low overfit, except **16% badly degrades val +236%→OOS +84%**. Fix raised the participation FLOOR,
not the return ceiling. Recommendation shifted to **low allocation (~8%) deep-OTM** — breadth without
12%'s concentration or the debit-spread's theta/fees.

## Exit mechanics finding (why DD ~45%) — VERIFIED via close events (`6a456c2b…`)
- Only exit rule = **TP +250%** (closes winners). No stop-loss, no DTE roll.
- 12mo trace: **400/400 daily close-leg evals = SKIPPED_NO_TRIGGER**; realized closes ~100% win rate /
  ~+270% avg → exits are **TP winners; losers stay open** as unrealized drawdown.
- **SelectTop = 21 of a 21-name universe → the limit never binds → rotation-close never deselects a
  laggard.** So losers are neither stopped nor rotated out — they ride to expiry. This is the DD driver.
- Lever identified: **lower SelectTop (<21)** makes the rebalance rotate out momentum laggards (a
  momentum-native loss-cut); several full-sweep fold winners already chose **top-11**.

## IN FLIGHT — SelectTop sweep (`6a456feed9f46b79e55d5327`)
Genes: Select top {5,8,11,15,21} × alloc {5,8,12} × TP {250,400}, v3 base, post-backfill, 5 folds,
no-floor rank by DD/Sortino/participation/%chg. Goal: find the SelectTop that cuts drawdown via
rotation while keeping return/breadth; then fixed-config OOS-cert the winner. RUNNING.

## totalBudget BUG — confirmed, then FIXED (Austin) → prior results invalidated
Bug doc: `episode-11/attempt2/TOTALBUDGET_BUG.md`. Symptom: 40% `totalBudget` deployed ~96% of NAV at
cold start (backfill loop wasn't decrementing remaining budget per fill). **All attempt2 backtests/
sweeps before this point ran at inflated leverage → returns AND drawdowns overstated; budget gene was
non-differentiating.**

**Fix verified** (post-fix backtests):
- Cold-start first tick (`6a458139…`, $29k): day-1 fills OSCR+OKTA+DUOL+HOOD = **$12.4k ≈ 43% of NAV**
  (~40% cap, slight contract-granularity overshoot); subsequent days = rotation only, NOT +40% stacked.
- 12mo posture (`6a458140…`): median deployment **52%**, max **79.6%**, **0 days >90%** (= ~40% cost +
  LEAP appreciation). Budget now a binding cap. ✅

⇒ Everything below the Option-2 cert must be re-validated. **FULL RE-TEST running** on corrected engine:
`6a4581c1c62bc68393f6119d` — SelectTop {5,8,11,21} × alloc {5,8,12} × budget {40,60} × TP {250,400},
v3 base, 5 folds anchored 2022→2026-07, no-floor rank by DD/Sortino/participation/%chg. Superseded/
invalid (pre-fix): full sweep `6a454eee…`, Option2 cert `6a4509aa…`, SelectTop sweep `6a456fee…`.

## FULL RE-TEST post budget-fix — VALID results (`6a4581c1…`)
SelectTop {5,8,11,21} × alloc {5,8,12} × budget {40,60} × TP {250,400}, v3 base, 5 folds.
**OOS aggregate: %chg mean +62% / min +39% (all 5 folds +) · Sortino mean 3.77 / min 2.68 · maxDD mean
17% / worst 21% · 13–18 names.**

**Corrections vs the buggy runs:** with budget binding, **DD collapsed ~45%→~17–21%** and **return
+120–176%→+62%** — the bug was ~doubling both. This is the honest risk/return.

**SelectTop thesis CONFIRMED:** every fold winner uses **SelectTop 5 or 11 (never 21)** + **5% alloc**,
budget 40–60%, TP 250–400. Lowering the limit → rebalance rotates out momentum laggards = the loss-cut.
Fold winners: f0/f1 top?/5%; f2 top11/5%/60%/TP400; f3 top5/12%/60%/TP400; f4 top11/5%/40%/TP250.
Caveat: winner UNSTABLE; maximin pick (top5/12%) has a **−12.8% fold** (top-5 too concentrated).

**Finalist chosen (steadiest, least-leveraged): top-11 / 5% per-name / 40% budget / TP 250** —
materialized `6a4583e1d02da4ae54e67e67`.

### Finalist fixed-config OOS cert (`6a45845e…`) — PASS ✅ (best-validated config to date)
OOS %chg [56,99,62,99,39] **mean +71% / min +39%** (all 5 folds +) · Sortino [4.70,6.44,3.65,5.86,3.50]
**min 3.50** · maxDD [13.6,11.3,21.6,19.9,12.9] **mean 16% / worst 22%** · 13–17 names · winRate ~43–58%
(losers realized via top-11 rotation). Held-fixed numbers BEAT the per-fold-winner aggregate (mean +71
vs +62, min Sortino 3.50 vs 2.68) → generalizes well, not fold-overfit.
- vs deployed-book Option 2 (12%, buggy-era cert): min Sortino 3.50 vs 2.49, **worst DD 22% vs 46%.**
- Caveat: training/validation windows (2022-bear-heavy) are weak/flat (fold0 train −9%, val −12%); OOS
  (2023–2026 trending) strong. Edge is momentum-trending; soft in bear. DD now tame (~16–22%) regardless.
- Cold-start breadth (`6a458519…`, 12mo $25k): **16/21 names (participation 0.76)** — ANET/OSCR/COP/GS/
  ADI/MU/DDOG/GLD/OKTA/META/XOM/AMAT/AVGO/HOOD/NET/TSM fill; zero-fill = APP/DUOL/LLY/SNDK (cheapest
  contract > 5% slot even w/ backfill) + SPCX (noOptionsData in backtest; live has data). Concentration:
  ANET ~20%, OSCR ~12%, COP ~9%.
- CONCLUSION: **top-11 / 5% / 40% / TP250** = diversified (16 names cold-start), momentum-rotation
  loss-cut (top-11 deselects laggards), low leverage (40% budget), outright LEAPs, spread-shape clean.
  **Recommended deploy candidate.** Achieves the Ep-goal (participation across the watchlist at solid
  validated gain: OOS +71% mean / worst-DD 22%). Pending Austin's go + fresh reconcile (live blocked).

## Nega-end removal (stop-loss, P/L ≤ −40%) + debit-spread — both TESTED, both LOSE to the finalist
User asked: sell-to-close a spread when its P/L drops (stop-loss), esp. on a debit-spread book.

**A/B — deep-OTM finalist ± stop-loss (`6a458e34…`, fixed cert):** stop-loss HURTS.
| top-11/5%/40%/250 | no stop | + stop −40% |
|---|---|---|
| OOS ret mean / min | +71% / +39% | +61% / **+17%** |
| OOS Sortino min | 3.50 | **1.44** |
| OOS worst DD | 22% | **23% (no better)** |
Classic stop-on-convex-LEAP whipsaw: stops out of momentum names that then recover; kills return +
Sortino, zero DD benefit. **Top-11 momentum rotation is the better loss-cut; a P/L stop is redundant/harmful.**

**Debit-spread + stop-loss full sweep (`6a458e2e…`, COMPLETE 5 folds):**
OOS %chg [6, 127, 95, 67, 289] **mean +117% / min +6%** · Sortino [0.64, 4.16, 3.29, 2.11, 4.19]
**mean 2.88 / min 0.64** · maxDD [33, 24, 28, 35, 43] **mean 33% / worst 43%** · 12–19 names.
Higher HEADLINE return than the finalist (+117 vs +71) but **~2× the worst-fold drawdown (43% vs 22%)**
and a near-dead fold (Sortino 0.64). Even WITH the stop-loss, the ≤30-DTE debit-spread whipsaws/bleeds —
higher-octane, far less consistent. Loses to the finalist on risk-adjusted/consistency.

**VERDICT unchanged:** **deep-OTM top-11 / 5% / 40% / TP250 (no stop, no debit spread)** remains the
best — OOS +71% mean / min Sortino 3.50 / worst DD 22% / 16 names. Adding loss-cutting machinery
(stop-loss or short-dated debit spreads) only adds churn and drawdown here; the momentum-rotation
loss-cut already does the job. Recommended deploy candidate stands: `6a4583e1d02da4ae54e67e67`.

## STAGE E — DEPLOYED (user: "let's deploy this" → "stage it")
Finalist verified by field (SelectTop 11 / 5% / 40% / TP250 / 7 outright-LEAP rungs / approval off),
renamed deploy config `6a45951f664648e51f975c53`, **cloned onto LIVE `69a7dc7a…`** (isLive, replaced the
buggy-era 12% clone; 2 strategies). Reconcile preview (corrected engine, NAV $30,572): single-tick
target = 1 OSCR $32 call (same single-tick under-fill as noted — live strategy accretes the rest over
subsequent rebalances). **4 delta orders STAGED UNAPPROVED** (net +$3,650 credit, realized −$520, no
wash flags): roll OSCR $30→$32 (sell 4 / buy 1) + close LLY vertical (multiLegGroupId
`6a4596d2…dfa81`). Order IDs `…dfa82/dfa89/dfa8d/dfa91`. **Awaiting Austin's manual approval in UI;
tool did NOT submit to broker.** Post-approval: re-run reconcile to confirm delta→~empty; the deployed
top-11/5% strategy then builds the ~16-name book over the next daily rebalances.

## COLD-START BREADTH SOLVED — top-11 was the trap; top-21 is the fix (no code change)
Reconcile of the deployed top-11 showed target = **1 OSCR** again. Root cause (verified via reconcile
events): `SelectTop 11` truncates the candidate pool to the 11 highest-momentum names BEFORE affordability;
today 10 of those 11 are unaffordable at 5% (SPCX/MU/LLY/AMAT/DDOG/SNDK/TSM/GS/ADI/OKTA), only OSCR fits →
backfill has nothing else in the pool. The "16 names" I'd cited was a 12mo COMPOUNDING artifact. I
over-stated breadth; owned it.

**Fix = SelectTop 21** (full pool → backfill reaches cheap names XOM/COP/GLD/HOOD…). Confirmed:
- Full-sweep re-run (`6a45a568…`) dominant/robust winner = **top-21 / 5% / 40% / TP250** (also top-15 #1
  by val-Sortino) — the sweep independently favors the WIDE selection now that budget is fixed.
- Cold-start $30k first-tick (`6a45a74a…`): opens **OSCR, XOM, COP, GLD (day1) + HOOD** = 4–5 names vs
  top-11's 1. Backfill reaches affordable names because the pool is all 21.
- **Fixed-config OOS cert (`6a45a7aa…`) PASS:** %chg [76,54,48,94,105] **mean +75% / min +48%** · Sortino
  [5.19,3.28,2.90,4.22,5.41] **min 2.90** · maxDD [13,16,24,25,12] **worst 25%** · 17–18 names OOS.
- vs top-11 cert: ~equal OOS (+75 vs +71, min +48 vs +39), min Sortino 2.90 vs 3.50, worst DD 25 vs 22 —
  but top-21 **actually diversifies cold-start**. Tradeoff: no momentum loss-cut (top-21 never deselects);
  the loss-cut wasn't helping anyway (stop-loss hurt; top-11 edge marginal + broke cold-start breadth).

**NEW RECOMMENDED FINALIST: top-21 / 5% / 40% / TP250** (`6a45a705664648e51f978bea`). Supersedes the
top-11 deploy. Pending Austin's go to re-deploy: cancel the 4 staged top-11 orders, re-clone top-21 onto
live `69a7dc7a…`, re-reconcile (expect multi-name target), re-stage. Nothing changed yet on this decision.

## Artifact index
- Live/v3 config: `69a7dc7acdb6bf6a4681d36c` (live, now has Option 2 cloned) · `6a39ae0e1278ae0b7f69700e` (v3 build, per-name 5%)
- Option 2 (12%): `6a450132bcd19f94d5aaba82` · deploy-renamed `6a450c04bcd19f94d5aae3d7`
- Debit-spread variant (E): `6a44f651bcd19f94d5aaa7d1`
- Key studies: full sweep `6a454eee…` · Option2 fixed cert `6a4509aa…` · SelectTop sweep `6a456fee…`
- Live reconcile: BLOCKED by auto-mode (deploy approval superseded by engine changes + re-analysis)
