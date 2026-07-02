# Episode 11 / Attempt 2 — Participation Repair + Re-Certification, orchestrated by Claude Code

> **Paste this whole file into Claude Code** with the NexusTrade MCP server connected (Austin's
> account). My deployed live book (v3, certified in attempt1) is **only buying OSCR** — it is not
> participating across my watchlist. I need Claude Code to be the **orchestrator + independent
> verifier**: reproduce the participation collapse, find the **configuration fix** that restores
> **actual cross-watchlist participation** at a **similar-ish validated gain** to v3, and re-certify
> the fix with a walk-forward study. **Nothing deploys and no orders are placed** until I explicitly
> say "deploy + clean up" (gated Stage E). Not generalized: this operates on my real artifacts.

> **Operating principles:**
> - **The objective is participation WITHOUT giving up the validated edge.** The target is a config
>   that (a) actually holds multiple names simultaneously at cold-start $25k and (b) certifies at a
>   gain/risk profile *in the same ballpark* as v3 — not a config that maximizes breadth at any cost
>   (that's what v2's short-vertical sleeve did, and it **FAILED** cert).
> - **v3 is the performance bar, not a floor to beat.** "Similar-ish" = same order of magnitude of
>   OOS return, drawdown no materially worse, OOS Sortino above the ~0.5 floor. If the participation
>   fix costs some return, that trade is acceptable *if* it's modest and honestly reported.
> - **Changing sizing IS a structural change → re-sweep, never inherit v3's knobs.** (Standing
>   methodology rule from the attempt1 retro — see bottom. Per-name alloc / budget / sizing policy are
>   structure-dependent; a `backtest_only` cert on inherited knobs proves generalization, not that the
>   knobs are good for the new sizing.)
> - **Measure breadth at FIXED $25k, never on a compounded run.** The whole bug is that v3's headline
>   "19/21 names" came from NAV compounding + distinct-names-over-time. Cold-start simultaneous
>   participation is the metric that matters, and it must be read from `audit_backtest_breadth` at a
>   held-fixed capital base, not inferred from a full-cycle backtest that compounds to ~$300k notional.

---

> **Tools:** the NexusTrade MCP tools are deferred — load schemas via ToolSearch as you need them
> (`fetch_portfolios`, `get_portfolio`, `query_portfolio_events`, `summarize_portfolio_events`,
> `audit_backtest_breadth`, `backtest_portfolio`, `audit_backtest_posture`, `get_sweep_surface`,
> `run_walk_forward_study`, `get_walk_forward_study_results`, `list_walk_forward_studies`,
> `get_optimization_results`, `compare_backtests`, `clone_strategies_to_portfolio`, the reconcile tool,
> `create_orders`). Log your run to `episode-11/attempt2/CAMPAIGN_LOG.md` (the live-collapse evidence,
> the fixed-$25k breadth before/after, the sweep/study IDs, the per-fold OOS table, the re-cert verdict,
> the chosen fix with provenance labels, and — if Stage E runs — the reconcile preview/fills).

## The job

**My live book only buys OSCR. Find out why, fix the configuration so it participates across the
watchlist, and prove the fix still certifies at a similar-ish gain.** Claude Code does the running AND
the independent verification — the numbers are Claude Code's own.

### Fixed
- **Universe (21):** ANET DUOL HOOD LLY GS META TSM AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD MU SNDK SPCX.
- **Capital:** **$25,000**, Day interval. This is the whole point — the fix must work at cold-start
  $25k, not at compounded NAV.
- **Structure family:** outright-calls-only momentum-LEAP (v3's 7-rung deep-OTM ladder is the starting
  point). Only sizing/affordability knobs are in play; the let-winners-run convexity that drove v3's
  gain must survive.
- **Spread-shape rule (hard constraint — still in force):**
  - **Long-dated exposure (≥ ~120 DTE) = outright long calls ONLY** (uncapped convexity, no short leg).
  - **Any debit / vertical spread must be short-dated (≤ ~30 DTE).** (v2 proved a ≤30 DTE sleeve buys
    breadth but bleeds theta and **fails** cert — so a short sleeve is *not* the preferred fix here.)

### The performance bar to match (v3, certified PASS in attempt1)
| Metric | v3 certified |
|---|---|
| OOS folds (5, anchored, validation) | **all 5 positive** · mean +110% / median +108% / **min +62.2%** |
| OOS Sortino | mean 5.26 / **min 3.34** |
| OOS maxDD | mean 21.3% / **worst 28.6%** |
| Full-cycle backtest ($25k→compounded) | ~+1,510% / 43.5% maxDD / Sortino 3.32 |
| Spread-shape | outright calls only, 365–730 DTE — compliant |

"Similar-ish gain" = re-certified fix lands in the same neighbourhood on OOS return **and** does not
blow past v3's ~28.6% worst-fold OOS DD by a wide margin, **and** OOS Sortino stays well above 0.5.

### The subject + references (confirm by field/posture, never by name)
| Role | ID | What it is |
|---|---|---|
| **SUBJECT — LIVE** | `69a7dc7acdb6bf6a4681d36c` | Deployed book (v3 config). **The book that's only buying OSCR.** What we repair + re-certify. |
| ref — v3 build | `6a39ae0e1278ae0b7f69700e` | v3 deep-OTM ladder build (certified). Reference / re-sweep base. |
| ref — attempt1 log | `episode-11/attempt1/CAMPAIGN_LOG.md` | Full v1→v2→v3 history, incl. the affordability finding this attempt exists to fix. |

---

## What we already know (confirmed before writing this runbook)

Do not re-derive from scratch — **verify these hold**, then move on:

1. **The live rebalance targeted 7 names on 2026-06-29** (SPCX, MU, DDOG, SNDK, OSCR, OKTA, AMAT) —
   top-weighted by 63D ROC, 40% budget / 5% per name ⇒ ~8 slots. Only **OSCR resolved to an order**.
2. **The other 6 were rejected at option-resolution:** *"Cannot afford even 1 contract: every priced
   spread needs more than your allocation per contract. Allocation: 5% of portfolio, Buying power ≈
   $23.4k."* At ~$29k NAV, 5% ≈ $1,200–1,450; only OSCR's Jan-'28 $30 call (~$1,205) fit.
3. **v3's "19/21 breadth" was a NAV/compounding + distinct-names-over-time artifact** (attempt1 log
   lines 126–127 warned exactly this). Cold-start simultaneous breadth at $25k is far lower — the live
   book is the proof.
4. **`automaticOrderApproval: false`** on the live book — hence the `Pending User Approval → Canceled`
   order churn. Note it; it's a deploy-hygiene issue, not the root cause of single-name participation.

**Root cause in one line:** at $25k, a 5%-per-name budget only ever affords the *cheapest* underlying's
LEAP, and the sizing policy **strands the budget** on unaffordable top-weighted names instead of flowing
it to the next affordable ones — so the book collapses to one name.

---

## Stage A — Reproduce the collapse + measure true fixed-$25k participation

Claude Code runs this directly. Establish the *before* picture with hard numbers.

1. **`get_portfolio 69a7dc7acdb6bf6a4681d36c`** — confirm the deployed config really is v3 by **field,
   not name**: `conditionFieldAudit`, the 7 `structureTemplates` (ATM/+10/+20/+35/+50/+75/+100 % OTM,
   365–730 DTE, all single long call), `perNameAllocation` 5%, `totalBudget` 40%, weight 63D ROC,
   CloseOption TP 250%. Flag `automaticOrderApproval` state.
2. **`query_portfolio_events` (OptionResolutionAttempt, from 2026-06-25)** — confirm the "cannot afford
   even 1 contract" rejections and which names cleared. This is the live evidence of the collapse.
3. **`audit_backtest_breadth` at FIXED $25k** on the current v3 config (12mo window, and separately the
   full cycle). Capture **simultaneous distinct names held**, `participation`, `distinctNamesFilled`,
   and per-name `cannotAfford` counts. This quantifies the gap between certified-breadth (compounded)
   and real cold-start breadth. **Lead the Stage-A finding with this number.**

Deliver a one-paragraph *before* state: "at $25k the deployed book participates in ~N names, funds the
budget into the cheapest 1–2, and strands the rest as `cannotAfford`." Then go to Stage B.

---

## Stage B — Candidate fixes (hypotheses to VALIDATE, not assume) → sweep

The fixes below are hypotheses. **Do not hand-pick one and deploy it** — encode the levers as sweep
genes and let the walk-forward study choose, subject to the breadth floor and the spread-shape rule.
Because sizing changed, this is `engine_kind:"sweep"`, not `backtest_only` (standing rule #1).

**Candidate levers (the sizing/affordability knobs — all keep outright-calls-only):**

| # | Fix hypothesis | Lever | Trade-off to watch |
|---|---|---|---|
| A | **Raise per-name allocation** (e.g. 8–15%) | `perNameAllocation` | Funds ≥1 contract on more names, but fewer *simultaneous* slots (budget/alloc). Sweep already tried ≤12% in attempt1 — LLY's cheapest rung still ~$4.8k. Deep-OTM rungs change this; re-test. |
| B | **Affordability-aware / backfill sizing** — let stranded budget flow to the next affordable name instead of dying on an unaffordable top-weighted pick; or **guarantee 1 contract to top-N by weight** before doubling up | sizing policy / `weightIndicator` handling / min-1-contract rule | This is the most direct breadth lever at low NAV. Verify the engine actually backfills (Stage A rejections suggest it currently does **not**). |
| C | **Rung depth / count** — deeper OTM (already at +100%) or more granular rungs so premium names enter as cheap long-dated convex calls | `structureTemplates` | Deeper OTM = lower delta = weaker convexity capture. Watch OOS return erosion vs v3. |
| D | **Total budget** | `totalBudget` (currently 40%) | Higher budget = more slots fillable; interacts with per-name alloc. |
| E | **Short-dated WIDE debit spread sleeve** (≤30 DTE, long ATM / short +20–35% OTM) for names whose LEAP is unaffordable | `structureTemplates` (sleeve) + **width gene** + **sleeve-share cap gene** + name-eligibility | Short tenor buys affordability; **wide** keeps convexity v2's thin +3% threw away. But short tenor reintroduces theta bleed + roll/churn/fees — the exact thing that failed v2. Must clear the same OOS gates + a turnover/fee guardrail. |

**Why E is IN the sweep and not excluded (revised per Austin):** v2 did **not** disprove the vertical
class — it disproved one point in it (thin **+3%**, width fixed/unswept, **uncapped share**, every name
eligible). A short-dated *wide* debit spread is a different structure v2 never searched, and it's
spread-shape-legal (verticals ≤30 DTE). So we **let the sweep and OOS cert adjudicate it**, not a prior —
but instrumented so the v2 failure mode can't hide: **width is a gene** (not fixed), **sleeve share of the
book is a capped gene** (so it can't take over the way it did in v2), and it is judged on the **same OOS
gates + a turnover/fee guardrail** (Stage C). If it still bleeds theta / churns fees / craters the
Apr-2025 fold, it dies on *this* attempt's evidence.

**Genuinely out of scope:**
- **Pruning the universe** — Austin wants participation across *his* watchlist; don't drop names.
- **Adding capital** — out of scope unless Austin says so.

**Sweep setup:**
```jsonc
// mcp__nexustrade__run_walk_forward_study   (preview_only:true first — fold calendar + cost)
{
  "portfolio_id": "6a39ae0e1278ae0b7f69700e",   // v3 build as the re-sweep BASE (same structure)
  "engine_kind": "sweep",                         // GA overfits — sweep is the certified path
  "inner_mode": "optimize",
  "certification": true,                          // activity-floor + %chg≥0 + Sortino≥0.5 policy
  "mode": "validation",
  "walk_forward_mode": "anchored",
  "fold_count": 5,
  "global_start_date": "2022-01-01",
  "global_end_date":   "<TODAY>",
  "oos_width_days": 252,
  "embargo_days": 14,
  "interval": "Day",
  "gene_intents": [ /* per-name alloc, sizing/backfill policy, total budget, rung depth — levers A–D */ ],
  "preview_only": true
}
```
1. `get_sweep_surface` on the v3 build first to get the **real sweepable field names** for levers A–D.
2. Run `preview_only:true`; confirm the fold calendar spans 2022→today (must include the **2022 bear**
   and the **April-2025 selloff** — v3's worst DD is Apr-2025). Then run for real, record the `study_id`.
3. **Keep the spread-shape rule in the gene design** (long-dated = outright calls; no short leg ≥120 DTE).
4. **Add a breadth constraint to selection:** prefer/require candidates that hold **≥ a target number of
   names simultaneously at fixed $25k** (read via `audit_backtest_breadth`, not compounded NAV). A config
   that certifies but still funds one name is a non-answer.

---

## Stage C — Re-certification checks (these ARE the verdict)

Read per-fold OOS + breadth and decide PASS / FAIL holistically. **No single aggregate number.**

1. **Per-fold OOS table** for the chosen candidate held FIXED across all 5 folds: train/OOS windows,
   OOS return, OOS maxDD, OOS Sortino, median deployment, distinct names, participation + the aggregate.
2. **Independent re-backtest spot-check** — `backtest_portfolio` ($25k) on full cycle, 2022 bear, and
   last 12mo; `audit_backtest_posture` the full-cycle run. Study folds must agree with a fresh backtest.
   Baseline ≠ SPY — use a material underlying or equal-weight-universe B&H; note it.
3. **Breadth gate (the point of this attempt) — measure at FIXED $25k.** `audit_backtest_breadth` on the
   chosen candidate: **simultaneous distinct names ≥ target, participation ≥ ~0.5, `cannotAfford` sharply
   down vs Stage-A before.** If breadth didn't actually improve at $25k, the fix failed regardless of return.
4. **Similar-ish-gain check vs the v3 bar** (table at top): OOS return same order of magnitude, OOS worst
   DD not materially worse than ~28.6%, OOS min Sortino comfortably > 0.5. Make the trade explicit
   (breadth gained vs return/DD given up).
5. **Degradation** (train vs OOS per fold), **drawdown honesty** (OOS DD next to OOS return; lead with risk).
   **Turnover/fee guardrail (kills the v2 failure mode):** if the winner uses the short-dated sleeve (lever
   E), report per-fold **fees + turnover** and the **sleeve's share of the book**. v2 ballooned to
   $1.5–8.9k/fold (vs v3's ~$100–600). A sleeve winner must keep fees in v3's neighbourhood AND survive the
   **April-2025 fold** (v2 went negative / 61.6% DD there) — otherwise it fails regardless of headline return.
6. **Reproducibility / field audit** — `conditionFieldAudit` matches intended knobs;
   `compare_backtests {tolerance_bps:0}` on a re-run. Verify by **field, never display name**.
7. **Spread-shape compliance (hard reject)** — outright long calls for long-dated; any spread ≤30 DTE.
   Violation = automatic FAIL.

**PASS test:** majority of OOS folds profitable, OOS Sortino positive & steady (~0.5 floor), DD tolerable,
deployment stable, modest degradation, **AND fixed-$25k simultaneous breadth materially higher than the
Stage-A before**, at a gain in v3's neighbourhood. Breadth without the gain (v2's failure mode) = FAIL;
gain without breadth (status quo) = FAIL for *this* attempt's purpose.

---

## Stage D — Present, then stop

Deliver a decision-ready package and **stop**:
- **Verdict up top:** does a config fix restore participation at similar-ish validated gain? PASS/FAIL, one line.
- **Before → after breadth at fixed $25k** (simultaneous names, participation, `cannotAfford`) — the headline.
- **Per-fold OOS table** + aggregate, and the **side-by-side vs v3** (return / DD / Sortino / breadth),
  with the trade made explicit.
- **The chosen fix's plain-English rules** + `conditionFieldAudit` + build id, and **provenance labels for
  every parameter** (`swept-on-this-book` / `inherited-from <study-id>` / `hand-set` — "inherited" is amber).
- **Honest caveats:** options fill realism, leverage/fragility, hindsight in the frozen 21, the
  `automaticOrderApproval:false` churn (recommend flipping it on at deploy), that worst DD is **April-2025**,
  and any baseline caveat. **No deploy. No orders.** Wait for me.

---

## Stage E — Fresh-portfolio cleanup (GATED — only after I say "deploy + clean up")

Only runs if I say so, and only for the finalist I name. Goal: make my **live positions equal a fresh
deploy of the chosen finalist today** via **delta** trades (don't round-trip overlaps).

1. **Clone the finalist onto the live book FIRST** — `clone_strategies_to_portfolio` (source = finalist,
   target = live `69a7dc7acdb6bf6a4681d36c`), field-verify. This is the "deploy" and sets the strategies
   the next step reconciles against. (`reconcile_portfolio_to_strategy` has **no** `strategy_source` arg.)
   Also flip **`automaticOrderApproval`** per my instruction at deploy (default: leave as-is unless I say).
2. **Reconcile preview** — `reconcile_portfolio_to_strategy({ portfolio_id: "69a7dc7acdb6bf6a4681d36c",
   mode: "delta" })`. **Preview-only — never places orders.** Returns target/current/orders/cost/P&L/wash flags.
3. **Show me the preview + get explicit approval.** Orders touch only the delta; `target` == a fresh deploy;
   confirm the target now spans multiple names (participation restored), not just OSCR.
4. **Stage the orders** — `create_orders({ portfolio_id: "69a7dc7acdb6bf6a4681d36c", orders: <array from step 2> })`.
   Staged **UNAPPROVED**; the tool never submits. **I approve manually in the NexusTrade UI.**
5. **Verify** — after fills, re-run the reconcile preview; delta should be ~empty. Report fills, remainder,
   realized P&L, wash-sale flags, and the resulting live participation (distinct names held).

Never run Stage E without my explicit go for that specific finalist. Default `mode:"delta"`.

---

## Working rules
- Claude Code **runs and verifies** directly — no Aurora agent in the loop (an agent is optional only as a
  gene-design idea generator).
- **Reproduce the live collapse with numbers first** (Stage A), then fix, then re-certify.
- **Breadth is measured at fixed $25k** (`audit_backtest_breadth`), never inferred from a compounded backtest.
- **Sizing change ⇒ re-sweep** (`engine_kind:"sweep"`), never inherit v3's knobs on the new sizing.
- **Short-dated verticals are sweep candidates, not excluded** — but only the *wide, share-capped* variant
  v2 never tested, and they must clear the same OOS gates + the turnover/fee guardrail. v2's thin/uncapped
  design failed; the class is not banned. Let cert kill it on evidence, not on a prior.
- **Spread-shape rule is a hard reject.** Baseline ≠ SPY for this options book.
- **No deploy, no orders** until Stage E, gated on my explicit "deploy + clean up".

---

## Standing methodology rules (carried from Ep-11 attempt1 retro — apply here)

1. **Re-optimize on ANY structural change — never inherit a genome across structures.** Per-name size,
   total budget, sizing policy, rung depth are **structure-dependent**. Changing them (this attempt's whole
   point) requires an `engine_kind:"sweep"` walk-forward on the new sizing *before* certifying. A
   `backtest_only` cert on inherited knobs only confirms it **generalizes**, not that the knobs are **good**.
2. **Separate "explore designs" from "optimize the chosen design."** Pick the sizing design → sweep that
   exact design's knobs → then `backtest_only`-certify. Don't sweep neighbours and hand-tune the finalist.
3. **Label every deployed parameter's provenance** in Stage D — `swept-on-this-book` / `inherited-from
   <study-id>` / `hand-set`. "Inherited" is **amber**, not green, until re-swept on the current structure.

**Self-check trigger words:** "just raise the allocation," "reuse v3's knobs," "same config, bigger size,"
"already certified." Each must prompt: *the sizing structure changed — re-sweep before certifying or deploying.*
