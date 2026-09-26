# 06 箱札（card）

箱 1 つに `box.yaml` を 1 つ、箱のディレクトリ直下に置く。札が正、コードは写し。

## 項目

| 項目 | 型 | 必須 | 意味 |
| --- | --- | --- | --- |
| `name` | string | ○ | 箱の名前。名詞。8 字以下推奨 |
| `role` | enum | ○ | `vocabulary` `meter` `mirror` `translator` `registry` `facade` |
| `knows` | string[] | ○ | import してよい箱の `name`。空配列は「誰も知らない」 |
| `external` | string | mirror のみ○ | 写す外界の名（`aws pricing api` `s3` `clock`） |
| `surface` | string[] | ○ | 公開する入口の名。facade は 4 本まで |
| `evidence.tests` | string | ○ | テストの場所 |
| `evidence.fake` | string | mirror のみ○ | 偽物の場所 |
| `evidence.contract` | string | mirror のみ○ | 契約テストの場所 |
| `evidence.bench` | string | — | bench の場所 |
| `evidence.demo` | string | — | 見本の場所 |
| `state` | enum | ○ | `open`（書いている） `closed`（閉じた。手で直さない） `nurtured`（育てる。repo に 3 つまで） |
| `closed_on` | date | closed のとき○ | 閉じた日。`YYYY-MM-DD`。検査器が文字列に正規化する |
| `regenerable` | bool | — | 札と証拠から作り直してよいか。既定 true |
| `note` | string | — | 1 行。理由だけ。経緯は書かない |

## 例

```yaml
# provider/aws/pricelist/box.yaml
name: pricelist
role: mirror
external: aws pricing api
knows: []
surface: [Fetch]
evidence:
  tests: pricelist_test.go
  fake: fake.go
  contract: contract_test.go
state: closed
closed_on: 2026-06-02
```

```yaml
# meter/box.yaml
name: meter
role: meter
knows: [book]
surface: [Load, Rate, Headroom]
evidence:
  tests: meter_test.go
  bench: bench/meter
state: nurtured
note: 単位の変換規則が増え続けるので育てる
```

## 規則

| 規則 | 内容 |
| --- | --- |
| 1 箱 1 札 | 札の無い箱は眼 3 で落とす |
| 役と `knows` の整合 | 役の表で許されない相手が `knows` にあれば眼 3 で告げる |
| 入口は札が先 | 公開シンボルを増やすときは札の `surface` を先に直す |
| 閉じる | `state: closed` にしたら `closed_on` を書く。以後の変更は再生成として新しい札で行う |
