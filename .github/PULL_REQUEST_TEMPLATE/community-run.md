## Community run submission

- Run folder: `community-runs/<handle>/<run>/`
- Agent/model:
- Runbook commit (full SHA):
- Paper or live:
- Mean fixed deploy-shape OOS return:
- OOS Sortino:
- Worst fold max drawdown:
- Gate result: PASS / FAIL

## Evidence checklist

- [ ] I included `result.json`, a readable run summary, and the full campaign log or a durable public link.
- [ ] I reported OOS numbers, not training or optimizer-validation numbers.
- [ ] I evaluated one fixed deploy-shape book across every fold.
- [ ] I did not change the frozen universe, capital, calendar, or gates, or I clearly marked the run non-comparable.
- [ ] I ran `python3 scripts/update_leaderboard.py` and `python3 -m unittest discover -s tests`.
- [ ] I disclosed owner overrides, engine failures, burned lockboxes, and live deployment status.

Maintainers set `verification_status: verified` after reviewing the evidence. Please leave new submissions as `pending`.
