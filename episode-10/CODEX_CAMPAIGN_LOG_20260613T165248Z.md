# CODEX Campaign Log - 20260613T165248Z

Run start UTC: 2026-06-13T16:52:48Z
Agent: CODEX
Workspace: /Users/austinstarks/Desktop/public-portfolio-challenge

## Runbook Compliance Notes

- Isolated run log created before campaign execution.
- This run will not read, diff, import, or reference other `*_CAMPAIGN_LOG_*.md` files or artifacts from other runs.
- Runtime portfolio/backtest/study steps will use MCP tools only, except for reading committed snapshots from `snapshots/`.

## Calendar

- Run date: 2026-06-13
- Lockbox width: 126 calendar days
- Walk-forward/search span: 2022-01-01 to 2026-02-07
- Lockbox span: 2026-02-07 to 2026-06-13

## S0 - Engine Sanity

### S0.1 Walk-forward sweep smoke

- Smoke seed: `CODEX S0 Smoke SPY SMA50 20260613T165248Z`
- Smoke chatPortfolioId: `6a2d8b2408bb1349f5b63e52`
- `get_sweep_surface` returned applicable fields: Portfolio/Subject, Action/RankSignal, UniversePipeline/UniversePipelineFilter, UniversePipeline/SelectTopLimit.
- Smoke gene axis selected: `Select top limit: 1, 5, 10` (harmless on one-name SPY universe; contract check only).
- Preview accepted: 2 folds, 8 planned units, 3 child sweep cells, no gene warnings.
- Smoke study launched: `6a2d8b4d08bb1349f5b63ee2`; initial status RUNNING.
- Smoke study completed: `6a2d8b4d08bb1349f5b63ee2`, 8/8 units, 2/2 folds complete.
- Fold 0 selectedChatPortfolioId: `6a2d8ba8e5a40a29b74c6800`.
- Fold 1 selectedChatPortfolioId: `6a2d8ba8e5a40a29b74c6804`.
- Persistence PASS: every completed fold returned a real `selectedChatPortfolioId`; no materialization error reported.
- Window disjointness PASS from fold calendar:
  - Fold 0 train 2022-01-01T05:00:00Z to 2024-02-22T04:59:59.999Z; validation 2024-03-07T05:00:00Z to 2024-09-22T03:59:59.999Z; OOS 2024-09-22T04:00:00Z to 2025-06-01T03:59:59.999Z.
  - Embargo separates train from validation; validation ends 1 ms before OOS starts.

### S0.2 Window fidelity

- Standalone validation backtest for fold-0 winner with exact UTC window: `6a2d8be0daff5c67a9716010`.
- Fold validation statistics matched exactly: return 11.25820452667859%, Sortino 1.442201015738444, maxDD 8.999188303077196%.
- Standalone OOS backtest for fold-0 winner with exact UTC window: `6a2d8be3daff5c67a971601b`.
- Fold OOS statistics matched exactly: return 4.017399924017649%, Sortino 0.2612468956125016, maxDD 19.891435250146372%.
- Note: bare date inputs matched return/maxDD but had small Sharpe/Sortino drift; exact UTC fold boundaries are required for strict fidelity.

### S0.4 Dead-name handling

- Dead-name audit seed: Baseline B 20-name options ladder.
- Baseline B chatPortfolioId: `6a2d8b8ce5a40a29b74c67d8`
- Early-2022 backtest will use `generate_events: true` to inspect SNDK not-yet-listed handling.
- Dead-name audit backtest: `6a2d8ba1daff5c67a9715f76` for 2022-01-01 to 2022-03-31.
- Status PASS: backtest completed (return -1.1837597906113224%, maxDD 26.788475190420773%).
- SNDK PASS: breadth audit showed SNDK openFills 0, closeFills 0, entryNotional 0, resolutionAttempts 0, no pre-resolution aborts, no rejections, and empty samples.
- SNDK event query PASS: no SNDK OptionResolutionAttempt/OpenOptionSignal/OrderRejected/TradingAudit events found.

S0 verdict: PASS. Proceeding to S1 baseline scoring.

## S1 - Baselines

- Baseline A loaded from `snapshots/baseline_a.json` and persisted as chatPortfolioId `6a2d8b70daff5c67a9715f10`.
- Baseline B loaded from `snapshots/baseline_b.json` and persisted as chatPortfolioId `6a2d8b8ce5a40a29b74c67d8`.
- Baseline C bar is frozen from the runbook, not recomputed.
- Incumbent seed source: `snapshots/incumbent.example.json` (no `snapshots/incumbent.json` present).
- Incumbent example seed persisted as chatPortfolioId `6a2d8c65e5a40a29b74c692c`. This seed is for the certification loop only and is not the frozen Baseline C bar.
- Baseline A backtest-only WF study launched: `6a2d8c0b08bb1349f5b63fff` (4 folds, 12 planned units, tokenCost 16).
- Baseline B backtest-only WF study launched: `6a2d8c0edaff5c67a971604e` (4 folds, 12 planned units, tokenCost 25.8).

### Baseline A results

- Study `6a2d8c0b08bb1349f5b63fff` COMPLETE.
- Fold 0 OOS 2023-05-07 to 2024-01-14: return 42.221312528523704%, Sortino 3.805782747380374, maxDD 9.687878613583473%, breadth 19/20.
- Fold 1 OOS 2024-01-14 to 2024-09-22: return 41.00001744463426%, Sortino 2.793670524082655, maxDD 17.964835902071925%, breadth 19/20.
- Fold 2 OOS 2024-09-22 to 2025-06-01: return 25.215624891982664%, Sortino 1.4619988125636227, maxDD 30.638954146047393%, breadth 20/20.
- Fold 3 OOS 2025-06-01 to 2026-02-08: return 51.76976521022938%, Sortino 3.5091917074683145, maxDD 11.062133362146426%, breadth 20/20.
- Aggregate OOS return mean 40.051680018842504%, median 41.61066498657898%, min 25.215624891982664%, max 51.76976521022938%.
- Aggregate OOS Sortino mean 2.8926609478737415, median 3.151431115775485, min 1.4619988125636227, max 3.805782747380374.
- Aggregate OOS maxDD worst 30.638954146047393%.

### Baseline B original results

- Original Baseline B full-span backtest for posture: `6a2d8c7ddaff5c67a97160fe`.
- Original Baseline B full-span stats: return 1385.9588876922014%, Sortino 2.054234406177131, maxDD 70.88337876543291%, breadth 20/20.
- Original Baseline B posture audit: median deployment 63.77%, mean 65.13%, p90 85.3%, max 98.66%, days >70% 431/1268 (34.0%), regime violations total 692.
- S1.5 FIRED: original Baseline B is not posture-comparable because median deployment exceeds 55%. It remains an unconstrained reference only.
- Original Baseline B WF study `6a2d8c0edaff5c67a971604e` COMPLETE.
- Fold 0 OOS 2023-05-07 to 2024-01-14: return 25.807063857819536%, Sortino 1.1707434779389665, maxDD 34.57348165374384%, breadth 13/20 from WF stats.
- Fold 1 OOS 2024-01-14 to 2024-09-22: return 54.759319916981006%, Sortino 1.798699981199952, maxDD 39.59704436523272%, breadth 13/20 from WF stats.
- Fold 2 OOS 2024-09-22 to 2025-06-01: return 80.01518312309915%, Sortino 2.6169245236935925, maxDD 50.80230166470473%, breadth 11/20 from WF stats.
- Fold 3 OOS 2025-06-01 to 2026-02-08: return 147.3923040746555%, Sortino 3.366196855755351, maxDD 23.20837958218877%, breadth 14/20 from WF stats.
- Aggregate OOS return mean 76.9934677431388%, median 67.38725152004008%, min 25.807063857819536%, max 147.3923040746555%.
- Aggregate OOS Sortino mean 2.2381412096469657, median 2.2078122524467725, min 1.1707434779389665, max 3.366196855755351.
- Aggregate OOS maxDD worst 50.80230166470473%.

### S1.5 posture-matched Baseline B

- First derated candidate: totalBudget 80%, chatPortfolioId `6a2d8cc4daff5c67a971612f`.
- Full-span posture backtest launched: `6a2d8ccd08bb1349f5b641bf`.
- 80% budget posture result: median 63.6%, mean 64.79%, p90 84.0%, max 96.78%; FAIL median cap.
- 55% budget candidate: chatPortfolioId `6a2d8d1408bb1349f5b6424d`, backtest `6a2d8d1ddaff5c67a9716203`; median 65.71%, mean 64.33%, p90 85.5%, max 93.19%; FAIL median cap.
- 35% budget candidate: chatPortfolioId `6a2d8d4ddaff5c67a9716279`, backtest `6a2d8d55e5a40a29b74c6a56`; median 61.42%, mean 60.67%, p90 88.8%, max 94.92%; FAIL median cap.
- 20% budget candidate: chatPortfolioId `6a2d8d7a08bb1349f5b642e3`, backtest `6a2d8d8108bb1349f5b642f6`; median 21.86%, mean 31.56%, p90 73.7%, max 89.75%; PASS median cap.
- 10% budget candidate: chatPortfolioId `6a2d8da5daff5c67a97162ba`, backtest `6a2d8daf08bb1349f5b6435b`; median 11.43%, mean 14.42%, p90 26.3%, max 77.13%; PASS but over-derated.
- S1.5 selected posture-matched Baseline B: 20% totalBudget variant `6a2d8d7a08bb1349f5b642e3` (first passing derate).
- Official posture-matched B WF study launched: `6a2d8de1daff5c67a971634e`.
- Official WF status currently RUNNING at 9/12 units with folds 0-2 complete and fold 3 in OOS; direct fold-3 OOS backtest completed and is logged below as supporting evidence while waiting for wrapper aggregate.
- Official posture-matched B WF study `6a2d8de1daff5c67a971634e` COMPLETE.
- Official posture-matched B fold 0 OOS 2023-05-07 to 2024-01-14: return 3.1140751171112058%, Sortino 0.06599490355650792, maxDD 11.187081397546454%, breadth 3/20.
- Official posture-matched B fold 1 OOS 2024-01-14 to 2024-09-22: return 45.586150005876554%, Sortino 2.115848893461185, maxDD 32.81589881001869%, breadth 6/20.
- Official posture-matched B fold 2 OOS 2024-09-22 to 2025-06-01: return 64.08938741578156%, Sortino 2.7362588368932577, maxDD 44.937220467038344%, breadth 11/20.
- Official posture-matched B fold 3 OOS 2025-06-01 to 2026-02-08: return 50.7554415368881%, Sortino 1.6424040455276419, maxDD 28.218937003373718%, breadth 13/20.
- Official posture-matched B aggregate: mean return 40.886263518914355%, median 48.17079577138233%, min 3.1140751171112058%, max 64.08938741578156%; mean Sortino 1.6401266698596482, median 1.8791264694944134, min 0.06599490355650792, max 2.7362588368932577; worst maxDD 44.937220467038344%.
- Gate-4 B bar after S1.5: return bar uses posture-matched B official WF. B Sortino bar applies only in folds with >= 9/20 breadth, so folds 2 and 3 from the official WF.
- Supporting direct OOS fold backtests for posture-matched B:
  - Fold 0 `6a2d8e1508bb1349f5b643b9`: return 3.202680237388558%, Sortino 0.07670182387255466, maxDD 11.184385484839465%, breadth audit 3/20.
  - Fold 1 `6a2d8e18e5a40a29b74c6b51`: return 45.76328304233547%, Sortino 2.1236010128647167, maxDD 32.79444491536487%, breadth audit 6/20.
  - Fold 2 `6a2d8e1ce5a40a29b74c6b67`: return 69.33143891700503%, Sortino 2.909965415551476, maxDD 44.22879073998737%, breadth audit 11/20.
  - Fold 3 `6a2d8e2108bb1349f5b643d5`: return 52.15907969169604%, Sortino 1.668396288585345, maxDD 28.14559492612935%, breadth audit 13/20.
- B Sortino validity by breadth from direct audits: folds 0-1 invalid (<9/20); folds 2-3 valid (>=9/20).

## Search Layer

### Mandatory systematic_sweep

- Seed: incumbent example / regime-switched momentum seed `6a2d8c65e5a40a29b74c692c`.
- `get_sweep_surface` applicable fields included BuyingPowerPct, AllocationPct, DteBracket, StrikeDistance, SelectTopLimit, RankSignal, RollTriggerDte, TakeProfitPct.
- Preview compiled successfully for deployment x allocation x DTE x strike/structure x breadth:
  - BuyingPowerPct: 20%, 35%, 55%
  - AllocationPct: 4%, 6%, 8%
  - DTE bracket: 90-180, 150-365, 365-730
  - Strike distance / structure aggressiveness: ATM, 5% OTM, 10% OTM
  - SelectTopLimit: 8, 10, 12
- Planned evaluations: 243 exhaustive variants; no gene warnings.
- Systematic sweep launched: `6a2d8f0508bb1349f5b64577` (243 planned evaluations, Auto -> Exhaustive).
- Latest status: RUNNING, evaluationsDone 0/243, no leaderboard materialized yet.

### Certification attempt 1 - Regime-switched momentum / incumbent seed

- Family: regime-switched momentum / incumbent example mechanism.
- Seed: `6a2d8c65e5a40a29b74c692c`.
- `get_sweep_surface`: PASS; same surface as mandatory sweep, including BuyingPowerPct, AllocationPct, DteBracket, StrikeDistance, SelectTopLimit, RankSignal, RollTriggerDte, TakeProfitPct.
- Preview: PASS. 4 axes x 3 values = 81 child cells, 328 planned units, estimated token cost 728.1, no warnings.
- Gene intents:
  - BuyingPowerPct: 20%, 35%, 55%.
  - AllocationPct: 4%, 6%, 8%.
  - DTE bracket: 90-180, 150-365, 365-730.
  - TakeProfitPct: 75%, 100%, 150%.
- Certification study launched: `6a2d8f3b08bb1349f5b6460a`.
- Latest status: RUNNING, 0/328 units complete, rootOptimizerId `6a2d8f3b08bb1349f5b64611`.

### Certification attempt 2 - Single-sleeve momentum calls/verticals

- Family: single-sleeve momentum long calls/verticals.
- Clean seed created from Baseline B: `6a2d8ff008bb1349f5b64872`.
- Seed mechanics: 20-name fixed universe, 21-day cadence, per-name Price > SMA150 filter, SelectTop top 12 by ROC126, ROC126 weight/rank, 5% per-name allocation, 55% total budget, Baseline-B LEAP ladder and DTE roll exit.
- `get_sweep_surface`: PASS. Applicable fields included Action/RankSignal, Action/BuyingPowerPct, Action/AllocationPct, Action/RollTriggerDte, Action/TakeProfitPct, OptionLeg/StrikeDistance, OptionLeg/DteBracket, UniversePipeline/UniversePipelineFilter, UniversePipeline/SelectTopLimit.
- Preview: PASS. Compiled genes included:
  - BuyingPowerPct: 20%, 35%, 55%.
  - AllocationPct: 4%, 5%, 6%.
  - SelectTopLimit: top 8, top 10, top 12.
  - RankSignal: template ranking, 63D momentum, 126D momentum, 252D momentum.
  - DteBracket: 90-180, 150-365, 365-730.
- Preview planned units 1300; launch deduped/compiled to 976 planned units, tokenCost 2168.26.
- Certification study launched: `6a2d9036e5a40a29b74c6ef5`, rootOptimizerId `6a2d9036e5a40a29b74c6efc`.

### Certification attempt 3 - Momentum call diagonals/calendars

- Family: calendar / diagonal time-spreads.
- Clean seed created from Seed 2: `6a2d905908bb1349f5b648f7`.
- Seed mechanics: same fixed watchlist and momentum pipeline as Seed 2, but option structures are call diagonals/calendars with far-dated long calls and 60-120 DTE short calls; seed keeps DTE roll at <= 45 to avoid immediate short-leg closure.
- `get_sweep_surface`: PASS. Applicable fields included Action/RankSignal, Action/BuyingPowerPct, Action/AllocationPct, Action/RollTriggerDte, Action/TakeProfitPct, OptionLeg/StrikeDistance, OptionLeg/DteBracket, UniversePipeline/UniversePipelineFilter, UniversePipeline/SelectTopLimit.
- Preview: PASS. Compiled genes included:
  - BuyingPowerPct: 20%, 35%, 55%.
  - AllocationPct: 3%, 4%, 5%.
  - SelectTopLimit: top 8, top 10, top 12.
  - RankSignal: template ranking, 63D price ROC, 126D price ROC, 252D price ROC.
  - RollTriggerDte: 30, 45, 60.
- Preview planned units 1300, tokenCost 2888.36, no warnings.
- Certification study launched: `6a2d909adaff5c67a9716930`, rootOptimizerId `6a2d909bdaff5c67a971693c`.

### Certification attempt 4 - Momentum put credit spreads

- Family: defined-credit / short-premium put credit spreads.
- Clean seed created from Seed 2: `6a2d90bd08bb1349f5b649af`.
- Seed mechanics: same fixed watchlist and momentum pipeline as Seed 2, but option structures are put credit verticals with short puts and farther OTM long puts, 4% per-name allocation, 55% total budget.
- `get_sweep_surface`: PASS. Applicable fields included Action/RankSignal, Action/BuyingPowerPct, Action/AllocationPct, Action/RollTriggerDte, Action/TakeProfitPct, OptionLeg/StrikeDistance, OptionLeg/DteBracket, UniversePipeline/UniversePipelineFilter, UniversePipeline/SelectTopLimit.
- Preview: PASS. Compiled genes included:
  - BuyingPowerPct: 20%, 35%, 55%.
  - AllocationPct: 3%, 4%, 5%.
  - SelectTopLimit: top 8, top 10, top 12.
  - RankSignal: template ranking, 63D ROC, 126D ROC, 252D ROC.
  - DteBracket: 45-90, 60-120, 90-180.
- Preview planned units 1300, tokenCost 2888.36, no warnings.
- Certification study launched: `6a2d90e8e5a40a29b74c7137`, rootOptimizerId `6a2d90e8e5a40a29b74c713e`.

## Certification Ledger

| Family | Seed id | `get_sweep_surface` | gene_intents axes | Study id | `crossFoldRobustSelection` key | Assembled book id | Per-fold OOS gate result | PROMOTE / KILL (reason) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Regime-switched momentum / incumbent seed | `6a2d8c65e5a40a29b74c692c` | PASS | BuyingPowerPct 20/35/55; AllocationPct 4/6/8; DTE 90-180/150-365/365-730; TakeProfitPct 75/100/150 | `6a2d8f3b08bb1349f5b6460a` | `9068de59ca55162140b95c4056214bc8f4b09df19f94482ff9eed6c28e0a2d64` | `6a2d9185e5a40a29b74c7264` | Direct OOS assembled: F0 -2.82%, Sortino -0.47, maxDD 8.55%, breadth 10/20; F1 +19.96%, Sortino 2.79, maxDD 7.76%, breadth 8/20; F2 +21.30%, Sortino 1.20, maxDD 23.23%, breadth 12/20; F3 +12.87%, Sortino 0.85, maxDD 13.48%, breadth 7/20. | KILL - binding gate: Gate 4 vs Baseline C (fails C return and Sortino in every fold; F0 also fails positive OOS / Sortino floor). |
| Single-sleeve momentum calls/verticals attempt 1 | `6a2d8ff008bb1349f5b64872` | PASS | BuyingPowerPct 20/35/55; AllocationPct 4/5/6; SelectTopLimit 8/10/12; RankSignal 63/126/252/template; DTE 90-180/150-365/365-730 | `6a2d9036e5a40a29b74c6ef5` | none | none | Fold 0 certification failed after 243 units: no validation candidate passed certification floors. | KILL attempt - fold selection floors; family not exhausted. |
| Single-sleeve momentum calls/verticals attempt 2 | `6a2d91e0daff5c67a9716c3e` | PASS | BuyingPowerPct 20/35/55; AllocationPct 4/6/8; SelectTopLimit 8/10/12; DTE 90-180/150-365/365-730; TakeProfitPct 75/100/150 | `6a2d91ffe5a40a29b74c7366` | none | none | Mechanical compile/runtime error: TakeProfitPct axis did not match any non-roll CloseOption with a take-profit trigger. | KILL attempt - seed missing take-profit close action; repaired in attempt 3. |
| Single-sleeve momentum calls/verticals attempt 3 | `6a2d934108bb1349f5b64ece` | PASS | BuyingPowerPct 20/35/55; AllocationPct 4/6/8; SelectTopLimit 8/10/12; DTE 90-180/150-365/365-730; TakeProfitPct 75/100/150 | `6a2d935fdaff5c67a9716f58` | pending | pending | Preview PASS, study running; rootOptimizerId `6a2d935fdaff5c67a9716f60`. | PENDING. |
| Calendar / diagonal time-spreads attempt 1 | `6a2d905908bb1349f5b648f7` | PASS | BuyingPowerPct 20/35/55; AllocationPct 3/4/5; SelectTopLimit 8/10/12; RankSignal 63/126/252/template; RollTriggerDte 30/45/60 | `6a2d909adaff5c67a9716930` | none | none | Fold 0 certification failed after 324 units: no validation candidate passed certification floors. | KILL attempt - fold selection floors; family not exhausted. |
| Calendar / diagonal time-spreads attempt 2 | `6a2d921808bb1349f5b64c99` | PASS | BuyingPowerPct 20/35/55; AllocationPct 3/4/5; SelectTopLimit 8/10/12; DTE 90-180/150-365/365-730; TakeProfitPct 75/100/150 | `6a2d923908bb1349f5b64cc4` | none | none | Fold 0 certification failed after 243 units: no validation candidate passed certification floors. | KILL attempt - fold selection floors; family not exhausted. |
| Defined-credit / put credit spreads attempt 1 | `6a2d90bd08bb1349f5b649af` | PASS | BuyingPowerPct 20/35/55; AllocationPct 3/4/5; SelectTopLimit 8/10/12; RankSignal 63/126/252/template; DTE 45-90/60-120/90-180 | `6a2d90e8e5a40a29b74c7137` | none | none | Fold 0 certification failed after 324 units: no validation candidate passed certification floors. | KILL attempt - fold selection floors; family not exhausted. |
| Defined-credit / put credit spreads attempt 2 | `6a2d9250daff5c67a9716d06` | PASS | BuyingPowerPct 20/35/55; AllocationPct 2/3/4; SelectTopLimit 8/10/12; DTE 60-120/90-180/120-240; TakeProfitPct 50/75/100 | `6a2d92ed08bb1349f5b64e0e` | none | none | Fold 0 certification failed after 243 units: no validation candidate passed certification floors. | KILL attempt - fold selection floors; family not exhausted. |
| Regime long/flat momentum | `6a2d940fdaff5c67a97170b5` | PASS | BuyingPowerPct 20/35/55; AllocationPct 4/6/8; SelectTopLimit 8/10/12; DTE 90-180/150-365/365-730; TakeProfitPct 75/100/150 | `6a2d9437e5a40a29b74c76e0` | `0fba895dd44c9903b62511055b13ae1b74c73c52ba945a2e09878a2a01b9b5f1` | none | Certified OOS selected winners: F0 +4.62%, Sortino 0.28; F1 +24.00%, Sortino 1.42; F2 -0.11%, Sortino -0.06; F3 +19.75%, Sortino 1.00. Aggregate mean +12.07%, Sortino mean 0.66. Robust min Sortino -0.583. | KILL - binding gate: Gate 3 robust selection weak/negative; also Gate 4 vs Baseline C. |
| Mixed regime credit attempt 3 | `6a2d960208bb1349f5b65455` | PASS | BuyingPowerPct 20/35/55; AllocationPct 2/3/4; SelectTopLimit 8/10/12; DTE 60-120/90-180/120-240; TakeProfitPct 50/75/100 | `6a2d962ce5a40a29b74c79fa` | none | none | Fold 0 certification failed after 243 units: no validation candidate passed certification floors. | KILL attempt - fold selection floors; credit family exhausted after 3 attempts. |
| Calendar / diagonal time-spreads attempt 3 | `6a2d976fe5a40a29b74c7b6d` | PASS | BuyingPowerPct 20/35/55; AllocationPct 3/4/5; SelectTopLimit 8/10/12; DTE 90-180/150-365/365-730; TakeProfitPct 75/100/150 | `6a2d97a008bb1349f5b656fa` | `dc95ecc9e565cb026d937e939acdcb7ffd793c3c324d1850e838273ef2a05dfb` | none | Certified selected-winner OOS: F0 +0.35%, Sortino -0.12; F1 +10.22%, Sortino 0.64; F2 -13.29%, Sortino -0.89; F3 +23.56%, Sortino 1.78. Aggregate mean +5.21%, Sortino mean 0.35. Robust min Sortino 0.214. | KILL - binding gate: Gate 3 robust selection weak; Gate 4 vs Baseline C also fails. Calendar family exhausted after 3 attempts. |

### Certification attempt 1 completed details

- Study `6a2d8f3b08bb1349f5b6460a` completed 328/328 units.
- Per-fold selected winners were unstable (`winnerStableAcrossFolds=false`).
- `aggregate.crossFoldRobustSelection`:
  - candidateKey `9068de59ca55162140b95c4056214bc8f4b09df19f94482ff9eed6c28e0a2d64`
  - metric `minSortino`; score `0.916921680503794`
  - perFoldSortino `[0.916921680503794, 1.232181007755007, 1.8230968444550708, 0.9238627760566036]`
  - perFoldPercentChange `[12.06043896063618, 24.473974211675653, 54.62617597366138, 34.198203238555784]`
- Robust candidate materialized in optimizer page as `6a2d9141e5a40a29b74c7209`; field inspection showed per-name allocation rewritten to `percent of buying power` at `8`, long DTE `365-730`, take-profit `100%`.
- Assembled deploy-shape book from a clean seed: `6a2d9185e5a40a29b74c7264`.
- Direct OOS backtests:
  - Fold 0 `6a2d91c1e5a40a29b74c72ef`: -2.8168%, Sortino -0.4657, maxDD 8.5536%, breadth 10/20.
  - Fold 1 `6a2d91c4e5a40a29b74c7309`: +19.9556%, Sortino 2.7920, maxDD 7.7573%, breadth 8/20.
  - Fold 2 `6a2d91c808bb1349f5b64c03`: +21.3020%, Sortino 1.1951, maxDD 23.2315%, breadth 12/20.
  - Fold 3 `6a2d91cb08bb1349f5b64c13`: +12.8681%, Sortino 0.8488, maxDD 13.4804%, breadth 7/20.
- Fold 0 posture audit on `6a2d91c1e5a40a29b74c72ef`: median deployment 15.52%, p90 28.10%, zero days >70%; no posture violation. Binding failure is not overdeployment.
- Fold 0 breadth audit: distinct names filled 10/20, top1 16.17%, top5 69.71%; `namesWithRejectionsAndZeroFills` = ANET, AVGO, DUOL, GS, NET, OKTA, OSCR. Gate 1 also fails by top-5 concentration.

### Certification attempt 2C completed details

- Study `6a2d935fdaff5c67a9716f58` completed 976/976 units.
- Per-fold selected winners:
  - F0 selected key `d82281897f27f74802ae434eb0ef047d3208cd9d476eea6ada8c2694127d0ab1`; OOS -7.2186%, Sortino -0.4580, maxDD 21.9575%, breadth 17/20.
  - F1 selected key `1628e1669c746ea7d179f1f4cf6cedf4f172c5fe92e606149da71e4708e347c1`; OOS +37.3796%, Sortino 1.8636, maxDD 24.9721%, breadth 15/20.
  - F2 selected key `773475bbf2fa49cf06be740ce680557d4239ec71670d3ae0fbfde6a27ed6cb94`; OOS +18.2873%, Sortino 0.9428, maxDD 28.7099%, breadth 15/20.
  - F3 selected key `773475bbf2fa49cf06be740ce680557d4239ec71670d3ae0fbfde6a27ed6cb94`; OOS +108.6141%, Sortino 3.1972, maxDD 15.1675%, breadth 15/20.
- Aggregate selected-winner OOS: mean return +39.2656%, min -7.2186%; mean Sortino 1.3864, min -0.4580; `winnerStableAcrossFolds=false`.
- `aggregate.crossFoldRobustSelection`: candidateKey `1628e1669c746ea7d179f1f4cf6cedf4f172c5fe92e606149da71e4708e347c1`, minSortino score `-0.12637701554518196`, perFoldSortino `[-0.12637701554518196, 1.5491004411171014, 1.946528235467545, 1.886589130140055]`, perFoldPercentChange `[-3.3826749927479103, 35.12109497342335, 81.44463400349959, 131.3721740229707]`.
- Robust materialization inspected at `6a2d94c2daff5c67a97171e5`: top 8 ROC126, 8% of buying power per name, 90-180 DTE, +75% take-profit.
- Assembled deploy-shape book from clean seed: `6a2d958b08bb1349f5b6534d`.
- Direct OOS assembled-book backtests:
  - F0 `6a2d959208bb1349f5b65360`: +0.3250%, Sortino 0.0247, maxDD 23.5642%, breadth 14/20.
  - F1 `6a2d959bdaff5c67a9717318`: +39.2699%, Sortino 1.9558, maxDD 24.5062%, breadth 15/20.
  - F2 `6a2d95a2e5a40a29b74c78f7`: +14.0102%, Sortino 0.8152, maxDD 29.6484%, breadth 16/20.
  - F3 `6a2d95aadaff5c67a9717339`: +75.7713%, Sortino 2.9597, maxDD 20.8137%, breadth 14/20.
- Kill reason: Gate 4 vs Baseline C is the binding gate. F0/F2/F3 all fail C return and Sortino; F0/F2 also fail the absolute Sortino floor (<0.9).

### Certification attempt 5 completed details

- Seed `6a2d940fdaff5c67a97170b5`: incumbent-style calm sleeve only; opportunity sleeve removed, so the book is long/flat outside calm regime.
- Study `6a2d9437e5a40a29b74c76e0` completed 976/976 units.
- Selected-winner OOS per fold: `[+4.6243%, +23.9962%, -0.1130%, +19.7536%]`.
- Selected-winner Sortino per fold: `[0.2792, 1.4234, -0.0591, 1.0035]`.
- Aggregate selected-winner OOS: mean return +12.0653%, min -0.1130%; mean Sortino 0.6617, min -0.0591.
- `aggregate.crossFoldRobustSelection`: candidateKey `0fba895dd44c9903b62511055b13ae1b74c73c52ba945a2e09878a2a01b9b5f1`, minSortino score `-0.5833794684549402`, perFoldPercentChange `[-5.093307625879316, 9.432164682324888, 66.06401270523217, 52.91846747255144]`.
- Kill reason: Gate 3 robust selection is weak/negative; Gate 4 vs Baseline C also fails decisively. No direct assembly because the cross-fold robust pick itself has negative min Sortino and therefore is not an acceptable robust parameterization.

### Credit-family exhaustion

- Attempt 1 `6a2d90e8e5a40a29b74c7137`: put credit spreads; fold 0 failed certification floors after 324 units.
- Attempt 2 `6a2d92ed08bb1349f5b64e0e`: regime put credit spreads; fold 0 failed certification floors after 243 units.
- Attempt 3 `6a2d962ce5a40a29b74c79fa`: mixed regime credit (calm put credit, opportunity call credit); fold 0 failed certification floors after 243 units.
- Binding constraint for the credit family: certification fold-winner selection floors, specifically no candidate simultaneously met participation >= 0.35, distinct underlyings >= 9, validation return >= 0, and validation Sortino >= 0.5 on the first fold's validation window.

### Calendar-family exhaustion

- Attempt 1 `6a2d909adaff5c67a9716930`: call diagonals/calendars; fold 0 failed certification floors after 324 units.
- Attempt 2 `6a2d923908bb1349f5b64cc4`: regime diagonals/calendars; fold 0 failed certification floors after 243 units.
- Attempt 3 `6a2d97a008bb1349f5b656fa`: light diagonal far-OTM short-call overlay; completed but failed WF gates.
- Attempt 3 selected-winner OOS returns: `[+0.3462%, +10.2153%, -13.2905%, +23.5598%]`.
- Attempt 3 selected-winner OOS Sortino: `[-0.1160, 0.6397, -0.8875, 1.7758]`.
- Attempt 3 aggregate selected-winner OOS: mean return +5.2077%, min -13.2905%; mean Sortino 0.3530, min -0.8875.
- Attempt 3 `aggregate.crossFoldRobustSelection`: candidateKey `dc95ecc9e565cb026d937e939acdcb7ffd793c3c324d1850e838273ef2a05dfb`, minSortino score `0.21388450813259405`, perFoldPercentChange `[2.0083167400310047, 33.76065904865885, 7.343660262711245, 35.097925561375625]`.
- Binding constraint for the calendar family: Gate 3 robust selection weak plus Gate 4 vs Baseline C.

## Final WF Verdict

- Execution mandate satisfied:
  - S0 engine sanity PASS.
  - Baseline A/B built from committed snapshots and scored on the current engine.
  - Baseline B posture-matched substitution fired and was logged.
  - Baseline C frozen bar copied and used as the incumbent gate.
  - Mandatory `systematic_sweep` completed: `6a2d8f0508bb1349f5b64577`.
  - Incumbent/example seed certified: `6a2d8f3b08bb1349f5b6460a`.
  - Distinct certified mechanisms: regime-switched momentum, broad single-sleeve momentum calls/verticals, regime long/flat momentum, light diagonal/calendar.
  - Additional exhausted mechanisms: defined-credit / mixed regime credit.
- No finalist passed walk-forward gates.
- Lockbox was NOT touched. No `backtest_portfolio` call was run on `2026-02-07` -> `2026-06-13`.
- No deploy target was discovered and no live deployment was attempted, because deploy preconditions were not met.

### Binding constraints by family

- Regime-switched momentum / incumbent seed: Gate 4 vs Baseline C; direct assembled book failed C return and Sortino in every fold.
- Broad single-sleeve momentum calls/verticals: Gate 4 vs Baseline C; direct assembled book failed C return and Sortino in F0/F2/F3 and failed absolute Sortino in F0/F2.
- Regime long/flat momentum: Gate 3 robust selection weak/negative and Gate 4 vs Baseline C.
- Calendar / diagonal time-spreads: Gate 3 robust selection weak and Gate 4 vs Baseline C.
- Defined-credit / mixed credit: certification floors; no fold-0 validation candidate passed quality floors in any of 3 attempts.

### Final decision

NO DEPLOY. The run produced no deployable finalist, and the lockbox remains pristine for a future campaign.
