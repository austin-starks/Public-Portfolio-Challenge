# Diagnose: systematic direct-OpenOption sweep terminates before any evaluation

## Resolution status — 2026-07-20

**CLOSED by the shipped engine fix.** Post-fix walk-forward study `6a5da1d09dffb90d2c07de8a`
successfully evaluated the direct-OpenOption seed and persisted a fold winner. The three IDs below
remain quarantined historical artifacts. Certification is still blocked by the separate option-fee
fidelity failure documented in `WALK_FORWARD_OPTION_FEE_FIDELITY_BUG.md`.

## One-line

Three exhaustive minute-option sweeps—including a non-DTE moneyness/take-profit/cadence grid—ended
`ERROR` with 0 evaluations, blocking server-side parameter re-optimization and materialization even
though their gene plans compiled without warnings. The non-DTE reproduction disproves DTE mutation as
a necessary cause and points to a broader direct-OpenOption sweep dispatch failure.

## Expected vs observed

- **Expected:** the optimizer should evaluate all 27 combinations in `6a5ce9053f94098f5434f34d`, or
  all three DTE values in minimal reproduction `6a5ce95a14879ee3b06ddb08`, then materialize ranked
  portfolios with training and validation statistics.
- **Observed:** both optimizers reached terminal `ERROR` in seconds with `evaluationsDone: 0`, an empty
  leaderboard, no materialized portfolios, and no diagnostic error exposed by
  `get_optimization_results`. Both launches reported complete gene compilation and no warnings.

## Reproduction

- Portfolio: `6a5ce81814879ee3b06dd8e6` (`$8,000`; MU/SNDK; four outright-long one-leg call/put entries;
  15–30 DTE seed; one global open-position gate; intraday close; broad 0–3650 DTE cooldown filters;
  +100% TP / −50% SL; no spreads; automatic approval off).
- Full sweep: `6a5ce9053f94098f5434f34d` — 2026-01-02 through 2026-04-30, Minute, exhaustive 27 cells:
  DTE 3–10/10–21/21–45 × 5%/10%/15% OTM × 75%/100%/150% TP. Terminal `ERROR`, 0/27.
- Minimal reproduction: `6a5ce95a14879ee3b06ddb08` — same portfolio/window/interval, exhaustive
  DTE-only 3–10/10–21/21–45. Terminal `ERROR`, 0/3.
- Non-DTE corroboration: `6a5cf47e05df5ce63265966d` — F2 direct-OpenOption seed
  `6a5cf368392c6f50da48e7d6`, same window/interval, exhaustive 27 cells across all-leg strike
  distance 5/10/15% OTM, TP 50/75/100%, and entry cooldown 0/1/2 days. Terminal `ERROR`, 0/27.
- `get_optimization_results` exposes the frozen template and compiled genes but no worker error;
  `status: ERROR`, `materialized: false`, and empty `portfolios`/`leaderboard` are the hard evidence.

## Leading hypothesis (verify, don't assume)

**Hypothesis:** the worker fails while cloning or dispatching direct-OpenOption sweep templates before
the first evaluation. The non-DTE reproduction removes `OptionLeg.DteBracket` as a necessary cause.
The missing terminal diagnostic in the read endpoint is a separate observability defect or symptom.

## Alternatives to rule out (so this isn't a false alarm)

1. **Template cloning.** The optimizer may be failing to clone this chat-portfolio template rather
   than to apply DTE. Test a no-DTE numeric gene on the same seed.
2. **Minute option-data preparation.** A common input preparation error could occur before every
   candidate. Test a single manually materialized DTE variant over the same window; ordinary search
   backtests for L1/L2/L3 already completed, which argues against a general data outage.
3. **DTE/cooldown coupling.** Cooldown filters were deliberately widened to 0–3650 DTE to prevent a
   stale selector, but an undocumented validator may require their DTE range to equal the option leg.
   If so, the sweep compiler should mutate the coupled fields or reject the plan during preview.

## Where to look

- Direct-OpenOption sweep template cloning and first-candidate dispatch, before gene-specific backtest
  evaluation begins.
- Optimizer job dispatch/error persistence between template cloning and evaluation 1, plus the
  `get_optimization_results` response mapping for terminal error details.

## Diagnostic checks

1. Apply one non-DTE genome from `6a5cf47e05df5ce63265966d` to its stored template and assert the
   portfolio serializes and passes the same validation used by `build_portfolio`.
2. A/B a direct-OpenOption seed with an equivalent RebalanceOption representation; if only the direct
   form fails before evaluation 1, the dispatch problem is isolated to portfolio shape.

## Impact on prior results (why this blocks conclusions)

Neither failed optimizer produced performance results, so no return or drawdown number is
quarantined. The two optimizer IDs themselves are invalid research artifacts and cannot rank or
materialize a winner. Attempt 7 must use explicit portfolio variants and ordinary backtests until the
sweep path is fixed; any future fixed-engine rerun must repeat the full 27-cell grid before deployment.
