# alt-data-indicators

Build alternative-data custom indicators on NexusTrade (Reddit/WSB mentions, congressional disclosures, insider filings, news-flow) and wire them into a certified book as a rank/tilt/filter signal. Use when adding alt-data to a strategy, building a CustomIndicator via compute sessions, auditing lookahead safety or per-ticker coverage, or deciding whether a data series is dense enough to drive a rank. Covers the compute-session workflow, the sparse-series rule, and source recipes (see references/). Invoke with the NexusTrade MCP connected.

## Activation

Invoke with `/alt-data-indicators`, or let it auto-activate when a task matches the description above.
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
