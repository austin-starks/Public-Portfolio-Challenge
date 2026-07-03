# portfolio-certification

Orchestrate an out-of-sample certification of a NexusTrade trading strategy or live book — the master discipline behind the Public Portfolio Challenge. Use whenever you must decide PASS/FAIL on whether a portfolio holds up out of sample before deploying real money, replaying the episode-10/episode-11 runbooks, or running a "certify my book" / "prove it out of sample" / "re-certify the fix" task with the NexusTrade MCP connected. Pulls in walk-forward-oos, breadth-audit, sweep-reoptimization, options-structure-rules, bug-protocol, and deploy-gate.

## Activation

Invoke with `/portfolio-certification`, or let it auto-activate when a task matches the description above.
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
