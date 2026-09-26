"""import 文とパスを箱に対応づける。"""
import re

_SEP = re.compile(r"[/:.\\]+")
_DROP = {"", ".", "..", "@", "crate", "super", "self"}


def segments(imp):
    return [s for s in _SEP.split(imp.strip("\"' ")) if s not in _DROP]


def resolve(imp, dirs):
    """(箱名, 曖昧か)。dirs は 箱名 → ディレクトリ。"""
    segs = segments(imp)
    best, score, tie = None, 0.0, False
    for name, d in dirs.items():
        ds = [s for s in d.split("/") if s] or [name]
        sc = _score(segs, ds)
        if sc > score:
            best, score, tie = name, sc, False
        elif sc and sc == score:
            tie = True
    return best, tie


def _score(segs, ds):
    n = len(ds)
    for i in range(len(segs) - n + 1):
        if segs[i:i + n] == ds:
            return float(n)
    return 0.5 if ds[-1] in segs else 0.0


def box_of(path, dirs):
    best, depth = "", -1
    for name, d in dirs.items():
        if (d == "" or path.startswith(d + "/")) and len(d) > depth:
            best, depth = name, len(d)
    return best
