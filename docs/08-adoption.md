# 08 導入（adoption）

## 新しい repo

| 順 | すること |
| --- | --- |
| 1 | `templates/ogumatic.yaml` と `templates/CLAUDE.md` を repo 直下に写す |
| 2 | 最初の箱を vocabulary から切り、`box.yaml` を先に書く |
| 3 | 外界に触る箱は mirror・fake・契約テストを 1 コミットで作る |
| 4 | registry を 1 つ、facade を 1 つ置く |
| 5 | 眼を CI とフックに入れる（言語別の検査器は `eye/`） |

## 既存の repo

| 順 | すること | 眼の段階 |
| --- | --- | --- |
| 1 | 箱ごとに役を判定し、`box.yaml` を書く。判定に迷う箱は「翻訳」と「計器」の混在なので割る | 告げるだけ |
| 2 | 地図を書く。既存の許可表（archgopher の `internal/layers`、dependency-cruiser）があれば `knows` に写す | 告げるだけ |
| 3 | 眼 3（import）と眼 4（副作用）を落とす側にする。違反は例外に期限付きで書く | 落とす |
| 4 | 眼 1・2・5・6 を落とす側にする | 落とす |
| 5 | mirror に fake と契約テストを足す | 落とす |

## pin の作法

| 場面 | 順序 |
| --- | --- |
| 術の版上げ | この repo でタグ → 使う側が `ogumatic:` を上げる → 眼を回す |
| kit の版上げ | kit でタグ → 使う側が `kits:` を上げる → 契約テストを回す |
| 逆順 | しない。使う側の都合で術や kit を直すときも、先に術・kit 側で着地させる |

## 段階（術そのものの進み）

| 段階 | 内容 | 状態 |
| --- | --- | --- |
| 0 | 抽象。文書・スキーマ・雛形・skill | 着手済み（v0.1.0） |
| 1 | 眼の検査器。Almide で書き、抽出器は gramide | 済（v0.3.0） |
| 2 | 試験導入。syncenv か tocsin | 未 |
| 3 | archgopher の許可表を札に変換 | 未 |
| 4 | kit-go・kit-ts・kit-rs | 未 |
| 5 | 各 repo が pin | 未 |
