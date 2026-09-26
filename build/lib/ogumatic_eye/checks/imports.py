"""眼 3: import。札の knows と役の表。"""
from ..vocab.finding import Finding
from ..vocab.roles import ALLOWED_KNOWS
from .resolve import resolve


def check_imports(facts, cards, dirs):
    by = {c.name: c for c in cards}
    out = []
    for ff in facts:
        if not ff.box or ff.is_test:
            continue
        out += _file_imports(ff, by[ff.box], dirs)
    for c in cards:
        out += _knows_vs_roles(c, by)
    return out


def _file_imports(ff, card, dirs):
    out = []
    for imp in ff.imports:
        name, tie = resolve(imp, dirs)
        if not name or name == ff.box:
            continue
        if name not in card.knows:
            out.append(Finding("import", ff.box, ff.path, f"{imp} → {name} は札の knows に無い", "fail"))
        elif tie:
            out.append(Finding("import", ff.box, ff.path, f"{imp} の解決が曖昧（{name} と判定）", "warn"))
    return out


def _knows_vs_roles(card, by):
    out = []
    for k in card.knows:
        other = by.get(k)
        if other is None:
            out.append(Finding("import", card.name, card.path, f"knows の {k} は地図に無い", "warn"))
        elif other.role not in ALLOWED_KNOWS[card.role]:
            out.append(Finding("import", card.name, card.path, f"{card.role} が {other.role}（{k}）を知るのは役の表に無い", "warn"))
    return out
