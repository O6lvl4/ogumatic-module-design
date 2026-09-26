"""偽物。メモリだけで本物と同じ入口を持つ。"""


class FakeFs:
    def __init__(self, files=None, changed=(), subject="", today="2026-01-01"):
        self.files = dict(files or {})
        self.changed = list(changed)
        self._subject = subject
        self._today = today

    def list_files(self, root, skip):
        return sorted(p for p in self.files if not _skipped(p, skip))

    def read_text(self, root, rel):
        return self.files[rel]

    def write_text(self, root, rel, text):
        self.files[rel] = text

    def changed_files(self, root, rng):
        return list(self.changed)

    def subject(self, root):
        return self._subject

    def today(self):
        return self._today


def _skipped(path, skip):
    return any(seg in skip or seg.startswith(".") for seg in path.split("/")[:-1])
