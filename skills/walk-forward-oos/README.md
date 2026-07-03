# walk-forward-oos

> Run and read a NexusTrade walk-forward out-of-sample study — the certification engine behind the Public Portfolio Challenge. Use when certifying a fixed portfolio (backtest_only) or re-optimizing one (sweep), when setting fold_count / anchored / validation / embargo params, when monitoring a run_walk_forward_study to completion, when reading per-fold OOS returns/Sortino/drawdown, or when a variant's fold calendar needs calendar-alignment against a base control. Invoke with the NexusTrade MCP connected.

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

The installer copies this skill into your tool's native skills path and generates the
native adapter where needed (Cursor `.mdc`, Windsurf/Trae/Cline/Roo/Kilo `.md` rules,
Junie `guidelines.md`), plus a universal `~/.agents/skills/` symlink.

### Manual (git clone this repo, then point your tool at this folder)

```bash
# Claude Code   → ~/skills/walk-forward-oos
# Codex CLI     → ~/.agents/skills/walk-forward-oos
# Gemini CLI    → ~/.gemini/skills/walk-forward-oos
# Cursor (proj) → .cursor/rules/walk-forward-oos
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/walk-forward-oos` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
