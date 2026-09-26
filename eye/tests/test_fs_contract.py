"""契約テスト。本物（RealFs）と偽物（FakeFs）に同じケースを流す。"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ogumatic_eye.fsmirror.fake import FakeFs  # noqa: E402
from ogumatic_eye.fsmirror.real import RealFs  # noqa: E402

FILES = {"a/b.go": "package b\n", "c.py": "x = 1\n", "node_modules/x.js": "", ".git/HEAD": "ref"}


def _real_root():
    root = tempfile.mkdtemp()
    for p, t in FILES.items():
        os.makedirs(os.path.join(root, os.path.dirname(p)) or root, exist_ok=True)
        with open(os.path.join(root, p), "w") as fh:
            fh.write(t)
    return root


class FsContract(unittest.TestCase):
    def cases(self):
        return ((RealFs(), _real_root()), (FakeFs(dict(FILES)), "/fake"))

    def test_list_skips_hidden_and_skip_dirs(self):
        for fs, root in self.cases():
            self.assertEqual(fs.list_files(root, {"node_modules"}), ["a/b.go", "c.py"])

    def test_read_write_roundtrip(self):
        for fs, root in self.cases():
            self.assertEqual(fs.read_text(root, "c.py"), "x = 1\n")
            fs.write_text(root, "c.py", "y = 2\n")
            self.assertEqual(fs.read_text(root, "c.py"), "y = 2\n")

    def test_today_is_iso(self):
        for fs, _ in self.cases():
            self.assertRegex(fs.today(), r"^\d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()
