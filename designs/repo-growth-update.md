# Public Portfolio Challenge repository growth update

## Goal

Turn the repository into a current, verifiable record and a repeatable community challenge without weakening the runbook's evidence standards.

## Decisions

- Generate the live scoreboard from anonymous NexusTrade API endpoints. The generated table is delimited by HTML comments so automation only replaces its own block.
- Use the portfolio history window for every comparison. SPY is sampled from the first portfolio observation through the latest portfolio observation; no mismatched year-to-date comparison is allowed.
- Commit both the rendered README table and a machine-readable `data/scoreboard.json` snapshot each week.
- Compare agent runs using fixed deploy-shape OOS evidence where their logs contain it. A deployed owner override is not represented as a clean gate pass.
- Preserve Episodes 1-9 as historical index entries. When the exact prompt artifact was not retained, say so instead of reconstructing one.
- Rank community submissions by mean OOS return only after the submission declares every current runbook gate passed and provides reproducible artifacts. Failed or pending runs remain visible but unranked.

## Automation boundaries

- The weekly scoreboard workflow has repository `contents: write` permission only.
- Public API calls require no brokerage credentials or repository secrets.
- Community submissions are validated structurally in CI; maintainers still verify evidence during PR review.
- Automation never deploys a strategy or places an order.
