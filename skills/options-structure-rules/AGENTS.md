# options-structure-rules

The hard structural constraints for the Public Portfolio Challenge momentum-LEAP options book — the spread-shape rule, the take-profit convexity-cap footgun, the affordability ladder, and the known losers not to re-test. Use whenever building or auditing an options strategy structure, checking spread-shape compliance before a certification, choosing DTE/strike rungs, or deciding whether a proposed structure change is even allowed. A violation is an automatic certification FAIL.

## Activation

Invoke with `/options-structure-rules`, or let it auto-activate when a task matches the description above.
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
