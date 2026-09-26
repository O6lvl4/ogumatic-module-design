"""括弧の対応と字下げで関数の範囲を測る。"""
import bisect
import re

from . import rules

_BLOCK_KW = re.compile(r"^(if|elif|else|for|while|try|except|finally|with|def|class|match|case)\b")


def blocks(text, lang):
    """(name, line, length, nesting, params, public) の列。"""
    if lang in ("Python", "Ruby"):
        return _indent_blocks(text, lang)
    sig = rules.SIG.get("TS" if lang == "JS" else lang)
    if sig is None:
        return []
    lines = text.split("\n")
    starts = _line_starts(lines)
    out = []
    for m in sig.finditer(text):
        name = next((g for g in m.groups() if g), "?")
        if lang in ("TS", "JS") and name in rules.TS_CONTROL:
            continue
        ob = text.find("{", m.end(), min(len(text), m.end() + 1500))
        if ob == -1 or ";" in text[m.end():ob]:
            continue
        end, depth = _match(text, ob, lang)
        sl, el = _line_of(starts, m.start()), _line_of(starts, end)
        out.append((name, sl + 1, el - sl + 1, depth, _params(text[m.start():ob], lang), rules.is_public(lang, lines[sl])))
    return out


def _match(text, ob, lang):
    depth = maxd = 0
    j, n = ob, len(text)
    while j < n:
        c = text[j]
        if c == '"' or (c == "'" and lang != "Rust") or (c == "`" and lang in ("TS", "JS")):
            j = _skip_string(text, j, c)
            continue
        if text.startswith("//", j):
            j = _line_end(text, j)
            continue
        if text.startswith("/*", j):
            k = text.find("*/", j + 2)
            j = n if k == -1 else k + 2
            continue
        if c == "{":
            depth += 1
            maxd = max(maxd, depth)
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j, maxd
        j += 1
    return n - 1, maxd


def _skip_string(text, j, q):
    k, n = j + 1, len(text)
    while k < n:
        if text[k] == "\\":
            k += 2
            continue
        if text[k] == q or (text[k] == "\n" and q != "`"):
            return k + 1
        k += 1
    return n


def _line_end(text, j):
    k = text.find("\n", j)
    return len(text) if k == -1 else k


def _line_starts(lines):
    starts, pos = [], 0
    for s in lines:
        starts.append(pos)
        pos += len(s) + 1
    return starts


def _line_of(starts, pos):
    return bisect.bisect_right(starts, pos) - 1


def _params(sig, lang):
    if lang == "ObjC":
        return sig.count(":")
    inside = sig.split("(", 1)[1].split(")", 1)[0] if "(" in sig else ""
    return len([p for p in inside.split(",") if p.strip()])


def _indent_blocks(text, lang):
    sig = rules.SIG[lang]
    lines = text.split("\n")
    out = []
    for m in sig.finditer(text):
        ind = len(m.group(1).expandtabs(4))
        ln = text.count("\n", 0, m.start())
        end = _indent_end(lines, ln, ind, lang)
        body = [s for s in lines[ln:end + 1] if s.strip()]
        nest = max(((len(s) - len(s.lstrip())) // 4 - ind // 4 + 1 for s in body if _BLOCK_KW.match(s.strip())), default=1)
        head = lines[ln]
        params = head.split("(", 1)[1].split(")", 1)[0] if "(" in head else ""
        npar = len([p for p in params.split(",") if p.strip() and p.strip() not in ("self", "cls")])
        out.append((m.group(2), ln + 1, end - ln + 1, nest, npar, rules.is_public(lang, head)))
    return out


def _indent_end(lines, ln, ind, lang):
    end = ln
    for j in range(ln + 1, len(lines)):
        s = lines[j]
        if not s.strip() or s.strip().startswith("#"):
            continue
        cur = len(s) - len(s.lstrip())
        if lang == "Ruby" and cur == ind and s.strip() == "end":
            return j
        if cur <= ind:
            break
        end = j
    return end
