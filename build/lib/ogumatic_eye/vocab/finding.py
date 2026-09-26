"""眼の判定 1 件。"""
from dataclasses import dataclass

CHECKS = ("function", "file", "import", "effect", "surface", "commit", "coverage", "atlas")


@dataclass(frozen=True)
class Finding:
    check: str
    box: str
    location: str
    message: str
    level: str

    def line(self):
        return f"{self.level.upper():4} {self.check:8} {self.box or '-':10} {self.location}  {self.message}"
