# deploy-gate

The GATED deploy + cleanup flow for a NexusTrade live book — clone the finalist, preview a delta reconcile, stage UNAPPROVED orders, verify fills. Use ONLY after the human explicitly says "deploy + clean up" and names a finalist. Covers the clone-before-reconcile ordering, the single-tick reconcile expectation, stale-pending-order hygiene, the signal-freshness gate, and why you can never approve orders yourself. Nothing here runs during certification.

## Activation

Invoke with `/deploy-gate`, or let it auto-activate when a task matches the description above.
This is a `SKILL.md` skill on the open Agent Skills standard — Claude Code, Codex CLI,
Cursor, Gemini CLI, GitHub Copilot and ~15 other tools read it (natively or via the
`install.sh` adapter).

## Usage

See [SKILL.md](./SKILL.md) for the full workflow, triggers, hard constraints, and detail.
Reference material (if any) lives in [references/](./references/).

## Requirements

The **NexusTrade MCP server** must be connected — this skill drives NexusTrade's
deterministic backtest/certification/compute tools (deferred; load schemas via ToolSearch).

## Part of

The **Public Portfolio Challenge** skills library — a functional decomposition of the
episode-10 / episode-11 certification runbooks. See the library index at
[../README.md](../README.md).
