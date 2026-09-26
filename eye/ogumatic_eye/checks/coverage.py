"""眼 7: 箱の外にあるソース。"""
from ..extract.rules import PLUMBING
from ..vocab.finding import Finding


def check_coverage(facts):
    dirs = sorted({ff.path.rsplit("/", 1)[0] if "/" in ff.path else "."
                   for ff in facts if not ff.box and not ff.is_test and ff.path.rsplit("/", 1)[-1] not in PLUMBING})
    return [Finding("coverage", "", d, "箱の外にソースがある", "warn") for d in dirs]
