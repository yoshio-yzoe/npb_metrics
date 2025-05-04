# NPB_Metrics

NPB（日本プロ野球）公式戦のチーム／選手成績を[Baseball-Reference](https://www.baseball-reference.com/) からスクレイピングし、  `pandas.DataFrame` で簡単に扱えるようにする Python ライブラリ



## 特長
- **投手・打者のシーズン成績をワンライナーで取得**
- DataFrame インデックスを `team / year / Name` で階層化


## インストール

### 前提

| ツール | 推奨バージョン |
|--------|---------------|
| Python | 3.10 – 3.12 |
| Poetry | ≥ 1.8 |

### 手順

```bash
git clone https://github.com/yoshio-yzoe/NPB_Metrics.git
cd NPB_Metrics

poetry install
poetry shell
```

## クイックスタート

```python
from npb_metrics import Pitcher, Batter

# 2024 年の阪神タイガース投手成績
df_pitch = Pitcher(years=[2024], team="Hanshin Tigers").dataframe()
print(df_pitch.head())

# セ・パ両リーグ 2023–2024 年の打者成績（全チーム）
df_bat = Batter(years=[2023, 2024]).dataframe()
# チーム別 OPS 上位 10 名
print(
    df_bat.assign(OPS=df_bat["OBP"].astype(float) + df_bat["SLG"].astype(float))
         .sort_values("OPS", ascending=False)
         .head(10)
)
```

## GitHub Pages
2005~2024年までのデータを格納済み
現在はチームと年を選択可能です。

yoshio-yzoe.github.io/npb_metrics/


## How to use
以下は使用例です。

### ① 年度・リーグを絞らず全チーム投手成績
```python
from npb_metrics import Pitcher

# 2024 年の全投手（セ・パ両リーグ）
df = Pitcher(years=[2024]).dataframe()
print(df.head())
````

### ② パ・リーグ 2010–2020 の打者成績（全チーム）

```python
from npb_metrics import Batter

df = Batter(years=range(2010, 2021), league="JPPL").dataframe()
```

### ③ 特定チーム × 複数年の縦持ち DataFrame

```python
from npb_metrics import Pitcher

df = Pitcher(
    years=[2022, 2023, 2024],
    team="Fukuoka Softbank Hawks"
).dataframe()
# インデックスは (team, year, Name)
```

### ④ 投手 + 打者を結合して 1 テーブルにする

```python
from npb_metrics import Pitcher, Batter
import pandas as pd

df = pd.concat([
    Pitcher(years=[2024]).dataframe().reset_index(),
    Batter(years=[2024]).dataframe().reset_index()
])
```

### ⑤ 直近 20 年分をまとめて取得（キャッシュ対応）

```python
from npb_metrics import Pitcher

df = Pitcher(years=range(2005, 2025)).dataframe().reset_index()
df.to_parquet("npb_pitchers_2005_2024.parquet")
```

> `requests-cache` が有効なので初回は時間が掛かりますが、
> 2 回目以降はローカルキャッシュが使われ高速になります。

---

### 引数まとめ

* **`years`**: 取得したい年度のイテラブル（必須。複数年 OK）
* **`league`**: `"JPCL"`（セ） / `"JPPL"`（パ） / `None`（両リーグ）。デフォルト `None`
* **`team`**: チーム英語名を指定するとそのチームだけ取得。デフォルト `None`

速度をもっと上げたい場合は年度を小分けにして `gen_site.py --append` でJSON をマージすると、レート制限を守りつつ大量データを安全に取得できます。

