# Diagnose: fetch_portfolios corrupts deployed strategy summaries

## One-line

`fetch_portfolios` returns nine blank strategy IDs named ` when  condition` for a newly deployed
paper portfolio even though both the deploy response and `get_portfolio` return all nine complete
persisted strategies; this appears to be a compact-list serialization defect rather than runtime
strategy corruption.

## Expected vs observed

- **Expected:** fetching paper portfolio `6a5e1f9d814d31180a1c8768` should summarize the nine deployed
  strategies with their real IDs and names.
- **Observed:** `fetch_portfolios` reports `strategyCount: 9`, but every `strategyId` is empty and every
  name is ` when  condition`. `get_portfolio` on the same ID returns real strategy IDs
  `6a5e1f9d814d31180a1c873c` through `6a5e1f9d814d31180a1c874c`, complete actions/conditions, and a
  complete condition-field audit.

## Reproduction

- Source chat portfolio: `6a5df976ea0d6db55c697601` — 40% MU core, 40% SNDK core, four
  one-leg outright-long 0DTE call/put entries, and three close rules.
- Paper deployment: `6a5e1f9d814d31180a1c8768`, created through `edit_portfolio(type=deploy)`.
- Call `fetch_portfolios` with `portfolio_ids:["6a5e1f9d814d31180a1c8768"]`, paper enabled and
  positions enabled. Observe nine blank IDs and nine malformed names.
- Call `get_portfolio` with the same ID. Observe nine complete persisted strategies and valid audit
  fields.

## Leading hypothesis (verify, don't assume)

**Hypothesis:** the compact deployed-portfolio projection/formatter reads a normalized strategy
summary shape that does not match the persisted embedded strategy shape (`_id`, `name`, `condition`,
`action`). The count survives, but ID/name reconstruction receives empty fields.

## Alternatives to rule out

1. **Eventual consistency.** Re-fetch after deployment and compare; the full `get_portfolio` record
   was already coherent while the compact summary remained malformed.
2. **Display-only synthesis.** If `fetch_portfolios` intentionally synthesizes names, it must still
   preserve IDs and should fall back to persisted `name` instead of emitting blanks.

## Where to look

- The deployed strategy summary mapping used by `fetch_portfolios`.
- The formatter that constructs `<action> when <condition>` names and chooses `_id` versus
  `strategyId`.

## Diagnostic checks

1. Assert that every returned summary has a non-empty ID and name for this deployed portfolio.
2. Compare `fetch_portfolios` and `get_portfolio` summaries for the same chat, paper, and live record
   shapes.

## Impact on prior results

No backtest or certification result is invalidated, and the paper deployment itself is verified by
`get_portfolio`. The defect blocks trusting `fetch_portfolios` strategy names/IDs for post-deploy
field verification, strategy removal, or UI summaries until fixed.
