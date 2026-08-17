# strategy-bakeoff

Run a multi-family strategy bakeoff — the SEARCH→CERTIFY funnel that screens many candidate mechanisms down to a certified deploy winner without letting the cheap search layer issue a verdict. Use when replaying the Episode 10 bakeoff, when exploring several distinct strategy families before certifying, when deciding whether "no deployable winner" is even a legal conclusion, or when building the per-family certification ledger. Enforces verdict-integrity: only certification can end a campaign.

## Activation

Invoke with `/strategy-bakeoff`, or let it auto-activate when a task matches the description above.
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
