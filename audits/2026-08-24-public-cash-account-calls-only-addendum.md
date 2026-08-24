# August 24, 2026 addendum: cash-account conversion test and spread-book restoration

## Final decision

The temporary calls-only conversion described below was reversed the same day. The owner clarified that the objective is maximum repeatable real-dollar return, not lower drawdown or higher Sortino. Both live books were restored to their higher-return debit-spread configurations after explicit authorization to replace active strategies even if the operation cancelled system orders.

Public's earlier `Option level required.` response was an account-state bug that the owner fixed. No escalation email to Public is pending. NexusTrade still needed a notable alert for that rejection, because the platform had classified Public's singular `Option level` message as generic `Other`.

## Verified final live state

### Public Portfolio Challenge: Biotech

- Portfolio: `6a5e20a3ea0d6db55c69a171`
- Public account: `5OH86568`
- Restored entry strategy: `6a8c70578be832eb562f9e7e`
- Structure ladder: 16 templates, including four single long-call fallbacks and 12 vertical debit-spread templates
- Selector: 0.50-delta long calls with the original spread ladder
- Expiration: 365-730 DTE
- Sizing: 6% per name, 75% total budget
- Universe: MRNA, MRK, BNTX, RXRX, SDGR, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, A, BMY
- Exits preserved: +80% P/L and DTE <= 90
- Deployment: active Public live trading, `Constant`
- Automated approval: false

### Public Portfolio Challenge: Semis

- Portfolio: `6a45f218e6b1f2131d1f26be`
- Public account: `5OH79160`
- Restored long-duration vertical: `6a8c70588be832eb562f9ea9`
- Restored 90-180 DTE vertical: `6a8c70598be832eb562f9ec5`
- Restored take-profit: `6a8c705a8be832eb562f9ee1`
- Structures: 20% OTM long calls paired with 25% OTM short calls
- Expirations: 365-730 DTE and 90-180 DTE
- Selection: top seven of NVDA, TSM, AVGO, AMAT, LRCX, ANET, MRVL
- Sizing: 12% per name for the long-duration sleeve and 15% for the 90-180 DTE sleeve
- Take-profit restored from the temporary +100% setting to +300%
- Existing DTE and per-ticker trend exits preserved
- Deployment: active Public live trading, `Constant`
- Automated approval: false

## Why the calls-only replacements were rejected

All comparisons used the same five anchored walk-forward folds and each live book's actual capital.

| Book | Spread version | Calls-only version | Decision |
| --- | --- | --- | --- |
| Biotech | +41.18% mean OOS, +33.69% median, 4/5 positive, 19.45% worst drawdown | +15.27% mean, +5.09% median, 3/5 positive, 15.55% worst drawdown | Restore spreads. The calls-only book was materially weaker. |
| Semis | +67.69% mean OOS, +85.97% median, 5/5 positive, 33.73% worst drawdown | +52.54% mean, +37.62% median, 4/5 positive, 29.82% worst drawdown | Restore spreads. Lower drawdown did not compensate for lower return and consistency under the owner's objective. |

The temporary tuned Biotech calls-only candidate reported +64.78% mean OOS, but its folds were +4.79%, +36.22%, -15.55%, -19.06%, and +317.49%. Removing its best fold left a +1.60% average across the other four. It was rejected as a right-tail lottery ticket rather than a demonstrated repeatable edge.

## Why orders were not firing during the audit

The live engines were running and VIX passed at approximately 16.

- Biotech's entry condition read `0 >= 7 days`.
- Semis read `38 >= 63 days`.

The current `DaysSinceLastRebalanceOptionOrder` implementation uses an order's creation time when it is not filled, so rejected RebalanceOption attempts can reset the shared portfolio cooldown. The temporary Biotech strategy therefore emitted `NoSignal` after the earlier rejection batch even though no option position had opened. This requires a separate filled-only cooldown design or a narrowly scoped semantic fix; it is not evidence that the Constant deployment stopped evaluating.

## Notable-event fix

NexusTrade commit [`dff1e2a120`](https://github.com/austin-starks/NexusTrade/commit/dff1e2a120) recognizes both `options level` and Public's singular `option level`, defensively promotes a generic rejection to `OptionsLevelTooLow`, records leg count, and produces a warning-level notable event with an explicit multi-leg explanation. Rust and server hydration tests passed. Application deployment remains separate from source publication.

## Research direction

The live spread books are the incumbents. Future candidates must target the owner's actual utility:

1. Primary objective: real-dollar and percentage return at the executable account value.
2. Legitimacy: repeatability across folds and a materially positive median, not a mean dominated by one fold.
3. Risk metrics: reporting and catastrophic-failure guards, not the optimization target.
4. Deployment: replace an incumbent only after a fixed-book walk-forward and event-level contract/fill audit beat it on the return objective.
