# Corrected diagnosis: DynamicRebalance wrong-field validation trap

**Observed and corrected 2026-07-18. Engine defect claim withdrawn.**

The campaign originally supplied `action.totalBudget` to `DynamicRebalance`. That field belongs to `RebalanceOption`, not `DynamicRebalance`. The correct DynamicRebalance book-level exposure field is `deploymentPercent` (legacy alias `maxAllocationPercent`). When absent, the engine correctly defaults to 100% deployment.

## Why the mistaken runs matched

- 90-labelled portfolio: `6a5bc36dbdc6c18b552b3e50`
- 95-labelled portfolio: `6a5bc40eae60bca443567c37`
- backtests: `6a5bc3bc0a9bbbb42abdd488`, `6a5bc419bdc6c18b552b3ef6`

Both stored the irrelevant `totalBudget` key and omitted `deploymentPercent`, so both correctly executed at the default 100% deployment and produced identical results.

## Remaining MCP/tooling issue

`build_portfolio` reported both malformed DynamicRebalance actions as valid and preserved the unsupported `totalBudget` key. Because action objects accept additional properties, the wrong field survived and looked operative even though the runtime ignored it. Validation should either reject `totalBudget` on DynamicRebalance or emit a warning that the field is unsupported and deployment will default to 100%.

## Campaign impact

The prior engine-bug diagnosis is retracted. The mislabeled S1-S4 evidence is quarantined only because it did not test the intended cash reserve. Corrected variants must use `deploymentPercent: 90` and `deploymentPercent: 95` and be rerun.

