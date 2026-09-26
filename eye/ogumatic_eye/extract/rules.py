"""言語の規則表（資料）。抽出器だけがここを読む。段階 2 で YAML に出す。"""
import re

LANG_BY_EXT = {".swift": "Swift", ".m": "ObjC", ".h": "ObjC-h", ".go": "Go", ".ts": "TS", ".tsx": "TS",
               ".js": "JS", ".jsx": "JS", ".mjs": "JS", ".cjs": "JS", ".py": "Python", ".kt": "Kotlin",
               ".java": "Java", ".dart": "Dart", ".rs": "Rust", ".rb": "Ruby"}
SKIP_DIRS = {"node_modules", "vendor", "target", "dist", "build", "Pods", "Carthage", ".build", "__pycache__",
             ".next", "coverage", ".venv", "venv", "out", "_site", ".cache", "generated"}
PLUMBING = {"__init__.py", "__main__.py", "mod.rs"}
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__|spec|specs|Tests?|e2e|testdata|fixtures)/"
                       r"|(Tests?|TestCase|_test|\.test|\.spec|Spec)\.[a-z]+$")
TS_CONTROL = {"if", "for", "while", "switch", "catch", "return", "else", "function", "constructor", "do", "try"}

_MOD = r"(?:(?:public|private|fileprivate|internal|open|static|class|final|override|mutating|convenience|required|@objc|nonisolated|dynamic)\s+)*"
SIG = {
    "Swift": re.compile(r"^[ \t]*(?:@\w+(?:\([^)]*\))?\s+)*" + _MOD + r"(?:func\s+([\w`]+)|(init)\b|(deinit)\b|(subscript)\b)", re.M),
    "ObjC": re.compile(r"^[-+]\s*\([^)]*\)\s*(\w+)", re.M),
    "Go": re.compile(r"^func\s+(?:\([^)]*\)\s*)?(\w+)", re.M),
    "TS": re.compile(r"^[ \t]*(?:export\s+)?(?:default\s+)?(?:(?:public|private|protected|static|async|readonly|override|abstract)\s+)*"
                     r"(?:function\s*\*?\s*(\w+)|(?:const|let)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*(?::[^=]+)?=>"
                     r"|(\w+)\s*(?:<[^>]*>)?\s*\([^)]*\)\s*(?::\s*[^{;]+)?\{)", re.M),
    "Python": re.compile(r"^([ \t]*)(?:async\s+)?def\s+(\w+)", re.M),
    "Kotlin": re.compile(r"^[ \t]*(?:(?:public|private|internal|protected|override|open|abstract|suspend|inline|operator|infix)\s+)*fun\s+(?:<[^>]*>\s*)?(?:[\w.]+\.)?(\w+)", re.M),
    "Java": re.compile(r"^[ \t]+(?:(?:public|private|protected|static|final|synchronized|abstract|native)\s+)*[\w<>\[\],?\s]+?\s+(\w+)\s*\([^)]*\)\s*(?:throws[^{]+)?\{", re.M),
    "Dart": re.compile(r"^[ \t]*(?:static\s+)?(?:Future<[^>]*>|Widget|void|String|int|bool|double|[\w<>?]+)\s+(\w+)\s*\([^)]*\)\s*(?:async\s*)?\{", re.M),
    "Rust": re.compile(r"^[ \t]*(?:pub(?:\([^)]*\))?\s+)?(?:const\s+|async\s+|unsafe\s+|extern\s+\"C\"\s+)*fn\s+(\w+)", re.M),
    "Ruby": re.compile(r"^([ \t]*)def\s+(?:self\.)?([\w?!=]+)", re.M),
}
TYPE = {
    "Swift": re.compile(r"^[ \t]*(?:(?:public|open|private|fileprivate|internal|final|indirect)\s+)*(?:class|struct|enum|protocol|actor)\s+([\w.]+)", re.M),
    "ObjC": re.compile(r"^@interface\s+(\w+)\s*(?::|$)", re.M),
    "ObjC-h": re.compile(r"^@interface\s+(\w+)\s*(?::|$)", re.M),
    "Go": re.compile(r"^type\s+(\w+)\s+(?:struct|interface)\b", re.M),
    "TS": re.compile(r"^[ \t]*(?:export\s+)?(?:declare\s+)?(?:abstract\s+)?(?:class|interface|enum)\s+(\w+)", re.M),
    "Python": re.compile(r"^class\s+(\w+)", re.M),
    "Kotlin": re.compile(r"^[ \t]*(?:\w+\s+)*(?:class|interface|object)\s+(\w+)", re.M),
    "Java": re.compile(r"^[ \t]*(?:\w+\s+)*(?:class|interface|enum)\s+(\w+)", re.M),
    "Dart": re.compile(r"^(?:abstract\s+)?(?:class|mixin|enum)\s+(\w+)", re.M),
    "Rust": re.compile(r"^[ \t]*(?:pub(?:\([^)]*\))?\s+)?(?:struct|enum|trait|union)\s+(\w+)", re.M),
    "Ruby": re.compile(r"^[ \t]*(?:class|module)\s+([\w:]+)", re.M),
}
TYPE["JS"] = TYPE["TS"]
GO_IMPORT = re.compile(r'^import\s*\([^)]*\)|^import\s+(?:\w+\s+)?"[^"]+"', re.M)
IMPORT = {
    "TS": re.compile(r"""(?:import|export)\s[^'";]*?\sfrom\s*['"]([^'"]+)['"]|import\s*\(\s*['"]([^'"]+)['"]\s*\)"""
                     r"""|require\(\s*['"]([^'"]+)['"]\s*\)|^[ \t]*import\s+['"]([^'"]+)['"]""", re.M),
    "Rust": re.compile(r"^[ \t]*(?:pub(?:\([^)]*\))?\s+)?use\s+([\w:]+)|^[ \t]*extern\s+crate\s+(\w+)", re.M),
    "Python": re.compile(r"^[ \t]*import\s+([\w.]+)|^[ \t]*from\s+([\w.]+)\s+import", re.M),
    "Swift": re.compile(r"^[ \t]*import\s+(\w+)", re.M),
    "ObjC": re.compile(r'^[ \t]*#import\s+["<]([^">]+)[">]', re.M),
    "Kotlin": re.compile(r"^[ \t]*import\s+([\w.]+)", re.M),
    "Dart": re.compile(r"""^[ \t]*import\s+['"]([^'"]+)['"]""", re.M),
    "Ruby": re.compile(r"""^[ \t]*require(?:_relative)?\s+['"]([^'"]+)['"]""", re.M),
}
IMPORT["ObjC-h"] = IMPORT["ObjC"]
IMPORT["Java"] = IMPORT["Kotlin"]
EFFECT = {
    "Go": re.compile(r'"(os|os/exec|net|net/http|io/ioutil|database/sql|syscall)"|\btime\.Now\(|\brand\.'),
    "TS": re.compile(r"""from\s*['"](?:node:)?(fs|fs/promises|child_process|http|https|net|dns|os)['"]"""
                     r"""|\bfetch\(|\bDate\.now\(|new Date\(\)|Math\.random\(|process\.env|crypto\.random"""),
    "Rust": re.compile(r"\bstd::(fs|net|process|env)\b|\bSystemTime\b|\bInstant::now\b|\brand::|\btokio::(fs|net|process)\b|\breqwest\b"),
    "Python": re.compile(r"^[ \t]*(?:import|from)\s+(os|subprocess|socket|shutil|requests|urllib|http|random|time|datetime)\b|\bopen\(|os\.environ", re.M),
    "Swift": re.compile(r"\bFileManager\b|\bURLSession\b|\bDate\(\)|\bProcessInfo\b|\bUUID\(\)|\barc4random"),
    "ObjC": re.compile(r"\bNSFileManager\b|\bNSURLSession\b|\[NSDate date\]|\bNSProcessInfo\b|\barc4random"),
    "Kotlin": re.compile(r"\bjava\.io\.File\b|\bjava\.net\b|\bSystem\.currentTimeMillis\b|\bRandom\(|\bProcessBuilder\b|\bSystem\.getenv\b"),
    "Dart": re.compile(r"\bdart:io\b|\bHttpClient\b|\bDateTime\.now\(|\bRandom\("),
    "Ruby": re.compile(r"\bFile\.|\bNet::HTTP\b|\bTime\.now\b|\bENV\[|\bsystem\("),
}
EFFECT["Java"] = EFFECT["Kotlin"]
PUBLIC = {
    "Go": re.compile(r"^(?:func|type|var|const)\s+([A-Z]\w*)", re.M),
    "TS": re.compile(r"^export\s+(?:default\s+)?(?:declare\s+)?(?:abstract\s+)?(?:async\s+)?(?:function\*?|class|interface|type|enum|const|let|var)\s+(\w+)", re.M),
    "Rust": re.compile(r"^pub\s+(?:\([^)]*\)\s+)?(?:(?:const|async|unsafe)\s+)*(?:fn|struct|enum|trait|type|const|static|mod)\s+(\w+)", re.M),
    "Python": re.compile(r"^(?:def|class)\s+([A-Za-z]\w*)|^([A-Z][A-Z0-9_]*)\s*=", re.M),
    "Swift": re.compile(r"^[ \t]*(?:public|open)\s+(?:\w+\s+)*?(?:func|class|struct|enum|protocol|var|let)\s+(\w+)", re.M),
    "ObjC-h": re.compile(r"^[-+]\s*\([^)]*\)\s*(\w+)", re.M),
    "Kotlin": re.compile(r"^(?:public\s+)?(?:(?:open|data|sealed|abstract|suspend|inline)\s+)*(?:fun|class|interface|object|val|var)\s+(?:<[^>]*>\s*)?(\w+)", re.M),
    "Java": re.compile(r"^[ \t]*public\s+(?:(?:static|final|abstract)\s+)*(?:class|interface|enum)\s+(\w+)", re.M),
    "Dart": re.compile(r"^(?:class|mixin|enum|extension|typedef)\s+([A-Za-z]\w*)|^(?:[\w<>?]+\s+)?([a-z]\w*)\s*\(", re.M),
    "Ruby": re.compile(r"^[ \t]*(?:class|module)\s+([\w:]+)", re.M),
}
TS_EXPORT_LIST = re.compile(r"^export\s*\{([^}]*)\}", re.M)


def is_public(lang, line):
    if lang == "Swift":
        return bool(re.search(r"\b(public|open)\b", line))
    if lang == "Go":
        return bool(re.match(r"^func\s+(?:\([^)]*\)\s*)?[A-Z]", line))
    if lang in ("TS", "JS"):
        return line.lstrip().startswith("export")
    if lang == "Python":
        m = re.match(r"^def\s+(\w+)", line)
        return bool(m and not m.group(1).startswith("_"))
    if lang == "Rust":
        return line.lstrip().startswith("pub")
    if lang == "Kotlin":
        return not re.search(r"\b(private|internal|protected)\b", line)
    if lang == "Java":
        return "public" in line
    return False
