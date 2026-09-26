"""六段を順に回す。"""
from .commit import check_commit
from .coverage import check_coverage
from .effects import check_effects
from .files import check_files
from .functions import check_functions
from .imports import check_imports
from .surface import check_surface


def run_checks(facts, funcs, cards, dirs, th, changed=None, subject=""):
    out = []
    out += check_functions(funcs, th)
    out += check_files(facts, th)
    out += check_imports(facts, cards, dirs)
    out += check_effects(facts, cards)
    out += check_surface(facts, cards, th)
    out += check_coverage(facts)
    if changed is not None:
        out += check_commit(changed, subject, dirs, th)
    return out
