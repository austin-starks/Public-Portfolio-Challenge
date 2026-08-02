import importlib.util
import pathlib
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "update_leaderboard.py"
SPEC = importlib.util.spec_from_file_location("update_leaderboard", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class LeaderboardTests(unittest.TestCase):
    def test_verified_runs_rank_before_pending_runs(self):
        passing = {
            "display_name": "Passing",
            "github_handle": "passer",
            "agent": "Agent A",
            "oos_return_pct": 12.5,
            "oos_sortino": 2.1,
            "worst_max_drawdown_pct": 8.0,
            "gates": {str(index): True for index in range(1, 9)},
            "verification_status": "verified",
            "evidence_url": "https://example.com/pass",
            "result_path": "community-runs/passer/run/result.json",
        }
        pending = {
            **passing,
            "display_name": "Pending",
            "github_handle": "pending",
            "oos_return_pct": 99.0,
            "verification_status": "pending",
            "result_path": "community-runs/pending/run/result.json",
        }

        rendered = MODULE.render([pending, passing])

        self.assertLess(rendered.index("| 1 | Passing"), rendered.index("| — | Pending"))

    def test_replace_block_preserves_surrounding_text(self):
        source = f"before\n{MODULE.START_MARKER}\nold\n{MODULE.END_MARKER}\nafter"
        rendered = f"{MODULE.START_MARKER}\nnew\n{MODULE.END_MARKER}"
        self.assertEqual(MODULE.replace_block(source, rendered), f"before\n{rendered}\nafter")


if __name__ == "__main__":
    unittest.main()
