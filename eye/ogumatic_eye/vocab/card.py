"""箱札。box.yaml 1 枚の値。"""
from dataclasses import dataclass

ROLES = ("vocabulary", "meter", "mirror", "translator", "registry", "facade")
STATES = ("open", "closed", "nurtured")


@dataclass(frozen=True)
class Card:
    name: str
    role: str
    knows: tuple
    surface: tuple
    evidence: dict
    state: str
    path: str
    external: str | None = None
    closed_on: str | None = None
    regenerable: bool = True
    note: str = ""
