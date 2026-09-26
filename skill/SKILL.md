---
name: ogumatic
description: Ogumatic Module Design（モジュールを役割の段で切り、正を札・証拠・資料に置く設計術）で箱を切る・札を書く・眼で検査する・地図を更新する・写しを三つ組で作る。「この機能をどう分割するか」「モジュールを切って」「箱札を書いて」「役を判定して」「眼を回して」「写しを作って」「地図を更新して」「ogumatic で」と言われたら使う。導入されていない repo でも、役の判定と切り方の提案だけなら使える。
---

# /ogumatic

術の本文は `../docs/`。判断に迷ったら読む順は `02-roles.md` → `04-rules.md` → `05-eye.md`。

## 入口

| 言われ方 | すること |
| --- | --- |
| 切る（「分割して」「箱に切って」） | 役の判定 → 箱の一覧 → 札の下書き。コードはまだ書かない |
| 札（「box.yaml を書いて」） | 対象の箱を読み、札を書く。`surface` は実体の公開シンボルから、`knows` は import から起こす |
| 写し（「外界 X の写しを作って」） | mirror・fake・契約テストを 1 コミットで作る。翻訳は別の箱 |
| 眼（「検査して」「眼を回して」） | `uvx --from git+https://github.com/O6lvl4/ogumatic-module-design ogumatic eye .` を回す（コミットの段は `--range HEAD~1..HEAD`）。地図が無ければ `ogumatic facts . --auto` で事実だけ出す |
| 地図（「地図を更新して」） | `box.yaml` を走査して `ogumatic.yaml` の `boxes` を同期する。無い札は作らず告げる |
| 閉じる（「この箱を閉じて」） | 眼を回し、落ちていなければ `state: closed` と `closed_on` を書く |

## 切るときの手順

1. 業務の名詞を列挙する。名詞 1 つが vocabulary の候補。
2. 外界（fs・net・process・時計・env・乱数）を列挙する。外界 1 つが mirror 1 つ。
3. 名詞を受けて名詞を返す判断を列挙する。それが meter。段は import の向きで決め、フォルダで掘らない。
4. mirror ごとに translator を 1 つ。
5. registry を 1 つ、facade を 1 つ。facade の入口は 4 本まで。
6. 箱ごとに札を下書きし、`knows` が役の表に反していないか見る。
7. 提案は「箱の一覧（名前・役・knows・surface）」の表で返す。散文で語らない。

## 守ること

- 札が正。コードと札がずれていたら札を直すか、札に合わせてコードを直す。黙ってコードだけ直さない。
- 層名（domain・infrastructure・service・manager・utils）で箱を切らない。名詞で切る。
- 1 コミット 1 箱。件名は理由。
- `state: closed` の箱は触らない。作り直すなら新しい札。
- 導入されていない repo では、札と地図を置く前にユーザーに置き場を確認する。
