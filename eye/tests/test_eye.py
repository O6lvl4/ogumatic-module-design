import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ogumatic_eye.fsmirror.fake import FakeFs  # noqa: E402
from ogumatic_eye.fsmirror.real import RealFs  # noqa: E402
from ogumatic_eye.registry import registry  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "testdata", "mixed")


def load_fake(changed=(), subject=""):
    real = RealFs()
    files = {p: real.read_text(ROOT, p) for p in real.list_files(ROOT, set())}
    return FakeFs(files, changed, subject, today="2026-06-01")


class EyeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found = registry.eye(load_fake(), ROOT)

    def has(self, level, check, box, needle):
        return any(f.level == level and f.check == check and f.box == box and needle in f.message for f in self.found)

    def test_file_two_types(self):
        self.assertTrue(self.has("fail", "file", "model", "型が 2"))

    def test_effect_in_meter_with_expired_exception(self):
        self.assertTrue(self.has("fail", "effect", "meter", "期限切れ"))

    def test_import_not_in_knows(self):
        self.assertTrue(self.has("fail", "import", "cli", "meter"))
        self.assertTrue(self.has("fail", "import", "web", "meter"))

    def test_surface(self):
        self.assertTrue(self.has("fail", "surface", "cli", "5 本"))
        self.assertTrue(self.has("fail", "surface", "cli", "F は札の surface に無い"))

    def test_function_downgraded_by_exception(self):
        self.assertTrue(self.has("warn", "function", "report", "例外"))
        self.assertFalse(self.has("fail", "function", "report", "build"))

    def test_role_table_warns(self):
        self.assertTrue(self.has("warn", "import", "cli", "facade が mirror"))

    def test_coverage(self):
        self.assertTrue(any(f.check == "coverage" and f.location == "tools" for f in self.found))

    def test_mirrors_are_clean(self):
        self.assertFalse(any(f.box in ("store", "api") and f.level == "fail" for f in self.found))

    def test_commit(self):
        fs = load_fake(["model/model.go", "meter/meter.go", "cli/main.go"], "feat: x")
        found = registry.eye(fs, ROOT, rng="HEAD~1..HEAD", with_commit=True)
        self.assertTrue(any(f.check == "commit" and f.level == "fail" and "3 箱" in f.message for f in found))
        self.assertTrue(any(f.check == "commit" and "接頭辞" in f.message for f in found))

    def test_facts_auto(self):
        facts, funcs = registry.facts_only(load_fake(), ROOT, auto=True)
        self.assertIn("store", {f.box for f in facts})
        self.assertTrue(any(x.name == "build" and x.length > 30 for x in funcs))


if __name__ == "__main__":
    unittest.main()
