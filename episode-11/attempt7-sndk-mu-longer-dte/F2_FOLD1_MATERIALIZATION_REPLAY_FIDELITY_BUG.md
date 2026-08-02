# F2 fold-1 materialization replay fidelity bug

Status: **OPEN — study statistic is quarantined**

## Symptom

Fresh qualifying study `6a5dd72aea0d6db55c694eeb` reports fold-1 OOS return −13.210625%,
max drawdown 27.575738%, dollars sold $15,307.50, fees $15.60, and 96 null-gated evaluations
over `2026-05-12T04:00:00Z` through `2026-06-01T03:59:59.999Z`. Its persisted selected
ChatPortfolio is `6a5dd9762ee25ecab46bbca3`.

Exact standalone replay of that materialized winner over May 12–31 produced −11.257500%, max
drawdown 25.856929%, dollars sold $14,950.00, fees $15.60, and 120 null-gated evaluations in
event-enabled backtest `6a5de246ea0d6db55c696248`. The event trace contains 12 completed
round trips and no unmatched fill.

The first fold was separately replayed with the correct exclusive-end translation and matched its
study return exactly (−11.328750%), while folds 2 and 3 also match exactly because their displayed
end dates fall on weekends. This isolates the discrepancy to fold 1 rather than to event generation
or the general standalone date boundary.

## Impact

The fold-1 study statistic cannot certify the materialized strategy object. The study remains useful
as search evidence, but the divergent fold is quarantined for promotion decisions. Attribution and
future refinement use the fresh materialized replay, not the stale study economics.

## Required platform investigation

Compare the selected individual's exact strategy ordering and resolved actions with the persisted
ChatPortfolio, then compare the minute-by-minute global `Open option position count < 1` arbitration
path. The equal fee count but different dollars sold is consistent with a different same-minute
winner/contract path rather than a fee-contract error.
