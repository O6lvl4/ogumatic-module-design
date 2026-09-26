# 05 眼（eye）

六段の検査。言語に依存しない定義をここに置き、言語への写像は `eye/` に置く。

## 六段

| # | 段 | 測るもの | 落とす | 告げる | 根拠（手書き期の実測） |
| --- | --- | --- | --- | --- | --- |
| 1 | 関数 | 行数・引数・ネスト | 30 行超 | 引数 4 以上、ネスト 4 以上 | 中央値 5〜12、p90 14〜47、40 行超 0〜2% |
| 2 | ファイル | 型の数・行数 | 型宣言 2 つ以上（その型の extension / impl は除く）、120 行超 | 80 行超 | 中央値 21〜32、1 ファイル 1 型 52% |
| 3 | import | 札の `knows` | `knows` に無い箱を import | 役の表と食い違う `knows` | archgopher 許可表、dependency-cruiser |
| 4 | 副作用 | fs・net・process・時計・env・乱数 | mirror 以外での使用 | fake での使用 | archgopher 31 中 6、qusp-core 30/44 が違反 |
| 5 | 入口 | 公開シンボル | 札の `surface` に無い公開、facade で 5 本以上 | — | MOAspects 4、GADInjector 3 |
| 6 | コミット | 触った箱の数・件名 | 3 箱以上 | 2 箱、件名が接頭辞だけ | 2015〜21 の 1 ファイル 12 行、1 ファイル率 55% |

## 判定

| 語 | 意味 |
| --- | --- |
| 落とす | CI とエージェントのフックで exit 1 |
| 告げる | 出力に出すが止めない |
| 例外 | 地図の `exceptions` に理由と期限を書いたものだけ落とさない |

## 閾値の持ち方

閾値は地図の `eye:` に書く。書かなければ上の既定。閾値を緩めるときは理由を書く。

## 作り

眼は言語に依存しない中核と、言語ごとの薄い抽出器に分ける。中核は**事実（facts）**だけを見る。

```
repo ──抽出器（言語ごと）──▶ facts ──中核──▶ 落とす / 告げる
       ▲                      ▲
       │                      └ 言語を知らない。関数・ファイル・import・副作用・公開の事実だけ
       └ 言語を知る唯一の場所。正規表現でも tree-sitter でもよい
```

| 事実 | 項目 |
| --- | --- |
| 関数 | 箱・ファイル・名前・開始行・行数・引数の数・ネスト・公開か |
| ファイル | 箱・パス・言語・行数・型の名前・公開シンボル・import 文・副作用の出現（行と原語）・テストか |
| 変更 | 触ったファイル・件名（git から） |

抽出器の契約は「テキストと言語名を受けて事実を返す」だけ。精度の低い正規表現の抽出器から始め、言語ごとに tree-sitter の抽出器へ差し替えられる。差し替えても中核と札は変わらない。

## 言語への写像（抽出器の規則表）

| 段 | 何を「関数」「型」「import」「副作用」「公開」と見なすか |
| --- | --- |
| Go | func / type / import path / `os` `net` `io` `time.Now` `os/exec` `math/rand` / 大文字始まり |
| TypeScript | function・メソッド・arrow / class・interface・type・enum / import 文 / `node:fs` `child_process` `fetch` `Date.now` `crypto.random*` / `export` |
| Rust | fn / struct・enum・trait / `use` と Cargo の path 依存 / `std::fs` `std::net` `std::process` `std::env` `SystemTime` `rand` / `pub` |
| Swift | func・init / class・struct・enum・protocol（extension は本体に帰属） / import と target 依存 / `FileManager` `URLSession` `Date()` `ProcessInfo` / `public` `open` |
| Python | def / class / import / `os` `subprocess` `socket` `time` `random` / `_` で始まらない |

コミットの段は言語に依らず git で測る。
