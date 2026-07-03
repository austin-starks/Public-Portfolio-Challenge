# Public Portfolio Challenge — Skills Library

The certification discipline from the Public Portfolio Challenge runbooks, decomposed into composable
agent skills on the open [`SKILL.md` standard](https://agentskills.io) (Claude Code, Codex CLI, Cursor,
Gemini CLI, Copilot, and ~15 other tools). Instead of pasting a 730-line runbook into a fresh agent,
connect the **NexusTrade MCP** and let the agent auto-invoke the skill that fits the task. Each skill is
one function of the discipline; they cross-reference each other by name. **`run-episode`** is the
top-level entry point that sequences a whole episode.

The episode runbooks (`episode-10/`, `episode-11/`) remain as the worked examples these skills distill.

## The skills

| Skill | What it does |
|---|---|
| **run-episode** | **Entry point** — `/run-episode 10` or `/run-episode 11 attempt 3`: loads the runbook, pins artifacts, and sequences the stages, delegating each to the skill below. |
| **portfolio-certification** | Umbrella orchestrator — the staged PASS/FAIL run, first principles, the holistic verdict. Pulls in the rest. |
| **walk-forward-oos** | The certification engine: `run_walk_forward_study` params, monitoring, per-fold OOS checks, calendar alignment. |
| **breadth-audit** | True participation at fixed $25k — defeats the compounded-NAV breadth illusion (the OSCR-collapse). |
| **sweep-reoptimization** | Re-sweep on any structural change; gene authoring; robust (not argmax) winner selection; provenance labels. |
| **options-structure-rules** | Hard constraints: spread-shape rule, convexity-cap footgun, affordability ladder, known losers. |
| **alt-data-indicators** | Build custom indicators (Reddit/WSB, congressional, insider, news) and wire them as rank/tilt/filter signals. |
| **bug-protocol** | "Loudly declare" — bugs are a first-class deliverable; characterize, log, hand-off doc, quarantine results. |
| **deploy-gate** | The GATED Stage-E deploy: clone → delta reconcile preview → stage UNAPPROVED orders → verify fills. |
| **engine-sanity** | Stage-S0 pre-flight contract checks that prove the certification engine is trustworthy before any design work. |
| **strategy-bakeoff** | The SEARCH→CERTIFY funnel: ≥3 families, the ledger, verdict-integrity (only certification can end a campaign). |
| **lockbox-holdout** | The single-touch 126-day final holdout, the A/B/C baselines, and the S1.5 gate-coherence auto-relax. |

## How they compose

A full campaign typically flows:

```
run-episode  ─▶  engine-sanity → strategy-bakeoff ─┬─ options-structure-rules (hard gates)
(reads the runbook,                                ├─ sweep-reoptimization (per-seed)
 sequences the stages)                             ├─ alt-data-indicators   (signal variants)
                                                   └─ walk-forward-oos + breadth-audit (certify)
                                                         → lockbox-holdout (final confirm)
                                                         → deploy-gate (only on "deploy + clean up")
```

**run-episode** is the top-level entry point (it sequences a whole episode); **portfolio-certification**
is the umbrella discipline the stages share; **bug-protocol** applies at every stage.

## Install (any tool)

These are `SKILL.md` skills on the [open, cross-tool standard](https://agentskills.io) — the **same
`skills/` folder is the one canonical copy**, read by Claude Code, Codex CLI, Cursor, Gemini CLI,
Copilot, and ~15 others.

### Clone → already active (Claude Code · Codex · OpenCode)

The repo commits two discovery symlinks that point back at this folder — no second copy, no install step:

```
.claude/skills  → ../skills      # Claude Code
.agents/skills  → ../skills      # Codex CLI (primary), OpenCode/Gemini/Goose (fallback)
```

So a fresh `git clone` + opening any of those agents in the repo picks up all 12 skills immediately
(alongside the MCP wiring the repo already ships in `.codex/config.toml` / `opencode.jsonc`). Symlinks
work on macOS/Linux/WSL; on native Windows, enable git symlinks or use `install.sh` below.

### Every other tool → one command

`install.sh` copies each skill into your tool's own skills path and generates the native adapter where
needed (Cursor `.mdc`, Windsurf/Trae/Cline/Roo/Kilo `.md` rules, Junie `guidelines.md`), plus the
`AGENTS.md` companion.

```bash
cd skills

./install.sh --list                 # show the 12 skills
./install.sh --dry-run              # preview, no changes
./install.sh                        # auto-detect your tool, install user-level
./install.sh --platform cursor --project   # into ./.cursor/rules/ for this repo
./install.sh --all                  # every detected tool at once
```

Supported `--platform` values: `claude-code, copilot, cursor, windsurf, cline, codex, gemini, kiro,
trae, goose, opencode, roo-code, kilo-code, factory, junie, antigravity, universal`.

The installer is adapted from [agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skill-creator)'s
`install-template.sh`, generalized from one skill to the whole library. To author *new* cross-platform
skills, install that tool and run `/agent-skill-creator <describe your workflow>`:

```bash
curl -fsSL https://raw.githubusercontent.com/FrancyJGLisboa/agent-skill-creator/main/scripts/bootstrap.sh | sh
```

## Requirements

- The **NexusTrade MCP server** connected (its tools are deferred — load schemas via ToolSearch as
  needed).
- Operates on real artifacts (live book, builds, studies). Nothing deploys or places orders until an
  explicit "deploy + clean up" (see **deploy-gate**).
