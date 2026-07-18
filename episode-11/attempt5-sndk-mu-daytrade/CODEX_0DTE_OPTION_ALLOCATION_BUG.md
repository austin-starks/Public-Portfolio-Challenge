# Diagnose: OpenOption allocation does not cap backtest contract quantity

## One-line

The minute backtester generated identical oversized option orders for fixed-dollar and percent-of-portfolio allocations, allowing a nominal $800–$1,000 ticket to buy 29 MU contracts costing $6,699 in an $8,000 account.

## Severity and campaign impact

**Critical for options certification.** Return, drawdown, fees, turnover, affordability, and risk-adjusted statistics from the affected 0DTE runs cannot be trusted. All C3/F/G/H option backtests and the C3 walk-forward study are quarantined. No portfolio was deployed and no live order was created.

## Expected vs observed

- **Expected:** A long-option order's whole-contract quantity is bounded by its resolved allocation. With a $2.31 contract price and a 100 multiplier, a $1,000 allocation permits at most four contracts before fees; 10% of an $8,000 portfolio permits at most three.
- **Observed:** Both configurations bought 29 contracts at $2.31, or $6,699 of MU premium. They also bought one SNDK contract at $3.40, consuming about $7,039 before fees and leaving roughly $941.50 cash.
- **Required invariant:** `quantity × fillPrice × multiplier + costs <= resolvedAllocation`, except that a policy may deliberately reserve additional cash rather than spend it. It must never exceed the allocation.

## Minimal reproduction

### Fixed-dollar case

- Portfolio: `6a5b9e7c5e9beacc0a17e8bb` — `CODEX SNDK + MU 0DTE F1 Strict RSI 70-30`.
- Persisted entry allocation on all four OpenOption strategies: `{ "type": "dollars", "amount": 1000 }`.
- Minute event backtest: `6a5ba1795e9beacc0a17f35e`, 2026-01-02, initial value $8,000.

### Percent-of-portfolio case

- Portfolio: `6a5ba09d075cfa92d0b21a30` — `CODEX 0DTE H5 Strict RSI 10 Percent NAV Per Name`.
- Persisted entry allocation on all four OpenOption strategies: `{ "type": "percent of portfolio", "amount": 10 }`.
- Minute event backtest: `6a5ba175075cfa92d0b21cc6`, 2026-01-02, initial value $8,000.

### Identical filled orders in both cases

| Timestamp | Symbol | Order | Quantity | Fill | Notional |
|---|---|---|---:|---:|---:|
| 2026-01-02 15:01 | `SNDK260102C00265000` | Buy limit | 1 | $3.40 | $340 |
| 2026-01-02 15:04 | `MU260102C00310000` | Buy limit | 29 | $2.31 | $6,699 |
| 2026-01-02 20:31 | `SNDK260102C00265000` | Sell market | 1 | $8.08 | $808 |
| 2026-01-02 20:31 | `MU260102C00310000` | Sell market | 29 | $4.82 | $13,978 |

The event formatter exposes the exact quantities and fill prices. The backtest histories for F1 and H5 are identical, confirming that the allocation change had no effect on the executed quantity.

## Secondary pricing contradiction

For the SNDK entry at 15:00, the raw resolution trace contains conflicting prices for the same selected contract and resolution cycle:

- a `resolutionAudits` record near $0.42 with roughly $44.50 net cost;
- a later `resolutionResult` / risk path near $3.50 and $350 total cost;
- the actual filled limit order at $3.40.

The final fill is plausible, but the disagreement means affordability and liquidity decisions may be using a different price surface from the order engine. Diagnose this independently of the quantity cap.

## Leading hypotheses — verify, do not assume

1. The resolver computes `finalQty` from buying power or liquidity capacity after recording `allocationRequested`, but never applies the allocation-derived quantity ceiling.
2. A liquidity-cap field is interpreted as a minimum/override instead of a maximum, replacing the allocation result.
3. The quantity is derived from an earlier low audit price and is not recomputed after the selected entry price changes.

## Where to look

- The OpenOption resolution path that converts `action.allocation` into `requestedQuantity` or `finalQty`.
- The merge order between allocation sizing, buying-power checks, risk audit, and liquidity caps.
- Any fallback that changes `entryPrice` after quantity calculation.
- The simulator's invariant check before an option order is accepted or filled.

## Acceptance test

1. Replay both portfolios on 2026-01-02 with an $8,000 initial value and events enabled.
2. For F1, assert MU quantity is at most four at a $2.31 fill; for H5, assert at most three.
3. Assert F1 and H5 no longer produce identical orders/equity histories solely because their signals match.
4. Assert every long-option entry satisfies the allocation invariant using the final fill price, contract multiplier, fees, and resolved allocation.
5. Assert the price used for quantity, affordability, risk, submitted limit, and fill-slippage audit is either the same value or explicitly versioned with a documented transition.
6. Add a regression covering a price change between preliminary chain audit and final order construction.

## Evidence retention

Event traces are in the Mongo hot store and expire after three days. Preserve the two backtest IDs above and the filled-order table in this report; rerun the one-session reproduction if raw traces have expired.

## Campaign restart gate

After the fix, rerun the one-day acceptance test first. Only then rerun the full C3/F/H search set, matched baselines, and a fresh walk-forward OOS study. Prior affected statistics remain historical diagnostics and must not be relabeled as valid evidence.

## Safe campaign workaround confirmed

Until the allocator is repaired, use only explicit contract allocations. J1 `6a5ba30a595ed3a6ef3bc7a1` persisted `{ "type": "contracts", "amount": 1 }`; event replay `6a5ba315075cfa92d0b22141` filled one MU contract and one SNDK contract. J3's two-contract replay `6a5ba3e7075cfa92d0b223e9` filled two MU contracts and reduced SNDK to one under its liquidity cap. These controls show that explicit contract counts are honored by the tested simulator path.

This is a narrow workaround, not a bug resolution. Dollar and percent-of-portfolio allocations remain prohibited for the campaign, and every promoted backtest must retain an event replay proving requested-versus-filled quantities.
