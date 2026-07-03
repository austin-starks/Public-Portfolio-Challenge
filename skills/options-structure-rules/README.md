# options-structure-rules

> The hard structural constraints for the Public Portfolio Challenge momentum-LEAP options book — the spread-shape rule, the take-profit convexity-cap footgun, the affordability ladder, and the known losers not to re-test. Use whenever building or auditing an options strategy structure, checking spread-shape compliance before a certification, choosing DTE/strike rungs, or deciding whether a proposed structure change is even allowed. A violation is an automatic certification FAIL.

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
# Claude Code   → ~/skills/options-structure-rules
# Codex CLI     → ~/.agents/skills/options-structure-rules
# Gemini CLI    → ~/.gemini/skills/options-structure-rules
# Cursor (proj) → .cursor/rules/options-structure-rules
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/options-structure-rules` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
