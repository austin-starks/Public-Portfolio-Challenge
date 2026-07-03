# strategy-bakeoff

> Run a multi-family strategy bakeoff — the SEARCH→CERTIFY funnel that screens many candidate mechanisms down to a certified deploy winner without letting the cheap search layer issue a verdict. Use when replaying the Episode 10 bakeoff, when exploring several distinct strategy families before certifying, when deciding whether "no deployable winner" is even a legal conclusion, or when building the per-family certification ledger. Enforces verdict-integrity: only certification can end a campaign.

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
# Claude Code   → ~/skills/strategy-bakeoff
# Codex CLI     → ~/.agents/skills/strategy-bakeoff
# Gemini CLI    → ~/.gemini/skills/strategy-bakeoff
# Cursor (proj) → .cursor/rules/strategy-bakeoff
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/strategy-bakeoff` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
