# NPB_Metrics

**NPB（日本プロ野球）公式戦のチーム／選手成績を  
[Baseball-Reference](https://www.baseball-reference.com/) からスクレイピングし、  
`pandas.DataFrame` で簡単に扱えるようにする Python ライブラリ**



## 特長

- **投手・打者のシーズン成績をワンライナーで取得**
- DataFrame インデックスを `team / year / Name` で階層化 → 集計が容易
- 依存は最小限：`requests` + `BeautifulSoup` + `pandas`
- **Poetry ベース**で再現性の高い環境構築
- MIT ライセンス（OSS 利用・商用利用可）



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

