"""関数の事実。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Func:
    box: str
    file: str
    name: str
    line: int
    length: int
    params: int
    nesting: int
    public: bool
    is_test: bool
