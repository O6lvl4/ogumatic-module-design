"""眼 2: ファイル。1 型、120 行まで。"""
from ..vocab.finding import Finding


def check_files(facts, th):
    out = []
    for ff in facts:
        if ff.is_test or not ff.box:
            continue
        if len(ff.types) > 1:
            out.append(Finding("file", ff.box, ff.path, f"型が {len(ff.types)} つ（{', '.join(ff.types[:4])}）", "fail"))
        if ff.lines > th["file_max"]:
            out.append(Finding("file", ff.box, ff.path, f"{ff.lines} 行（上限 {th['file_max']}）", "fail"))
        elif ff.lines > th["file_warn"]:
            out.append(Finding("file", ff.box, ff.path, f"{ff.lines} 行", "warn"))
    return out
