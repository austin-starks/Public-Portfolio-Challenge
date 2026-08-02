#!/usr/bin/env python3
"""Validate community results and render the README leaderboard."""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from typing import Any


START_MARKER = "<!-- COMMUNITY_LEADERBOARD:START -->"
END_MARKER = "<!-- COMMUNITY_LEADERBOARD:END -->"
GATE_KEYS = {str(number) for number in range(1, 9)}
STATUSES = {"pending", "verified", "rejected"}


def number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def load_result(path: pathlib.Path, repo_root: pathlib.Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: root must be an object")

    gates = payload.get("gates")
    if not isinstance(gates, dict) or set(gates) != GATE_KEYS:
        raise ValueError(f"{path}: gates must contain string keys 1 through 8")
    if any(not isinstance(value, bool) for value in gates.values()):
        raise ValueError(f"{path}: every gate must be boolean")

    status = text(payload.get("verification_status"), "verification_status")
    if status not in STATUSES:
        raise ValueError(f"{path}: verification_status must be pending, verified, or rejected")
    if status == "verified" and not all(gates.values()):
        raise ValueError(f"{path}: a verified run must pass every gate")

    runbook_commit = text(payload.get("runbook_commit"), "runbook_commit")
    if len(runbook_commit) != 40 or any(character not in "0123456789abcdef" for character in runbook_commit.lower()):
        raise ValueError(f"{path}: runbook_commit must be a full 40-character SHA")

    evidence = text(payload.get("evidence_url"), "evidence_url")
    if not evidence.startswith(("https://", "http://")):
        evidence_path = (repo_root / evidence).resolve()
        if repo_root.resolve() not in evidence_path.parents or not evidence_path.exists():
            raise ValueError(f"{path}: local evidence_url does not exist inside the repository")

    return {
        "display_name": text(payload.get("display_name"), "display_name"),
        "github_handle": text(payload.get("github_handle"), "github_handle"),
        "agent": text(payload.get("agent"), "agent"),
        "runbook_commit": runbook_commit,
        "oos_return_pct": number(payload.get("oos_return_pct"), "oos_return_pct"),
        "oos_sortino": number(payload.get("oos_sortino"), "oos_sortino"),
        "worst_max_drawdown_pct": abs(
            number(payload.get("worst_max_drawdown_pct"), "worst_max_drawdown_pct")
        ),
        "gates": gates,
        "verification_status": status,
        "evidence_url": evidence,
        "result_path": path.relative_to(repo_root).as_posix(),
    }


def discover_results(repo_root: pathlib.Path) -> list[dict[str, Any]]:
    paths = sorted((repo_root / "community-runs").glob("*/*/result.json"))
    paths = [path for path in paths if "example" not in path.parts]
    return [load_result(path, repo_root) for path in paths]


def escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def signed_percent(value: float) -> str:
    return f"{value:+.2f}%"


def render(results: list[dict[str, Any]]) -> str:
    eligible = sorted(
        [result for result in results if result["verification_status"] == "verified"],
        key=lambda result: result["oos_return_pct"],
        reverse=True,
    )
    ranks = {result["result_path"]: index + 1 for index, result in enumerate(eligible)}
    ordered = eligible + [result for result in results if result not in eligible]
    lines = [
        START_MARKER,
        "| Rank | Run | Agent | OOS return | OOS Sortino | Worst max drawdown | Gates | Evidence |",
        "| ---: | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    if not ordered:
        lines.append(
            "| — | No verified community runs yet | — | — | — | — | — | "
            "[Submit the first run](community-runs/README.md) |"
        )
    for result in ordered:
        rank = ranks.get(result["result_path"], "—")
        gates = (
            "PASS"
            if all(result["gates"].values())
            else "FAIL: " + ", ".join(key for key, passed in result["gates"].items() if not passed)
        )
        if result["verification_status"] != "verified":
            gates = f"{result['verification_status'].upper()} · {gates}"
        lines.append(
            f"| {rank} | {escape(result['display_name'])} (@{escape(result['github_handle'])}) "
            f"| {escape(result['agent'])} | {signed_percent(result['oos_return_pct'])} "
            f"| {result['oos_sortino']:.2f} | −{result['worst_max_drawdown_pct']:.2f}% "
            f"| {gates} | [log]({result['evidence_url']}) |"
        )
    lines.append(END_MARKER)
    return "\n".join(lines)


def replace_block(readme: str, rendered: str) -> str:
    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise ValueError("README leaderboard markers are missing or out of order")
    end += len(END_MARKER)
    return readme[:start] + rendered + readme[end:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    readme_path = args.repo_root / "README.md"
    expected = replace_block(readme_path.read_text(), render(discover_results(args.repo_root)))
    if args.check:
        if expected != readme_path.read_text():
            print("README community leaderboard is stale; run scripts/update_leaderboard.py", file=sys.stderr)
            raise SystemExit(1)
        return
    readme_path.write_text(expected)


if __name__ == "__main__":
    main()
