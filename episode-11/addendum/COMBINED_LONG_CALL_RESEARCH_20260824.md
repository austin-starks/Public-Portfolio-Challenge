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

## Final live state and next gate

- The two former cash books were consolidated at Public. Their old NexusTrade rows no longer appear in the current live-portfolio list.
- Combined live target `6a8cb433e3971b7c87943f11`: $13,500 cash, no positions, no strategies, `Constant` frequency, automatic approval false.
- Residual `Trace Bitcoin` row `6a8cb433e3971b7c87943f17`: $5.58 cash, no positions, no strategies. This is cash bookkeeping after the completed BTC sale, not a crypto holding.
- Original margin-account portfolio: untouched.
- Superseded MRNA-plus-semis candidate: chat portfolio `6a8cbdfd89dc23e08ed9e2d4`, preserved inactive as research history.
- Deployment: none. A failed lockbox is a hard rejection even when the pre-lockbox walk-forward is exceptional.

Because the April-August period has now been observed repeatedly, it cannot be reused as an untouched lockbox or relabeled as certification. The cash is consolidated and the target is ready, but the candidate remains inactive until owner review. If approved, its next honest test is genuinely unseen forward behavior in that combined account; NexusTrade cannot combine buying power across separate brokerage accounts.

## August 25 correction: restore the biotech thesis

The MRNA-plus-semis draft solved the cash-account problem by deleting too much of the investment thesis. That was not an acceptable final answer. MRNA is still the direct bet, but the original article also argued for the neoantigen chain around it: the drug partner, the closest mRNA competitor, sequencing and diagnostics, liquid biopsy, research tools, and adjacent computational drug discovery.

The corrected architecture uses three mutually aware entry regimes in one cash portfolio:

1. **MRNA core:** one 5% OTM call at 45-90 DTE, up to 25% of portfolio, when MRNA is above its 100-day SMA with positive 63-day rate of change. It uses a 21-day `DaysSinceStrategyFired` clock and closes at 21 DTE, +150%, or a confirmed trend break.
2. **Biotech chain:** MRK, BNTX, RXRX, SDGR, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, A, BMY. When XBI is at or above its 200-day SMA and VIX is below 35, the book ranks the eligible names by 126-day momentum and sizes outright long calls at 6% per name with a 75% total cap. It tries 365-730 DTE first, then 180-365, 90-180, and finally 30-400 when the longer windows do not exist. These are single-leg calls, never long-dated verticals. The sleeve takes profit at +80% and exits at 90 DTE.
3. **Semiconductor regime:** when XBI is below its 200-day SMA, rank NVDA, ANET, KLAC, TSM, MRVL, and LRCX by 126-day momentum and attempt only the top name. The entry is one 10% OTM call at 45-90 DTE, subject to a real bid and a 10% maximum spread, with a 20% total budget and a 42-day strategy clock. It closes at 21 DTE or +150%.

The opposite XBI gates matter. The weak designs ran biotech and semis concurrently and let both sleeves consume cash in the same losing regimes. The corrected book allocates to the biotech chain when the biotech sector is healthy and uses semis as the alternate regime. MRNA remains separately eligible because it is the thesis, not a generic XBI constituent.

### Corrected pre-readout evidence

The fixed source is chat portfolio `6a8cdcef3317b9f122a67740`. The exact inactive review clone is `6a8cdf9789dc23e08edb62bb`, **FINAL REVIEW — MRNA + Biotech/Semis XBI200 Regime Book**. Replaying either semantic object over March 7, 2022 through April 19, 2026 resolves to backtest `6a8cdf9df68259010d8f9e77`:

- **+327.80%** return;
- **52.91%** maximum drawdown;
- 19 of 23 names traded; and
- 22.18% median capital deployment.

| Study | OOS folds | Mean | Median | Positive folds | Worst drawdown |
| --- | --- | ---: | ---: | ---: | ---: |
| Five-fold anchored `6a8cdcff89dc23e08edb45cd` | 49.28%, 12.54%, 80.63%, -38.14%, 69.17% | **34.70%** | **49.28%** | **4/5** | 67.05% |
| Seven-fold rolling `6a8cdd0c3317b9f122a678be` | 4.24%, 52.89%, 62.45%, 8.02%, 22.69%, 13.41%, 74.44% | **34.02%** | **22.69%** | **7/7** | 50.83% |

The return was not rescued by one fold. All seven rolling OOS folds were positive. Increasing the MRNA core from 25% to 35% raised the full replay to +408.30%, but reduced rolling OOS to 6/7 positive and anchored OOS to 3/5 positive, including a -40.50% fold. Increasing the defensive semi budget to 40% also reduced rolling consistency and median return. Both higher-allocation variants were rejected.

### Universe audit

MRNA, MRK, and BNTX are the direct therapy, partner, and closest mRNA competitor. GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, and A cover tumor profiling, sequencing, diagnostics, and laboratory tooling. SDGR and ADPT add computational drug discovery and immune-response exposure. BMY is an adjacent oncology franchise. RXRX is the weakest company in the set on current revenue, cash-flow, and momentum evidence, so it is explicitly a speculative satellite capped at 6%, not a co-equal core holding.

Two prospective quality changes were tested rather than assumed:

| Prospective universe | Full replay | Anchored OOS | Rolling OOS | Observed Apr 20-Aug 18 replay |
| --- | ---: | ---: | ---: | ---: |
| Replace RXRX with TEM | +345.01% | 41.10% mean, 4/5 positive | 44.64% mean, 6/7 positive | -1.98% |
| Remove RXRX, no replacement | +390.67% | 35.49% mean, 4/5 positive | 34.18% mean, 6/7 positive | +7.37% |
| Frozen RXRX universe | +327.80% | 34.70% mean, 4/5 positive | 34.02% mean, **7/7 positive** | **+70.41%** |

The April-August column is already burned and cannot select or certify a universe. It does expose the capital-path risk of swapping names after the fact. The frozen universe therefore stays for the owner-review candidate. TEM and no-RXRX remain inactive research branches until genuinely unseen data can distinguish them. The no-RXRX observed replay also warned that more than half of option pricings used modelled synthetic spreads instead of observed NBBO, another reason not to promote it from that window.

### Observed-window execution audit

Event backtest `6a8cdf83f68259010d8f9e6a` covered April 20 through August 18, ending before Moderna's August 19 readout. It returned **+70.41%** with **19.18%** maximum drawdown. This is a post-selection replay, not a new lockbox.

The book filled 13 of 23 names. MRNA represented 47.94% of entry notional, so the portfolio still feels the direct bet. Twelve biotech-chain names also filled. The six semiconductors had zero resolution attempts because XBI stayed above its 200-day SMA during the window; that is the intended regime switch, not an execution failure. Median deployment was 20.30%, maximum deployment was 55.15%, and there were no days above 70% deployment.

### Final owner-review state

- Inactive review candidate: `6a8cdf9789dc23e08edb62bb`.
- Live target: `6a8cb433e3971b7c87943f11`, $13,500 cash, no positions, no strategies.
- Live deployment frequency: `Constant`; alerts enabled; automatic approval false.
- Structure audit: single-leg long calls only, no spreads, no short legs. MRNA and semis use 45-90 DTE. Only the biotech-chain sleeve may open longer-dated exposure, and every such position is an outright long call.
- Deployment: none. Owner review is still required before cloning the eight strategies to the live target. Any resulting orders remain manual-approval only.
