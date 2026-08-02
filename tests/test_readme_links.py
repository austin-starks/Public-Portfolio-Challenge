import pathlib
import re
import unittest
from urllib.parse import unquote


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class ReadmeLinkTests(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        missing = []
        for raw_target in MARKDOWN_LINK.findall(README.read_text()):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            path = REPO_ROOT / unquote(target)
            if not path.exists():
                missing.append(target)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
