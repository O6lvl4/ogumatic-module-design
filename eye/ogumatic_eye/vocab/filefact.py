"""ファイルの事実。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class FileFact:
    box: str
    path: str
    lang: str
    lines: int
    types: tuple
    publics: tuple
    imports: tuple
    effects: tuple
    is_test: bool
