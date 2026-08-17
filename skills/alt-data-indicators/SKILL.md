---
name: alt-data-indicators
description: "Build alternative-data custom indicators on NexusTrade (Reddit/WSB mentions, congressional disclosures, insider filings, news-flow) and wire them into a certified book as a rank/tilt/filter signal. Use when adding alt-data to a strategy, building a CustomIndicator via compute sessions, auditing lookahead safety or per-ticker coverage, or deciding whether a data series is dense enough to drive a rank. Covers the compute-session workflow, the sparse-series rule, and source recipes (see references/). Invoke with the NexusTrade MCP connected."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /alt-data-indicators
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 runbooks
---

# Alt-Data Custom Indicators

Alt-data is a **SIGNAL experiment, not a structure experiment** — it may touch the rank / weighting /
filtering signal only, never the options structure (see **options-structure-rules**). The incumbent is
the bar: alt-data must EARN its way in by beating (or materially de-risking) the certified book held to
the same OOS gates. "The indicator is cool" is not a result.

## Build with steerable compute sessions (preferred)

Prefer `compute_session_start` / `compute_session_exec` → `compute_session_promote_indicator` /
`compute_session_end` for any multi-step data build: `/work` persists, you observe every step, and the
whole history lands in ONE promoted indicator. **List and end stale sessions first**
(`compute_session_list`); send periodic execs while long work runs. Oneshot `run_compute` is for small,
single-query jobs only. Other stack tools: `dataset_to_indicator`, `build_signal_indicator`,
`create_indicator`, `list_custom_indicators`, `collect_web_data`, `discover_sources`, `enrich_source`,
`ingest_content`, `probe_url`, `sec_edgar`, `get_compute_status`, `cancel_compute_job`.

Every source gets: **build → point-count + coverage check → lookahead audit → value spot-check vs the
primary source → log.** Platform failures get the **bug-protocol**; after two distinct failures on a
source, park it and move on — don't let one broken pipeline stall the campaign.

## Never wire an unverified indicator (lessons #10/#11)

Before referencing any `CustomIndicator` in a strategy, confirm all four with
`list_custom_indicators` + a source spot-check:

1. **Point count** — cull 0-point corpses.
2. **Per-ticker coverage** of the *whole* universe (all 21 names, not a sample).
3. **Freshness** — the max date; a signal whose data has gone stale must NOT drive a live book.
4. **Lookahead safety** — see below.

### The sparse-series rule

A rank/weight expression only works with a series that is **DENSE across the whole universe**. A
sparse / partial-coverage series (e.g. one politician's buys covering ~1 of 21 names) can only be a
**tilt or overlay, never a rank input** — and a rank built on it will trade ZERO (degenerate wiring).
Say so and deprioritize; don't force it.

### Lookahead safety is non-negotiable (lesson #11)

Every alt-data point is stamped at the date the information was **PUBLIC** (filing / disclosure / post
date), NOT the trade/event date. Congressional trades carry a STOCK Act lag of up to ~45 days — the
signal must embed that lag. Audit explicitly per indicator before any backtest uses it. Cross-validate
values with a second, independently-generated build when possible (a WSB-count series was verified this
way — two independent builds matched exactly). A retro scrape of historical posts is fine; a sentiment
model applied retroactively is fine (note it as a caveat); using deletion-survivors is a caveat to note.

## Data coverage bounds the certification window

Check the source lake's **max month first** and treat the signal's coverage end as a **hard
constraint** on certification windows and deployability. The walk-forward engine clips the fold
calendar to the indicator's coverage, so certification comparisons must be **calendar-aligned** — run a
base control on the variant's clipped calendar (see **walk-forward-oos**).

## Integration shapes (choose per coverage)

| # | Integration | Where | Coverage needed |
|---|---|---|---|
| S1 | **Blend into rank** — alt-signal combined with momentum ROC as the `weightIndicator` / SelectTop metric | rank | broad (most of 21) |
| S2 | **Tilt** — momentum ranks; alt-data over/under-weights names with recent signal | weight | partial OK |
| S3 | **Entry filter** — only open a name if alt-signal fired within N days / above X | condition | partial OK (re-check cold-start **breadth-audit**!) |
| S4 | **Confirmation overlay** — alt-signal relaxes/tightens an existing gate (e.g. VIX) | condition | any |

Momentum stays primary, buzz is a tilt: an attention-*only* rank has lost badly; a log-damped attention
tilt on top of momentum has won. Proven S1 anchor shape:
`weightIndicator = Multiply(ROC63, Plus(1, Log(base 10, Plus(1, IndicatorSimpleMovingAverage(21d,
CustomIndicator)))))`. Grid axes worth varying: SMA window (10/21/42), tilt strength (log vs
linear-capped).

Integration is **hand-built, not swept** (`CustomIndicator` isn't a sweepable type) — build a variant
grid via `create_portfolio_variant` (deep-copy base + JSON-Pointer patch, `dry_run` first), label
hand-set (amber), and smoke-test each with one 12-mo $25k backtest before spending on folds
(zero/near-zero trades ⇒ the rank/filter isn't resolving → fix or drop). See **sweep-reoptimization**.

## Source recipes

- `references/reddit-wsb-recipe.md` — the proven Reddit Arctic lake mention-count pipeline.
- `references/congressional-disclosures.md` — House Clerk PTR pipeline (all-Congress aggregate).
- `references/other-sources.md` — insider Form 4, news-flow, attention; and `sec_edgar` scope.
