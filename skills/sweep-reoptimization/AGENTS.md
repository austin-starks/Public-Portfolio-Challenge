# sweep-reoptimization

Re-optimize a NexusTrade strategy with a walk-forward SWEEP and label parameter provenance — the discipline that prevents deploying inherited knobs. Use whenever a structural change (sizing, rung depth, universe membership, DTE family, adding a rank signal) forces a re-sweep, when authoring gene_intents from get_sweep_surface, when choosing sweep over GA for a deploy cert, or when selecting the cross-fold-robust winner instead of the per-fold argmax. Invoke with the NexusTrade MCP connected.

## Activation

Invoke with `/sweep-reoptimization`, or let it auto-activate when a task matches the description above.
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
