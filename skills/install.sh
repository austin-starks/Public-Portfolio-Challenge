#!/bin/sh
# install.sh — Cross-platform installer for the Public Portfolio Challenge skills library.
#
# Installs every skill in this directory (each subfolder containing a SKILL.md)
# into your AI coding agent's skills path, auto-detecting the platform and
# generating native format adapters where a tool doesn't read SKILL.md directly
# (Cursor .mdc, Windsurf rules, Trae/Cline/Roo/Kilo plain rules, Junie guidelines).
#
# Adapted from agent-skill-creator's install-template.sh (github.com/FrancyJGLisboa/
# agent-skill-creator), generalized from single-skill to a multi-skill library.
#
# POSIX-compatible (bash, dash, zsh, ash). Exit codes:
#   0 success · 1 validation failed · 2 platform not detected · 3 permission denied
set -eu

LIBRARY_NAME="public-portfolio-challenge"
VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -t 1 ]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; BLUE=''; BOLD=''; NC=''
fi
info()    { printf "${BLUE}[INFO]${NC}  %s\n" "$1"; }
success() { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()    { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
error()   { printf "${RED}[ERROR]${NC} %s\n" "$1" >&2; }

SUPPORTED_PLATFORMS="claude-code, copilot, cursor, windsurf, cline, codex, gemini, kiro, trae, goose, opencode, roo-code, kilo-code, factory, junie, antigravity, universal"

show_help() {
    cat <<EOF
${BOLD}install.sh${NC} — Install the ${BOLD}${LIBRARY_NAME}${NC} skills library (v${VERSION})

Installs all skills found in this directory (subfolders with a SKILL.md).

USAGE
    ./install.sh [OPTIONS]

OPTIONS
    --platform PLATFORM   One of: ${SUPPORTED_PLATFORMS}
    --project             Install at project level (current directory) instead of user-level
    --path PATH           Custom base install path (overrides detection)
    --all                 Install to ALL detected tool paths at once
    --list                List the skills that would be installed, then exit
    --dry-run             Show what would happen without making changes
    -h, --help            Show this help

EXAMPLES
    ./install.sh                       # Auto-detect platform, user-level
    ./install.sh --platform codex      # Force Codex CLI (~/.agents/skills/)
    ./install.sh --platform cursor --project
    ./install.sh --all                 # Every detected tool
    ./install.sh --dry-run
EOF
}

PLATFORM=""; PROJECT_LEVEL=false; CUSTOM_PATH=""; DRY_RUN=false; INSTALL_ALL=false; LIST_ONLY=false
parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --platform) [ $# -ge 2 ] || { error "Missing value for --platform"; exit 1; }; PLATFORM="$2"; shift 2 ;;
            --project)  PROJECT_LEVEL=true; shift ;;
            --path)     [ $# -ge 2 ] || { error "Missing value for --path"; exit 1; }; CUSTOM_PATH="$2"; shift 2 ;;
            --all)      INSTALL_ALL=true; shift ;;
            --list)     LIST_ONLY=true; shift ;;
            --dry-run)  DRY_RUN=true; shift ;;
            -h|--help)  show_help; exit 0 ;;
            *)          error "Unknown option: $1"; show_help; exit 1 ;;
        esac
    done
}

# Discover skills: every immediate subdirectory of SCRIPT_DIR that holds a SKILL.md.
SKILLS=""
discover_skills() {
    for d in "${SCRIPT_DIR}"/*/; do
        [ -f "${d}SKILL.md" ] || continue
        name="$(basename "$d")"
        SKILLS="${SKILLS} ${name}"
    done
    SKILLS="$(printf '%s' "$SKILLS" | sed 's/^ //')"
    if [ -z "$SKILLS" ]; then
        error "No skills found under ${SCRIPT_DIR} (expected subfolders each containing SKILL.md)."
        exit 1
    fi
}

validate_skill_md() {
    skill_md="$1"
    [ -f "$skill_md" ] || { error "SKILL.md not found: $skill_md"; exit 1; }
    [ "$(head -n 1 "$skill_md")" = "---" ] || { error "SKILL.md must start with YAML frontmatter (---): $skill_md"; exit 1; }
    found_name=false; found_desc=false; in_fm=false; n=0
    while IFS= read -r line; do
        n=$((n + 1))
        if [ "$n" -eq 1 ]; then in_fm=true; continue; fi
        if $in_fm && [ "$line" = "---" ]; then break; fi
        if $in_fm; then
            case "$line" in name:*) found_name=true ;; description:*) found_desc=true ;; esac
        fi
    done < "$skill_md"
    $found_name || { error "SKILL.md missing 'name': $skill_md"; exit 1; }
    $found_desc || { error "SKILL.md missing 'description': $skill_md"; exit 1; }
}

detect_platform() {
    if [ -n "$PLATFORM" ]; then
        case "$PLATFORM" in
            claude-code|copilot|cursor|windsurf|cline|codex|gemini|kiro|trae|goose|opencode|roo-code|kilo-code|factory|junie|antigravity|universal)
                info "Platform explicitly set to: ${PLATFORM}"; return 0 ;;
            *) error "Unknown platform: ${PLATFORM}"; error "Supported: ${SUPPORTED_PLATFORMS}"; exit 2 ;;
        esac
    fi
    if   [ -d "${HOME}/.claude" ]; then PLATFORM="claude-code"
    elif [ -d "${HOME}/.copilot" ] || [ -d ".github" ]; then PLATFORM="copilot"
    elif [ -d "${HOME}/.cursor" ] || [ -d ".cursor" ]; then PLATFORM="cursor"
    elif [ -d "${HOME}/.codeium/windsurf" ] || [ -d ".windsurf" ]; then PLATFORM="windsurf"
    elif [ -d "${HOME}/.cline" ] || [ -d ".clinerules" ]; then PLATFORM="cline"
    elif [ -d "${HOME}/.agents" ]; then PLATFORM="codex"
    elif [ -d "${HOME}/.gemini" ]; then PLATFORM="gemini"
    elif [ -d "${HOME}/.kiro" ] || [ -d ".kiro" ]; then PLATFORM="kiro"
    elif [ -d ".trae" ]; then PLATFORM="trae"
    elif [ -d "${HOME}/.roo" ] || [ -d ".roo" ]; then PLATFORM="roo-code"
    elif [ -d "${HOME}/.kilocode" ] || [ -d ".kilocode" ]; then PLATFORM="kilo-code"
    elif [ -d "${HOME}/.factory" ] || [ -d ".factory" ]; then PLATFORM="factory"
    elif [ -d ".junie" ]; then PLATFORM="junie"
    elif [ -d "${HOME}/.config/goose" ]; then PLATFORM="goose"
    elif [ -d "${HOME}/.config/opencode" ]; then PLATFORM="opencode"
    else
        error "Could not auto-detect a supported AI coding platform."
        error "Use --platform PLATFORM. Supported: ${SUPPORTED_PLATFORMS}"; exit 2
    fi
    info "Auto-detected platform: ${PLATFORM}"
}

detect_all_platforms() {
    ALL_PLATFORMS=""
    [ -d "${HOME}/.claude" ] && ALL_PLATFORMS="${ALL_PLATFORMS} claude-code"
    { [ -d "${HOME}/.copilot" ] || [ -d ".github" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} copilot"
    { [ -d "${HOME}/.cursor" ] || [ -d ".cursor" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} cursor"
    { [ -d "${HOME}/.codeium/windsurf" ] || [ -d ".windsurf" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} windsurf"
    { [ -d "${HOME}/.cline" ] || [ -d ".clinerules" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} cline"
    [ -d "${HOME}/.gemini" ] && ALL_PLATFORMS="${ALL_PLATFORMS} gemini"
    { [ -d "${HOME}/.kiro" ] || [ -d ".kiro" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} kiro"
    [ -d ".trae" ] && ALL_PLATFORMS="${ALL_PLATFORMS} trae"
    { [ -d "${HOME}/.roo" ] || [ -d ".roo" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} roo-code"
    { [ -d "${HOME}/.kilocode" ] || [ -d ".kilocode" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} kilo-code"
    { [ -d "${HOME}/.factory" ] || [ -d ".factory" ]; } && ALL_PLATFORMS="${ALL_PLATFORMS} factory"
    [ -d ".junie" ] && ALL_PLATFORMS="${ALL_PLATFORMS} junie"
    [ -d "${HOME}/.config/goose" ] && ALL_PLATFORMS="${ALL_PLATFORMS} goose"
    [ -d "${HOME}/.config/opencode" ] && ALL_PLATFORMS="${ALL_PLATFORMS} opencode"
    ALL_PLATFORMS="${ALL_PLATFORMS} codex"   # always include the universal ~/.agents path
    ALL_PLATFORMS="$(printf '%s' "$ALL_PLATFORMS" | sed 's/^ //')"
    [ -n "$ALL_PLATFORMS" ] || ALL_PLATFORMS="codex"
}

# Resolve the BASE skills dir for the active platform (skill dirs land under it).
resolve_base() {
    if [ -n "$CUSTOM_PATH" ]; then BASE="$CUSTOM_PATH"; return 0; fi
    if $PROJECT_LEVEL; then
        case "$PLATFORM" in
            claude-code) b=".claude/skills" ;; copilot) b=".github/skills" ;; cursor) b=".cursor/rules" ;;
            windsurf) b=".windsurf/rules" ;; cline) b=".clinerules/skills" ;; codex) b=".agents/skills" ;;
            gemini) b=".gemini/skills" ;; kiro) b=".kiro/skills" ;; trae) b=".trae/rules" ;;
            goose) b=".goose/skills" ;; opencode) b=".opencode/skills" ;; roo-code) b=".roo/skills" ;;
            kilo-code) b=".kilocode/skills" ;; factory) b=".factory/skills" ;; junie) b=".junie/skills" ;;
            antigravity) b=".agent/skills" ;; universal) b=".agents/skills" ;;
        esac
        BASE="$(pwd)/${b}"
    else
        case "$PLATFORM" in
            claude-code) BASE="${HOME}/.claude/skills" ;; copilot) BASE="${HOME}/.copilot/skills" ;;
            cursor) BASE="${HOME}/.cursor/rules" ;; windsurf) BASE="${HOME}/.codeium/windsurf/skills" ;;
            cline) BASE="${HOME}/.cline/skills" ;; codex) BASE="${HOME}/.agents/skills" ;;
            gemini) BASE="${HOME}/.gemini/skills" ;; kiro) BASE="${HOME}/.kiro/skills" ;;
            trae) BASE="${HOME}/.trae/rules" ;; goose) BASE="${HOME}/.config/goose/skills" ;;
            opencode) BASE="${HOME}/.config/opencode/skills" ;; roo-code) BASE="${HOME}/.roo/skills" ;;
            kilo-code) BASE="${HOME}/.kilocode/skills" ;; factory) BASE="${HOME}/.factory/skills" ;;
            junie) BASE="${HOME}/.junie/skills" ;; antigravity) BASE="${HOME}/.gemini/antigravity/skills" ;;
            universal) BASE="${HOME}/.agents/skills" ;;
        esac
    fi
}

# --- format adapters (per skill) ---
skill_body() { awk 'BEGIN{c=0} /^---$/{c++;next} c>=2{print}' "$1"; }
# Return the human-readable description: strip the `description:` key, then unwrap a
# surrounding double-quoted YAML scalar (unescaping \" and \\) so downstream prose is clean.
skill_desc() {
    in_fm=false; n=0; d=""
    while IFS= read -r line; do
        n=$((n + 1)); [ "$n" -eq 1 ] && { in_fm=true; continue; }
        $in_fm && [ "$line" = "---" ] && break
        $in_fm && case "$line" in description:*) d="$(echo "$line" | sed 's/^description:[[:space:]]*//')" ;; esac
    done < "$1"
    case "$d" in
        \"*\") d="$(printf '%s' "$d" | sed 's/^"//; s/"$//; s/\\"/"/g; s/\\\\/\\/g')" ;;
    esac
    printf '%s' "$d"
}
# Re-emit text as a safe double-quoted YAML scalar (escape \ and ").
yaml_quote() { printf '"%s"' "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"; }

generate_cursor_mdc() {
    name="$1"; dir="$2"; md="$3"; f="${dir}/${name}.mdc"
    $DRY_RUN && { info "Would generate Cursor .mdc: ${f}"; return 0; }
    { printf -- "---\ndescription: %s\nglobs:\nalwaysApply: false\n---\n" "$(yaml_quote "$(skill_desc "$md")")"; skill_body "$md"; } > "$f"
    success "Cursor .mdc: ${f}"
}
generate_plain_rule() {
    name="$1"; dir="$2"; md="$3"; f="${dir}/${name}.md"
    $DRY_RUN && { info "Would generate plain rule: ${f}"; return 0; }
    mkdir -p "$dir"; skill_body "$md" > "$f"; success "Plain rule: ${f}"
}
generate_junie_guideline() {
    name="$1"; dir="$2"; md="$3"; f="${dir}/guidelines.md"
    $DRY_RUN && { info "Would generate Junie guideline: ${f}"; return 0; }
    mkdir -p "$dir"; { echo "# ${name}"; echo; skill_body "$md"; } >> "$f"; success "Junie guideline: ${f}"
}
generate_windsurf_rule() {
    name="$1"; md="$2"
    if $PROJECT_LEVEL; then
        dir="$(pwd)/.windsurf/rules"
        $DRY_RUN && { info "Would generate Windsurf rule: ${dir}/${name}.md"; return 0; }
        mkdir -p "$dir"; skill_body "$md" > "${dir}/${name}.md"; success "Windsurf rule: ${dir}/${name}.md"
    else
        gf="${HOME}/.codeium/windsurf/memories/global_rules.md"
        $DRY_RUN && { info "Would append to Windsurf global_rules.md (${name})"; return 0; }
        mkdir -p "$(dirname "$gf")"
        if [ -f "$gf" ]; then
            awk -v b="<!-- BEGIN ${name} -->" -v e="<!-- END ${name} -->" 'BEGIN{s=0} $0==b{s=1;next} $0==e{s=0;next} !s{print}' "$gf" > "${gf}.tmp" && mv "${gf}.tmp" "$gf"
        fi
        { printf "\n<!-- BEGIN %s -->\n" "$name"; skill_body "$md"; printf "\n<!-- END %s -->\n" "$name"; } >> "$gf"
        success "Windsurf global_rules.md += ${name}"
    fi
}

generate_agents_md() {
    name="$1"; dest="$2"; md="$3"
    [ -f "${SCRIPT_DIR}/${name}/AGENTS.md" ] && return 0
    $DRY_RUN && { info "Would generate companion AGENTS.md for ${name}"; return 0; }
    { printf "# %s\n\n%s\n\n## Usage\n\nInvoke with \`/%s\` or by describing a task matching its description. See [SKILL.md](./SKILL.md) for full details.\n" "$name" "$(skill_desc "$md")" "$name"; } > "${dest}/AGENTS.md"
}

install_one_skill() {
    name="$1"; src="${SCRIPT_DIR}/${name}"; md="${src}/SKILL.md"
    validate_skill_md "$md"
    dest="${BASE}/${name}"
    if $DRY_RUN; then info "Would install '${name}' → ${dest}"; else
        [ -d "$dest" ] && rm -rf "$dest"
        mkdir -p "$dest" 2>/dev/null || { error "Cannot create ${dest} (permissions?)"; exit 3; }
        # copy skill contents (SKILL.md + references/ etc.)
        for f in "$src"/* "$src"/.*; do
            bn="$(basename "$f")"; [ "$bn" = "." ] || [ "$bn" = ".." ] && continue
            [ -e "$f" ] || continue
            cp -R "$f" "${dest}/" 2>/dev/null || { error "Failed copying ${bn} → ${dest}"; exit 3; }
        done
        success "Installed '${name}' → ${dest}"
    fi
    case "$PLATFORM" in
        cursor)                 generate_cursor_mdc "$name" "$dest" "$md" ;;
        windsurf)               generate_windsurf_rule "$name" "$md" ;;
        cline|roo-code|kilo-code|trae) generate_plain_rule "$name" "$dest" "$md" ;;
        junie)                  generate_junie_guideline "$name" "$dest" "$md" ;;
    esac
    $DRY_RUN || generate_agents_md "$name" "$dest" "$md"
}

install_for_platform() {
    resolve_base
    info "Base install dir: ${BASE}"
    for s in $SKILLS; do install_one_skill "$s"; done
}

main() {
    parse_args "$@"
    discover_skills
    if $LIST_ONLY; then
        printf "${BOLD}Skills in this library:${NC}\n"
        for s in $SKILLS; do printf "  - %s\n" "$s"; done
        exit 0
    fi
    printf "${BOLD}Installing ${LIBRARY_NAME} skills library (v${VERSION})${NC}\n"
    printf "%s\n" "----------------------------------------"
    count=0; for s in $SKILLS; do count=$((count + 1)); done
    info "Found ${count} skill(s): ${SKILLS}"

    if $INSTALL_ALL; then
        detect_all_platforms
        info "Installing to all detected platforms: ${ALL_PLATFORMS}"
        for p in $ALL_PLATFORMS; do printf "\n"; info "--- ${p} ---"; PLATFORM="$p"; install_for_platform; done
    else
        detect_platform
        install_for_platform
    fi

    printf "\n"
    if $DRY_RUN; then info "Dry run complete — no changes made."; else
        success "Done. Start a new agent session; skills load from their skills path."
        printf "  Invoke a skill by name (e.g. ${BOLD}/portfolio-certification${NC}) or let it auto-activate on a matching task.\n"
        printf "  Requires the ${BOLD}NexusTrade MCP${NC} server connected for the tools these skills call.\n"
    fi
    exit 0
}
main "$@"
