# lockbox-holdout

The single-touch lockbox — a final anti-overfitting holdout run once, after design freeze, on a window held out from every fold, sweep, and search. Use when finalizing a bakeoff winner before deploy, setting up the A/B/C baselines as OOS bars, or running the S1.5 gate-coherence auto-relax. Covers why looking at the lockbox twice burns it, the lockbox pass conditions, and the three baselines. The lockbox is distinct from the walk-forward OOS folds.

## Activation

Invoke with `/lockbox-holdout`, or let it auto-activate when a task matches the description above.
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
