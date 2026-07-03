# walk-forward-oos

Run and read a NexusTrade walk-forward out-of-sample study — the certification engine behind the Public Portfolio Challenge. Use when certifying a fixed portfolio (backtest_only) or re-optimizing one (sweep), when setting fold_count / anchored / validation / embargo params, when monitoring a run_walk_forward_study to completion, when reading per-fold OOS returns/Sortino/drawdown, or when a variant's fold calendar needs calendar-alignment against a base control. Invoke with the NexusTrade MCP connected.

## Activation

Invoke with `/walk-forward-oos`, or let it auto-activate when a task matches the description above.
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
