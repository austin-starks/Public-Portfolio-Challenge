# run-episode

The single entry point that executes a Public Portfolio Challenge episode or attempt runbook end-to-end, delegating each stage to the functional skills. Use when asked to run/execute/replay an episode — e.g. 'run episode 10', 'execute episode 11 attempt 3', 'run the bakeoff', 'replay the runbook' — with the NexusTrade MCP connected. Reads the target runbook, pins its real artifacts (IDs, the incumbent bar), sequences the stages, and stops at the gated deploy. It orchestrates; the functional skills do the work.

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
episode-10 / episode-11 certification runbooks. See the library index at
[../README.md](../README.md).
