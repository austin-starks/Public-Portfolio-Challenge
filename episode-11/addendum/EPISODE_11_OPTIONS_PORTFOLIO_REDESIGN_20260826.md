# Episode 11: final options portfolio redesign

**Date:** August 26, 2026  
**Portfolio:** Public Portfolio Challenge: Semis + Biotech  
**Funded size used for every certification result:** **$13,500**  
**Decision:** The research candidate is robust, executable, and interpretable enough to stage for owner-approved reconciliation. No live strategy, holding, or order has been changed.

## Final answer

This remains an **options-only portfolio**. Common stocks are the underlyings used to evaluate company-specific signals. The portfolio holds only outright long calls. It does not hold stock, debit spreads, or short option legs.

The final design is one central allocator over 26 thesis-approved companies. The eight thesis buckets remain important for explaining why each company belongs in the portfolio and for auditing results. They are not implemented as eight independent order queues. Testing showed that separate queues introduce fixed ordering and concentration effects: lowering their aggregate exposure cap from 48% to 40% or 32% made worst drawdown worse, not better.

The final implementation therefore separates three decisions:

1. **Thesis eligibility:** Austin decides which companies belong and why.
2. **Company timing:** each stock must pass its own trend and momentum rules. XBI and SMH cannot veto it.
3. **Portfolio construction:** one allocator ranks all currently eligible companies and spends the shared options risk budget.

There is no special MRNA allocation and no special ANET allocation. There is also no sector-wide XBI or SMH gate.

## What the final portfolio contains

### Therapy platforms and oncology partners

- MRNA
- MRK
- BNTX
- BMY

### Computational drug discovery

- RXRX
- SDGR

### Precision-oncology diagnostics

- ADPT
- GH
- NTRA
- VCYT

### Measurement infrastructure

- ILMN
- TWST
- QGEN
- TXG
- PACB

### Diversified life-science tools

- TMO
- DHR
- A
- TECH

### AI compute and custom silicon

- NVDA
- AVGO
- MRVL

### Semiconductor manufacturing and equipment

- TSM
- AMAT
- LRCX

### AI networking

- ANET

These categories are different business mechanisms. They were tested separately before selecting the construction. The final allocator does not assert that MRNA and ANET are the same trade. It only gives their long calls access to the same scarce cash budget after their own stock signals qualify.

## Exact strategy

| Component | Final rule |
| --- | --- |
| Starting capital | $13,500 |
| Security held | Single-leg long call only |
| Entry universe | The 26 names above |
| Company entry filter | Underlying price above its own 100-day SMA **and** its own 63-day return above zero |
| Candidate ordering | Highest 126-day return |
| Allocation weight | 63-day return divided by 63-day price volatility |
| Rebalance cadence | At least 7 days since the last RebalanceOption order |
| Broad stress gate | VIX below 35 |
| Sector gates | None; no XBI or SMH condition |
| Per-company allocation | Maximum 6% of current portfolio value |
| Per-rebalance budget | 45% of current portfolio value |
| Portfolio entry gate | Do not start another rebalance cycle when current option gross exposure is 39% or higher |
| Expiry at entry | 270 to 730 DTE; prefer the middle of the available range |
| Strike ladder | 0%, 10%, 20%, 35%, 50%, 75%, then 100% OTM, using the first executable structure |
| Execution filter | Maximum 20% bid-ask spread |
| Profit exit | Close at a 300% option gain |
| Time exit | Close at 180 DTE remaining |
| Company deterioration exit | Close when its stock falls below its own 100-day SMA **or** its own 63-day return falls below zero |
| Position scope | Portfolio-wide, so an existing QGEN call counts and should not be duplicated |
| Automatic approval | Off |

The 39% portfolio gate controls whether another entry cycle may begin. It is not a forced deleveraging rule. Existing calls can appreciate and push marked exposure above 39% without being sold solely for that reason.

## Why this construction won

The selected design is the best balance of deployability, breadth, risk, and interpretability at the actual account size.

### Five non-overlapping out-of-sample folds

| OOS window | Return | Sortino | Max drawdown | Median deployment | Participation |
| --- | ---: | ---: | ---: | ---: | ---: |
| Nov. 8, 2022 to Jul. 18, 2023 | +42.87% | 3.26 | 15.01% | 28.30% | 65.4% |
| Jul. 18, 2023 to Mar. 26, 2024 | +25.00% | 1.99 | 15.33% | 14.17% | 50.0% |
| Mar. 26, 2024 to Dec. 3, 2024 | -2.22% | -0.31 | 21.64% | 19.42% | 53.8% |
| Dec. 3, 2024 to Aug. 12, 2025 | +9.95% | 0.62 | 22.47% | 22.76% | 65.4% |
| Aug. 12, 2025 to Apr. 20, 2026 | +65.40% | 5.61 | 8.09% | 25.38% | 53.8% |

The gate is **not** five profitable folds out of five. The candidate passes because:

- 4 of 5 folds were profitable;
- the one losing fold was only -2.22%;
- median OOS return was +25.00%;
- median OOS Sortino was 1.99;
- worst OOS drawdown was 22.47%; and
- no fold reported a validation warning.

Study: `6a8f7ca76c9d5ad71a636c07`

### Full event replay

The matched March 7, 2022 through April 20, 2026 replay at $13,500 produced:

- +252.37% return;
- 2.02 Sortino;
- 29.79% maximum drawdown;
- 30.53% median deployment;
- 20 of 26 names traded;
- 13.32% largest underlying share of cumulative entry notional; and
- 496 option fills with default option fees included.

Marked option exposure reached 62.78% after positions moved. It exceeded the 39% entry gate because the gate blocks new entry cycles; it does not liquidate appreciated calls. The full replay's longest underwater period was 573 days. Those are material risk disclosures, not details to hide.

Full event replay: `6a8f7dd2f68259010d956f8d`

## What the thesis-bucket test taught us

The best separate-bucket implementation used 8% per bucket, 120 to 270 DTE, a 20% spread ceiling, and a 48% gross-entry gate. Its OOS returns were:

- +44.48%
- +82.54%
- +3.50%
- -4.24%
- +94.41%

That is also 4 of 5 profitable folds, with a 2.54 median Sortino. It lost the construction decision because its worst drawdown was 33.43%.

The weak fold was not caused by missing ANET. ANET was its best gross cash-flow contributor at approximately **+$1,867**. The loss came from several independent sleeves losing together, led by RXRX at approximately -$1,120 of closed gross cash flow, MRVL at -$506, BMY at -$374, MRK at -$354, and marked losses in open GH and TXG calls. The order-level cash flows, remaining option marks, and $122.20 of fees reconcile to the fold loss.

Lowering the bucket gate did not fix it:

| Bucket gate | Profitable folds | Median OOS return | Worst OOS drawdown |
| --- | ---: | ---: | ---: |
| 32% | 4/5 | +46.80% | 37.85% |
| 40% | 4/5 | +51.89% | 34.04% |
| 48% | 4/5 | +44.48% | 33.43% |

Lower gates let the earliest strategy queues crowd out later thesis buckets. The central allocator removed that fixed queue priority and reduced worst OOS drawdown to 22.47%.

## Current executable snapshot

An empty $13,500 replay on August 25, 2026 resolved four positions at 19.13% total deployment:

| Underlying | Contract | Quantity | Simulated fill |
| --- | --- | ---: | ---: |
| NVDA | Dec. 17, 2027 $420 call | 1 | $5.60 |
| QGEN | Dec. 17, 2027 $45 call | 1 | $6.35 |
| RXRX | Jan. 21, 2028 $4 call | 5 | $1.40 |
| PACB | Jan. 21, 2028 $2 call | 13 | $0.58 |

This proves that the strategy is not structurally idle at $13,500. These are simulated fills, not live order instructions.

ANET passed the stock-level research logic but one long-dated contract cost approximately $2,225 in the audited resolver snapshot. That exceeds the 6% per-company budget of about $810, so the strategy rejected it. Buying it anyway would require knowingly increasing single-name risk or shortening duration. The strategy does neither silently.

Current executable replay: `6a8f7dd5f68259010d956f8e`

## Live holdings decision

The live portfolio was re-read after certification:

- cash: $12,910.02;
- buying power: $12,904.53;
- one position: 1 QGEN Dec. 17, 2027 $45 call;
- current audited value: $425;
- average cost: $590;
- unrealized P/L: -$165, or -27.97%; and
- no Pending, Accepted, Pending User Approval, or Partially Filled orders.

The QGEN call was not force-sold merely because the strategy architecture changed. QGEN remains in the thesis universe, the final strategy uses portfolio-wide position scope, and the existing call counts against its QGEN allocation.

## Deployment record

The exact research portfolio is:

- Final candidate: `6a8f7ea36c9d5ad71a63775d`
- Certified source: `6a8f7c8c6c9d5ad71a636b36`
- Legacy sector-gated paper portfolio: `6a8f9b0ec67c177db82d5b0f`
- Live Public portfolio: `6a8cb433e3971b7c87943f11`
- Current-book reconciliation: `6a8f9b603a0c760d5849f380`

Austin explicitly approved preserving the current strategies in paper and replacing the live strategy set. The live mutation removed six strategies and added 29 exact semantic copies from the final candidate. The account identity, history, cash and existing QGEN contract were preserved. Portfolio-level automated approval and all 29 strategy-level automatic approvals remain disabled.

The post-deployment current-book reconciliation resolved a $13,335.02 NAV. Its target was the same single QGEN contract already held. It produced zero orders, $0 estimated cost, $0 realized P/L, no wash-sale flags and no canceled orders. No QGEN exit condition fired, and no duplicate QGEN order was created. Future live orders still require Austin's manual approval.

## Engine defects found during certification

Two engine defects were separated from portfolio evidence:

1. Walk-forward studies previously accepted zero starting capital and produced invalid no-signal results. Positive starting capital is now enforced in commit `a8f4b169d9`.
2. Breadth-audit sample truncation sliced UTF-8 strings by raw byte index and could panic on a multibyte character. Character-boundary-safe truncation and regression tests are in commit `32c9c377ef`.

The selected 39% study completed all five folds without either defect. The 33% sensitivity run remains quarantined because it hit the UTF-8 bug before that fix was deployed to the research worker. It is not being used to select the final portfolio.
