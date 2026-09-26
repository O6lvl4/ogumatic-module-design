"""眼 1: 関数。"""
from ..vocab.finding import Finding


def check_functions(funcs, th):
    out = []
    for f in funcs:
        if f.is_test:
            continue
        loc = f"{f.file}:{f.line}"
        if f.length > th["function_max"]:
            out.append(Finding("function", f.box, loc, f"{f.name} が {f.length} 行（上限 {th['function_max']}）", "fail"))
        if f.params >= th["params_warn"]:
            out.append(Finding("function", f.box, loc, f"{f.name} の引数が {f.params}", "warn"))
        if f.nesting >= th["nesting_warn"]:
            out.append(Finding("function", f.box, loc, f"{f.name} のネストが {f.nesting}", "warn"))
    return out
