# Diagnose: Fly optimizer wake returns HTTP 500 before fold 0

## One-line

The first qualifying 112-unit F2 walk-forward launch compiled and previewed successfully but failed
while waking Fly optimizer capacity, leaving study `6a5dc72cea0d6db55c693cd7` and optimizer
`6a5dc72cea0d6db55c693cdb` terminal `ERROR` at 0 units with `fly_api_error: Request failed with
status code 500`.

## Reproduction status — recovered after two failed launches

The exact frozen request was retried unchanged (name only changed) and failed identically. Retry study
`6a5dc798814d31180a1c2df1` and optimizer `6a5dc798814d31180a1c2df5` are terminal `ERROR` at
0/112 with the same Fly API 500. A later unchanged retry recovered: study
`6a5dd72aea0d6db55c694eeb` / optimizer `6a5dd72bea0d6db55c694ef5` completed all 112 units and
materialized all four fold winners. This proves the incident was recoverable at the same workload,
but does not erase the two quarantined 500 artifacts or explain the control-plane failure.

## Expected vs observed

- **Expected:** the validated 27-cell, four-fold study should create a root optimizer, transition to
  RUNNING, and evaluate 112 planned units.
- **Observed:** the launch call returned a walk-forward error; the persisted study is `ERROR`,
  `rootOptimizerId:null`, folds 0/4 complete, and units 0/112. A separately persisted optimizer exists
  in `ERROR` at 0/112, so no candidate backtest began.

## Reproduction

- Portfolio: `6a5cf368392c6f50da48e7d6` ($8,000; MU/SNDK; four outright-long one-leg
  call/put entries; no spreads; intraday exits; automatic approval off).
- Preview: four anchored folds over 2026-01-02 through 2026-07-10; 27 exhaustive cells from DTE
  1/3-10/10-21 x strike 5/10/15% OTM x take-profit 75/150/300%; 112 planned units; 165.95
  estimated tokens; no warnings.
- Study: `6a5dc72cea0d6db55c693cd7`; optimizer: `6a5dc72cea0d6db55c693cdb`.
- Exact error: `fly_api_error: Request failed with status code 500`.
- Exact retry: study `6a5dc798814d31180a1c2df1`; optimizer `6a5dc798814d31180a1c2df5`;
  same error, 0/112.

## Leading hypothesis (verify, don't assume)

The failure occurred in the infrastructure wake boundary, not sweep compilation or backtesting.
`stageWakeChargeAndQueueOptimizer` calls `flyMachineService.ensureWorkersForJobs` before queueing;
`ensureWorkersForJobs` maps a Fly list/start exception to `fly_api_error`. The missing study root ID,
persisted optimizer at 0 units, and successful same-engine S0 immediately beforehand support this
classification. Whether the Fly 500 is transient or workload/capacity-dependent is unverified.

## Alternatives to rule out (so this isn't a false alarm)

1. **Invalid sweep config.** Ruled out: `preview_only:true` compiled all three axes, produced the
   expected 27 cells/four folds, and returned no warnings.
2. **Backtest engine regression.** Ruled down: no evaluation started, and fresh S0 study
   `6a5dc4c82ee25ecab46ba437` had just completed 8/8 units with exact replay parity.
3. **Transient Fly control-plane failure.** Ruled down by one exact retry with the same terminal
   error and zero work. A persistent Fly outage remains possible; inspect the upstream response.

## Where to look

- Fly optimizer machine `listMachines` / `startMachine` response body and status around
  2026-07-20 06:58:52Z.
- `stageWakeChargeAndQueueOptimizer` and `ensureWorkersForJobs`: persist the upstream Fly response
  body/request ID and make study-to-error-optimizer linkage visible even when root creation throws.

## Diagnostic checks

1. Inspect the exact Fly API response body/request ID for both timestamps and verify configured
   optimizer machines can be listed and started outside the launch path.
2. After fixing the wake path, compare a smaller wake and the 112-unit four-fold wake to determine
   whether `machinesNeeded` or a specific Fly machine causes the 500.

## Impact on prior results

No strategy result exists in the two failed launches because zero units ran. Their study and optimizer
IDs remain quarantined infrastructure artifacts and cannot count toward certification. S0 remains
valid. The fresh recovered study `6a5dd72aea0d6db55c694eeb` is the qualifying post-fix F2 result.

## Current status

**RECOVERED, ROOT CAUSE OPEN.** The same 112-unit request eventually completed, so strategy research
can continue. The wake path should still retain the upstream Fly response body/request ID so a future
500 can be attributed without inference.
