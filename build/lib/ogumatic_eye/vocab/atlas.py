"""地図。ogumatic.yaml の値。"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Atlas:
    version: str
    boxes: dict
    nurtured: tuple = ()
    kits: dict = field(default_factory=dict)
    eye: dict = field(default_factory=dict)
    exceptions: tuple = ()
