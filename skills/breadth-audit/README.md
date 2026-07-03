# breadth-audit

> Measure a NexusTrade options book's TRUE participation at a fixed cold-start capital base, defeating the compounded-NAV breadth illusion. Use whenever a book's headline "holds N/21 names" needs validating, when a live book collapses to a single name (the OSCR trap), when checking whether a SelectTop / per-name-allocation / total-budget change degraded simultaneous participation, or when a certification needs a breadth gate. Uses audit_backtest_breadth at held-fixed $25k.

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
# Claude Code   → ~/skills/breadth-audit
# Codex CLI     → ~/.agents/skills/breadth-audit
# Gemini CLI    → ~/.gemini/skills/breadth-audit
# Cursor (proj) → .cursor/rules/breadth-audit
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/breadth-audit` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
