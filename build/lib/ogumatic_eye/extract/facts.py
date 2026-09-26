"""テキストから事実を出す。言語を知るのはこの箱だけ。"""
import re

from ..vocab.filefact import FileFact
from ..vocab.func import Func
from . import blocks, rules


def lang_of(path):
    dot = path.rfind(".")
    return rules.LANG_BY_EXT.get(path[dot:]) if dot >= 0 else None


def is_test(path):
    return bool(rules.TEST_PATH.search(path))


def file_fact(box, path, text, lang):
    return FileFact(box=box, path=path, lang=lang, lines=_code_lines(text), types=tuple(_types(text, lang)),
                    publics=tuple(_publics(text, lang)), imports=tuple(_imports(text, lang)),
                    effects=tuple(_effects(text, lang)), is_test=is_test(path))


def funcs(box, path, text, lang):
    t = is_test(path)
    return [Func(box, path, n, ln, length, par, nest, pub, t) for n, ln, length, nest, par, pub in blocks.blocks(text, lang)]


def _first(m):
    return next((g for g in m.groups() if g), None)


def _code_lines(text):
    return sum(1 for s in text.split("\n") if s.strip() and not s.strip().startswith(("//", "#", "*", "/*")))


def _types(text, lang):
    rx = rules.TYPE.get(lang)
    return [n for n in (_first(m) for m in rx.finditer(text)) if n] if rx else []


def _publics(text, lang):
    rx = rules.PUBLIC.get("TS" if lang == "JS" else lang)
    names = [_first(m) for m in rx.finditer(text)] if rx else []
    if lang in ("TS", "JS"):
        for m in rules.TS_EXPORT_LIST.finditer(text):
            names += [p.split(" as ")[-1].strip() for p in m.group(1).split(",") if p.strip()]
    return sorted({n for n in names if n})


def _imports(text, lang):
    if lang == "Go":
        return [s for m in rules.GO_IMPORT.finditer(text) for s in re.findall(r'"([^"]+)"', m.group(0))]
    rx = rules.IMPORT.get("TS" if lang == "JS" else lang)
    return [n for n in (_first(m) for m in rx.finditer(text)) if n] if rx else []


def _effects(text, lang):
    rx = rules.EFFECT.get("TS" if lang == "JS" else lang)
    if rx is None:
        return []
    return [(text.count("\n", 0, m.start()) + 1, m.group(0).strip().strip('"')) for m in rx.finditer(text)]
