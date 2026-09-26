"""YAML のテキストを札と地図の値に直す。"""
import yaml

from ..vocab.atlas import Atlas
from ..vocab.card import ROLES, STATES, Card
from ..vocab.errors import LoadError


def parse_atlas(text):
    d = _norm(yaml.safe_load(text) or {})
    _need(d, ("ogumatic", "boxes"), "ogumatic.yaml")
    return Atlas(
        version=str(d["ogumatic"]),
        boxes=dict(d["boxes"] or {}),
        nurtured=tuple(d.get("nurtured") or ()),
        kits=dict(d.get("kits") or {}),
        eye=dict(d.get("eye") or {}),
        exceptions=tuple(d.get("exceptions") or ()),
    )


def parse_card(text, path):
    d = _norm(yaml.safe_load(text) or {})
    _need(d, ("name", "role", "knows", "surface", "evidence", "state"), path)
    if d["role"] not in ROLES:
        raise LoadError(f"{path}: role が不正 ({d['role']})")
    if d["state"] not in STATES:
        raise LoadError(f"{path}: state が不正 ({d['state']})")
    return Card(
        name=str(d["name"]),
        role=d["role"],
        knows=tuple(d["knows"] or ()),
        surface=tuple(d["surface"] or ()),
        evidence=dict(d["evidence"] or {}),
        state=d["state"],
        path=path.rsplit("/", 1)[0] if "/" in path else "",
        external=d.get("external"),
        closed_on=d.get("closed_on"),
        regenerable=bool(d.get("regenerable", True)),
        note=str(d.get("note") or ""),
    )


def _need(d, keys, where):
    missing = [k for k in keys if k not in d]
    if missing:
        raise LoadError(f"{where}: 必須項目が無い ({', '.join(missing)})")


def _norm(o):
    if isinstance(o, dict):
        return {k: _norm(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_norm(v) for v in o]
    if hasattr(o, "isoformat"):
        return o.isoformat()[:10]
    return o
