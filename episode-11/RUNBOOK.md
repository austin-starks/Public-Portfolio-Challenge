# Episode 11 — Portfolio Certification, orchestrated by Claude Code

> **Paste this whole file into Claude Code** with the NexusTrade MCP server connected (Austin's
> account). I need to know whether my **current live book holds up under the engine it runs on now**.
> Claude Code is the **orchestrator + independent verifier**: it runs a **walk-forward certification**
> of the live book itself (deterministic tool, no Aurora agent needed), reads the out-of-sample folds,
> and delivers a **PASS / FAIL certification verdict**. If it FAILS, Claude Code runs a **walk-forward
> re-optimization (sweep + certification)** and certifies the winner. **Nothing deploys and no orders
> are placed** until I explicitly say "deploy + clean up" — and even then only through the gated
> cleanup in Stage E. Not generalized: this operates on my real artifacts.

> **Operating principles:**
> - **The objective is certification.** Median deployment is **settled** — do NOT tune it, do NOT
>   target any deployment number. The only question is: *is the current book strong under this engine?*
> - **No Aurora agent for the certify path.** Walk-forward `backtest_only` is deterministic — Claude
>   Code calls it directly. An agent is **optional** only as an idea-generator if the re-opt gene
>   design needs exploration; the default is no agent.
> - **The subject is the LIVE book**, certified as a *fixed* portfolio first; re-optimization is the
>   fallback, not the default.

---

> **Tools:** the NexusTrade MCP tools are deferred — load schemas via ToolSearch as you need them
> (`run_walk_forward_study`, `get_walk_forward_study_results`, `list_walk_forward_studies`,
> `get_sweep_surface`, `backtest_portfolio`, `audit_backtest_posture`, `get_optimization_results`,
> `fetch_portfolios`, `get_portfolio`, `compare_backtests`, `clone_strategies_to_portfolio`, the
> reconcile tool, `create_orders`). Log your run to `episode-11/CAMPAIGN_LOG.md` (the study IDs, the
> per-fold OOS table, the certification verdict, the finalist if re-opt runs, and — if Stage E runs —
> the reconcile preview/fills).

## The job

**Certify that my current live momentum-LEAP options book is strong under the engine it runs on.** Judge
it **holistically** across out-of-sample walk-forward folds (no "green on every fold" rule). If it
certifies, say so plainly and stop. If it does **not** certify, **re-optimize + re-certify** and
present the certified winner. Claude Code does the running AND the independent verification — there is
no agent whose numbers need second-guessing here; the numbers are Claude Code's own.

### Fixed
- **Universe (20):** ANET DUOL HOOD LLY GS META TSM AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD MU SNDK.
- **Capital:** $25,000, Day interval. **Structure:** momentum-ranked long-dated calls (~150–365 DTE), affordability ladder. Only knobs move (and only if re-opt runs).
- **Spread-shape rule (hard constraint — still in force):**
  - **Long-dated exposure (≥ ~120 DTE) = outright long calls ONLY** (uncapped convexity, no short leg). No long-dated debit spreads.
  - **Any debit / vertical spread must be short-dated — expiring in ≤ ~1 month (≤ 30 DTE).** Thin is fine there.
  - (Excludes: long-dated *and* capped verticals like `ATM/+3 … +20`.)

### Median deployment — settled, not a target
The book's backtest-median deployment (~60–69% depending on window) is **acceptable as-is**. Do **not**
optimize toward any deployment number. If certification or re-opt happens to move it, that's fine —
report it, don't steer it. (If I ever want to cap *live* exposure, that's Stage E cleanup, not here.)

### The subject + references (confirm by field/posture, never by name)
| Role | ID | What it is |
|---|---|---|
| **SUBJECT — LIVE** | `69a7dc7acdb6bf6a4681d36c` | Deployed book. **This is what we certify.** The thing that must hold up out-of-sample. |
| ref — optimizer source | `6a2c044d99fc925d9b7bacf6` | Prior sweep source (opt `6a2c026699fc925d9b7ba68c`). Reference only. |
| ref — deploy-build | `6a2eba08d0e6238f8baab940` | Paper "MLT v16 — DEPLOY BUILD". Reference only. |

---

## Stage A — Walk-forward CERTIFICATION of the live book (fixed portfolio)

Claude Code runs this directly. Certify the live book **as-is** (no inner optimizer) so we see how the
*current* strategy generalizes out-of-sample.

**Pre-flight (do first):**
1. `get_portfolio 69a7dc7acdb6bf6a4681d36c` — capture the current strategy set, `conditionFieldAudit`,
   and the **exit ladder**. Note any **LaunchAgent** strategy: it can't run historically and contaminates
   backtests (it fires once and logs thousands of `cooldownSkip` events). For a clean certification,
   certify a **LaunchAgent-free copy** of the book if one is present (clone the rebalance + close rules
   only) and say you did so.
2. **Spread-shape check** the live structures (`get_portfolio` → leg DTE/strikes). The live book has
   historically held **long-dated vertical spreads** (Mar-'27 ATM/+3/+10/+20) — if those are still the
   deployed structure, that is a **hard spread-shape violation** and the book **cannot certify as-is**;
   report it and go straight to Stage C-re-opt with "long-dated = outright calls, spreads ≤30 DTE".
3. **Sanity-check the exit ladder for a convexity cap.** If multiple "always" take-profit closes exist
   (e.g. P/L ≥ 20% / 50% / 200%), the **lowest one binds first** and effectively caps every winner at
   ~+20% — which defeats the uncapped-convexity rationale for outright calls. Flag it; it is the most
   likely reason returns trail a let-winners-run book.

```jsonc
// mcp__nexustrade__run_walk_forward_study   (preview_only first to see the fold calendar + cost)
{
  "portfolio_id": "69a7dc7acdb6bf6a4681d36c",   // or the LaunchAgent-free clone id
  "global_start_date": "2022-01-01",
  "global_end_date":   "<TODAY>",
  "fold_count": 5,
  "inner_mode": "backtest_only",                // certify the FIXED book — no per-fold optimizer
  "mode": "validation",                          // per-fold independent OOS
  "walk_forward_mode": "anchored",
  "oos_width_days": 252,
  "embargo_days": 14,
  "interval": "Day",
  "preview_only": true                           // flip to false to actually run
}
```

Run `preview_only:true` first; confirm the fold calendar covers 2022→today — it must include both the
**2022 bear** and the **April-2025 selloff** (the deepest drawdown for this book is an April-2025 event,
so the folds have to span it). Then run for real and record the `study_id`.

---

## Stage B — Monitor the study

Poll `list_walk_forward_studies` / `get_walk_forward_study_results <study_id>` until terminal
(`COMPLETE`/`ERROR`/`CANCELLED`). Parse with jq — payloads are large, don't dump them.

**Watch for the known failure modes (surface them, don't paper over):**
- **Study silent-fail / ERROR** — no fold stats / empty `validationAggregate`. Report it; don't invent a verdict.
- **Wrong window** — fold calendar not starting 2022-01-01 / skipping the bear.
- **Backtest contamination** — LaunchAgent firing in folds (you should have stripped it in Stage A).
- **Zero-trade / NaN folds** — upstream position-marking corruption; report which folds, don't average over NaNs.
- (No 30-min "stall" worry here — there's no Aurora agent. A study that's genuinely hung past its
  estimated cost/time → stop, summarize, wait for me; I may be fixing the engine in another tab.)

---

## Stage C — Mandatory certification checks (these ARE the verdict)

Read the per-fold OOS results and decide PASS / FAIL holistically. **Do not certify on a single
aggregate number.**

1. **Per-fold OOS table.** For each fold: train window, OOS window, OOS return, OOS maxDD, OOS Sortino,
   median deployment, distinct underlyings, participation. Plus the `validationAggregate`.
2. **Independent re-backtest spot-check.** Re-run `backtest_portfolio` ($25k) on the **full cycle
   (2022-01-01→today)**, the **2022 bear (2022-01-01→2023-01-01)**, and the **last 12 months**, and
   `audit_backtest_posture` the full-cycle run. Confirm the study's fold numbers are consistent with a
   fresh backtest — verify the study and a standalone backtest agree with each other.
   - **Baseline:** for this 20-name options book, set `baseline_symbol` to a material underlying or use
     an equal-weight universe B&H — **do NOT default to SPY** (SPY only colours the excess metric, but
     get it right). Note this in the deliverable.
3. **Degradation:** compare train vs OOS per fold. Large train→OOS collapse = overfit / not robust, even
   if the full-cycle backtest looks great.
4. **Drawdown honesty.** Put OOS maxDD next to OOS return per fold; lead with risk, not the headline
   return. At this leverage a fold can post a huge return and a 50–77% drawdown.
5. **Holistic PASS test (no per-fold green rule):** certify **PASS** if the *majority* of OOS folds are
   profitable, OOS Sortino is positive and reasonably steady (rough floor ~0.5), drawdown is within
   tolerance you'd actually hold, deployment is stable across folds, and train→OOS degradation is modest.
   One weak fold ≠ FAIL. Persistent OOS losses, exploding drawdown, or train-only strength = **FAIL**.
6. **Reproducibility / field audit.** `conditionFieldAudit` matches the intended knobs;
   `compare_backtests {tolerance_bps:0}` where you re-run the same config. Verify by **field, never by
   display name**.
7. **Spread-shape compliance (hard reject).** Re-confirm the certified structure is outright long calls
   for long-dated exposure (no short leg ≥~120 DTE) and any spread is ≤30 DTE. A violation = automatic FAIL.

---

## Stage C-re-opt — ONLY if Stage C returns FAIL

Re-optimize + re-certify with a walk-forward **sweep** study (this is the certified path; GA overfits and
is rejected for deploy certification). Claude Code drives it directly.

1. `get_sweep_surface` on the live book (or a clean clone) to get the real sweepable field names.
2. `run_walk_forward_study` with `engine_kind:"sweep"`, `inner_mode:"optimize"`, `certification:true`,
   `mode:"validation"`, `fold_count:5`, anchored, 2022-01-01→today, and **`gene_intents`** for the levers
   that matter — explicitly including the **take-profit ladder** (fix the +20% convexity cap → let winners
   run, e.g. single TP ≥ ~150–300% or none), plus per-name size, total budget, DTE bracket, entry cooldown,
   and rank window. `certification:true` applies the activity-floor + percentChange≥0 + sortino≥0.5 policy
   and defaults `validation_percent` to 50. **Keep the spread-shape rule in the gene design** (long-dated =
   outright calls; spreads ≤30 DTE).
3. Read the leaderboard / fold winners (`get_walk_forward_study_results`, `get_optimization_results`), pick
   the **certified** winner (passes the certification policy across folds, best holistic balance), then run
   **Stage C checks 1–7 on that winner** before it is allowed to be the finalist.

---

## Stage D — Present, then stop

Deliver a decision-ready package and **stop**:
- **Certification verdict up top: PASS or FAIL**, one line, with the reason.
- **Per-fold OOS table** (train/OOS windows, OOS return/maxDD/Sortino/deployment) + the aggregate.
- If re-opt ran: live-book-as-is vs certified winner, side by side, with the **trade made explicit**, the
  winner's plain-English rules + `conditionFieldAudit` + `chatPortfolioId`, and why it beats the runners-up.
- **Honest caveats:** hindsight in the frozen 20, options spread cost, leverage/fragility, the exit-ladder
  convexity point, any baseline/LaunchAgent caveats, and that the worst drawdown was the **April-2025**
  event (not 2022). **No deploy. No orders.** Wait for me.

---

## Stage E — Fresh-portfolio cleanup (GATED — only after I say "deploy + clean up")

Only runs if I say so, and only for the finalist I name (the certified live book itself, or the re-opt
winner). Goal: make my **live positions equal a fresh deploy of the chosen finalist today** — not
polluted by old strategies — via **delta** trades (don't round-trip overlaps).

1. **Clone the finalist onto the live book FIRST** — `clone_strategies_to_portfolio` (source = finalist,
   target = live `69a7dc7acdb6bf6a4681d36c`), field-verify. This is the "deploy", and it sets the live
   book's strategies that the next step reconciles against. (`reconcile_portfolio_to_strategy` has **no**
   `strategy_source` arg — it reconciles the live book against **its own** strategies, so the clone has to
   happen first.) *If the finalist IS the already-deployed live book unchanged, no clone is needed — say so.*
2. **Reconcile preview** — `reconcile_portfolio_to_strategy({ portfolio_id: "69a7dc7acdb6bf6a4681d36c",
   mode: "delta" })`. **Preview-only — it never places orders.** Returns `target`, `current`, `orders`
   (already in `create_orders` shape), estimated cost, realized P&L, and wash-sale flags.
3. **Show me the preview and get explicit approval.** Sanity-check: orders touch only the delta (overlaps
   untouched), costs sane, `target` == a fresh deploy.
4. **Stage the orders** — `create_orders({ portfolio_id: "69a7dc7acdb6bf6a4681d36c", orders: <the orders
   array from step 2> })`. Staged **UNAPPROVED**; the tool never submits to the broker. **I approve them
   manually in the NexusTrade UI** — there is no approval tool and you cannot approve them for me. Options
   auto-stage as LIMIT.
5. **Verify** — after I've approved + they fill, re-run the reconcile preview; the delta `orders` array
   should be ~empty. Report fills, any remainder, realized P&L, and wash-sale flags.

Never run Stage E without my explicit go for that specific finalist. Default `mode: "delta"`; only use
`"liquidate_all"` if I explicitly ask for a clean cost-basis reset.

---

## Working rules
- Claude Code **runs and verifies** the certification directly — no Aurora agent in the loop for certify.
- **Certify the FIXED live book first** (`inner_mode: backtest_only`); re-optimize only on FAIL.
- **Walk-forward, validation mode, anchored, 5 folds, 2022→today** — OOS folds are the verdict, not a single backtest.
- **Median deployment is settled** — never tune toward a deployment number.
- **Spread-shape rule is a hard reject**; the exit-ladder convexity cap is a known footgun — check it.
- **Baseline ≠ SPY** for this options book; **strip the LaunchAgent** before certifying.
- **No deploy, no orders** until Stage E, which is itself gated on my explicit "deploy + clean up".
