# 03 役以外の部品（parts）

六役の箱とは別に、必ず置くもの。Atomic Design には無い。

| 部品 | 英名 | 何か | 置き場 | 規則 |
| --- | --- | --- | --- | --- |
| 偽物 | `fake` | mirror と同じ入口を持つ、外界に触らない実装 | mirror の隣 | mirror を作った瞬間に作る。契約テストで本物と突き合わせる |
| 資料 | `catalog` | 変わる部分をコードの外に出したデータ | `catalog/` `spec/` `templates/` など | スキーマを持つ。コードは解釈器に留める |
| 証拠 | `evidence` | テスト・bench・proofs・evidence | 箱の隣、または `bench/` `proofs/` | 箱ごとに同じ大きさで 1 つ |
| 見本 | `demo` | 使い手そのもの | `examples/` `Demo/` | ライブラリなら同居させる |

## 写しの三つ組

mirror は単体で存在させない。

```
storage/
  storage.go      ← 入口（interface）
  s3.go           ← mirror（本物）
  fake.go         ← fake（偽物）
  contract_test.go← 契約テスト。本物と偽物に同じケースを流す
```

| 規則 | 内容 |
| --- | --- |
| 同時に作る | mirror・fake・契約テストは 1 コミットで生まれる |
| 契約テスト | 本物と偽物の両方に同じケースを流す。偽物が本物からずれたら落ちる。本物側は環境変数で opt-in |
| fake の純度 | fake は副作用禁止。メモリだけ |
| 1.0 の根拠 | SwiftyAPIRequest の `mockResponse()`（2017）、syncenv `storage/mock.go`、connpass `fakeconnpass` |

## 資料

| 規則 | 内容 |
| --- | --- |
| スキーマ | 資料には必ずスキーマを付ける。エージェントが増やす対象 |
| 解釈器 | 資料を読むコードは小さく保ち、人が読む |
| 1.0 の根拠 | archgopher `catalog/` 1,300 ファイル、als `spec/` 1,000 本、codopsy `Formula/` |
