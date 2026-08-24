# Episode 11 addendum: combined long-call book research

**Date:** August 24, 2026
**Scope:** Public Portfolio Challenge: Biotech and Public Portfolio Challenge: Semis

## Why this campaign changed

Public permits debit spreads only in the user's single margin account. These two newer Public accounts are cash accounts, so a strategy that depends on debit spreads cannot execute there even when the individual symbol supports spread trading.

The two existing entry strategies were removed and their new pending orders were canceled before this research began. Existing exit strategies were preserved. The original margin-account Public Portfolio Challenge book was not changed. Automatic order approval remains off.

At the campaign snapshot, Biotech had **$5,500.09** of cash and buying power and Semis had **$8,000.00**, for **$13,500.09** of combined research capital. That total is a model assumption, not money that NexusTrade can move between two brokerage accounts. A real combined deployment requires the owner to consolidate cash in one chosen Public account first.

## Research mandate

The replacement had to:

- use single-leg long calls only, never debit spreads;
- keep every entry at 90 DTE or less;
- preserve MRNA as the explicit core bet;
- allow several independently spaced entry sleeves in one portfolio;
- use `positionScope: strategy` and `DaysSinceStrategyFired` for the RebalanceOption sleeves;
- keep manual order approval; and
- beat a real walk-forward and a frozen lockbox before deployment.

The researched semi universe was **NVDA, ANET, KLAC, TSM, MRVL, and LRCX**. The broader screen also reviewed AVGO, AMD, MU, VRT, and AMAT, but whole-contract affordability at $13,500.09 constrained the executable universe. Biotech work treated MRNA as the direct thesis exposure, MRK as the strongest adjacent exposure, BNTX as a competitor, ILMN as broad sequencing infrastructure, TEM as a higher-risk platform name, and PSNL as an announced-acquisition situation rather than an ordinary long-call candidate.

## Mechanism families tested

Search ended on April 19, 2026. The period from April 20 through August 24 was frozen before candidate selection.

| Family | Walk-forward study | OOS folds | Mean | Median | Positive folds | Worst drawdown |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Momentum | `6a8c9ba2eb9ac3dc8af06efb` | -73.23%, 32.65%, -39.47%, -9.03%, -0.37% | -17.89% | -9.03% | 1/5 | 87.04% |
| Pullback | `6a8c9ba9eb947512c1fa564a` | 103.29%, 19.41%, 27.87%, -6.45%, 68.36% | 42.50% | 27.87% | 4/5 | 62.92% |
| Tuned pullback | `6a8c9cea92a28d61ec55c25a` | 151.67%, -32.67%, 29.88%, 88.75%, 28.69% | 53.26% | 29.88% | 4/5 | 66.92% |
| Concentrated breakout | campaign record | campaign record | -28.86% | -37.34% | 1/5 | 83.05% |
| Fixed trend | campaign record | campaign record | 35.83% | 26.74% | 3/5 | 61.49% |
| Regime ensemble | campaign record | campaign record | 39.13% | 13.82% | 4/5 | 60.82% |
| Concurrent MRNA, momentum, and pullback finalist | `6a8c9e67d7d8ff987f31782e` | 152.16%, 354.57%, -8.84%, 66.19%, 100.69% | 132.95% | 100.69% | 4/5 | 72.50% |

The finalist used three independent entry sleeves:

1. **MRNA core:** 35% allocation, 5% OTM long call, 45-90 DTE, MRNA above its 100-day SMA with positive 63-day rate of change, 42-day strategy cooldown.
2. **Semi momentum:** 30% allocation, top one name by 126-day rate of change, 10% OTM long call, 45-90 DTE, 42-day strategy cooldown.
3. **Semi pullback:** 30% allocation, bottom one name by 21-day rate of change, ATM long call, 45-90 DTE, 42-day strategy cooldown.

It closed at 21 DTE, took profit at 150%, and retained the MRNA trend exit. Capital sensitivity across $10,000, $12,000, $13,500.09, $15,000, and $17,500 remained positive in the pre-lockbox period, but the results were not monotonic because option contracts are indivisible.

## Frozen lockbox result: rejected

The finalist was touched once on the frozen April 20 through August 24, 2026 window. Event backtest `6a8c9f42f68259010d8eb487` returned:

- **-44.15%** return;
- **82.44%** maximum drawdown;
- six closed trades across four names; and
- no order-rejection warning that explains away the loss.

This is a failed lockbox. The combined book was **not deployed**.

### What failed

MRNA was not the problem in this window. Its first two entries lost about $1,986 and $1,500, but the August readout trade gained about $4,227, leaving MRNA approximately **+$741 before fees**.

The largest loss was the momentum sleeve's MRVL trade. On June 2, the resolver selected an August 21 320 call after MRVL showed roughly +250.65% 126-day momentum. The expected entry was about $25.20 per contract and fit the sleeve's budget, but the backtest market fill was $42.525. One contract therefore cost about **$4,252.50**, roughly 55% above the intended $2,747 sleeve allocation, and later exited near $4.49 for a loss of about **$3,804**.

The deeper failure was portfolio path dependence. On the already-burned window, MRNA alone returned +36.66%, MRNA plus momentum returned +80.12%, and MRNA plus pullback returned +17.09%, yet all three together returned -44.15%. Those decompositions are diagnostics, not new certification. Shared cash, whole-contract sizing, resolver prices, and the order in which sleeves consume buying power made the combined portfolio non-additive.

## Optimizer defect found during the campaign

The cooldown sweep exposed a separate implementation bug. When a strategy's entire condition was a standalone `DaysSinceStrategyFired >= 21` rule, the `EntryCooldownDays` sweep wrapped it and appended a second `>= 42` rule instead of replacing it. The malformed candidates therefore had `21 days AND 42 days` while reporting only the new resolved parameter.

NexusTrade commit `b0dccadba5` replaces the standalone cooldown directly and adds a regression test for this exact condition shape. The targeted cooldown tests passed 5/5, and the fix was deployed across the backtesting, optimizer, and live-trading Rust services. The manually authored finalist had one clean 42-day cooldown per sleeve, so this tooling bug does not rescue its failed lockbox.

## Final live state and next gate

- Biotech portfolio `6a5e20a3ea0d6db55c69a171`: prior entry strategy `6a8c7b7501471d61b006b171` removed; exits retained; no positions or pending orders at the verification snapshot.
- Semis portfolio `6a45f218e6b1f2131d1f26be`: prior entry strategy `6a8c70598be832eb562f9ec5` removed; exits retained; no positions or pending orders at the verification snapshot.
- Original margin-account portfolio: untouched.
- Combined research portfolio: preserved as an inactive chat portfolio only.
- Deployment: none. A failed lockbox is a hard rejection even when the pre-lockbox walk-forward is exceptional.

Because the April-August period has now been observed, it cannot be reused as an untouched lockbox. A future replacement needs a new point-in-time campaign and a genuinely unseen forward window. Before any eventual live deployment, the owner must also consolidate the desired cash into one Public account; NexusTrade cannot combine buying power across brokerage accounts.
