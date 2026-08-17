# portfolio-certification

> Orchestrate an out-of-sample certification of a NexusTrade trading strategy or live book — the master discipline behind the Public Portfolio Challenge. Use whenever you must decide PASS/FAIL on whether a portfolio holds up out of sample before deploying real money, replaying the Episode 10 runbooks, or running a "certify my book" / "prove it out of sample" / "re-certify the fix" task with the NexusTrade MCP connected. Pulls in walk-forward-oos, breadth-audit, sweep-reoptimization, options-structure-rules, bug-protocol, and deploy-gate.

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
# Claude Code   → ~/skills/portfolio-certification
# Codex CLI     → ~/.agents/skills/portfolio-certification
# Gemini CLI    → ~/.gemini/skills/portfolio-certification
# Cursor (proj) → .cursor/rules/portfolio-certification
cp -R . <one-of-the-paths-above>
```

This repo's canonical copy of the skill is `skills/` — point any tool straight at it, or run `./install.sh`.

## Use

Start a new session and type `/portfolio-certification` (or just describe a matching task and it
auto-activates). Requires the **NexusTrade MCP** server connected.

## Files

- `SKILL.md` — the skill (workflow, constraints, triggers)
- `AGENTS.md` — companion instruction file for AGENTS.md-first tools
- `references/` — on-demand detail (present on skills that need it)
- `install.sh` — cross-platform installer
