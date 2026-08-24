# Episode 11 addendum: short-term debit spreads and symbol eligibility

**Date:** August 24, 2026
**Live books:** Public Portfolio Challenge: Biotech and Public Portfolio Challenge: Semis

> **Status update:** This is a historical snapshot from before the account constraint was confirmed. These two books are cash accounts and cannot execute spreads; their entry strategies were subsequently removed. See the [combined long-call research addendum](./COMBINED_LONG_CALL_RESEARCH_20260824.md) for the current state and failed replacement lockbox.

## Decision

Debit verticals are now a short-term structure only. Both live books may still use long-dated single-leg calls, but no debit vertical may resolve beyond **180 calendar days to expiration**. This also rejects a long-dated narrow spread such as a 70/75 call debit spread. The rule is based on the resolved expiration and quoted legs, not the authored strategy label.

This is separate from Public account options approval. The account can place spreads. Public can still mark an individual underlying as ineligible for spread trading through its instrument capability data. The explicit live example in this audit was **TXG**, reported as `optionSpreadTrading=DISABLED`. That is a symbol-level enablement request for Public, not an options-level upgrade request.

## Live changes

### Biotech

- Live portfolio: `6a5e20a3ea0d6db55c69a171`
- Entry strategy: `6a8c7b7501471d61b006b171`
- MRNA remains in the full universe and remains the central thesis exposure.
- Long single calls remain available in the 365-730, 180-365, 90-180, and fallback expiration bands.
- Debit-vertical templates in the 365-730 and 180-365 bands were removed.
- Every remaining debit-vertical template has a maximum of 180 DTE.
- Deployment frequency is `Constant`, so the book evaluates continuously.

### Semis

- Live portfolio: `6a45f218e6b1f2131d1f26be`
- The 365-730 DTE entry strategy was removed.
- The retained entry strategy, `6a8c70598be832eb562f9ec5`, uses 90-180 DTE.
- Existing exit strategies were preserved.
- Deployment frequency is `Constant`, so the book evaluates continuously.

## Matched walk-forward evidence

Both replacements used the same five-fold calendar: January 3, 2022 through August 21, 2026, rolling 252-day out-of-sample windows, 252-day stride, five-day embargo, and an 85/15 train/validation split.

| Book | Study | OOS fold returns | Mean | Median | Positive folds | Worst drawdown |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Biotech, short-term-spread-safe | `6a8c7ad78be832eb562fe902` | 3.96%, 6.63%, 32.33%, -2.59%, 163.95% | 40.86% | 6.63% | 4/5 | 25.43% |
| Prior Biotech live control | `6a8c4e710263fc9cafb6d44d` | -10.95%, 16.13%, 24.02%, 29.99%, 96.16% | 31.07% | 24.02% | 4/5 | 25.52% |
| Semis, short-term-spread-safe | `6a8c7b2901471d61b006b08f` | 98.71%, 66.33%, -0.68%, 64.44%, 72.76% | 60.31% | 66.33% | 4/5 | 58.43% |
| Prior Semis combined incumbent | campaign control | see prior campaign record | 67.69% | 85.97% | 5/5 | 33.73% |

The Biotech replacement improved mean OOS return while lowering the median because its result is driven heavily by one large fold. The Semis replacement is weaker than the prior combined incumbent reported during the campaign, but it retains high OOS return while satisfying the new hard structure rule. These are research results, not forecasts.

## Why neither book is placing an order right now

The continuous deployment loop is running. At **2026-08-24 17:13:56 UTC**, each book produced a `NoSignal` before it attempted to stage an order:

- **Biotech:** `DaysSinceLastRebalanceOptionOrder = 0.10028935185`; the entry rule requires at least 7 days. VIX was 16.01 and passed its risk gate.
- **Semis:** `DaysSinceLastRebalanceOptionOrder = 38`; the active cadence branch requires at least 63 days. VIX was 16.01 and passed its risk gate.

Therefore the immediate no-trade cause is cadence, not a broker rejection. If a later eligible signal reaches broker preflight and Public reports `optionSpreadTrading=DISABLED` for an underlying, that symbol should be sent to Public for spread enablement. TXG is the currently evidenced request.

## Platform enforcement

NexusTrade commit `1ea709adfbe4ff8aa9b29e087828ba7ffe0565cc` adds the 180-DTE debit-vertical ceiling at three layers:

1. strategy authoring templates,
2. semantic validation for generated strategy code, and
3. the Rust option resolver after actual strikes, quotes, and expiration are known.

Long-dated single-leg options and credit verticals are not blocked by this rule.
