# 02 六役（roles）

箱は**大きさ**ではなく**役割**で段に並べる。段はフォルダで掘らず、import の向きで作る。

## 六役

| 役 | 英名 | 何をする箱か | 知ってよい相手 | 副作用 | 数 |
| --- | --- | --- | --- | --- | --- |
| 語彙 | `vocabulary` | 値と型。業務の名詞そのもの | 標準ライブラリだけ | 無し | 多い。26 行でも 1 箱 |
| 計器 | `meter` | 語彙を受けて語彙を返す純ロジック | vocabulary、下段の meter | 無し | 中段の大半 |
| 写し | `mirror` | 外界 1 つを 1 関数 1 呼び出しで写す | その外界だけ。内側を知らない葉 | **ここだけ許す** | 外界 1 つに 1 箱 |
| 翻訳 | `translator` | 写しの形を語彙の形に直す | mirror、vocabulary、meter | 無し（mirror に委ねる） | mirror と 1 対 1 |
| 名簿 | `registry` | 翻訳を全部知り、組み立てる唯一の場所 | translator、meter、vocabulary | 無し | **repo に 1 つ** |
| 顔 | `facade` | 使う側に見せる入口 | registry。署名に使う vocabulary | 無し | 入口 4 本まで |

## 段

```
facade        顔      ─ 入口 4 本まで
registry      名簿    ─ repo に 1 つ。"the one place that lists the providers"
translator    翻訳    ─ mirror ごとに 1 つ
mirror        写し    ─ 外界ごとに 1 つ。副作用はここだけ。fake を隣に置く
meter         計器    ─ 純ロジック。段は import が作る
vocabulary    語彙    ─ 最下段。fan-in 最大
```

矢印は上から下へだけ。同じ段どうしは頼らない（meter → 下段の meter は可）。

## 役の判定

| 問い | はい | いいえ |
| --- | --- | --- |
| fs・net・process・時計・env・乱数に触るか | mirror | 次へ |
| 外の形を内の形に直しているか | translator | 次へ |
| 翻訳を列挙し、組み立てているか | registry | 次へ |
| 使う側が最初に呼ぶ入口か | facade | 次へ |
| 語彙を受けて語彙を返す判断があるか | meter | vocabulary |

## 命名

| 規則 | 内容 |
| --- | --- |
| 名詞 | 箱の名前は業務の名詞（model・meter・report）。層名（domain・infrastructure・service・manager・utils）を使わない |
| 短く | 8 字以下を推奨。造語でよい |
| 外界の名 | mirror は写す外界の名（pricelist・retailprices・s3）。translator は内側の語（provider/aws） |
| 名簿 | registry は「列挙している対象」の名（cloud・providers）。composition でも可 |

## 1.0 での実例

| 役 | 実例 |
| --- | --- |
| vocabulary | archgopher `model` `book` `field`、MOAspectsTarget、GADField |
| meter | archgopher `meter` `traffic` `facet` `scouter` `engine` `report` |
| mirror | MOARuntime、GADSender、`provider/aws/pricelist`、`storage/s3` |
| translator | `provider/aws`、MOAspects の private 部、syncenv storage の Upload / Download |
| registry | archgopher `cloud`、llmine providerRegistry、memre `internal/composition` |
| facade | MOAspects、GADInjector、`api`、`cmd`、`cli` |
