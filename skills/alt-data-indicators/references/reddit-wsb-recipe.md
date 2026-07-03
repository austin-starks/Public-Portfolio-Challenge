# Reddit / WSB mention-count recipe (proven)

Daily WSB mention counts per ticker — the primary, proven alt-data signal.

## Source lake
`s3://nexustrade-parquet/reddit/arctic/submissions/YYYY/MM/NNN.parquet` — **~20 shards/month.**

## Pipeline (in a compute session)
1. **Read ALL shards per month — never sample shard 000.** Submissions shards are subreddit-sorted, so
   shard 000 is not representative.
2. Filter `lower(subreddit) = 'wallstreetbets'`.
3. Select only `title`, `selftext`, `created_at` (~15–25 s/month).
4. Count mentions per ticker per day. **Guard ambiguous tickers** (NET, APP, GLD, COP, GS, META) with
   **cashtag-or-alias matching** so common English words don't inflate counts.
5. Stamp each point at the **UTC post date** (the date the post was public) — this is the lookahead
   guarantee.
6. Dedupe against any existing series and `compute_session_promote_indicator` the extended history as
   ONE indicator.

## Freshness / refresh discipline
- **Check the lake's max month FIRST.** A prior full build covered 2021-12 → 2025-12 (7,228 pts, all 21
  tickers) because the lake had no 2026 data at build time.
- **Refresh, don't rebuild:** run the recipe only over months the lake has gained since the last max
  month; dedupe; promote the extended history. Only rebuild history if the recipe itself changes.
- Coverage end is a hard constraint on certification windows and deployability — a stale rank series is
  a dead book, and may not drive the live book until refreshed to the present.

## Validation
Cross-validate counts with a second, independently-generated build — a prior build matched exactly.
Optional enrichment if time allows: a title/selftext **sentiment/polarity** variant of the same scan,
under the same lookahead rules (retroactive sentiment model on historical posts is acceptable, noted as
a caveat).
