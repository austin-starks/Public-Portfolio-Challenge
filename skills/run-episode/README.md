# run-episode

> The single entry point that executes a Public Portfolio Challenge episode or attempt runbook end-to-end, delegating each stage to the functional skills. Use when asked to run/execute/replay an episode — e.g. 'run episode 10', 'execute episode 11 attempt 3', 'run the bakeoff', 'replay the runbook' — with the NexusTrade MCP connected. Reads the target runbook, pins its real artifacts (IDs, the incumbent bar), sequences the stages, and stops at the gated deploy. It orchestrates; the functional skills do the work.

A cross-platform agent skill on the [Agent Skills open standard](https://agentskills.io)
(`SKILL.md` + `AGENTS.md`). Part of the **Public Portfolio Challenge** skills library.

## Install

### Auto-detect (recommended)

```bash
./install.sh                 # detect your tool, install user-level
./install.sh --all           # install to every detected tool
./install.sh --platform codex        # or: claude-code, cursor, gemini, copilot, ...
./install.sh --project       # into the current repo instead of user-level
./install.sh --dry-run       # preview, no changes
```

Already using Claude Code / Codex / OpenCode in the `public-portfolio-challenge` repo? The
committed `.claude/skills` and `.agents/skills` symlinks point at `../skills`, so it's active
on clone — no install needed.

## Use

Start a new session and type `/run-episode` (e.g. `/run-episode 11 attempt 3`), or describe a
matching task and it auto-activates. Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (orchestration order + per-episode delegation)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `install.sh` — cross-platform installer
