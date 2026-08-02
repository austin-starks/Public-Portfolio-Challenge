import importlib.util
import pathlib
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "update_scoreboard.py"
SPEC = importlib.util.spec_from_file_location("update_scoreboard", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ScoreboardTests(unittest.TestCase):
    def test_builds_same_window_scoreboard(self):
        portfolio = {
            "history": [
                {"time": "2026-03-09T13:34:06.748Z", "value": 25000},
                {"time": "2026-03-11T19:57:32.278Z", "value": 27500},
            ]
        }
        performance = {
            "performance": {
                "gains": {"allTime": 10},
                "statistics": {"maxDrawdown": 4.25},
            }
        }
        spy = {
            "history": [
                {"time": "2026-03-08T15:45:00", "value": 90},
                {"time": "2026-03-09T15:45:00", "value": 100},
                {"time": "2026-03-11T15:45:00", "value": 105},
                {"time": "2026-03-12T15:45:00", "value": 120},
            ]
        }

        result = MODULE.build_scoreboard(portfolio, performance, spy)

        self.assertEqual(result["account_value"], 27500)
        self.assertEqual(result["days_live"], 2)
        self.assertEqual(result["spy_return_pct"], 5)
        self.assertEqual(result["excess_return_vs_spy_pct"], 5)
        self.assertEqual(result["max_drawdown_pct"], 4.25)

    def test_rejects_return_drift(self):
        portfolio = {
            "history": [
                {"time": "2026-03-09T13:34:06Z", "value": 25000},
                {"time": "2026-03-10T13:34:06Z", "value": 27500},
            ]
        }
        performance = {
            "performance": {
                "gains": {"allTime": 9.5},
                "statistics": {"maxDrawdown": 1},
            }
        }
        spy = {
            "history": [
                {"time": "2026-03-09T15:45:00", "value": 100},
                {"time": "2026-03-10T15:45:00", "value": 101},
            ]
        }

        with self.assertRaisesRegex(ValueError, "differ"):
            MODULE.build_scoreboard(portfolio, performance, spy)

    def test_replaces_only_generated_block(self):
        source = f"before\n{MODULE.START_MARKER}\nold\n{MODULE.END_MARKER}\nafter\n"
        rendered = f"{MODULE.START_MARKER}\nnew\n{MODULE.END_MARKER}"

        self.assertEqual(
            MODULE.replace_scoreboard(source, rendered),
            f"before\n{rendered}\nafter\n",
        )

    def test_renders_excess_return_as_percentage_points(self):
        rendered = MODULE.render_scoreboard(
            {
                "as_of": "2026-03-11T19:57:32Z",
                "account_value": 27500,
                "total_return_pct": 10,
                "spy_return_pct": 5,
                "excess_return_vs_spy_pct": 5,
                "max_drawdown_pct": 4.25,
                "days_live": 2,
            }
        )

        self.assertIn("+5.00 pp (SPY +5.00%)", rendered)
        self.assertNotIn("% pp", rendered)


if __name__ == "__main__":
    unittest.main()
