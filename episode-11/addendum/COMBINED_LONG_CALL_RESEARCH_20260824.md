# Episode 11 addendum: combined long-call book research

**Date:** August 24, 2026
**Scope:** Public Portfolio Challenge: Biotech and Public Portfolio Challenge: Semis

> **Continuation status:** The first three-sleeve finalist still failed its one valid lockbox and remains rejected. A later MRNA-plus-semis draft was also rejected because it deleted the rest of the biotech thesis. The current result is an inactive, biotech-inclusive owner-review candidate, not a newly certified or deployed book. The only untouched proof available now is future live or forward data.

## Why this campaign changed

Public permits debit spreads only in the user's single margin account. These two newer Public accounts are cash accounts, so a strategy that depends on debit spreads cannot execute there even when the individual symbol supports spread trading.

The two existing entry strategies were removed and their new pending orders were canceled before this research began. Existing exit strategies were preserved. The original margin-account Public Portfolio Challenge book was not changed. Automatic order approval remains off.

At the campaign snapshot, Biotech had **$5,500.09** of cash and buying power and Semis had **$8,000.00**, for **$13,500.09** of combined research capital. That total is a model assumption, not money that NexusTrade can move between two brokerage accounts. A real combined deployment requires the owner to consolidate cash in one chosen Public account first.

## Research mandate

The replacement had to:

- use single-leg long calls only, never debit spreads;
- keep MRNA and semiconductor entries at 90 DTE or less, while allowing only outright long calls for longer-dated biotech exposure;
- preserve MRNA as the explicit core bet;
- allow several independently spaced entry sleeves in one portfolio;
- use `positionScope: strategy` and `DaysSinceStrategyFired` for the RebalanceOption sleeves;
- keep manual order approval; and
- beat a real walk-forward and a frozen lockbox before deployment.

The researched semi universe was **NVDA, ANET, KLAC, TSM, MRVL, and LRCX**. The broader screen also reviewed AVGO, AMD, MU, VRT, and AMAT, but whole-contract affordability at $13,500.09 constrained the executable universe. The frozen biotech chain was **MRK, BNTX, RXRX, SDGR, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, A, and BMY**, with MRNA held outside that sleeve as the direct concentrated bet. TEM and a no-RXRX universe were tested later as prospective quality changes. PSNL remained excluded as an announced-acquisition situation rather than an ordinary long-call candidate.

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

## Superseded owner-review draft: MRNA plus capital-gated semi momentum

The former review object is chat portfolio `6a8cbdfd89dc23e08ed9e2d4`, named **FINAL REVIEW — MRNA + Capital-Gated Semi Momentum**. It is an exact semantic clone of the tested two-sleeve source; backtests `6a8cbcaaf68259010d8ec5a4` and `6a8cbe05f68259010d8ec613` matched at zero-basis-point tolerance with no tape divergence. It is preserved as research history but rejected as the final book because it omitted the broader biotech thesis.

The deploy-shape rules are:

1. **MRNA core:** 25% of portfolio, one 5% OTM call, 45-90 DTE, bid at least $0.05, maximum 10% bid-ask spread, no existing MRNA long call, 21-day `DaysSinceStrategyFired` spacing, MRNA above its 100-day SMA, and positive 63-day rate of change.
2. **Semi momentum:** rank NVDA, ANET, KLAC, TSM, MRVL, and LRCX by 126-day rate of change; attempt only the top name; buy one 10% OTM call at 45-90 DTE subject to the same liquidity limits; cap the sleeve at 20% of portfolio; use `positionScope: strategy`; and space attempts by 42 days.
3. **Capital gate:** there is no fallback to the second-ranked semi. If the top-ranked contract is not liquid or affordable inside the sleeve budget, the resolver skips the entry. This is deliberate and is now named explicitly.
4. **Exits:** close at 21 DTE, take profit at 150%, and close MRNA when both its price is below the 100-day SMA and its 63-day rate of change is negative.
5. **Structure:** every entry is a single-leg long call at no more than 90 DTE. There are no debit spreads, short legs, or long-dated calls.

### Fixed-book walk-forward result

These studies end before the original April 20 lockbox boundary. They are fixed-book stability evidence, but they are not a replacement lockbox because this branch was developed after the original lockbox had been observed.

| Study | OOS folds | Mean | Median | Positive folds | Worst drawdown |
| --- | --- | ---: | ---: | ---: | ---: |
| Five-fold anchored `6a8cbc0889dc23e08ed9c5e2` | 76.73%, 83.59%, 0.85%, 40.30%, 108.22% | **61.94%** | **76.73%** | **5/5** | 59.55% |
| Seven-fold rolling `6a8cbc4ca3f1596c4439fbe4` | 48.22%, 16.70%, 1.30%, 60.07%, -46.90%, 103.72%, 138.77% | **45.98%** | **48.22%** | **6/7** | 57.78% |

The full pre-lockbox replay returned **+401.31%** with **57.04%** maximum drawdown. That is a path diagnostic, not the OOS headline. Entry notional was 53.02% MRNA, 35.77% ANET, 9.03% KLAC, and 2.18% LRCX. NVDA, TSM, and MRVL received resolution attempts but zero fills at this account size.

On the already-burned April 20-August 24 window, event backtest `6a8cbc7ef68259010d8ec591` returned **+203.92%** with **38.46%** maximum drawdown. MRNA buy-and-hold returned about 165.9% over the matched history, leaving about 38.9 percentage points of excess. This result cannot be called a holdout, lockbox, or certification.

### Why the zero-fill names remain

I tested the obvious cleanup instead of rationalizing it. Variant `6a8cbd1289dc23e08ed9d576` removed NVDA, TSM, and MRVL so the semi sleeve always ranked only historically executable names.

| Executable-only audit | Mean OOS | Median OOS | Positive folds | Worst drawdown |
| --- | ---: | ---: | ---: | ---: |
| Five-fold anchored `6a8cbd24a3f1596c443a0158` | 36.55% | 34.40% | 3/5 | 68.22% |
| Seven-fold rolling `6a8cbd6f89dc23e08ed9d8f0` | 42.84% | 37.23% | 6/7 | 51.82% |

The executable-only branch weakened the anchored mean by 25.39 points, added two losing anchored folds, and worsened its worst anchored drawdown. The broader six-name universe therefore stays, but not as fake breadth. Its actual mechanism is "attempt the strongest semi, then do nothing if the option is not executable." If account capital or contract prices change, a currently gated name may become tradable.

### Owner-review and deployment gate

The consolidated live target is `6a8cb433e3971b7c87943f11`, **Public Portfolio Challenge: Semis + Biotech**, Public account `5OH79160`. At final verification it held $13,500 cash, $13,494.51 buying power, no positions, and no strategies. Its deployment frequency is `Constant`, alerts are enabled, and automatic approval is false.

No strategy was cloned to that live target. The finalist stops here for owner review. If approved later, clone the exact five strategies from `6a8cbdfd89dc23e08ed9e2d4`, verify field parity and `Constant` frequency, reconcile, and leave any resulting orders for manual approval. Do not relabel the burned April-August replay as certification.

The remaining bad rolling fold was a real strategy loss, not a rejected-order or impossible-fill artifact. ANET was the largest loser, with additional losses in MRNA and LRCX. That loss is part of the book's honest high-risk profile.

## Optimizer defect found during the campaign

The cooldown sweep exposed a separate implementation bug. When a strategy's entire condition was a standalone `DaysSinceStrategyFired >= 21` rule, the `EntryCooldownDays` sweep wrapped it and appended a second `>= 42` rule instead of replacing it. The malformed candidates therefore had `21 days AND 42 days` while reporting only the new resolved parameter.

NexusTrade commit `b0dccadba5` replaces the standalone cooldown directly and adds a regression test for this exact condition shape. The targeted cooldown tests passed 5/5, and the fix was deployed across the backtesting, optimizer, and live-trading Rust services. The manually authored finalist had one clean 42-day cooldown per sleeve, so this tooling bug does not rescue its failed lockbox.

## State after the first pass

- The two former cash books were consolidated at Public. Their old NexusTrade rows no longer appear in the current live-portfolio list.
- Combined live target `6a8cb433e3971b7c87943f11`: $13,500 cash, no positions, no strategies, `Constant` frequency, automatic approval false.
- Residual `Trace Bitcoin` row `6a8cb433e3971b7c87943f17`: $5.58 cash, no positions, no strategies. This is cash bookkeeping after the completed BTC sale, not a crypto holding.
- Original margin-account portfolio: untouched.
- Superseded MRNA-plus-semis candidate: chat portfolio `6a8cbdfd89dc23e08ed9e2d4`, preserved inactive as research history.
- Deployment: none. A failed lockbox is a hard rejection even when the pre-lockbox walk-forward is exceptional.

Because the April-August period has now been observed repeatedly, it cannot be reused as an untouched lockbox or relabeled as certification. The cash is consolidated and the target is ready, but the candidate remains inactive until owner review. If approved, its next honest test is genuinely unseen forward behavior in that combined account; NexusTrade cannot combine buying power across separate brokerage accounts.

## August 25 final correction: rank MRNA, then audit every stock

The first biotech-inclusive correction still hardcoded a separate 25% MRNA sleeve. That interpretation created concentration by construction. Moderna remains the causal thesis, and MRNA now earns entries through the same ranking and 6% per-name ceiling as every other biotech candidate.

I then audited all 23 stocks for business quality, thesis transmission, liquidity, and current option access. The full evidence is in the [portfolio universe audit](./PORTFOLIO_UNIVERSE_AUDIT_20260825.md).

The audit removed three names from the final ranker:

- **RXRX** failed both tests. It had the weakest revenue, cash-flow, drawdown, and thesis-specificity combination.
- **SDGR** is a credible computational-discovery company. Its relationship to Moderna's individualized therapy was too loose for the final book.
- **BMY** is a strong large pharmaceutical company. Its oncology franchise and BioNTech partnership are adjacent rather than a dependency of V940.

The final biotech ranker is:

**MRNA, MRK, BNTX, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, A**

The architecture has two opposite entry regimes:

1. **Biotech regime:** when XBI is at or above its 200-day SMA and VIX is below 35, filter the 14 names on price and momentum, then score the survivors by 63-day return divided by 63-day standard deviation. The inherited top-17 selection limit is a no-op after cutting the universe to 14; the risk-adjusted momentum weight determines priority for capped capital. Size outright long calls at 6% per selected name with a 75% total cap and a seven-day `DaysSinceStrategyFired` clock. Try 365-730 DTE first, then 180-365, 90-180, and 30-400 when longer contracts do not exist. Take profit at +80% and exit at 90 DTE.
2. **Semiconductor regime:** when XBI is below its 200-day SMA, rank NVDA, ANET, KLAC, TSM, MRVL, and LRCX by 126-day momentum and attempt only the top name. Buy one 10% OTM call at 45-90 DTE, subject to a real bid and a 10% maximum spread, with a 20% total budget and a 42-day strategy clock. Close at 21 DTE or +150%.

Every entry is a single long call. There are no spreads or short legs. The semiconductor names are high-quality AI infrastructure companies used in the opposite XBI regime. They are not represented as material beneficiaries of one cancer-vaccine program.

### Candidate comparison

| Evidence | 17-name ranked MRNA | No RXRX | Mechanism-tight 14-name ranker |
| --- | ---: | ---: | ---: |
| Full pre-readout replay | **+274.91%** | +273.18% | +266.38% |
| Full replay maximum drawdown | **46.97%** | 50.54% | 48.76% |
| Full replay median deployment | **20.02%** | 19.68% | 17.86% |
| Anchored OOS mean | **+35.09%** | +33.90% | +33.45% |
| Anchored OOS median | +31.82% | +24.05% | **+38.67%** |
| Anchored positive folds | 4/5 | 4/5 | 4/5 |
| Rolling OOS mean | +29.31% | +45.46% | **+45.54%** |
| Rolling OOS median | +29.56% | **+39.20%** | +29.92% |
| Rolling positive folds | 6/7 | **7/7** | **7/7** |
| Worst rolling drawdown | 40.26% | **33.61%** | 36.27% |

The mechanism-tight version gives up 8.53 points of the full replay and 1.64 points of anchored mean versus the 17-name ranker. It improves anchored median by 6.85 points, rolling mean by 16.23 points, and rolling consistency from six positive folds to seven. That is enough to prefer the cleaner universe without pretending the result dominates every metric.

### Final pre-readout evidence

The fixed source is `6a8ce8012bafa06e1dad7466`. The exact inactive review clone is `6a8ce88aeca5765ba9cc1075`, **FINAL REVIEW — Quality-Screened Biotech/Semis XBI200**. Both resolve to pre-readout backtest `6a8ce80df68259010d8fa1dd` over March 7, 2022 through April 19, 2026:

- **+266.38%** return;
- **48.76%** maximum drawdown;
- 16 of 20 names traded; and
- **17.86%** median capital deployment.

| Study | OOS folds | Mean | Median | Positive folds | Worst drawdown |
| --- | --- | ---: | ---: | ---: | ---: |
| Five-fold anchored `6a8ce81f2bafa06e1dad752a` | 63.16%, 38.67%, 69.72%, -23.11%, 18.81% | **33.45%** | **38.67%** | **4/5** | 62.08% |
| Seven-fold rolling `6a8ce818eca5765ba9cc0b76` | 91.31%, 58.09%, 29.77%, 29.92%, 11.42%, 76.70%, 21.58% | **45.54%** | **29.92%** | **7/7** | 36.27% |

The already-observed April 20-August 18 replay returned **+20.86%** with **3.59%** maximum drawdown and **14.31%** median deployment. It is a stress diagnostic. The universe was selected after that period was known, so the result cannot become a new lockbox or decide the candidate by itself.

### Final owner-review state

- Inactive review candidate: `6a8ce88aeca5765ba9cc1075`.
- Live target: `6a8cb433e3971b7c87943f11`, $13,500 cash, no positions, no strategies.
- Live deployment frequency: `Constant`; alerts enabled; automatic approval false.
- Structure audit: six strategies, single-leg long calls only, no spreads, no short legs, and no dedicated MRNA strategy.
- Deployment: none. Owner review is still required before cloning the six strategies to the live target. Any resulting orders remain manual-approval only.

## Second pass: independent biotech and semiconductor sleeves

The owner consolidated the cash into one Public account and deleted the two sector accounts. The replacement objective was clarified after the first regime design: holding biotech and semiconductors at the same time is preferred when both have valid setups. It is not mandatory. The book must not force an allocation to a weak sleeve, and it must not make the sectors mutually exclusive.

The final candidate therefore uses two independent `RebalanceOption` strategies with `positionScope: strategy`:

1. **Biotech sleeve:** MRNA, MRK, BNTX, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, and A. The portfolio gate requires XBI at or above its 200-day SMA and VIX below 35. Candidates pass if price is at or above the stock's 100-day SMA or 63-day rate of change is nonnegative. The sleeve ranks by 126-day rate of change, weights by 63-day return divided by 63-day volatility, allocates 6% per name, and caps the sleeve at 75%. Entries use single-leg delta-0.50 long calls, preferring 365-730 DTE with shorter single-call fallbacks. It takes profit at 80% and exits at 90 DTE.
2. **Semiconductor sleeve:** NVDA, ANET, KLAC, TSM, MRVL, and LRCX. The portfolio gate requires SMH at or above its 100-day SMA and VIX below 35. Candidates must be at or above their own 100-day SMA with nonnegative 63-day rate of change. The sleeve selects the top one by 126-day rate of change and attempts a 10% OTM long call at 45-90 DTE. It is spaced by `DaysSinceStrategyFired >= 42`, capped at 15% of the portfolio, takes profit at 100%, and exits at 28 DTE.

There are no option spreads and no short option legs. The two sleeve caps sum to 90%, so simultaneous ownership is possible without making it compulsory.

### Architecture screen

Three independent-sleeve variants were screened against the earlier mutually exclusive regime book. The aggregate semiconductor gate was the only difference between the variants.

| Candidate | Portfolio | Full replay | Anchored mean / median | Rolling mean / median | Rolling positive |
| --- | --- | ---: | ---: | ---: | ---: |
| Earlier XBI regime switch | `6a8ce88aeca5765ba9cc1075` | +266.38% | +33.45% / +38.67% | +45.54% / +29.92% | 7/7 |
| Independent sleeves, SMH 200-day gate | `6a8cecb6687ce0e30a053949` | +310.90% | +56.26% / +16.68% | +57.27% / +47.45% | 5/7 |
| Independent sleeves, SMH 100-day gate | `6a8cecbbeca5765ba9cc34df` | +260.80% | +64.40% / +72.52% | +75.89% / +67.21% | 5/7 |
| Independent sleeves, no aggregate SMH gate | `6a8cecc2eca5765ba9cc350e` | +1,248.15% | +46.82% / +72.52% | not advanced | not advanced |

The ungated design's full replay was spectacular, but it did not improve the independent evidence. The SMH 100-day gate advanced because it produced the best anchored and rolling median among the gated mixed-sleeve designs and allowed all six semiconductor names to fill.

### Parameter sweep and robust fixed configuration

Walk-forward sweep `6a8ceeb4eca5765ba9cc4165` tested 27 combinations:

- semiconductor total budget: 15%, 20%, or 25%;
- semiconductor take-profit threshold: 100%, 150%, or 200%; and
- semiconductor time exit: 14, 21, or 28 DTE.

The adaptive fold winners reported +84.30% mean and +122.78% median OOS return, with four of five folds positive. That result cannot be deployed as one fixed book. The cross-fold robust selection was the 15% budget, 100% profit target, and 28 DTE exit. Its materialized chat portfolio is `6a8ceee4c2086e65999c1900`.

Fixed-parameter anchored certification `6a8cef81eca5765ba9cc48dd` returned:

| Fold | OOS return | Maximum drawdown |
| ---: | ---: | ---: |
| 1 | +1.99% | 32.51% |
| 2 | +119.56% | 42.05% |
| 3 | -42.96% | 55.42% |
| 4 | +124.42% | 26.17% |
| 5 | +122.78% | 44.32% |
| **Aggregate** | **+65.16% mean / +119.56% median** | **55.42% worst** |

Four of five anchored folds were positive. Fixed-parameter rolling study `6a8cefd1eca5765ba9cc4b6a` returned:

| Fold | OOS return | Maximum drawdown |
| ---: | ---: | ---: |
| 1 | +39.46% | 27.73% |
| 2 | -5.43% | 42.05% |
| 3 | +213.70% | 33.05% |
| 4 | -59.18% | 74.33% |
| 5 | +41.22% | 26.17% |
| 6 | +50.12% | 30.91% |
| 7 | -68.64% | 79.90% |
| **Aggregate** | **+30.18% mean / +39.46% median** | **79.90% worst** |

Four of seven rolling folds were positive. This is a high-return, high-variance candidate. It improves the owner's preferred return statistics and sector participation, but it is less consistent than the earlier regime switch.

### Full replay, breadth, and simultaneous holdings

The $13,500 event backtest `6a8cefb8f68259010d8fa462` returned +1,579.62% with a 64.07% maximum drawdown and 12.63% median deployment. All 20 eligible names filled. The $25,000 breadth check `6a8cefbcf68259010d8fa463` also traded all 20 names and returned +732.21%, with a 52.66% maximum drawdown and 17.05% median deployment.

The $13,500 event trace contained 369 filled orders. Reconstructing open single-call positions after each evaluation timestamp found 127 timestamps with at least one biotech and at least one semiconductor position open together. The first overlap, on July 20, 2022, held TWST with KLAC and NVDA. The final replay timestamp, April 16, 2026, held TXG, TWST, MRNA, BNTX, TMO, and ILMN alongside KLAC.

That confirms the implementation matches the clarified preference. It does not impose a permanent two-sector minimum. Either sleeve may remain in cash when its own gate or candidate filter fails.

## Live forward deployment

- The old Biotech and Semis portfolios were deleted. Their stale share links and snapshot embeds were removed from the article.
- The funded Public target is `6a8cb433e3971b7c87943f11`. It began this deployment with $13,500 cash, $13,494.51 buying power, and no holdings.
- The exact six-strategy finalist from chat portfolio `6a8ceee4c2086e65999c1900` was cloned into the funded account: two entry strategies and four matching exit strategies across the biotech and semiconductor sleeves.
- Source and target conditions, universes, allocations, option legs, spacing rules, and exits match. The serializer omitted only two `eligibility: null` fields, which has no executable effect.
- Deployment frequency is `Constant`. Portfolio-level automated approval and all six strategy-level automatic approval flags are off. No order can reach Public without manual approval.
- The immediate post-deployment event audit found no signals, orders, rejections, or positions. No order was approved during deployment.
- The April-August 2026 lockbox is burned. The first combined candidate failed it, and the replacement was designed after that result was known. The next honest test is forward trading, not another claim on the same dates.
- The owner authorized the finalist as a high-risk live forward test on August 24, 2026. This is a deployment decision, not a claim that the replacement passed a pristine lockbox. Its genuinely unseen record begins with this deployment.
