"""地図の exceptions で落とすを告げるに下げる。期限切れは落としたまま印を付ける。"""
from dataclasses import replace


def apply_exceptions(findings, exceptions, today):
    out = []
    for f in findings:
        ex = next((e for e in exceptions if e.get("box") == f.box and e.get("check") == f.check), None)
        if f.level == "fail" and ex:
            until = str(ex.get("until", ""))
            if until >= today:
                f = replace(f, level="warn", message=f"{f.message} [例外: {ex.get('reason', '')} / {until} まで]")
            else:
                f = replace(f, message=f"{f.message} [例外の期限切れ {until}]")
        out.append(f)
    return out
