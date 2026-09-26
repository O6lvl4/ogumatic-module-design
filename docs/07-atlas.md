# 07 地図（atlas）

repo 直下に `ogumatic.yaml` を 1 つ。全箱の札を列挙し、pin と閾値と例外を持つ。エージェントが最初に読む 1 枚。

役としての「名簿（registry）」はコードの箱、「地図（atlas）」はこのファイル。混ぜない。

## 項目

| 項目 | 型 | 必須 | 意味 |
| --- | --- | --- | --- |
| `ogumatic` | string | ○ | 従う術の版（`v0.1.0`） |
| `boxes` | map | ○ | `name: path/to/box.yaml` |
| `nurtured` | string[] | — | 育てる箱の名。3 つまで |
| `kits` | map | — | 依存する kit と版（`kit-go: v0.3.0`） |
| `eye` | map | — | 閾値の上書き（`function_max: 30` `file_max: 120` `surface_max: 4` `commit_boxes_max: 2`） |
| `exceptions` | list | — | `{box, check, reason, until}`。期限を過ぎた例外は眼が落とす |

## 例

```yaml
ogumatic: v0.1.0
boxes:
  model:      model/box.yaml
  book:       book/box.yaml
  meter:      meter/box.yaml
  pricelist:  provider/aws/pricelist/box.yaml
  aws:        provider/aws/box.yaml
  cloud:      cloud/box.yaml
  cmd:        cmd/archgopher/box.yaml
nurtured: [meter, engine]
kits:
  kit-go: v0.1.0
eye:
  file_max: 150
exceptions:
  - box: report
    check: file
    reason: 出力テンプレートを 1 ファイルに保つため
    until: 2026-12-31
```

## 規則

| 規則 | 内容 |
| --- | --- |
| 列挙が正 | 地図に無い `box.yaml` は眼 3 で告げる。地図にあって無い札は落とす |
| 版の pin | `ogumatic` の版は術の repo のタグ。上げるときは術が先に着地し、使う側が pin を上げる |
| 例外に期限 | 期限の無い例外は書けない |
