"""眼の閾値。地図の eye: で上書きできる。"""

DEFAULTS = {
    "function_max": 30,
    "params_warn": 4,
    "nesting_warn": 3,
    "file_max": 120,
    "file_warn": 80,
    "surface_max": 4,
    "commit_boxes_max": 2,
}


def thresholds(overrides):
    return {**DEFAULTS, **(overrides or {})}
