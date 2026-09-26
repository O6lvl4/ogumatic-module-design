"""本物。os と git と時計を 1 関数 1 呼び出しで写す。"""
import datetime
import os
import subprocess


class RealFs:
    def list_files(self, root, skip):
        out = []
        for d, dirs, files in os.walk(root):
            dirs[:] = sorted(x for x in dirs if x not in skip and not x.startswith("."))
            rel = os.path.relpath(d, root)
            for f in sorted(files):
                out.append(f if rel == "." else f"{rel}/{f}")
        return sorted(out)

    def read_text(self, root, rel):
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read()

    def write_text(self, root, rel, text):
        with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def changed_files(self, root, rng):
        out = _git(root, ["diff", "--name-only", rng or "--cached"])
        if not rng and not out.strip():
            out = _git(root, ["diff", "--name-only", "HEAD~1..HEAD"])
        return [line for line in out.splitlines() if line]

    def subject(self, root):
        return _git(root, ["log", "-1", "--format=%s"]).strip()

    def today(self):
        return datetime.date.today().isoformat()


def _git(root, args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True).stdout
