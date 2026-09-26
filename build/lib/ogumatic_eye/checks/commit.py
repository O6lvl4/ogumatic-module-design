"""眼 6: コミット。1 箱が正、2 箱は告げる、3 箱で落とす。"""
import re

from ..vocab.finding import Finding
from .resolve import box_of

_PREFIX = re.compile(r"^(feat|fix|chore|docs|refactor|test|build|ci|perf|style)(\(.*\))?!?:", re.I)


def check_commit(changed, subject, dirs, th):
    boxes = sorted({b for b in (box_of(f, dirs) for f in changed) if b})
    n, mx = len(boxes), th["commit_boxes_max"]
    out = []
    if n > mx:
        out.append(Finding("commit", "", "-", f"{n} 箱を同時に触っている（{', '.join(boxes)}）", "fail"))
    elif n == mx:
        out.append(Finding("commit", "", "-", f"{n} 箱を同時に触っている（{', '.join(boxes)}）", "warn"))
    if subject and _PREFIX.match(subject):
        out.append(Finding("commit", "", "-", "件名が接頭辞で始まる。理由を 1 文で", "warn"))
    return out
