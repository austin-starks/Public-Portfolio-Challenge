#!/usr/bin/env python3
"""Refresh the README scoreboard from public NexusTrade API data."""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any


SHARED_PORTFOLIO_ID = "69a7dc7cf99e43688fcec567"
API_ROOT = "https://nexustrade.io/api"
PORTFOLIO_URL = (
    f"{API_ROOT}/share-portfolio/portfolio/{SHARED_PORTFOLIO_ID}"
)
HISTORY_URL = f"{PORTFOLIO_URL}/history"
PERFORMANCE_URL = (
    f"{API_ROOT}/share-portfolio/{SHARED_PORTFOLIO_ID}/performance"
)
SPY_URL = f"{API_ROOT}/stock/SPY/history/price?brokerage=Public"
START_MARKER = "<!-- SCOREBOARD:START -->"
END_MARKER = "<!-- SCOREBOARD:END -->"


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Public-Portfolio-Challenge-scoreboard/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def parse_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        parsed = parsedate_to_datetime(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def normalize_history(payload: dict[str, Any], label: str) -> list[dict[str, Any]]:
    raw_history = payload.get("history")
    if not isinstance(raw_history, list) or not raw_history:
        raise ValueError(f"{label} history is empty")

    normalized = []
    for index, point in enumerate(raw_history):
        if not isinstance(point, dict) or not isinstance(point.get("time"), str):
            raise ValueError(f"{label} history point {index} is invalid")
        normalized.append(
            {
                "time": parse_datetime(point["time"]),
                "value": finite_number(point.get("value"), f"{label}[{index}].value"),
            }
        )
    return sorted(normalized, key=lambda point: point["time"])


def percentage_return(first_value: float, last_value: float) -> float:
    if first_value <= 0:
        raise ValueError("return anchor must be positive")
    return ((last_value / first_value) - 1) * 100


def build_scoreboard(
    portfolio_history_payload: dict[str, Any],
    performance_payload: dict[str, Any],
    spy_history_payload: dict[str, Any],
) -> dict[str, Any]:
    portfolio_history = normalize_history(portfolio_history_payload, "portfolio")
    spy_history = normalize_history(spy_history_payload, "SPY")

    live_since = portfolio_history[0]["time"]
    as_of = portfolio_history[-1]["time"]
    account_value = portfolio_history[-1]["value"]
    calculated_return = percentage_return(
        portfolio_history[0]["value"], account_value
    )

    performance = performance_payload.get("performance")
    if not isinstance(performance, dict):
        raise ValueError("performance payload is missing")
    gains = performance.get("gains")
    statistics = performance.get("statistics")
    if not isinstance(gains, dict) or not isinstance(statistics, dict):
        raise ValueError("performance gains or statistics are missing")
    reported_return = finite_number(gains.get("allTime"), "gains.allTime")
    if abs(reported_return - calculated_return) > 0.05:
        raise ValueError(
            "portfolio history and reported all-time return differ by more than 0.05pp"
        )

    spy_window = [
        point
        for point in spy_history
        if live_since.date() <= point["time"].date() <= as_of.date()
    ]
    if len(spy_window) < 2:
        raise ValueError("SPY history does not cover the live portfolio window")
    spy_return = percentage_return(spy_window[0]["value"], spy_window[-1]["value"])
    max_drawdown = abs(
        finite_number(statistics.get("maxDrawdown"), "statistics.maxDrawdown")
    )

    return {
        "shared_portfolio_id": SHARED_PORTFOLIO_ID,
        "as_of": as_of.isoformat().replace("+00:00", "Z"),
        "live_since": live_since.isoformat().replace("+00:00", "Z"),
        "days_live": (as_of.date() - live_since.date()).days,
        "account_value": round(account_value, 2),
        "total_return_pct": round(reported_return, 6),
        "spy_return_pct": round(spy_return, 6),
        "excess_return_vs_spy_pct": round(reported_return - spy_return, 6),
        "max_drawdown_pct": round(max_drawdown, 6),
        "sources": {
            "portfolio_history": HISTORY_URL,
            "portfolio_performance": PERFORMANCE_URL,
            "spy_history": SPY_URL,
        },
    }


def signed_percent(value: float) -> str:
    return f"{value:+.2f}%"


def signed_points(value: float) -> str:
    return f"{value:+.2f} pp"


def render_scoreboard(scoreboard: dict[str, Any]) -> str:
    as_of = parse_datetime(scoreboard["as_of"]).strftime("%B %-d, %Y")
    return "\n".join(
        [
            START_MARKER,
            "| Account value | Total return | Return vs. SPY | Max drawdown | Days live |",
            "| ---: | ---: | ---: | ---: | ---: |",
            (
                f"| ${scoreboard['account_value']:,.2f} "
                f"| {signed_percent(scoreboard['total_return_pct'])} "
                f"| {signed_points(scoreboard['excess_return_vs_spy_pct'])} "
                f"(SPY {signed_percent(scoreboard['spy_return_pct'])}) "
                f"| −{scoreboard['max_drawdown_pct']:.2f}% "
                f"| {scoreboard['days_live']} |"
            ),
            "",
            (
                f"<sub>As of {as_of}. Same-window comparison begins with the first stored "
                f"live observation. [Portfolio data]({HISTORY_URL}) · "
                f"[Performance data]({PERFORMANCE_URL}) · [SPY data]({SPY_URL}) · "
                "refreshed weekly by GitHub Actions.</sub>"
            ),
            END_MARKER,
        ]
    )


def replace_scoreboard(readme: str, rendered: str) -> str:
    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise ValueError("README scoreboard markers are missing or out of order")
    end += len(END_MARKER)
    return readme[:start] + rendered + readme[end:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()

    scoreboard = build_scoreboard(
        fetch_json(HISTORY_URL),
        fetch_json(PERFORMANCE_URL),
        fetch_json(SPY_URL),
    )
    readme_path = args.repo_root / "README.md"
    data_path = args.repo_root / "data" / "scoreboard.json"
    readme_path.write_text(
        replace_scoreboard(readme_path.read_text(), render_scoreboard(scoreboard))
    )
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(scoreboard, indent=2) + "\n")


if __name__ == "__main__":
    main()
