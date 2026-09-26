# eye（検査器）

抽象定義は [docs/05-eye.md](../docs/05-eye.md)。ここには言語別の実装を置く。

| 部品 | 状態 | 形 |
| --- | --- | --- |
| 中核 | v0.2.0 | 札・地図・事実を受けて六段を判定する。言語を知らない |
| 抽出器 | v0.2.0 | 正規表現と括弧対応で 10 言語（Go・TS/JS・Rust・Python・Swift・ObjC・Kotlin・Java・Dart・Ruby）の事実を出す。精度は低い |
| 抽出器（tree-sitter） | 未 | 言語ごとに差し替える。中核は変えない |

## 使い方

```
uvx --from git+https://github.com/O6lvl4/ogumatic-module-design ogumatic eye .      # 六段を回す
uvx --from git+https://github.com/O6lvl4/ogumatic-module-design ogumatic facts .    # 事実だけ見る（札が無くても動く）
uvx --from git+https://github.com/O6lvl4/ogumatic-module-design ogumatic atlas .    # box.yaml を走査して地図との差を出す
```

repo の中では `PYTHONPATH=eye python3 -m ogumatic_eye eye .` でも同じ。

## 眼の箱（自分に自分の眼を当てる）

| 箱 | 役 | 何をするか |
| --- | --- | --- |
| `vocab` | vocabulary | Card・Atlas・Func・FileFact・Finding・閾値・役の表 |
| `fsmirror` | mirror | ファイル列挙・読み取り・git。偽物と契約テストを隣に置く |
| `loader` | translator | YAML と git の出力を語彙に直す |
| `extract` | meter | テキストから事実を出す。言語の規則表を持つ |
| `checks` | meter | 事実と札から六段の判定を出す |
| `registry` | registry | 抽出器と検査を列挙し、組み立てる唯一の場所 |
| `cli` | facade | `eye` `facts` `atlas` の 3 入口 |

## 検査器の契約

| 項目 | 内容 |
| --- | --- |
| 入力 | repo 直下の `ogumatic.yaml` と各 `box.yaml`。YAML の日付（`closed_on` `until`）は ISO 文字列に正規化してからスキーマ検証する |
| 出力 | 段ごとに `落とす` / `告げる` の一覧。1 行 1 件。`<段> <箱> <場所> <理由>` |
| 終了コード | 落とすが 1 件でもあれば 1 |
| 例外 | 地図の `exceptions` を読み、期限内なら落とさない。期限切れは落とす |
