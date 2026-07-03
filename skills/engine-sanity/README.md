# engine-sanity

> The mandatory pre-flight contract checks (Stage S0) that must pass before trusting NexusTrade's certification engine for any strategy work. Use at the start of a bakeoff or certification campaign to prove the walk-forward engine runs end-to-end, windows don't leak, fold winners persist, and the engine doesn't fabricate values for dead/not-yet-listed names. Each check has a STOP-and-report failure mode; these runs do NOT count toward any certification minimum.

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
# Claude Code   → ~/skills/engine-sanity
# Codex CLI     → ~/.agents/skills/engine-sanity
# Gemini CLI    → ~/.gemini/skills/engine-sanity
# Cursor (proj) → .cursor/rules/engine-sanity
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/engine-sanity` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
