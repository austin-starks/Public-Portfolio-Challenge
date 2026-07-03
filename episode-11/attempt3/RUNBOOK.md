# Episode 11 / Attempt 3 — Alternative Data on the Certified Book, orchestrated by Claude Code

> **Paste this whole file into Claude Code** with the NexusTrade MCP server connected (Austin's
> account). My live book now runs the attempt2-certified **top-21 momentum-LEAP** config. This attempt
> asks one question: **can alternative data — congressional disclosures, Reddit/social, or other online
> sources — make the certified book measurably better out of sample?** Claude Code is the
> **orchestrator + independent verifier**: it builds the alt-data custom indicators with NexusTrade's
> compute + custom-indicator features, wires them into hand-built strategy variants (a grid over the
> indicator shape), and OOS-certifies against the incumbent bar with calendar-aligned base controls. **Nothing deploys and no orders are placed** until I
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

### Carried over from run #1 (reuse — do NOT rebuild from scratch)
| Artifact | ID | What it is |
|---|---|---|
| **WsbMentions21_Full** | customIndicatorId `6a45fa78248d2f46f43d5d79` | Daily WSB mention counts, ALL 21 tickers, 7,228 pts, **2021-12→2025-12** (lake had no 2026 at build time). Lookahead-safe (UTC post date), values cross-validated exactly by two independent builds. **Extend/refresh forward from 2026-01; only rebuild history if the recipe (lesson #13) changes.** |
| **V1 — WSB rank-blend** | `6a45fafc248d2f46f43d5f2d` | Base + `weightIndicator` = ROC63 × (1 + log10(1 + SMA21(WsbMentions21_Full))). Run #1's winner. Cert `6a45fc0d…`. |
| Aligned base control | study `6a45fd55…` | Base certified on V1's clipped calendar (`global_end_date` 2026-01-01). |
| PelosiBuyDollarsV2 | `6a452180024552e3a78c8ac2` | 11,502 pts, filing-date-stamped — but covers ~1/21 of our names (AVGO): tilt/overlay only, and a rank built on it traded ZERO (sparse-series rule, lesson #10). |

**Run #1 standing verdict (supersede only with new evidence):** on the calendar-aligned 5-fold
head-to-head, **V1 beat the base** — OOS mean +55.7% vs +46.3%, all 5 folds positive vs a negative
bear fold, Sortino mean 2.89 vs 2.35, drawdown ~equal (worst 34.5 vs 33.4), 19 names — while the
base's own full-window re-cert reproduced the attempt2 bar exactly. V2 (attention-only rank) lost
badly — momentum stays primary, buzz is a tilt. V3 (attention filter) ≈ base. **V1 is the deploy
candidate-in-waiting, gated on ONE thing: the WSB signal must be refreshed to the present (and kept
refreshed) before it may drive the live book — a stale rank series is a dead book.** First job of a
fresh run: check the lake's max month; if it now extends past 2025-12, refresh the indicator,
re-cert V1 on the longer calendar (+ aligned base control), and re-confirm the verdict.

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

**Book mechanics (attempt2):**
6. **Breadth illusions:** "19/21 names" on a compounded run means nothing. Measure simultaneous
   cold-start breadth at fixed $25k. SelectTop truncates the pool BEFORE affordability — a narrow
   top-N re-creates the OSCR-only collapse (that's why the incumbent is top-21).
7. **Reconcile is single-tick** (the live strategy accretes the rest over daily rebalances) and
   **stale pending orders block new staging** — check for both at Stage E.
8. **SelectTop 21-of-21 never truncates, so the `weightIndicator` rank ORDER is what decides which
   names the 40% budget funds first.** That rank is the natural alt-data injection point.

**Alt-data / custom-indicator craft (attempt3 run #1):**
9. **`sec_edgar` is corporate filings only** (10-K/10-Q/8-K, and Form 4 via `forms:["4"]`) —
   congressional PTRs live at the House Clerk: `…/financial-pdfs/{YEAR}FD.zip` (TSV index with
   FilingType="P" rows + DocID) → `…/ptr-pdfs/{YEAR}/{DocID}.pdf`.
10. **Verify before wiring:** never reference a CustomIndicator without confirming point count,
    per-ticker coverage of OUR 21 names, and freshness (`list_custom_indicators`); spot-check
    values against the primary source. **A rank expression only works with a series that is DENSE
    across the whole universe** — a sparse/partial-coverage series (e.g. one politician's buys)
    can only be a tilt/overlay, never a rank input, and a signal whose data has gone stale must
    not drive a live book.
11. **Lookahead safety is non-negotiable:** every alt-data point is stamped at the date the
    information was PUBLIC (filing/disclosure/post date), not the trade/event date. Congressional
    trades have a STOCK Act lag of up to ~45 days — the signal must embed that lag. Audit
    explicitly per indicator before any backtest uses it. Cross-validate values with a second,
    independently-generated build when possible (run #1 verified WSB counts this way, exact match).
12. **Prefer steerable compute sessions for multi-step data builds** (`compute_session_start/exec`
    → `compute_session_promote_indicator`): /work persists, you observe every step, and the whole
    history lands in ONE promoted indicator. List and end stale sessions first
    (`compute_session_list`); send periodic execs while long work runs. Oneshot `run_compute` is
    for small, single-query jobs.
13. **Reddit Arctic lake recipe (proven):** `s3://nexustrade-parquet/reddit/arctic/submissions/
    YYYY/MM/NNN.parquet`, ~20 shards/month — read ALL shards per month, never sample shard 000
    (submissions shards are subreddit-sorted). Filter `lower(subreddit)='wallstreetbets'`, select
    only title/selftext/created_at (~15-25s/month). Guard ambiguous tickers (NET APP GLD COP GS
    META) with cashtag-or-alias matching. **Check the lake's max month first** and treat signal
    coverage end as a hard constraint on certification windows and deployability.
14. **Certification comparisons must be calendar-aligned:** the walk-forward engine clips the fold
    calendar to the indicator's data coverage, so a variant's study can silently get different
    folds than the base's. Always run a base CONTROL with the same `global_end_date` as the
    variant's clipped calendar and compare fold-for-fold. Fixed-book certs use
    `inner_mode:"backtest_only"` (engine_kind ga/default — sweep is rejected).

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
   (median deployment should be ~50% against the 40% budget; 0 days >90%).
3. **Inventory existing custom indicators** — `list_custom_indicators`: point counts, coverage
   window, per-ticker coverage of OUR 21 names, freshness (lesson #10). Start from the carried-over
   table above — `WsbMentions21_Full` is the primary asset; check whether the Reddit lake now
   extends past 2025-12 and refresh it forward if so. Cull 0-point corpses; audit lookahead
   (lesson #11) on anything new.
4. Deliver a one-paragraph *before* state: what the live book is, what the bar is, which indicators
   are current vs need refreshing/building.

---

## Stage B — Build the alt-data indicators (the compute-stack shakeout)

Build in DESCENDING order of expected signal + data reliability. Each source gets: build → point-count
+ coverage check → lookahead audit → value spot-check vs primary source → log. Platform failures get
the Bug Protocol; after two distinct failures on a source, park it and move on (don't let one broken
pipeline stall the campaign).

**B1 — Reddit/WSB (primary — proven signal, proven recipe):**
- **Refresh, don't rebuild:** in a compute session, run the lesson-#13 recipe over the months the
  lake has gained since 2025-12, dedupe against the existing series, and promote the extended
  history as one indicator. Optional enrichment if time allows: a sentiment variant of the same
  scan (title/selftext polarity), same lookahead rules.
- Watch for: survivorship/retro-scrape lookahead (a scrape TODAY of historical posts is fine; a
  sentiment model applied retroactively is fine; using deletion-survivors is a caveat to note).

**B2 — Congressional disclosures (aggregate all-Congress, if pursued):**
- Coverage first: single politicians cover ~1 of our 21 names — only an **all-Congress aggregate**
  can reach rank-grade coverage. Pipeline: session fetches the House Clerk year indexes
  (lesson #9), filters FilingType="P", fetches PTR PDFs, text-extracts (count scanned-skipped
  honestly), parses purchase rows for our 21 tickers, midpoint dollars, stamped at FILING date.
- **Two shapes, both built:** (a) buy-dollars per {filing date, ticker}; (b) recent-buys rolling
  window. If per-ticker coverage still comes back sparse, it is a tilt/overlay candidate only
  (lesson #10) — say so and deprioritize.

**B3 — Opportunistic third source (only if B1+B2 go smoothly):**
- Candidates: insider transactions (corporate Form 4 via `sec_edgar forms:["4"]` — filed dates are
  free; buy-vs-sell needs the XML), news-flow intensity (`search_stock_news` derived), or
  Google-Trends-style attention. Pick ONE, by data quality for our 21 names. Two good indicator
  families beat three rushed ones.

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

**Integration is hand-built, not swept:** the sweep engine's `allowedIndicatorTypes` does not
include CustomIndicator, so indicator-shape exploration is a **hand-built variant grid** via
`create_portfolio_variant` (deep-copy base + JSON-Pointer patch, dry_run first), each certified
`backtest_only` and labeled hand-set (amber). Classic knobs (alloc/budget/TP/SelectTop/DTE) remain
sweepable via `get_sweep_surface` + `gene_intents` if a winner warrants a knob re-sweep (standing
rule #1).

Run #1's proven S1 shape (reuse as the grid's anchor):
`weightIndicator = Multiply(ROC63, Plus(1, Log(base 10, Plus(1, IndicatorSimpleMovingAverage(21d,
CustomIndicator)))))` — momentum primary, log-damped attention tilt. Grid axes worth varying:
SMA window (10/21/42), tilt strength (log vs linear-capped), and any new signal shapes from Stage B.
Always include the untouched base as the control arm.

- **Coverage-vs-fold caveat:** the cert calendar clips to the signal's coverage (lesson #14) — run
  the aligned base control, and report per-fold signal coverage next to per-fold OOS. A variant that
  only wins where the signal exists is a finding, not a cheat — but say it.
- **Degenerate-wiring smoke test before any cert:** one 12-mo $25k backtest per variant. Zero or
  near-zero trades ⇒ the rank/filter isn't resolving (sparse series, wrong ID) — fix or drop before
  spending on folds.

---

## Stage D — Certification vs the incumbent, then stop

1. **Fixed-config OOS cert** (`backtest_only`, same 5 anchored folds) of each finalist variant AND
   confirm the incumbent's numbers reproduce on today's engine (same-fold re-cert of the base —
   cheap, and it catches engine drift).
2. **Head-to-head table** per fold: incumbent vs variant(s) — OOS %chg, Sortino, maxDD, breadth,
   deployment. Lead with risk. The bar table at the top is the reference.
3. **Breadth gate at fixed $25k** (`audit_backtest_breadth`): variant must not degrade cold-start
   participation (S3 filters are the risk here).
4. **Posture check** (`audit_backtest_posture`: deployment respects the 40% budget) and
   **spread-shape compliance** (hard reject) on every finalist.
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
0. **Signal-freshness gate (hard):** a variant whose alt-data series does not extend to the present
   with a working refresh path may NOT deploy, whatever its cert says (lesson #10).
1. Check for stale pending orders on the live book FIRST (lesson #7) — surface them; I cancel in the UI.
2. `clone_strategies_to_portfolio` (finalist → live `69a7dc7a…`); field-verify the clone.
3. `reconcile_portfolio_to_strategy({mode:"delta"})` — preview only; expect a single-tick target
   (the live strategy accretes the rest over daily rebalances — say so, don't re-diagnose it as a bug).
4. Show me the preview → explicit approval → `create_orders` (stages UNAPPROVED; I approve in the UI).
5. Verify post-fill: re-reconcile → delta ~empty; report fills, realized P&L, wash flags, live breadth.

---

## Working rules
- Claude Code runs and verifies directly — no Aurora agent in the loop.
- **Steerable compute sessions preferred** for indicator builds (Austin's standing instruction —
  lesson #12); oneshot is for small single-query jobs; two distinct failures on a source → park it,
  log it, move on.
- **Never wire an unverified indicator** (point count + coverage + freshness + lookahead +
  spot-check first — lessons #10/#11); smoke-test every variant before certifying it.
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

---

## ⛔ DEPLOYMENT BLOCKER — Reddit/WSB (V1) real-time freshness (2026-07-03)

**Status: BLOCKED, moving on to a different approach.** V1 (the WSB rank-blend) remains the run-#1
deploy candidate-in-waiting, but it **cannot deploy** and the blocker is not a cert result — it is a
data-plumbing + methodology gap on the *freshness gate itself* (lessons #10/#11; Stage E step 0).

**The blocker, precisely:**
1. **The platform ingests on a backlog, not in real time.** The compute/custom-indicator stack builds
   the WSB series from the historical Reddit Arctic lake, which lands as periodic *backfills* — it lags
   the present. A signal that drives a live daily-rebalanced book needs a **to-the-present, kept-fresh**
   series (a stale rank series is a dead book — the standing gate), and the batch lake does not provide
   that on its own.
2. **A scraping workaround exists but changes the data-generating process.** The web-scraper tools
   (`collect_web_data` / `discover_sources` / `probe_url` / `ingest_content`) are **reliable at
   scraping** current Reddit and could supply the missing recent tail. **But the scraped real-time
   source is a *different* source than the historical backfill** — different collection path, dedup,
   deletion-survivor exposure, and possibly different mention-count distribution. Splicing a real-time
   feed onto the backfilled history risks a **regime break at the seam**: the same ticker's count could
   shift level/scale purely because the source changed, not because attention changed.
3. **Validating the swap is real, unfinished work.** Before a real-time feed may replace/extend the
   backfill under the live rank, we have to show the two sources are **comparable enough that the signal
   is invariant to the source** — e.g. **PCA** (and allied distribution-shift checks: per-ticker
   level/scale alignment, correlation of overlapping-window counts, and a re-cert of V1 on a
   real-time-fed series vs the backfilled one) to see whether moving from historical backfill to the
   real-time feed **changes the results**. That analysis has not been done.

**Why this is a stop, not a paper-over:** deploying V1 on the backfilled series alone violates the
signal-freshness gate (Stage E step 0). Deploying it on a naive backfill+scrape splice would wire an
**unverified, source-inconsistent** series under the live book — exactly what lessons #10/#11 forbid.
Either path fails the gate, so V1 is **parked, not killed**: the trading verdict (V1 > base OOS) still
stands from run #1; only the *deployability* is blocked, on the freshness/source-consistency work above.

**Unblock path (for a future run, do not attempt inside this attempt):** (a) stand up a real-time WSB
scrape on the lesson-#13 recipe's field definitions; (b) build an **overlap window** where backfill and
scrape both exist; (c) PCA / distribution-shift + correlation checks on that overlap to quantify the
source delta per ticker; (d) if invariant (or after a documented alignment transform), re-cert V1 on the
real-time-fed series with an aligned base control (lesson #14) and re-confirm the verdict; (e) only then
is V1 eligible for Stage E. Until (a)–(e) exist, the freshness gate holds V1 out.

**Next:** pivoting to a different alt-data approach (a source that is either natively fresh or whose
real-time and historical paths are the same DGP), per the Stage-B "two distinct failures on a source →
park it, log it, move on" rule.
