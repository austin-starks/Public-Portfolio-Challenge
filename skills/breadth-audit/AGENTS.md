# breadth-audit

Measure a NexusTrade options book's TRUE participation at a fixed cold-start capital base, defeating the compounded-NAV breadth illusion. Use whenever a book's headline "holds N/21 names" needs validating, when a live book collapses to a single name (the OSCR trap), when checking whether a SelectTop / per-name-allocation / total-budget change degraded simultaneous participation, or when a certification needs a breadth gate. Uses audit_backtest_breadth at held-fixed $25k.

## Activation

Invoke with `/breadth-audit`, or let it auto-activate when a task matches the description above.
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
