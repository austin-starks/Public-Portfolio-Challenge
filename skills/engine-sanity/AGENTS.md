# engine-sanity

The mandatory pre-flight contract checks (Stage S0) that must pass before trusting NexusTrade's certification engine for any strategy work. Use at the start of a bakeoff or certification campaign to prove the walk-forward engine runs end-to-end, windows don't leak, fold winners persist, and the engine doesn't fabricate values for dead/not-yet-listed names. Each check has a STOP-and-report failure mode; these runs do NOT count toward any certification minimum.

## Activation

Invoke with `/engine-sanity`, or let it auto-activate when a task matches the description above.
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
