"""入口。eye / facts / atlas の 3 本。"""
import argparse
import json
import statistics
import sys

from ..registry import registry
from ..vocab.errors import LoadError


def main(argv=None):
    args = _parse(argv)
    fs = registry.new_fs()
    try:
        return {"eye": _eye, "facts": _facts, "atlas": _atlas}[args.cmd](fs, args)
    except LoadError as ex:
        print(f"ERROR {ex}", file=sys.stderr)
        return 2


def _parse(argv):
    ap = argparse.ArgumentParser(prog="ogumatic", description="Ogumatic Module Design の眼")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("eye", help="六段の検査を回す")
    e.add_argument("path", nargs="?", default=".")
    e.add_argument("--range", help="コミットの段に使う git の範囲。無ければコミットの段は見ない")
    e.add_argument("--json", action="store_true")
    f = sub.add_parser("facts", help="事実だけを出す。札が無くても動く")
    f.add_argument("path", nargs="?", default=".")
    f.add_argument("--auto", action="store_true", help="トップ階層のディレクトリを箱と見なす")
    a = sub.add_parser("atlas", help="box.yaml と地図の差を出す")
    a.add_argument("path", nargs="?", default=".")
    return ap.parse_args(argv)


def _eye(fs, args):
    found = registry.eye(fs, args.path, args.range, with_commit=bool(args.range))
    found = sorted(found, key=lambda x: (x.level != "fail", x.check, x.box, x.location))
    if args.json:
        print(json.dumps([x.__dict__ for x in found], ensure_ascii=False, indent=2))
    else:
        for x in found:
            print(x.line())
    fails = sum(1 for x in found if x.level == "fail")
    print(f"--- 落とす {fails} / 告げる {len(found) - fails}")
    return 1 if fails else 0


def _facts(fs, args):
    facts, funcs = registry.facts_only(fs, args.path, args.auto)
    print(f"{'箱':<18}{'files':>6}{'lines':>7}{'funcs':>6}{'f_med':>6}{'f_p90':>6}{'types':>6}{'public':>7}{'effect':>7}")
    for b in sorted({f.box for f in facts}):
        ff = [f for f in facts if f.box == b and not f.is_test]
        fn = sorted(x.length for x in funcs if x.box == b and not x.is_test)
        med = statistics.median(fn) if fn else 0
        p90 = fn[int(len(fn) * 0.9)] if fn else 0
        pubs = len({s for f in ff for s in f.publics})
        print(f"{b or '(箱の外)':<18}{len(ff):>6}{sum(f.lines for f in ff):>7}{len(fn):>6}{med:>6.0f}{p90:>6}"
              f"{sum(len(f.types) for f in ff):>6}{pubs:>7}{sum(len(f.effects) for f in ff):>7}")
    return 0


def _atlas(fs, args):
    missing, gone = registry.atlas_diff(fs, args.path)
    for p in missing:
        print(f"地図に無い札: {p}")
    for p in gone:
        print(f"札が無い: {p}")
    if not missing and not gone:
        print("地図と札は一致")
    return 1 if gone else 0
