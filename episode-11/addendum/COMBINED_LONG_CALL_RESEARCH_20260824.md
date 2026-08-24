# Episode 11 addendum: combined long-call book research

**Date:** August 24, 2026
**Scope:** Public Portfolio Challenge: Biotech and Public Portfolio Challenge: Semis

> **Continuation status:** The first three-sleeve finalist still failed its one valid lockbox and remains rejected. Research continued only as diagnosis and candidate development. The current result is an inactive forward-test candidate, not a newly certified or deployed book.

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

## Post-lockbox continuation: execution-aware two-sleeve candidate

The failed fill was not treated as permission to erase the lockbox. Instead, the next branch made two structural changes:

1. every entry contract must have a bid of at least $0.05 and a bid-ask spread no wider than 10%; and
2. the pullback sleeve was removed, leaving one MRNA core and one independently spaced semi momentum sleeve.

The frozen forward candidate is chat portfolio `6a8cb278c57fd738a24f0409` with **$13,500.09** modeled capital:

- **MRNA core:** 25% allocation, 5% OTM long call, 45-90 DTE, 10% maximum spread, MRNA above its 100-day SMA with positive 63-day rate of change, 42-day `DaysSinceStrategyFired` cooldown.
- **Semi momentum:** 20% total budget, top one of NVDA, ANET, KLAC, TSM, MRVL, and LRCX by 126-day rate of change, 10% OTM long call, 45-90 DTE, 10% maximum spread, 42-day `DaysSinceStrategyFired` cooldown, `positionScope: strategy`.
- **Exits:** close at 21 DTE, take profit at 150%, and retain the MRNA trend exit.
- **Execution:** single-leg long calls only; automatic order approval false.

### Fixed-book stability evidence

The 81-cell allocation/liquidity sweep was `6a8cac0a73626b1004828728`. Its strongest region clustered around 25% MRNA, 20% semis, and a 10% spread cap rather than one isolated cell. Because that sweep used the historical search span, the following fixed-book studies are **stability diagnostics, not a fresh lockbox**:

| Study | OOS folds | Mean | Median | Positive folds | Worst drawdown |
| --- | --- | ---: | ---: | ---: | ---: |
| Five 240-day folds `6a8cad9ec57fd738a24ed742` | 108.20%, 112.73%, 76.59%, 3.76%, 46.77% | 69.61% | 76.59% | 5/5 | 67.05% |
| Seven 180-day rolling folds `6a8cada5c57fd738a24ed7a4` | 2.62%, 16.29%, 45.01%, 94.72%, -47.27%, 85.78%, 62.64% | 37.11% | 45.01% | 6/7 | 57.78% |

On the already-observed April 20-August 24 window, the exact candidate returned **+88.77%** with **38.46%** maximum drawdown at $13,500.09. That is diagnostic stress evidence only. The fills were economically plausible after the liquidity filter: the disastrous MRVL $24.41-to-$42.525 entry disappeared, while the candidate's submitted and filled prices remained close enough to represent tradable option markets.

Capital sensitivity on that same observed window was -6.36% at $10,000, +27.83% at $12,000, +88.77% at $13,500.09, +101.70% at $15,000, and +81.80% at $17,500. The strategy therefore has a real whole-contract capital floor. It should not be deployed into either existing cash account by itself.

### Rejected continuation branches

- Shortening MRNA to ATM 30-60 DTE improved the ranked historical tail but returned -10.15% on the observed Moderna window.
- A 21-day semi cadence produced four losing folds in the seven-fold rolling study.
- Combining both changes lost roughly 49-53% across every tested account size from $10,000 to $17,500.
- Positive-momentum and above-100-day-SMA semi filters did not remove the bad regime and weakened the broader fold record.
- Universal and semi-only option stop losses reduced one losing regime but destroyed too much of the MRNA event payoff. They were rejected because MRNA is the thesis, not a sleeve to be silently capped.
- A 63-day semi cooldown reduced the known bad regime but cut the five-fold mean from 69.61% to 28.99% and the observed Moderna-window result to 20.67%.

The remaining bad rolling fold was a real strategy loss, not a rejected-order or impossible-fill artifact. ANET was the largest loser, with additional losses in MRNA and LRCX. That loss is part of the book's honest high-risk profile.

## Optimizer defect found during the campaign

The cooldown sweep exposed a separate implementation bug. When a strategy's entire condition was a standalone `DaysSinceStrategyFired >= 21` rule, the `EntryCooldownDays` sweep wrapped it and appended a second `>= 42` rule instead of replacing it. The malformed candidates therefore had `21 days AND 42 days` while reporting only the new resolved parameter.

NexusTrade commit `b0dccadba5` replaces the standalone cooldown directly and adds a regression test for this exact condition shape. The targeted cooldown tests passed 5/5, and the fix was deployed across the backtesting, optimizer, and live-trading Rust services. The manually authored finalist had one clean 42-day cooldown per sleeve, so this tooling bug does not rescue its failed lockbox.

## Final live state and next gate

- Biotech portfolio `6a5e20a3ea0d6db55c69a171`: prior entry strategy `6a8c7b7501471d61b006b171` removed; exits retained; no positions or pending orders at the verification snapshot.
- Semis portfolio `6a45f218e6b1f2131d1f26be`: prior entry strategy `6a8c70598be832eb562f9ec5` removed; exits retained; no positions or pending orders at the verification snapshot.
- Original margin-account portfolio: untouched.
- Combined forward candidate: chat portfolio `6a8cb278c57fd738a24f0409`, preserved inactive with manual approval and the exact two-sleeve specification above.
- Deployment: none. A failed lockbox is a hard rejection even when the pre-lockbox walk-forward is exceptional.

Because the April-August period has now been observed repeatedly, it cannot be reused as an untouched lockbox or relabeled as certification. The candidate is ready for a genuinely unseen forward window, but not live deployment. Before any eventual deployment, the owner must also consolidate the desired cash into one Public account; NexusTrade cannot combine buying power across brokerage accounts.
