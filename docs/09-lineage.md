# 09 他の段との対照（lineage）

Ogumatic は何を借り、何を足したか。段を持つ既存の考え方と役ごとに突き合わせる。

## Atomic Design（Brad Frost, 2013）

| Atomic | 何で段を切るか | Ogumatic での位置 | 違い |
| --- | --- | --- | --- |
| atom | 最小の UI 部品 | vocabulary（描画の語彙） | Ogumatic は大きさで切らない。26 行の値も 900 行の写しも同じ段に置きうる |
| molecule / organism | 部品の組み合わせ | meter（組み立ての純ロジック） | 「上は下の組み合わせで作る」は同じ。段の名前は付けない。段は import が作る |
| template | 配置 | facade の手前 | — |
| page | データを入れた実体 | facade（URL を知る入口）＋ registry | Atomic には外界・偽物・名簿・資料が無い。データ取得の置き場を決めていない |

借りたもの: 合成の階層。足したもの: 役割の軸、mirror / fake / registry / catalog。

## AWS CDK の L1 / L2 / L3

| CDK | 何か | Ogumatic での役 | 一致する点 |
| --- | --- | --- | --- |
| L1（`Cfn*`） | CloudFormation の資源定義から**生成**された 1:1 の写し | **mirror** | 外界を 1 関数 1 呼び出しで写す。しかも資料（仕様）から生成する。2.0 の「コードは生成物」そのもの |
| L2 | L1 を包み、意図で呼べる既定値と検証を足したもの | **translator** ＋ 狭い **facade** | 写しの形を語彙の形に直す。入口は少なく、既定値は中に |
| L3（patterns） | L2 を組み合わせた定型 | **meter** の上段 | 上の層は下の組み合わせだけで作る |
| App / Stack | 構成の組み立てと入口 | **registry** ＋ **facade** | 全部を列挙し組み立てる唯一の場所 |

借りたもの: L1 を資料から生成する発想、段の番号を公開 API の階級として見せる発想。
足したもの: fake と契約テスト（CDK は L1 の偽物を持たない）、札と地図、閉じる。
CDK に無いもので Ogumatic が持つのは「札が正」。CDK はコードが正で、構成の意図はコードの外に残らない。

## Clean Architecture / Ports and Adapters

| 既存 | Ogumatic | 備考 |
| --- | --- | --- |
| Entities | vocabulary | 同じ |
| Use Cases | meter | 同じ。ただし Ogumatic は名詞で切り、層名を箱の名前にしない |
| Interface Adapters | translator | 同じ |
| Frameworks & Drivers | mirror | Ogumatic は 1 関数 1 呼び出しに限り、fake を必須にする |
| Port（Cockburn） | mirror の入口（interface） | 同じ |
| Adapter（Cockburn） | mirror の実装 ＋ translator | Ogumatic は写しと翻訳を別の箱に割る |
| DI container / main | registry | 同じ。repo に 1 つ |
| Controller / Presenter | facade | 入口 4 本まで |

借りたもの: 依存の向きと層の役。足したもの: 写しと翻訳の分離、fake の必須化、名簿を 1 つに限る規則、札。

## Parnas（1972）と Ousterhout（2018）

| 出典 | 原則 | Ogumatic での形 |
| --- | --- | --- |
| Parnas | 変わる理由ごとにモジュールを切り、決定を隠す | 「名で断ち切りて」。箱は名詞、札に知ってよい相手を書く |
| Ousterhout | 深いモジュール（狭い interface、厚い実装） | 「口はせまくて、腹ふかく」。facade は 4 本まで |
| Martin（SDP） | 安定な方へ依存する | 「矢は一路」。眼 3 が落とす |

## 一言で

| 借りた | 足した |
| --- | --- |
| Atomic の合成、CDK の生成される写し、Clean Architecture の役、Parnas の切り方、Ousterhout の深さ | 役割の軸で段を作ること、写しと翻訳の分離、fake と契約テスト、名簿 1 つ、資料、札と地図、眼、閉じる |
