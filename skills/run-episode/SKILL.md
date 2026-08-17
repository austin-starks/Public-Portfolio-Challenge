---
name: run-episode
description: "The single entry point that executes a Public Portfolio Challenge episode or addendum runbook end-to-end, delegating each stage to the functional skills. Use when asked to run/execute/replay Episode 10, its bakeoff, or its addendum with the NexusTrade MCP connected. Reads the target runbook, pins its real artifacts (IDs, the incumbent bar), sequences the stages, and stops at the gated deploy. It orchestrates; the functional skills do the work."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /run-episode
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 runbooks
---

# Run Episode

The **orchestrator entry point** for the Public Portfolio Challenge. Every episode is a specific job
over specific real artifacts, but the *discipline* is the same and lives in the functional skills. This
skill picks the right runbook, pins its artifacts, and runs the stages **in order**, delegating each to
the skill that owns it. It does not re-implement the discipline — it sequences it.

## Invocation

```
/run-episode <episode>[ <attempt>]
```

Examples: `/run-episode 10` · `/run-episode 10 addendum` · "run the episode-10 bakeoff".

## First: load the actual runbook (it is the source of truth for THIS run)

Read the target runbook and treat it as authoritative for the job + artifacts (this skill only encodes
the *ordering* and *delegation*):

| Episode | Runbook | Shape |
|---|---|---|
| 10 | `episode-10/BAKEOFF_RUNBOOK.md` | Multi-family **bakeoff** (search→certify→lockbox→deploy) |
| 10 / addendum | `episode-10/addendum/RUNBOOK.md` | **Redesign entries + exits**, prove sell behavior and retain the incumbent edge |

From the runbook, pin before doing anything: the SUBJECT (live book / build) IDs, the incumbent bar
(cert study id + per-fold numbers), the fixed universe + capital, and any carried-over artifacts. The
runbook's own Stage list wins if it disagrees with the generic ordering below.

## The bookend rules (fixed for every episode)

- **Stage A first** — confirm the SUBJECT by FIELD (`get_portfolio` → `conditionFieldAudit`), re-verify
  the incumbent bar, spot-check one fresh backtest, and (if live) check pending orders +
  `automaticOrderApproval`. Deliver a one-paragraph *before* state.
- **Deploy last, and GATED** — no clone, no reconcile, no orders until the human says the episode's
  explicit go phrase ("deploy + clean up"). See **deploy-gate**.
- **Bugs are a deliverable at every stage** — **bug-protocol** on any failure; quarantine tainted results.
- **Verify, don't assert** — every engine-behavior claim checked against events/fields/repro (via
  **portfolio-certification**'s first principles) before it lands in the log.

## Episode 10 — the bakeoff sequence

Delegates, in order:

1. **engine-sanity** — S0 contract checks. STOP on any failure. (These don't count toward the cert body.)
2. **lockbox-holdout** — load A/B/C baselines as OOS bars (S1); run the **S1.5** gate-coherence auto-relax.
3. **strategy-bakeoff** — the SEARCH→CERTIFY funnel: ≥3 families, per-family ledger, verdict-integrity.
   Each promoted seed is certified through **walk-forward-oos** + **breadth-audit**, held to
   **options-structure-rules** (hard gates) and **sweep-reoptimization** (re-sweep from a clean seed).
4. **lockbox-holdout** — the **single-touch** lockbox confirmation on the frozen finalist (S2).
5. **deploy-gate** — GATED. Discover the live target via `fetch_portfolios`, owner-confirm, clone,
   field-verify, re-attach monitoring.

## Episode 10 addendum — entry and exit redesign

The addendum follows the same certification spine with a redesigned middle:

1. **Stage A** baseline + inventory (bookend rule above).
2. **Entry + exit redesign:** current-engine authoring/sweep inventory → matched entry/exit mechanism
   families → event-level exit-binding audit → **sweep-reoptimization** on the promoted design →
   fixed-config **walk-forward-oos** vs a fresh control.
3. **options-structure-rules** hard-gate + **breadth-audit** gate on every finalist.
4. **Present, then stop** — verdict up top, per-fold OOS table, side-by-side vs incumbent, provenance
   labels, honest caveats, bug ledger. **No deploy.**
5. **deploy-gate** — GATED on the explicit go, for the named finalist only.

## What this skill guarantees

- The **bookends are never skipped** (Stage-A field-verify first; deploy gated last).
- Each stage runs through the skill that owns its checks, so the **verdict is holistic OOS**, breadth is
  at **fixed $25k**, structural changes force a **re-sweep**, and every parameter carries **provenance**.
- A **null result is a valid outcome** — the orchestrator does not torture variants to manufacture a win.

If the target runbook adds, renames, or reorders stages, follow the runbook — this skill is the default
spine, not an override.
