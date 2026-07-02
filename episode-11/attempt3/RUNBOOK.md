# Episode 11 / Attempt 3 — Alternative Data on the Certified Book, orchestrated by Claude Code

> **Paste this whole file into Claude Code** with the NexusTrade MCP server connected (Austin's
> account). My live book now runs the attempt2-certified **top-21 momentum-LEAP** config. This attempt
> asks one question: **can alternative data — congressional disclosures, Reddit/social, or other online
> sources — make the certified book measurably better out of sample?** Claude Code is the
> **orchestrator + independent verifier**: it builds the alt-data custom indicators with NexusTrade's
> compute + custom-indicator features, wires them into strategy variants, sweeps the indicator shape,
> and OOS-certifies against the incumbent bar. **Nothing deploys and no orders are placed** until I
> explicitly say "deploy + clean up" (gated Stage E). Not generalized: this operates on my real artifacts.

> **Operating principles:**
> - **The incumbent is the bar, and it is a good book.** Alt-data must EARN its way in by beating (or
>   materially de-risking) the certified top-21 finalist held to the same OOS gates. "The indicator is
>   cool" is not a result; "the indicator-augmented book certifies better" is.
> - **Alt-data is a SIGNAL experiment, not a structure experiment.** The options structure (7-rung
>   deep-OTM outright-LEAP ladder, spread-shape rule) is settled by attempt1/attempt2 evidence. Only
>   the *ranking / weighting / filtering signal* is in play.
> - **LOUDLY DECLARE bugs and platform issues.** The compute + custom-indicator stack is new. Every
>   failure gets the Bug Protocol below (log it, characterize it, hand-off doc if real) — attempt2's
>   `totalBudget` bug was caught exactly this way and invalidated weeks of results. Never paper over
>   an error to keep the campaign moving; a swallowed bug is worse than a blocked stage.
> - **Verify, don't assert.** Attempt2's worst moments were confabulated mechanisms (reconcile events,
>   SPCX pricing, budget behavior). Every claim about engine behavior gets checked against events,
>   fields, or a reproduction before it appears in the log.

---

> **Tools:** NexusTrade MCP tools are deferred — load schemas via ToolSearch as needed. The alt-data
> stack: `run_compute` (oneshot + interactive), `compute_session_start/exec/promote_indicator/end`,
> `dataset_to_indicator`, `build_signal_indicator`, `create_indicator`, `list_custom_indicators`,
> `collect_web_data`, `discover_sources`, `enrich_source`, `ingest_content`, `probe_url`, `sec_edgar`,
> `cancel_compute_job`, `get_compute_status`. The certification stack: `get_sweep_surface`,
> `run_walk_forward_study`, `get_walk_forward_study_results`, `backtest_portfolio`,
> `audit_backtest_breadth`, `audit_backtest_posture`, `compare_backtests`, `query_backtest_events`.
> Deploy stack (Stage E only): `clone_strategies_to_portfolio`, `reconcile_portfolio_to_strategy`,
> `create_orders`. Log the run to `episode-11/attempt3/CAMPAIGN_LOG.md` (indicator builds + point
> counts + lookahead audit, every bug with repro, sweep/study IDs, per-fold OOS tables, verdict,
> and — if Stage E runs — the reconcile preview/fills).

## The job

**Take my existing public portfolio, add alternative data to it, and prove out of sample whether it
helps.** Build the alt-data sources as custom indicators (leveraging all of NexusTrade's new compute
features), sweep how the signal is shaped and used, and certify any winner against the incumbent bar.
Claude Code does the running AND the independent verification — the numbers are Claude Code's own.

### Fixed
- **Universe (21):** ANET DUOL HOOD LLY GS META TSM AVGO XOM COP OSCR AMAT ADI DDOG OKTA NET APP GLD MU SNDK SPCX.
- **Capital:** $25,000 cold-start, Day interval. Breadth is measured at FIXED $25k (`audit_backtest_breadth`), never inferred from a compounded run (attempt2 lesson).
- **Structure family (settled — do not reopen):** outright-calls-only momentum-LEAP, 7-rung deep-OTM
  ladder (ATM/+10/+20/+35/+50/+75/+100% OTM, 365–730 DTE), TP +250%, affordability backfill, SelectTop 21.
- **Spread-shape rule (hard constraint):** long-dated (≥~120 DTE) = outright long calls ONLY; any
  debit/vertical spread must be ≤~30 DTE. Violation = automatic FAIL.
- **What alt-data may touch:** the rank signal (`weightIndicator` / SelectTop metric), entry filters,
  per-name tilts, or an overlay condition. **What it may not touch:** the structure rungs, the
  spread-shape rule, the universe.

### The performance bar to beat (incumbent — attempt2 certified finalist, NOW LIVE)
| Metric | top-21 / 5% / 40% / TP250 (cert `6a45a7aa…`, post-budget-fix engine) |
|---|---|
| OOS folds (5, anchored, validation) | all 5 positive · %chg [76, 54, 48, 94, 105] · **mean +75% / min +48%** |
| OOS Sortino | **min 2.90** (5.19 / 3.28 / 2.90 / 4.22 / 5.41) |
| OOS maxDD | mean ~18% / **worst 25%** |
| OOS breadth | 17–18 names |
| Cold-start first-tick breadth | 4–5 names (OSCR XOM COP GLD HOOD), builds out over rebalances |

**"Better" =** an alt-data variant, held FIXED across the same 5 folds, that improves OOS return at
no-worse risk, OR materially improves risk (Sortino/DD) at similar-ish return, OR demonstrably improves
the weak regime (bear-fold performance) — with breadth not degraded. Ties or noise-level deltas → keep
the incumbent; say so plainly. **A null result honestly reported is a valid outcome of this attempt.**

### The subject + references (confirm by field/posture, never by name)
| Role | ID | What it is |
|---|---|---|
| **SUBJECT — LIVE** | `69a7dc7acdb6bf6a4681d36c` | Live book (Public brokerage). Runs the top-21 finalist config. 7 staged orders may be pending my approval — check, never assume. |
| **BASE — incumbent build** | `6a45a705664648e51f978bea` | Top-21 finalist (deploy-renamed `6a45ab3d664648e51f979ba4`). The variant base + the bar. |
| ref — incumbent OOS cert | study `6a45a7aa…` | The bar's per-fold numbers (table above). |
| ref — attempt1/attempt2 logs | `episode-11/attempt{1,2}/CAMPAIGN_LOG.md` | Full history incl. the totalBudget bug + breadth saga. |
| ref — bug-doc template | `episode-11/attempt2/TOTALBUDGET_BUG.md` | The shape of a good bug hand-off doc. |

---

## Lessons ledger (from Ep-10, attempt1, attempt2, and the alt-data pre-work — BINDING)

Do not re-derive these; verify they still hold where cheap, then obey them.

**Methodology (Ep-10 + attempt1):**
1. **Deploy the cross-fold-robust config, never the per-fold argmax.** Validation score is a noisy
   proxy; the per-fold winner is high-variance. Use maximin OOS Sortino / robust selection.
2. **The value lives in the DESIGN, not the optimizer.** The optimizer is a modest knob-setter that
   confirms a design's neighborhood. Spend effort on the signal design; ask the sweep for little.
3. **Verify at the FIELD level, never by display name** (`conditionFieldAudit`; indicator IDs copied
   exactly from the catalog). **OOS is the only headline** — never present train/validation numbers
   as evidence of generalization.
4. **Re-sweep on ANY structural change; label every parameter's provenance**
   (swept-on-this-book / inherited-from `<study-id>` / hand-set — inherited is amber). Adding an
   alt-data rank signal IS a signal-structure change → the knobs it interacts with get re-swept.
5. **Known losers on this book (don't re-test without new cause):** stop-losses on long calls
   (whipsaw — tested twice, hurt twice), SPY>200SMA regime gates (go flat in 2022 → can't clear the
   certification activity floor; a 200D-SMA momentum filter also tested WORST in attempt2),
   long-dated verticals (banned), thin short-dated sleeves at uncapped share (v2's theta-bleed FAIL).

**Engine/platform (attempt2):**
6. **Breadth illusions:** "19/21 names" on a compounded run means nothing. Measure simultaneous
   cold-start breadth at fixed $25k. SelectTop truncates the pool BEFORE affordability — a narrow
   top-N re-creates the OSCR-only collapse (that's why the incumbent is top-21).
7. **Budget accounting was buggy once (totalBudget stacking to ~96% NAV) — trust but verify:** on the
   first serious backtest of this attempt, re-check median/max deployment vs the configured budget
   (`audit_backtest_posture`). If deployment materially exceeds budget again, STOP and file a bug doc.
8. **Reconcile is single-tick** (the live strategy accretes the rest over daily rebalances) and
   **stale pending orders block new staging** — check for both at Stage E.
9. **Walk-forward engine has had outages** (BSON "unit value" optimizer-claim error, sweep AND
   backtest_only). If studies ERROR at unitsDone:0, it's likely engine-side: file it, test the
   plain-`backtest_portfolio` fallback, and wait — don't fake a cert with full-sample backtests
   (they may be used as *interim comparisons only*, clearly labeled optimistic).

**Alt-data pre-work (this week — the compute stack is where the dragons are):**
10. **`sec_edgar` is corporate filings only** (10-K/10-Q/8-K) — congressional PTRs are NOT there;
    they need `run_compute` against the House/Senate clerk sources.
11. **Compute failures seen so far:** oneshot job `6a45b5b4…` failed discovery ("No PTR filings found
    for Dan Crenshaw"), and interactive mode failed twice on "Timed out acquiring Sprite lease for
    nt-compute-f6337deb…" (stuck lease / capacity). If a lease timeout recurs, try
    `cancel_compute_job` on stuck jobs, retry ONCE, then declare and move to the next source — don't
    hammer the backend.
12. **Dead indicators exist in the catalog** (several entries with 0 pts). NEVER wire a
    CustomIndicator node without first confirming its point count via `list_custom_indicators` and
    spot-checking values. A 0-point indicator silently no-ops the condition.
13. **Lookahead safety is non-negotiable:** every alt-data point is stamped at the date the
    information was PUBLIC (filing/disclosure/post date), not the trade/event date. Congressional
    trades have a STOCK Act lag of up to ~45 days — the signal must embed that lag. Audit this
    explicitly per indicator before any backtest uses it.

---

## Bug Protocol ("loudly declare") — applies to every stage

When any tool errors, hangs, or returns numbers that contradict the config:
1. **Stop and characterize** — is it config (my fault), data (source-side), or engine (NexusTrade)?
   Reproduce minimally (the smallest job/backtest that shows it).
2. **Log it immediately** in `CAMPAIGN_LOG.md` under a `⚠️ BUG/ISSUE` heading: symptom, repro IDs,
   expected-vs-observed, current hypothesis (labeled hypothesis), what it blocks.
3. **If it's a real engine/data bug**, write a hand-off doc `episode-11/attempt3/<NAME>_BUG.md`
   modeled on `TOTALBUDGET_BUG.md` (one-line, expected vs observed, repro, leading hypothesis,
   alternatives to rule out, where to look, impact on results).
4. **Quarantine affected results** — mark every backtest/study that ran before the fix as
   suspect/invalid, exactly as attempt2 did post-budget-fix. Re-run after the fix.
5. **Tell Austin in the chat, prominently** — bugs are a first-class deliverable of this episode,
   not an embarrassment to route around.

---

## Stage A — Baseline + inventory (before building anything)

1. **Audit the live book** — `get_portfolio 69a7dc7a…`: confirm by FIELD it runs the top-21 finalist
   (SelectTop 21, 5%/name, 40% budget, 63D-ROC rank, TP250, 7 outright-LEAP rungs). Check the state
   of the 7 previously staged orders (approved/filled/pending/cancelled) and current positions.
   Note `automaticOrderApproval` state.
2. **Re-verify the bar** — pull the incumbent cert (`6a45a7aa…`) numbers; spot-check one fresh
   `backtest_portfolio` ($25k, last 12mo) on the base build and `audit_backtest_posture` it
   (lesson #7 budget check: median deployment should be ~50%, 0 days >90%).
3. **Inventory existing custom indicators** — `list_custom_indicators`: point counts, asset vs
   global scope, coverage window, per-ticker coverage of OUR 21 names. Existing candidates:
   `Pelosi_Disclosed_Buys` (849 pts), `PelosiBuyDollarsV2` (11,502 pts), `Pelosi Recent Buys (6mo)`
   (1,560 pts), WSB mention counts (NVDA-only, wrong universe — a shape template at best). Cull the
   0-point corpses from consideration. **Spot-check 3–5 values of each survivor against the primary
   source** (a known Pelosi filing) and audit timestamps for lookahead (lesson #13).
4. Deliver a one-paragraph *before* state: what the live book is, what the bar is, which existing
   indicators are actually usable vs need (re)building.

---

## Stage B — Build the alt-data indicators (the compute-stack shakeout)

Build in DESCENDING order of expected signal + data reliability. Each source gets: build → point-count
+ coverage check → lookahead audit → value spot-check vs primary source → log. Platform failures get
the Bug Protocol; after two distinct failures on a source, park it and move on (don't let one broken
pipeline stall the campaign).

**B1 — Congressional disclosures (primary; the pre-work already started here):**
- Politicians: start with the best-documented traders already researched (Pelosi — existing
  indicators; then the deep-research names, e.g. Crenshaw/Gottheimer/Wyden) — but only where PTR
  discovery actually works (lesson #11: Crenshaw discovery failed once; the prompt was being fixed).
- Pipeline: `run_compute` (INTERACTIVE preferred — Austin's standing instruction — via
  `compute_session_start/exec` → `compute_session_promote_indicator`, falling back to oneshot
  `run_compute` + `dataset_to_indicator` if sessions stay infra-blocked) against House/Senate clerk
  PTR sources. NOT `sec_edgar` (lesson #10).
- **Two shapes per politician, both built:** (a) **buy-dollars** — disclosed buy amount midpoint per
  {date, ticker}; (b) **recent-buys window** — rolling count/sum of buys over a trailing window.
  Stamped at FILING date (lookahead-safe), asset-scoped to tickers.
- Coverage reality-check: congressional buys of OUR 21 names may be sparse. Report the per-ticker
  hit count honestly — an indicator covering 3 of 21 names can only be a *tilt/filter*, not a rank
  signal, and that constrains Stage C.

**B2 — Reddit/social (WSB mentions/sentiment on the 21 names):**
- Pipeline: `discover_sources` / `collect_web_data` / `ingest_content` → dataset → indicator; or
  `build_signal_indicator` templates if one fits. Daily mention counts and/or sentiment per ticker,
  stamped at post date. The existing WSB-NVDA indicator is the shape precedent (91 pts, worked).
- Watch for: survivorship/retro-scrape lookahead (a scrape TODAY of historical posts is fine; a
  sentiment model applied retroactively is fine; using deletion-survivors is a caveat to note).

**B3 — Opportunistic third source (only if B1+B2 go smoothly):**
- Candidates via `discover_sources`: insider transactions (corporate Form 4 IS in `sec_edgar`),
  news-flow intensity (`search_stock_news` derived), or Google-Trends-style attention. Pick ONE, by
  data quality for our 21 names. Skip entirely if the compute stack burned the time budget — two
  good indicator families beat three rushed ones.

**Stage B exit criteria:** ≥1 indicator family with real coverage of the universe, point counts
confirmed, lookahead audited, values spot-checked. Log a table: indicator ID · shape · points ·
tickers covered · window · lookahead verdict · build pipeline used · bugs hit.

---

## Stage C — Wire in + sweep the indicator shape

For each surviving indicator family, build variants of the BASE (`6a45a705…`) — the structure never
changes, only the signal plumbing. Candidate integration shapes (choose per coverage):

| # | Integration | Where | Coverage needed |
|---|---|---|---|
| S1 | **Blend into rank** — alt-signal combined with 63D ROC as the `weightIndicator` / SelectTop metric | rank | broad (most of 21) |
| S2 | **Tilt** — momentum ranks, alt-data over/under-weights names with recent signal | weight | partial OK |
| S3 | **Entry filter** — only open a name if alt-signal fired within N days (or is above X) | condition | partial OK (filtered subset must stay affordable/broad — re-check cold-start breadth!) |
| S4 | **Confirmation overlay** — alt-signal relaxes/tightens an existing gate (e.g. VIX) | condition | any |

Then **sweep the indicator shape + integration knobs** (`get_sweep_surface` first for real field
names; `run_walk_forward_study`, `engine_kind:"sweep"`, `inner_mode:"optimize"`, 5 folds anchored
2022-01-01→today, validation mode, oos_width 252, embargo 14, preview_only first — confirm the fold
calendar covers the 2022 bear and Apr-2025):
- genes: signal shape (buy-dollars vs recent-buys-window vs mention-count vs sentiment) ×
  lookback/decay window × blend weight (incl. **0 = incumbent as an arm of the same study** — the
  cleanest apples-to-apples) × integration shape where sweepable.
- Anything not sweepable gets a small hand-built variant grid, certified `backtest_only` — and
  labeled hand-set (amber).
- **Coverage-vs-fold caveat:** if an alt-data series only starts (say) 2021, early anchored folds
  may see a dead signal. Report per-fold signal-coverage next to per-fold OOS; a variant that only
  wins where the signal exists is a finding, not a cheat — but say it.

---

## Stage D — Certification vs the incumbent, then stop

1. **Fixed-config OOS cert** (`backtest_only`, same 5 anchored folds) of each finalist variant AND
   confirm the incumbent's numbers reproduce on today's engine (same-fold re-cert of the base —
   cheap, and it catches engine drift).
2. **Head-to-head table** per fold: incumbent vs variant(s) — OOS %chg, Sortino, maxDD, breadth,
   deployment. Lead with risk. The bar table at the top is the reference.
3. **Breadth gate at fixed $25k** (`audit_backtest_breadth`): variant must not degrade cold-start
   participation (S3 filters are the risk here).
4. **Budget/posture check** (lesson #7) and **spread-shape compliance** (hard reject) on every finalist.
5. **Reproducibility:** `compare_backtests {tolerance_bps:0}` on a re-run; field audit vs intended
   knobs; indicator IDs verified against the catalog (right ID, right point count).
6. **Provenance labels** on every parameter (swept / inherited / hand-set).
7. **Verdict up top, one line:** does alt-data beat the incumbent OOS — YES (deploy candidate named),
   NO (null result, incumbent stands), or BLOCKED (bugs, with docs). Include the bug ledger — for
   this episode, **the platform-shakeout findings are a co-equal deliverable with the trading result.**
   **No deploy. No orders. Wait for me.**

---

## Stage E — Deploy (GATED — only after I say "deploy + clean up")

Same drill as attempt2, only for the finalist I name:
1. Check for stale pending orders on the live book FIRST (lesson #8) — surface them; I cancel in the UI.
2. `clone_strategies_to_portfolio` (finalist → live `69a7dc7a…`); field-verify the clone.
3. `reconcile_portfolio_to_strategy({mode:"delta"})` — preview only; expect a single-tick target
   (the live strategy accretes the rest over daily rebalances — say so, don't re-diagnose it as a bug).
4. Show me the preview → explicit approval → `create_orders` (stages UNAPPROVED; I approve in the UI).
5. Verify post-fill: re-reconcile → delta ~empty; report fills, realized P&L, wash flags, live breadth.

---

## Working rules
- Claude Code runs and verifies directly — no Aurora agent in the loop.
- **Interactive compute preferred** for indicator builds (Austin's standing instruction); oneshot is
  the fallback; two distinct failures on a source → park it, log it, move on.
- **Never wire an unverified indicator** (point count + lookahead + spot-check first — lesson #12/#13).
- **Breadth at fixed $25k; OOS folds are the verdict; robust config over per-fold argmax.**
- **Null result is a valid result.** Don't torture variants until one "wins" — that's the per-fold-argmax
  trap wearing a costume.
- **Bugs are deliverables** — Bug Protocol on every failure, prominently, with quarantine of tainted results.
- **No deploy, no orders** until Stage E, gated on my explicit "deploy + clean up".

## Standing methodology rules (carried from attempt1/attempt2 retros — in force)
1. Re-optimize on ANY structural change — never inherit a genome across structures. (Adding a rank
   signal = signal-structure change → re-sweep the interacting knobs.)
2. Separate "explore designs" from "optimize the chosen design" — sweep base = the chosen design itself.
3. Label every deployed parameter's provenance; "inherited" is amber until re-swept.

**Self-check trigger words:** "the indicator looks predictive" (→ certify it, don't eyeball it),
"reuse the incumbent's knobs" (→ re-sweep the ones the signal touches), "the backtest proves it"
(→ OOS folds or it didn't happen), "probably an engine quirk" (→ Bug Protocol, verify, don't assert).
