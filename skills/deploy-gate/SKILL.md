---
name: deploy-gate
description: "The GATED deploy + cleanup flow for a NexusTrade live book — clone the finalist, preview a delta reconcile, stage UNAPPROVED orders, verify fills. Use ONLY after the human explicitly says \"deploy + clean up\" and names a finalist. Covers the clone-before-reconcile ordering, the single-tick reconcile expectation, stale-pending-order hygiene, the signal-freshness gate, and why you can never approve orders yourself. Nothing here runs during certification."
license: MIT
metadata:
  author: Austin Starks
  version: 1.0.0
  created: 2026-07-03
  last_reviewed: 2026-07-03
  review_interval_days: 90
activation: /deploy-gate
provenance:
  maintainer: Austin Starks
  source: public-portfolio-challenge episode-10 runbooks
---

# Deploy Gate (Stage E — GATED)

**Nothing deploys and no orders are placed until the human explicitly says "deploy + clean up"** and
names the specific finalist. This skill only runs then. Goal: make the live positions equal a **fresh
deploy of the chosen finalist today** via **delta** trades (don't round-trip overlaps).

## Pre-deploy gates (hard)

0. **Signal-freshness gate.** A finalist whose alt-data series does not extend to the present with a
   working refresh path may NOT deploy, whatever its cert says — a stale rank series is a dead book.
1. **Stale pending orders FIRST.** Check the live book for pending/`Pending User Approval → Canceled`
   orders — they **block new staging**. Surface them; the human cancels in the UI. Note
   `automaticOrderApproval` state (default: leave as-is unless told to flip it at deploy).

## The five steps

1. **Clone the finalist onto the live book FIRST** — `clone_strategies_to_portfolio` (source =
   finalist, target = live book), then field-verify the clone. This IS the "deploy": it sets the live
   book's strategies that the next step reconciles against. `reconcile_portfolio_to_strategy` has **no
   `strategy_source` arg** — it reconciles the live book against **its own** strategies, so the clone
   must happen first. *If the finalist is the already-deployed live book unchanged, no clone is needed —
   say so.*
2. **Reconcile preview** — `reconcile_portfolio_to_strategy({ portfolio_id: "<live>", mode: "delta" })`.
   **Preview-only — it never places orders.** Returns `target`, `current`, `orders` (already in
   `create_orders` shape), estimated cost, realized P&L, and wash-sale flags. Expect a **single-tick
   target** — the live strategy accretes the rest over daily rebalances. Say so; don't re-diagnose it
   as a bug.
3. **Show the human the preview and get explicit approval.** Sanity-check: orders touch only the delta
   (overlaps untouched), costs sane, `target` == a fresh deploy, and — for a participation fix — the
   target spans multiple names, not just one.
4. **Stage the orders** — `create_orders({ portfolio_id: "<live>", orders: <the orders array from
   step 2> })`. Staged **UNAPPROVED**; the tool never submits to the broker. **The human approves them
   manually in the NexusTrade UI** — there is no approval tool and you cannot approve them. Options
   auto-stage as LIMIT.
5. **Verify after fills** — re-run the reconcile preview; the delta `orders` array should be ~empty.
   Report fills, any remainder, realized P&L, wash-sale flags, and the resulting live participation
   (distinct names held).

## Rules

- Default `mode: "delta"`. Only use `"liquidate_all"` if the human explicitly asks for a clean
  cost-basis reset.
- Never run this without an explicit go for that **specific** finalist.
- Discover the live target via `fetch_portfolios` when it isn't already pinned in the run — never
  hardcode a live portfolio id you haven't confirmed by field/posture.
- On sign-off, re-attach any weekly monitor agent the deploy expects.
