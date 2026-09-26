"""抽出器と検査を列挙し、組み立てる唯一の場所。"""
from ..checks import apply_exceptions, run_checks
from ..checks.resolve import box_of
from ..extract import facts as ex
from ..extract import rules
from ..fsmirror.real import RealFs
from ..loader.load import parse_atlas, parse_card
from ..vocab.errors import LoadError
from ..vocab.finding import Finding
from ..vocab.thresholds import thresholds

ATLAS_FILE = "ogumatic.yaml"


def new_fs():
    return RealFs()


def eye(fs, root, rng=None, with_commit=False):
    atlas, cards, files = _world(fs, root)
    dirs = {c.name: c.path for c in cards}
    facts, funcs = _gather(fs, root, files, dirs)
    th = thresholds(atlas.eye)
    changed = fs.changed_files(root, rng) if with_commit else None
    subject = fs.subject(root) if with_commit else ""
    found = run_checks(facts, funcs, cards, dirs, th, changed, subject) + _atlas_findings(atlas, files)
    return apply_exceptions(found, atlas.exceptions, fs.today())


def facts_only(fs, root, auto=False):
    files = fs.list_files(root, rules.SKIP_DIRS)
    if auto or ATLAS_FILE not in files:
        dirs = {t: t for t in sorted({p.split("/")[0] for p in files if "/" in p})}
    else:
        _, cards, _ = _world(fs, root)
        dirs = {c.name: c.path for c in cards}
    return _gather(fs, root, files, dirs)


def atlas_diff(fs, root):
    atlas, _, files = _world(fs, root)
    on_disk = _cards_on_disk(files)
    listed = set(atlas.boxes.values())
    return sorted(on_disk - listed), sorted(listed - on_disk)


def _world(fs, root):
    files = fs.list_files(root, rules.SKIP_DIRS)
    if ATLAS_FILE not in files:
        raise LoadError(f"{ATLAS_FILE} が無い")
    atlas = parse_atlas(fs.read_text(root, ATLAS_FILE))
    cards = []
    for name, p in atlas.boxes.items():
        if p not in files:
            raise LoadError(f"地図の {name} の札 {p} が無い")
        cards.append(parse_card(fs.read_text(root, p), p))
    return atlas, cards, files


def _gather(fs, root, files, dirs):
    facts, funcs = [], []
    for p in files:
        lang = ex.lang_of(p)
        if lang is None:
            continue
        text = fs.read_text(root, p)
        box = box_of(p, dirs)
        facts.append(ex.file_fact(box, p, text, lang))
        funcs += ex.funcs(box, p, text, lang)
    return facts, funcs


def _cards_on_disk(files):
    return {p for p in files if (p == "box.yaml" or p.endswith("/box.yaml")) and not ex.is_test(p)}


def _atlas_findings(atlas, files):
    missing = sorted(_cards_on_disk(files) - set(atlas.boxes.values()))
    return [Finding("atlas", "", p, "地図に無い札", "warn") for p in missing]
