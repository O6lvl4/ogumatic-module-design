"""役ごとに知ってよい相手。"""

ALLOWED_KNOWS = {
    "vocabulary": set(),
    "meter": {"vocabulary", "meter"},
    "mirror": set(),
    "translator": {"mirror", "vocabulary", "meter"},
    "registry": {"translator", "mirror", "meter", "vocabulary"},
    "facade": {"registry", "vocabulary"},
}
EFFECT_ROLE = "mirror"
