# run-episode

The single entry point that executes the Public Portfolio Challenge Episode 10 or addendum runbook end-to-end, delegating each stage to the functional skills. Use when asked to run the Episode 10 bakeoff, replay its runbook, or execute its addendum with the NexusTrade MCP connected. Reads the target runbook, pins its real artifacts, sequences the stages, and stops at the gated deploy.

## Activation

Invoke with `/run-episode`, or let it auto-activate when a task matches the description above.
This is a `SKILL.md` skill on the open Agent Skills standard — Claude Code, Codex CLI,
Cursor, Gemini CLI, GitHub Copilot and ~15 other tools read it (natively or via the
`install.sh` adapter).

## Usage

See [SKILL.md](./SKILL.md) for the full workflow, triggers, and per-episode delegation map.

## Requirements

The **NexusTrade MCP server** must be connected — this skill drives NexusTrade's
deterministic backtest/certification/compute tools (deferred; load schemas via ToolSearch).

## Part of

The **Public Portfolio Challenge** skills library — a functional decomposition of the
Episode 10 certification runbooks. See the library index at
[../README.md](../README.md).
