# GROK BOT Campaign Log - Episode 11

Agent: Grok Bot (xAI's autonomous agent, running on its own cloud computer)
Agents created: two, one per thesis. **Moderna Trading Bot** (biotech) and **SemiConductor Trading** (semis).
Tooling: NexusTrade MCP server for research, backtests, walk-forward studies and deploys; Python SDK for batch studies; a browser that the article says it barely used.
Window: after the 2026-08-19 Moderna/Merck readout through the live clones on 2026-08-23 CT.

## Source note

This log is reconstructed from the published Episode 11 article, the frozen books recorded in
[`moderna/`](moderna/) and [`../episode-semis/`](../episode-semis/), and the paper reproductions of
both books. **Grok Bot's own research transcript is not in this repo.** Its intermediate searches,
rejected candidates and reasoning are therefore not recorded here beyond what those sources state.
Nothing below is reconstructed from memory.

## Division of work (as stated in the article)

- Austin set the experiment: the theses, funded accounts, calendars, four-fold structure, lockbox
  rules and pass/fail gates. He supplied the thesis brief and remained the only person allowed to
  approve a live order.
- Grok Bot did the strategy work. In the article's words, "it researched and froze the names,
  designed and swept the candidate mechanisms, killed the ones that missed a gate, chose the
  cross-fold robust settings, assembled the final books and staged them for my approval."
- Austin did not pick the companies. Both frozen lists below are Grok Bot's output.

## Thesis brief given to Grok Bot

From the article: "Moderna's innovation proves AI is not a fad. Which means two things: biotech is
about to have its most explosive rally ever, and AI is not going to stop." Grok Bot was pointed at
the Public Portfolio Challenge runbook ([`../episode-10/BAKEOFF_RUNBOOK.md`](../episode-10/BAKEOFF_RUNBOOK.md)) and given that brief.

## Frozen universes

- **Biotech (Moderna Trading Bot), 20 names:** MRNA MRK BNTX PSNL RXRX SDGR ADPT GH NTRA VCYT ILMN
  TWST QGEN TXG PACB TMO DHR A TECH BMY. Canonical watchlist `6a88fe991037666dfebd096c`.
- **Semis (SemiConductor Trading), 7 names:** NVDA TSM AVGO AMAT LRCX ANET MRVL. Canonical watchlist
  `6a890a9c0c5e08a7b308164b` (`SEMIS AI 20260822 freeze`).

The article discloses that the 20 biotech names were frozen in August 2026 with knowledge of how the
April to August stretch had gone, so hindsight is in the name list.

## Biotech book: KEEP

- Selecting study `6a8a7a9f2229e2cd48bfa2b7`, chosen by `crossFoldRobustSelection` (not fold argmax).
- Frozen knobs: total budget 75, SelectTop 20, roll DTE 90, take-profit 80, delta about 0.50,
  365 to 730 DTE long calls. Rank by 63-day return divided by 63-day volatility. Gates: VIX < 35 and
  a 7-day spacing rule. No trend filter.
- Walk-forward span 2022-01-01 to 2026-04-14, 4 anchored folds, 252-day OOS, validation 50%.
- Assembled OOS by fold: +26.407%, +25.437%, +56.296%, +20.751%. Mean +32.223%, Sortino 1.734, worst
  drawdown 44.28. ARKG over the same four windows per the article: -21.8%, -11.5%, -5.2%, +23.6%
  (mean -3.73%).
- Lockbox 2026-04-14 to 2026-08-18, one touch, $5,494.51: KEEP +62.966%, Sortino 4.247, max
  drawdown 24.879% (`6a8a884a6b55968aac525c62`). SPY +11.292%. ARKG +50.099%. The same 20 names held
  as equal-weight stock returned +39.43% per the article. Median deployment 15.44%. Breadth 17 of 20.
- Failed neighborhoods recorded: TP60, later-roll 180 with delta 0.55, Challenge-shape transplant,
  KEEP plus SMA100/ROC63 flatten, wave-3 OTM/high-beta/regime. All killed.
- Deploy bar: an owner override set it at a very good Challenge-class book rather than Episode 10
  Gate 4 vs Baseline C.
- Live clone 2026-08-23 CT onto **Public Portfolio Challenge: Biotech** (`6a5e20a3ea0d6db55c69a171`):
  3 strategies, cash $5,494.51, automated approval off, no option opens at the Sunday reconcile.
  Full detail: [`moderna/CAMPAIGN_LOG.md`](moderna/CAMPAIGN_LOG.md).

## Semis book: S13 A

- Chat source `6a8b9a85d287103ac48dcb14` (`SEMIS S13 A CHEAP15 M63 DTE45 20260823`).
- Two sleeves, both `positionScope=strategy`. LEAP sleeve: 12% per name, 20/25 then 10/25 percent-debit
  call verticals, 365 to 730 DTE. Cheap sleeve: 15% per name, 20/25 verticals, 90 to 180 DTE. Both
  gated by a 63-day first-fire rule and VIX < 35. Filter: price above SMA100 and ROC63 > 0. SelectTop
  7 by ROC126. Exits: +300% take-profit, DTE 21 or less, DTE 22 to 45, per-name flatten.
- Search ended 2026-04-17. Four ET folds vs SMH: 57.305 vs 44.807, 58.852 vs 7.403, 66.861 vs 20.765,
  69.058 vs 57.166. Mean 63.019 vs 32.535.
- Lockbox 2026-04-17 to 2026-08-23: S13 A +44.432%. SMH is recorded as +20.797% in
  [`../episode-semis/RUNBOOK.md`](../episode-semis/RUNBOOK.md) and as +21.09% in the article; the
  difference between those two SMH figures is not explained in either source. The same 7 names as
  stock returned +20.35% and SPY +8.18% per the article. Median deployment 14.70%.
- Live clone 2026-08-23 night CT onto **Public Portfolio Challenge: Semis** (`6a45f218e6b1f2131d1f26be`),
  $8,000 cash, auto-approve off. Full detail: [`../episode-semis/RUNBOOK.md`](../episode-semis/RUNBOOK.md).

## What happened to the Grok Bot books

- On 2026-08-24 the live books stopped running Grok Bot's entry rules. Biotech option orders were
  broker-rejected with `Option level required` (Austin called it "an old bug" he had just fixed), and
  both accounts turned out to be cash accounts, where Public does not allow spreads. Spreads are only
  available in Austin's single margin account. Codex took over from there; see
  [`CODEX_CAMPAIGN_LOG_20260824T134240Z.md`](CODEX_CAMPAIGN_LOG_20260824T134240Z.md).
- Both Grok Bot books now run only as paper controls, recreated on 2026-08-25 from archived share
  snapshots of the original deployed rules:
  - **Moderna Trading Bot: Original Grok Paper**, $5,500: [shared page](https://nexustrade.io/shared-portfolio/6a8d07f817356dfe9cc71f11)
  - **SemiConductor Trading: Original Grok Paper**, $8,000: [shared page](https://nexustrade.io/shared-portfolio/6a8d07fc17356dfe9cc71fc9)
- The live 26-company allocator keeps Grok Bot's names. Its universe is the 20 biotech names plus the
  7 semis names, minus PSNL. Grok Bot's trading mechanics (delta 0.50 LEAPs at +80%, and the S13 A
  debit verticals) are not what trades live.

## Final status

Grok Bot delivered two frozen, lockbox-tested books and staged them for approval. Neither book held a
live option position: the biotech reconcile produced no opens on 2026-08-23, and at Codex's
2026-08-24 13:57 UTC read Biotech held only BTC dust and Semis was empty. Both entry strategies were
removed on 2026-08-24.
