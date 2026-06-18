# Episode 11 — Posture-Retune, orchestrated by Claude Code

> **Paste this whole file into Claude Code** with the NexusTrade MCP server connected (Austin's
> account). Claude Code is the **orchestrator**: it launches a NexusTrade **Aurora agent**
> (`create_agent`) to create + optimize the strategies, **monitors** it, then runs the **mandatory
> verification checks itself over MCP** (the agent's numbers are not trusted on their own), and
> presents a finalist. **Nothing deploys and no orders are placed** until I explicitly say
> "deploy + clean up" — and even then only through the gated cleanup in Stage E.
> Not generalized: this operates on my real artifacts.

---

> **Tools:** the NexusTrade MCP tools are deferred — load schemas via ToolSearch as you need them
> (`create_agent`, `get_agent`, `backtest_portfolio`, `audit_backtest_posture`,
> `get_optimization_results` / `list_optimizations`, `fetch_portfolios`, `clone_strategies_to_portfolio`,
> the reconcile tool, `create_orders`). Log your run to `episode-11/CAMPAIGN_LOG.md` (agentId, the
> checks, the finalist, and — if Stage E runs — the reconcile preview/fills).

## The job

Retune my live momentum-LEAP options book toward a chosen **median-deployment target (~70%)** while
keeping returns **close to the live book**, judged **holistically** (no "green on every fold"). The
Aurora agent does the creating/optimizing; **Claude Code independently verifies** everything before
anything reaches me.

### Fixed
- **Universe (20):** ANET DUOL HOOD LLY GS META TSM AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD MU SNDK.
- **Capital:** $25,000, Day interval. **Structure:** momentum-ranked long-dated calls (~150–365 DTE), affordability ladder. Only knobs move.
- **Spread-shape rule (NEW — hard constraint):** **no long-dated, *thin* debit spreads.** Axes:
  *long/short = DTE*, *thin/wide = strike width / max profit*.
  - **Long-dated (≥ ~120 DTE) must be WIDE** — an outright long call (uncapped), or a debit spread whose
    short leg is far enough OTM for a large max profit (**up to ~$10K/contract**).
  - **Short-dated** spreads **may be thin** (narrow width).
  - **Forbidden: long-dated AND thin** — e.g. the live book's current `ATM/+3 … +20` verticals
    (9–15-month, only ~$1–2.5K max profit). Those are the shape we're removing.

### Resolve the deployment target FIRST (don't skip — prior runs got this wrong)
There are **two different "deployments"** and they're ~30 points apart:
- **Current live snapshot:** ~**93%** (the book is near fully invested *right now* — a position state).
- **Backtest median (2024→now):** ~**60.6%** (the strategy's *typical* exposure in simulation).

**The optimizer/sweep tunes the BACKTEST MEDIAN.** So "≈70%" means steering the backtest median to
~70% — which, from ~61%, is actually a small *increase*, not a trim. State this explicitly in the
deliverable so the direction isn't misread. If what I actually want is to cap the *live exposure*,
that's the **cleanup stage (E)**, not the optimizer.

### My three seeds (pinned — confirm by field/posture, never by name)
| Seed | ID | What it is |
|---|---|---|
| **A — LIVE** | `69a7dc7acdb6bf6a4681d36c` | Deployed book. ~93% net deployed now; backtest median ~60.6%. The performance bar. |
| **B — optimizer source** | `6a2c044d99fc925d9b7bacf6` | Raw sweep winner A was cloned-and-cleaned from (opt `6a2c026699fc925d9b7ba68c`). |
| **C — deploy-build** | `6a2eba08d0e6238f8baab940` | Paper "MLT v16 — DEPLOY BUILD". Mid-posture reference (~43%). |

---

## Stage A — Claude Code launches the Aurora agent

Prefer a **systematic sweep** over the GA. (Episode 10 evidence + this episode's prior runs: the
sweep is the reliable/certified path; the GA arm overfit and produced the dud candidate.) Keep the
agent brief **short and natural** — it has its own planner; over-specifying makes it loop.

```jsonc
// mcp__nexustrade__create_agent
{
  "modelConfig": { "planningModel": "google/gemini-3-flash-preview",
                   "executionModel": "openrouter::deepseek/deepseek-v4-flash:nitro" },
  "automationMode": "automated",
  "maxIterations": 38,
  "messages": [{ "sender": "User", "content":
    "Retune my live momentum long-dated-call options book on these 20 names (ANET DUOL HOOD LLY GS META TSM AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD MU SNDK) so its BACKTEST median deployment is near 70% with returns close to the live book. Seeds: live 69a7dc7acdb6bf6a4681d36c, optimizer source 6a2c044d99fc925d9b7bacf6, deploy-build 6a2eba08d0e6238f8baab940. Run a SYSTEMATIC SWEEP (not GA) with the posture-cap selection policy: medianDeployment between 65 and 72, participationRate >= 0.35, distinctUnderlyingsTraded >= 9, primary sortinoRatio. Sweep the levers that move deployment: per-name size, total budget, and the regime gate (try an always-on gate, SPY>200SMA, and SPY>=0.92x252d-max). The sweep leaderboard IS the candidate source — pick the top 2-3 cells nearest 70% from it, do not hand-build replacements. Backtest the finalists over BOTH the full cycle INCLUDING the 2022 bear (2022-01-01 to today) AND the last 12 months, and report return, max drawdown, Sortino, and median deployment for each next to the live book. Structure rule (hard): NO long-dated thin debit spreads — long-dated structures (>=120 DTE) must be outright long calls or WIDE spreads (far-OTM short leg, max profit up to ~10K); only short-dated spreads may be thin/narrow. Do NOT deploy and do NOT place any orders. Present for review."
  }]
}
```

Record the returned `agentId`. (Standard split shown; a budget comparison arm such as
`nvidia/nemotron-3-ultra-550b-a55b` for both roles is fine — 0.25 tokens, clears the cost guard.)

---

## Stage B — Monitor

Poll `mcp__nexustrade__get_agent <agentId>` until terminal (`completed`/`stopped`). The payload is
huge — parse it (jq/python), don't dump it. Per poll, capture: `status`, `currentIteration`,
`currentState.thought/action`, and the last few messages.

**Watch for the known failure modes (surface them, don't paper over):**
- **Optimizer/sweep silent-fail** — `List Optimizations` returns 0 / no `optimizationId`. If so, report it; do not let the agent quietly pivot to hand-built variants and pass them off as optimizer output.
- **Create-YAML emitting `Alert` instead of `RebalanceOption`** for option books.
- **Backtest "failed to create the backtest configuration"** loops.
- **Wrong window** — agent defaulting to "since 2024" and skipping 2022.
- **Stall** — `updatedAt` frozen + iteration not advancing for many minutes.

If it stalls or a tool fails repeatedly, **stop, summarize exactly what broke, and wait for me** (I may be fixing the planner/tools in another tab).

---

## Stage C — Claude Code's mandatory checks (DO NOT trust the agent's numbers)

When the agent finishes, **independently re-verify over MCP** before presenting anything:

1. **Was the sweep load-bearing?** Read the optimization (`get_optimization_results` /
   `get_walk_forward_study_results`) and confirm the finalists came **from its leaderboard**, that the
   **`medianDeployment` constraint was actually applied** (not just Sortino), and that the leaderboard
   surfaces per-candidate medianDeployment. If the good candidates were hand-built, say so.
2. **Re-backtest each finalist yourself** (`backtest_portfolio`, $25k) over **three windows**: the
   **2022 bear (2022-01-01→2023-01-01)**, the **full cycle (2022-01-01→today)**, and the **last 12
   months** — the agent's "full cycle" likely skipped 2022.
3. **Re-measure deployment** with `audit_backtest_posture` on the full-cycle backtest — do **not** trust
   the optimizer's stat. Confirm the finalist's median lands **~70% (65–72)**, and report whether it
   ever runs >70% outside a declared regime.
4. **Surface the deployment↔drawdown tradeoff honestly.** Prior run buried it: the ~70% candidate had a
   74% drawdown while a ~50% one had 40%. Put deployment and maxDD side by side; do **not** lead with
   the headline return.
5. **Holistic judgement** (no per-fold green rule): full-cycle return + maxDD + Sortino, the last-12mo
   read, and 2022 behavior — pick the best *balance* at ~70%, preferring shallower drawdown and
   steadier cross-window behavior. One weak window ≠ disqualified.
6. **Reproducibility:** `conditionFieldAudit` matches intended knobs; `compare_backtests {tolerance_bps:0}` identical. Verify by field, never by display name.
7. **Spread-shape compliance (hard reject).** Inspect the finalist's option structures (`get_portfolio` →
   leg strikes/DTE per template). **Reject any long-dated (≥~120 DTE) debit spread that is thin** (short
   leg near the long leg / small max profit). Long-dated legs must be outright calls or **wide** spreads
   (max profit up to ~$10K). Thin is allowed **only** short-dated. If the finalist contains a long+thin
   structure, it fails — pick the next candidate or have the agent re-run with the wide-only constraint.

---

## Stage D — Present, then stop

Deliver a decision-ready package and **stop**:
- Side-by-side table: **Live book vs each finalist** — median deployment, 2022-bear return/maxDD,
  full-cycle return/maxDD/Sortino, last-12mo, with the **trade made explicit** ("≈70% deploy buys/costs
  X return and Y drawdown vs live").
- Plain-English rules + `conditionFieldAudit` of the finalist; its `chatPortfolioId`.
- Which sweep cell it is and why it beats the runners-up.
- Honest caveats (hindsight in the frozen 20, options spread cost, leverage/fragility, the
  median-vs-snapshot point). **No deploy. No orders.** Wait for me.

---

## Stage E — Fresh-portfolio cleanup (GATED — only after I say "deploy + clean up")

Goal: make my **live positions equal a fresh deploy of the chosen finalist today** — not polluted by
old strategies — via **delta** trades (don't round-trip overlaps). Exact tool flow (both verified):

1. **Clone the finalist onto the live book FIRST** — `clone_strategies_to_portfolio` (source = finalist,
   target = live `69a7dc7acdb6bf6a4681d36c`), field-verify. This is the "deploy", and it sets the live
   book's strategies that the next step reconciles against. (`reconcile_portfolio_to_strategy` has **no**
   `strategy_source` arg — it reconciles the live book against **its own** strategies, so the clone has
   to happen first.)
2. **Reconcile preview** — `reconcile_portfolio_to_strategy({ portfolio_id: "69a7dc7acdb6bf6a4681d36c",
   mode: "delta" })`. **Preview-only — it never places orders.** It returns `target`, `current`,
   `orders` (already in `create_orders` shape), estimated cost, realized P&L, and wash-sale flags.
3. **Show me the preview and get explicit approval.** Sanity-check: orders touch only the delta
   (overlaps untouched), costs sane, `target` == a fresh deploy.
4. **Stage the orders** — `create_orders({ portfolio_id: "69a7dc7acdb6bf6a4681d36c", orders: <the
   orders array from step 2> })`. These are staged **UNAPPROVED**; the tool never submits to the broker.
   **I approve them manually in the NexusTrade UI** — there is no approval tool and you cannot approve
   them for me. Options auto-stage as LIMIT.
5. **Verify** — after I've approved + they fill, re-run the reconcile preview; the delta `orders` array
   should be ~empty. Report fills, any remainder, realized P&L, and wash-sale flags.

Never run Stage E without my explicit go for that specific finalist. Default `mode: "delta"`; only use
`"liquidate_all"` if I explicitly ask for a clean cost-basis reset.

---

## Working rules
- Claude Code **orchestrates** (launch agent → monitor → verify → present); the agent **creates/optimizes**.
- **Sweep, not GA**, for this bounded knob-retune; the leaderboard is the candidate source.
- **State the deployment target as backtest-median ~70%;** reconcile it with the ~93% live snapshot.
- **Independently re-verify** (windows incl. 2022, posture audit, field audit) — never trust the agent's stat.
- **No deploy, no orders** until Stage E, which is itself gated on my explicit "deploy + clean up".
