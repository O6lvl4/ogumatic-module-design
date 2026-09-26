"""眼 5: 入口。公開は札が先。"""
from ..vocab.finding import Finding


def check_surface(facts, cards, th):
    pubs = {}
    for ff in facts:
        if ff.box and not ff.is_test:
            pubs.setdefault(ff.box, set()).update(ff.publics)
    out = []
    for c in cards:
        have = pubs.get(c.name, set())
        for s in sorted(have - set(c.surface)):
            out.append(Finding("surface", c.name, c.path, f"{s} は札の surface に無い", "fail"))
        for s in c.surface:
            if s not in have:
                out.append(Finding("surface", c.name, c.path, f"surface の {s} が実体に無い", "warn"))
        if c.role == "facade" and len(c.surface) > th["surface_max"]:
            out.append(Finding("surface", c.name, c.path, f"facade の入口が {len(c.surface)} 本（上限 {th['surface_max']}）", "fail"))
    return out
