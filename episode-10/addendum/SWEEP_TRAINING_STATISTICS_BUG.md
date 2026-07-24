# Confirmed engine defect — sweep training statistics are reused across folds

**Found:** 2026-07-24

**Affected study:** `6a639fd78851af28134e04db`

**Root optimizer:** `6a639fd78851af28134e04df`

**Classification:** confirmed reporting, caching, or execution defect

**Deployment impact:** sweep training statistics are quarantined; fixed-config certification is not
affected

## Symptom

The five-fold anchored sweep reports the exact same training statistics in every fold, even though
each fold has a different training end date:

- return `4.097306802368034%`;
- Sortino `1.218188492548777`;
- max drawdown `8.20577651590287%`;
- nine names traded;
- median deployment `16.642514217004713%`;
- `140040` null-gated evaluations.

The study creation response also returned `sweepGenes: []` even though the preview compiled four genes
and the completed optimizer contains distinct parameter combinations. That response discrepancy may
be related, but it is not required to prove the statistics defect.

## Expected

Anchored folds have expanding training windows, so the stored training statistics should be computed
for each fold's own training window. At minimum, they should match a fixed-book run over the same
calendar when the same configuration is selected.

## Independent reproduction

Fixed-book study `6a63a0cee490b0ae31ed3569` used the identical five-fold calendar and the exact
cross-fold robust configuration. Its training return changes by fold:

`4.4656%, 11.5667%, 18.2180%, 75.8649%, 82.5045%`

Its training Sortino also changes:

`0.7737, 1.1197, 1.1910, 2.9946, 2.7130`

This directly contradicts the sweep's repeated training row.

## Scope and quarantine

- Do not use the sweep's training statistics for a robustness or deployment claim.
- Do not treat the defect as invalidating the fixed-book control or fixed-book F1 certification.
- The sweep's robust candidate key, `174357490c9db17753b3eb6ef02e008ac32987800479bb124b3f5156488e27f0`,
  resolves to the hand-built F1 seed: template 63/126-day ranking, SelectTop 19, 180-DTE roll,
  and 40% budget.
- That exact immutable seed was certified separately in study `6a63a0cee490b0ae31ed3569`; the PASS
  verdict relies on the fixed study, not the defective sweep training rows.

## Required platform follow-up

Trace fold-index propagation and cache keys when the walk-forward runner persists a sweep
individual's `trainingStatistics`. Add a regression test asserting different anchored training
windows cannot silently reuse fold-zero statistics.
