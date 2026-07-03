# Other alt-data sources (opportunistic — only if the primary sources go smoothly)

Pick ONE, by data quality for the specific 21 names. **Two good indicator families beat three rushed
ones.** Each still passes the full verify gate (point count + coverage + freshness + lookahead +
spot-check) before wiring.

## Insider transactions (corporate Form 4)
- Source: `sec_edgar` with `forms:["4"]`. **Filed dates are free**; buy-vs-sell direction needs the
  filing XML (the transaction code).
- Stamp at the Form 4 filing date. Direction matters — an aggregate needs net or buy-only dollars, not
  raw filing counts.

## News-flow intensity
- Derive from `search_stock_news` — a per-name daily article/mention count as an attention proxy.
- Stamp at article publish date. Watch for source-coverage bias across names.

## Attention (Google-Trends-style)
- Search-interest series per name if a clean source is available. Same lookahead + coverage rules.

## Scope reminder
`sec_edgar` is corporate filings only — 10-K / 10-Q / 8-K and Form 4. It does **not** carry
congressional PTRs (those are House Clerk — see `congressional-disclosures.md`).

## Selection principle
Build in **descending order of expected signal + data reliability**. Momentum stays the primary rank
signal; every alt-data source is a tilt/filter/overlay on top of it until proven otherwise on OOS
folds. A null result honestly reported is a valid outcome — don't torture a weak source until it
"wins."
