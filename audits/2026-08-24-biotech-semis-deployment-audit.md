# Biotech and Semis deployment audit

**Date:** August 24, 2026  
**Scope:** Public Portfolio Challenge: Biotech and Public Portfolio Challenge: Semis  
**Method:** Fixed-book, five-fold rolling walk-forward from January 3, 2022 through August 21, 2026. Each fold used 70% training, 15% validation, a five-day embargo, and a held-out OOS segment. No parameter search was used.

This audit answers a narrower question than the original Episode 11 research: are the stocks in the two funded Public books still reasonable holdings for their stated theses, and do the deployed strategy shapes hold up when re-tested without changing the bars?

## Decision

| Book | Decision | Live change |
| --- | --- | --- |
| Biotech | Keep MRNA and the remaining quality universe. Remove PSNL, TECH, and PACB. | Replaced the entry strategy with the 17-name cleanup. Deployment frequency is `Constant`. |
| Semis | Keep all seven names and both S13 A sleeves. | No strategy change. Deployment frequency remains `Constant`. |

The Biotech book is still intentionally exposed to the Moderna thesis. MRNA was not removed or diluted out of the universe. The cleanup targeted three weaker or less practical satellite names.

## Biotech: matched walk-forward

### Original 20-name control

- Study: `6a8c4e710263fc9cafb6d44d`
- OOS fold returns: **-10.95%, +16.13%, +24.02%, +29.99%, +96.16%**
- Mean OOS return: **+31.07%**
- Median OOS return: **+24.02%**
- Positive folds: **4 of 5**
- Mean OOS Sortino: **1.24**
- Worst OOS max drawdown: **25.52%**

### Cleaned 17-name book

Removed: **PSNL, TECH, PACB**

Remaining universe: **MRNA, MRK, BNTX, RXRX, SDGR, ADPT, GH, NTRA, VCYT, ILMN, TWST, QGEN, TXG, TMO, DHR, A, BMY**

- Study: `6a8c4e290263fc9cafb6cfd9`
- OOS fold returns: **-5.98%, +53.05%, +33.69%, +27.92%, +97.22%**
- Mean OOS return: **+41.18%**
- Median OOS return: **+33.69%**
- Positive folds: **4 of 5**
- Mean OOS Sortino: **1.57**
- Worst OOS max drawdown: **19.45%**

Against the matched control, the cleanup improved mean OOS return by **10.11 percentage points**, improved mean Sortino by **0.34**, and reduced the worst fold drawdown by **6.07 percentage points**.

The live Biotech entry strategy was replaced with the cleaned version. The live replacement strategy id is `6a8c4eda0263fc9cafb6e03d`.

## Rejected Biotech alternatives

Two plausible operational changes were tested and rejected instead of being promoted on intuition.

### Dedicated 30% MRNA core

A separate 30% MRNA spread sleeve would make the thesis easier to express when a 6% allocation cannot afford one contract. It did not hold up.

- Study: `6a8c4ff30263fc9cafb6fa71`
- Mean OOS return: **+21.04%**
- Positive folds: **3 of 5**
- Mean OOS Sortino: **0.66**
- Worst OOS max drawdown: **39.06%**

Decision: **reject**. MRNA remains central to the thesis, but the dedicated core sleeve degraded the tested portfolio.

### Put defined-risk spreads ahead of calls

Public brokerage permissions can reject outright long calls even when the strategy can resolve them. Reordering the templates to prefer verticals looked operationally cleaner, but the historical portfolio changed materially.

- Study: `6a8c508b0263fc9cafb6ff75`
- Mean OOS return: **+7.00%**
- Positive folds: **3 of 5**
- Mean OOS Sortino: **0.48**
- Worst OOS max drawdown: **30.64%**

Decision: **reject**. The live strategy keeps the tested template order. Broker eligibility remains an execution constraint, not a reason to substitute a materially worse strategy without evidence.

## Semis: fixed-book re-certification

Universe: **NVDA, TSM, AVGO, AMAT, LRCX, ANET, MRVL**

- Study: `6a8c4e247ae40153ecdd9f77`
- OOS fold returns: **+85.97%, +35.47%, +3.08%, +102.51%, +111.40%**
- Mean OOS return: **+67.69%**
- Median OOS return: **+85.97%**
- Positive folds: **5 of 5**
- Mean OOS Sortino: **1.79**
- Worst OOS max drawdown: **33.73%**

Decision: **keep S13 A unchanged**. The seven-name universe and both option sleeves survived the fresh fixed-book walk-forward.

## 24/7 deployment status

Both live portfolios now use NexusTrade deployment frequency `Constant`, and recent event logs show continuous strategy evaluation.

That is not the same as unattended broker execution. Automated order approval is disabled on both accounts, and the automated-trading approval status is `NOT_STARTED`. Signals can evaluate continuously, but orders still require the account owner's review until the brokerage application and consent flow are completed.

## Why the live books are not showing new option trades

The two portfolios have different blockers.

### Biotech: signals fire, but Public rejects the option level

At the August 24 14:25 UTC audit snapshot, the Biotech book had produced **140 OpenOptionSignal events**, **702 option-resolution attempts**, and **562 broker rejections** since midnight UTC. Of those rejections, **560** reported `Option level required.` and two were classified as `UnderlyingIneligible`.

This is not limited to outright calls. Public rejected both single-leg calls, including RXRX and SDGR, and resolved vertical spreads, including MRK and BMY, with the same option-level message. The signal and contract-resolution paths are working; the account's current Public options permission is the immediate execution blocker.

Affordability is a secondary constraint. The strategy allocates **6%**, or about **$330**, per name. MRNA was selected, but the closest contract cost roughly **$535 to $630** during the audit, so that sleeve could not buy one contract. Other names either exceeded the allocation or resolved multi-leg templates to the same contract.

Because rejected preflight attempts do not advance the `DaysSinceLastRebalanceOptionOrder` cooldown, Constant evaluation retries the same eligible set every few seconds. That explains the rejection volume. This audit records the behavior; it does not silently change the tested strategy.

### Semis: a legacy canceled SNDK spread is holding the cooldown closed

The Semis book produced **541 events** in the same snapshot window, but no `OpenOptionSignal`, new option `Order`, or `OrderRejected` events. Its entry gate currently reads **38 days since the last RebalanceOption order**, below the required **63 days**.

The only portfolio orders are a canceled SNDK vertical created July 17, 2026:

- Buy order `6a5a52b2c350658add1473c7`
- Sell order `6a5a52b2c350658add1473c8`
- Multi-leg group `6a5a52b2c350658add1473c6`

Those old system-created orders are counted by the portfolio-wide cooldown even though both legs were canceled and the current S13 A strategies were installed later. On the present clock, the 63-day gate does not reopen until approximately **September 18, 2026**. Changing or resetting that gate would be a material live-strategy decision, so this audit leaves it unchanged.

Automated approval is not the immediate blocker for either book. It becomes the next control only after the broker accepts an order: with automated approval disabled, an accepted order will wait for manual review.

## BTC dust

The Biotech account held `0.00007704 BTC-USD`, approximately six dollars at the audit quote. Market sell order `6a8c4eab7ae40153ecdda2ca` filled at a submitted price of **$78,819.60**.

Status at publication: **filled**. The Biotech account now has no remaining positions and **$5,500.09** in cash and buying power.

## What this proves

This is point-in-time research evidence, not a promise of future returns. The cleaned Biotech book beat its calendar-matched control out of sample, while two seemingly sensible structural alternatives failed. The Semis book remained strong across all five held-out folds. Live fills can still differ because of option liquidity, spreads, brokerage permissions, assignment, latency, and manual approval.
