# August 24, 2026 addendum: Public cash-account conversion to single-leg calls

## Decision

The two newer Public Portfolio Challenge accounts cannot rely on multi-leg option spreads. Public permits only one margin account, and that is not either of these books. Repeated live rejections returned `Option level required.`

The live Biotech and Semis books were therefore rebuilt as calls-only strategies at their actual account values, re-tested, and then updated in place. MRNA remains in the Biotech universe and was not removed or diluted out of the thesis.

No holdings were changed as part of this addendum. Existing orders were deliberately excluded from the research decision. NexusTrade warned that replacing live strategies could cancel system orders; the owner explicitly authorized the replacement with that side effect.

## Live state after replacement

### Public Portfolio Challenge: Biotech

- Live portfolio: `6a5e20a3ea0d6db55c69a171`
- Public account: `5OH86568`
- New entry strategy: `6a8c625b01471d61b00612c3`
- Entry structure: four fallback templates, each exactly one long call; no short legs and no `spreadType`
- Selector: 0.50 delta
- Expiration: 365-730 DTE
- Sizing: 6% per name, 75% total budget
- Universe: MRNA, MRK, BNTX, RXRX, SDGR, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, A, BMY
- Existing exits preserved: +80% P/L and DTE <= 90
- Deployment: active Public live trading, `Constant` evaluation
- Automated approval: false

MRNA is still the first name in the universe. At $5,500.09, a single long-dated MRNA contract was not affordable during the latest event window: 94 resolution attempts produced 50 affordability rejections and 44 Greek/liquidity-filter rejections. That is a capital-granularity fact, not a thesis removal. The owner explicitly said immediate MRNA affordability was preferred, not mandatory.

### Public Portfolio Challenge: Semis

- Live portfolio: `6a45f218e6b1f2131d1f26be`
- Public account: `5OH79160`
- New long-duration entry: `6a8c625d01471d61b00612f4`
- New 90-180 DTE entry: `6a8c625d01471d61b0061320`
- Entry structures: three total fallback templates, each exactly one long call; no short legs and no `spreadType`
- Strike: 20% OTM
- Expirations: 365-730 DTE and 90-180 DTE
- Selection: top four of NVDA, TSM, AVGO, AMAT, LRCX, ANET, MRVL
- Sizing: 12% per name for the long-duration sleeve and 15% for the 90-180 DTE sleeve
- Take-profit changed from +300% to +100%
- Existing DTE and per-ticker trend exits preserved
- Deployment: active Public live trading, `Constant` evaluation
- Automated approval: false

## Research record

All walk-forward studies used Day data from January 3, 2022 through August 21, 2026, five anchored folds, a 70% training window, a 15% validation window, and a five-day embargo. The executable account values were $5,500.09 for Biotech and $8,000 for Semis.

### Biotech

The exact calls-only control, study `6a8c5c0f5f6ea2ed29ff4238`, returned:

| Fold | OOS return |
| ---: | ---: |
| 1 | +5.09% |
| 2 | +12.67% |
| 3 | -2.52% |
| 4 | -5.34% |
| 5 | +66.48% |

Mean return was +15.27%, median +5.09%, three of five folds were positive, and worst drawdown was 15.55%.

A bounded allocation/delta sweep selected a 10% per-name, 0.45-delta candidate. Fresh fixed-book certification `6a8c5ee601471d61b005fa4e` showed a misleading +64.78% mean driven by a +317.49% fifth fold, only a +4.79% median, three positive folds, and 31.47% worst drawdown. That tuned candidate was rejected as unstable. The simpler 6%/0.50-delta control was deployed.

Recent event rerun `6a8c5f42f68259010d8e93b8` returned +66.48% with 6.04% max drawdown and filled six of 17 names. More than half of option pricings used synthetic rather than observed NBBO spreads, so its fill-quality and trading-cost estimates are modelled, not live-execution proof.

### Semis

The exact calls-only control, study `6a8c5c1f8be832eb562f0409`, had five positive folds, +42.68% mean return, +38.86% median return, and 50.53% worst drawdown.

The bounded take-profit/selection sweep chose top four and a +100% take-profit. Fresh fixed-book certification `6a8c5eee01471d61b005fa74` returned:

| Fold | OOS return |
| ---: | ---: |
| 1 | +15.38% |
| 2 | +81.79% |
| 3 | +37.62% |
| 4 | +129.65% |
| 5 | -1.74% |

Mean return was +52.54%, median +37.62%, four of five folds were positive, median Sortino was 2.18, and worst drawdown fell to 29.82%.

A second nine-cell strike-distance sweep, `6a8c60138be832eb562f27c8`, tested 20%, 30%, and 40% OTM independently for both entry sleeves. The 20%/20% configuration remained the validation winner at +38.69%, Sortino 2.29, 16.36% max drawdown, and five of seven names. Moving the active sleeve to 30% OTM reached seven of seven names but reduced return to +27.85%, Sortino to 1.59, and increased drawdown to 26.06%, so the added breadth was rejected.

The latest event window, backtest `6a8c5f3ef68259010d8e93b4`, was the weak fifth fold: -1.74%, 17.97% max drawdown, and fills in three of seven names. That weak window is included rather than hidden.

## Why the options-level failure was not visible

The live event carried `rejectionCode: Other` and the message `Option level required.` The classifier recognized `options level` plural but not Public's singular `option level`, so the durable account-capability failure was treated as a generic transient rejection and excluded from notable events.

NexusTrade commit [`dff1e2a120`](https://github.com/austin-starks/NexusTrade/commit/dff1e2a120) fixes the broker classifier and adds a defensive message fallback. It promotes this response to `OptionsLevelTooLow`, emits a warning-level notable event, records the attempted leg count, and explains when the account cannot place the multi-leg spread required by the strategy. Rust and server hydration tests passed. The commit was pushed separately from the live portfolio mutation; deployment status must be verified independently.

## Verdict

The calls-only books are not expected to reproduce the spread books' payoff shape. The conversion removes an account-ineligible structure while retaining the named theses and producing executable single-leg orders.

- Biotech: deploy the conservative calls-only control; reject the sweep winner.
- Semis: deploy the tuned top-four/+100% take-profit calls-only book.
- Keep both on Constant evaluation.
- Keep automated approval off.
- Treat modeled option fills and thin affordable-name participation as explicit limitations.
