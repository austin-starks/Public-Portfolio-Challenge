# alt-data-indicators

> Build alternative-data custom indicators on NexusTrade (Reddit/WSB mentions, congressional disclosures, insider filings, news-flow) and wire them into a certified book as a rank/tilt/filter signal. Use when adding alt-data to a strategy, building a CustomIndicator via compute sessions, auditing lookahead safety or per-ticker coverage, or deciding whether a data series is dense enough to drive a rank. Covers the compute-session workflow, the sparse-series rule, and source recipes (see references/). Invoke with the NexusTrade MCP connected.

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
# Claude Code   → ~/skills/alt-data-indicators
# Codex CLI     → ~/.agents/skills/alt-data-indicators
# Gemini CLI    → ~/.gemini/skills/alt-data-indicators
# Cursor (proj) → .cursor/rules/alt-data-indicators
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/alt-data-indicators` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
