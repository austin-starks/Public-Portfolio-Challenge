# sweep-reoptimization

> Re-optimize a NexusTrade strategy with a walk-forward SWEEP and label parameter provenance — the discipline that prevents deploying inherited knobs. Use whenever a structural change (sizing, rung depth, universe membership, DTE family, adding a rank signal) forces a re-sweep, when authoring gene_intents from get_sweep_surface, when choosing sweep over GA for a deploy cert, or when selecting the cross-fold-robust winner instead of the per-fold argmax. Invoke with the NexusTrade MCP connected.

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
# Claude Code   → ~/skills/sweep-reoptimization
# Codex CLI     → ~/.agents/skills/sweep-reoptimization
# Gemini CLI    → ~/.gemini/skills/sweep-reoptimization
# Cursor (proj) → .cursor/rules/sweep-reoptimization
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/sweep-reoptimization` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
