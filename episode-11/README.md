# Episode 11: the Moderna readout, Grok Bot's books, and the live Semis + Biotech allocator

Episode 11 started after the **2026-08-19** Moderna/Merck intismeran autogene + Keytruda Phase 3
melanoma readout. It has two agent campaigns and one live account.

| Stage | Agent | What it produced | Record |
| --- | --- | --- | --- |
| Original books (through 2026-08-23) | **Grok Bot** (xAI's autonomous agent) | Researched and froze the company lists, designed and swept the mechanisms, chose the cross-fold robust settings and assembled two books: the 20-name biotech book (Moderna Trading Bot) and the 7-name semiconductor book (SemiConductor Trading, S13 A). | [`GROK_BOT_CAMPAIGN_LOG.md`](GROK_BOT_CAMPAIGN_LOG.md), [`moderna/`](moderna/), [`../episode-semis/`](../episode-semis/) |
| Cash-account rebuild and redesign (2026-08-24 to 2026-08-26) | **Codex** (OpenAI's coding agent) | Audited the universe, combined the two cash accounts into one $13,500 book, deployed a sector-gated version on Aug 24 CT, then rebuilt it as the 26-company allocator that went live on Aug 26 CT. | [`CODEX_CAMPAIGN_LOG_20260824T134240Z.md`](CODEX_CAMPAIGN_LOG_20260824T134240Z.md), [`addendum/`](addendum/) |
| Live forward test (2026-08-26 onward) | none; the deployed strategies run on NexusTrade | Every live order, current positions and the return against SPY. | [`FORWARD_TEST_LOG.md`](FORWARD_TEST_LOG.md) |

Austin set the experiment, supplied the thesis brief and remained the only person allowed to approve
a live order. He did not pick the companies. The names in every Episode 11 book trace back to Grok
Bot's frozen lists. The live 26-company universe is Grok Bot's 20 biotech names plus its 7
semiconductor names, minus PSNL (which Tempus agreed to acquire on 2026-08-21).

## Live account

- **Portfolio:** **Public Portfolio Challenge: Semis + Biotech**, id `6a8cb433e3971b7c87943f11`,
  Public account `5OH79160`, `initialValue` $13,500, deployment frequency `Constant`.
- **Public page:** [nexustrade.io/shared-portfolio/6a8cb4ebc57fd738a24f1a41](https://nexustrade.io/shared-portfolio/6a8cb4ebc57fd738a24f1a41)
- **Strategy set:** 29 strategies deployed on 2026-08-26 CT (2026-08-27 02:05 UTC). One
  RebalanceOption allocator over 26 companies, two global CloseOption exits (+300% gain, 180 DTE
  remaining) and 26 company-specific CloseOption exits. Long calls only.
- **Positions as of 2026-10-02:** five long calls (SDGR, PACB, NVDA, RXRX, MRK). See
  [`FORWARD_TEST_LOG.md`](FORWARD_TEST_LOG.md) for the order list, marks and the SPY comparison.
- **Approval state as of 2026-10-02:** the portfolio policy reads `automatedApproval.enabled: true`
  (max 25 trades per day), last updated 2026-09-14 23:06 UTC by the owner account. All 29
  strategy-level `automaticOrderApproval` flags read `false`. At deployment on Aug 26 both levels
  were off.
- **Runbook for the live allocator:** [`LIVE_ALLOCATOR_RUNBOOK.md`](LIVE_ALLOCATOR_RUNBOOK.md).
- **Exact rules and certification:** [`addendum/EPISODE_11_OPTIONS_PORTFOLIO_REDESIGN_20260826.md`](addendum/EPISODE_11_OPTIONS_PORTFOLIO_REDESIGN_20260826.md).

## Historical and paper books

| Book | Status | Where |
| --- | --- | --- |
| Public Portfolio Challenge: Biotech (`6a5e20a3ea0d6db55c69a171`, former Public `5OH86568`) | Grok Bot's biotech KEEP book was cloned here on 2026-08-23. Entry strategies were removed on 2026-08-24 and the cash was consolidated into `5OH79160`. Historical record. | [`moderna/`](moderna/) |
| Public Portfolio Challenge: Semis (`6a45f218e6b1f2131d1f26be`) | Grok Bot's S13 A book. Its Public account `5OH79160` now carries the combined $13,500 book. Historical record. | [`../episode-semis/`](../episode-semis/) |
| Moderna Trading Bot: Original Grok Paper | Paper reproduction of Grok Bot's biotech rules, $5,500. | [shared page](https://nexustrade.io/shared-portfolio/6a8d07f817356dfe9cc71f11) |
| SemiConductor Trading: Original Grok Paper | Paper reproduction of Grok Bot's semis rules, $8,000. | [shared page](https://nexustrade.io/shared-portfolio/6a8d07fc17356dfe9cc71fc9) |
| Episode 11 Legacy Sector-Gated XBI + SMH (`6a8f9b0ec67c177db82d5b0f`) | The six-strategy Codex design that ran live between Aug 24 and Aug 26 CT, preserved in paper. | [`CODEX_CAMPAIGN_LOG_20260824T134240Z.md`](CODEX_CAMPAIGN_LOG_20260824T134240Z.md) |

## Addenda (Codex research record, in order)

1. [`addendum/SHORT_TERM_DEBIT_SPREADS_20260824.md`](addendum/SHORT_TERM_DEBIT_SPREADS_20260824.md): the 180-DTE debit-vertical ceiling. Superseded once the cash-account spread restriction was confirmed.
2. [`addendum/COMBINED_LONG_CALL_RESEARCH_20260824.md`](addendum/COMBINED_LONG_CALL_RESEARCH_20260824.md): the combined $13,500 long-call research and the failed lockbox (-44.15%).
3. [`addendum/PORTFOLIO_UNIVERSE_AUDIT_20260825.md`](addendum/PORTFOLIO_UNIVERSE_AUDIT_20260825.md): the stock-by-stock audit that removed RXRX, SDGR and BMY on Aug 25. Those three were restored on Aug 26.
4. [`addendum/EPISODE_11_OPTIONS_PORTFOLIO_REDESIGN_20260826.md`](addendum/EPISODE_11_OPTIONS_PORTFOLIO_REDESIGN_20260826.md): the deployed 26-company allocator. Its line "Austin decides which companies belong and why" describes the eligibility role, not who chose the names. The names came from Grok Bot.

## Method and grade

- **Runbook version:** Per-book. Walk-forward folds, `crossFoldRobustSelection`, capital posture and
  the single-touch lockbox are inherited from [`episode-10/BAKEOFF_RUNBOOK.md`](../episode-10/BAKEOFF_RUNBOOK.md).
- **Grade:** Grok Bot's biotech book used an owner override: the deploy bar was a very good
  Challenge-class book, not Episode 10 Gate 4 vs Baseline C (`+59.33%` / Sortino `3.02`). The live
  allocator was certified on five $13,500 out-of-sample folds (4 of 5 profitable, median +25.00%,
  worst OOS drawdown 22.47%). It was deployed without a fresh untouched lockbox; the only valid
  combined-book lockbox had already failed on Aug 24. The forward test is the evidence that matters
  now.
- **Article:** [Moderna basically cured cancer, so I used Grok Bot to create a trading strategy on it](https://nexustrade.io/blog/moderna-basically-cured-cancer-i-used-grok-bot-to-create-a-trading-strategy-20260823)

Earlier Episode 11 attempts on the $25k Challenge incumbent were archived off `main` (August 2026).
They are not reconstructed here.
