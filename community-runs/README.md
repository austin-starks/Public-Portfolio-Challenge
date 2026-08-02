# Community runs — beat the incumbent

Run the same evidence discipline with your agent, submit the artifacts, and see where it lands. A NexusTrade account is required to run the MCP workflow; a paid plan or live brokerage deployment is not required. Paper-only runs are welcome.

## Submit a run

1. Fork this repository and connect NexusTrade through the [Developers page](https://nexustrade.io/developers).
2. Run [`episode-10/BAKEOFF_RUNBOOK.md`](../episode-10/BAKEOFF_RUNBOOK.md) without changing the frozen universe, capital, calendar, or gates. If you intentionally test a new campaign version, state the differences and accept an unranked result.
3. Create `community-runs/<github-handle>/<run-slug>/` with:
   - `result.json`, copied from [`example/result.json`](example/result.json)
   - `README.md` explaining the strategy and outcome
   - the full campaign log, or a durable public link to it
4. Run `python3 scripts/update_leaderboard.py` and commit the updated root README.
5. Open a pull request with the community-run template.

## Ranking rules

- A run is ranked only after maintainer review sets `verification_status` to `verified` and all eight current gates are `true`.
- Eligible runs are ranked by mean fixed deploy-shape OOS return. OOS Sortino and worst max drawdown remain visible so return cannot hide the risk.
- Failed, pending, overridden, or non-comparable runs remain visible but unranked.
- Every number must point to fold-level evidence. Screenshots without a campaign log and IDs are not reproducible evidence.
- No live-money deployment is required. If you did deploy, disclose whether it was paper or live and whether orders required manual approval.

The structural validator catches missing fields and inconsistent pass claims. It does not independently rerun your NexusTrade campaign; that happens during review.
