# bug-protocol

The "loudly declare" protocol for platform, engine, or data bugs during a NexusTrade certification campaign — bugs are a first-class deliverable, not something to route around. Use whenever a NexusTrade tool errors, hangs, or returns numbers that contradict the config; whenever you're tempted to write "probably an engine quirk"; or when a discovered bug invalidates prior backtests and results must be quarantined. Includes the bug hand-off doc template (see references/BUG_TEMPLATE.md).

## Activation

Invoke with `/bug-protocol`, or let it auto-activate when a task matches the description above.
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
Episode 10 certification runbooks. See the library index at
[../README.md](../README.md).
