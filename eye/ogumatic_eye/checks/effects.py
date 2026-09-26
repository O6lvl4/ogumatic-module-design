"""眼 4: 副作用は mirror だけ。"""
from ..vocab.finding import Finding
from ..vocab.roles import EFFECT_ROLE


def check_effects(facts, cards):
    by = {c.name: c for c in cards}
    out = []
    for ff in facts:
        if not ff.box or ff.is_test or not ff.effects:
            continue
        card = by[ff.box]
        words = sorted({w for _, w in ff.effects})
        loc = f"{ff.path}:{ff.effects[0][0]}"
        if card.role != EFFECT_ROLE:
            out.append(Finding("effect", ff.box, loc, f"{card.role} の箱で副作用（{', '.join(words[:5])}）", "fail"))
        elif _is_fake(ff, card):
            out.append(Finding("effect", ff.box, loc, f"偽物が副作用に触れている（{', '.join(words[:5])}）", "warn"))
    return out


def _is_fake(ff, card):
    fake = card.evidence.get("fake")
    return bool(fake) and ff.path.endswith(str(fake))
