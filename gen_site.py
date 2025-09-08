"""
投手・打者を別 JSON に出力し、最後に結合して all_players.json を作る。

使い方:
    poetry run python gen_site.py --from 2005 --to 2024
    poetry run python gen_site.py --from 2010 --to 2014 --append
"""

from __future__ import annotations
import argparse
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd

from npb_metrics import Pitcher, Batter

OUT_DIR = Path("docs/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PITCHER_JSON = OUT_DIR / "pitcher.json"
BATTER_JSON  = OUT_DIR / "batter.json"
ALL_JSON     = OUT_DIR / "all_players.json"


# ─────────────────────────────────────────────
# スクレイピング関数
# ─────────────────────────────────────────────
def scrape_pitchers(years: list[int]) -> pd.DataFrame:
    return Pitcher(years=years).dataframe().reset_index()

def scrape_batters(years: list[int]) -> pd.DataFrame:
    return Batter(years=years).dataframe().reset_index()


# ─────────────────────────────────────────────
# JSON 書き込みユーティリティ
# ─────────────────────────────────────────────
def write_json(df: pd.DataFrame, path: Path, append: bool) -> None:
    if append and path.exists():
        old = pd.read_json(path)
        df = (
            pd.concat([old, df], ignore_index=True)
              .drop_duplicates(subset=["team", "year", "Name"])
        )
    df.to_json(path, orient="records", force_ascii=False)
    size_mb = path.stat().st_size / 1_048_576
    print(f"✔ wrote {path} ({size_mb:.1f} MB)")


def write_timestamp() -> None:
    ts = pd.Timestamp.now(tz=ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")
    (OUT_DIR.parent / "last_update.txt").write_text(
        f"last_update: {ts}\n", encoding="utf-8"
    )


# ─────────────────────────────────────────────
# メイン
# ─────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="year_from", type=int, default=2020)
    ap.add_argument("--to",   dest="year_to",   type=int, default=2024)
    ap.add_argument("--append", action="store_true",
                    help="既存 JSON に追記モード")
    args = ap.parse_args()

    years = list(range(args.year_from, args.year_to + 1))
    print(f"▶ scraping {years}")

    
    # 投手
    try:
        df_pitch = scrape_pitchers(years)
        write_json(df_pitch, PITCHER_JSON, append=args.append)
    except Exception as e:
        print(f"❌ Failed to scrape pitchers: {e}")
        return
    

    # 打者
    try:
        df_bat = scrape_batters(years)
        write_json(df_bat, BATTER_JSON, append=args.append)
    except Exception as e:
        print(f"❌ Failed to scrape batters: {e}")
        return

    
    # 結合
    df_all = (
        pd.concat([pd.read_json(PITCHER_JSON), pd.read_json(BATTER_JSON)],
                  ignore_index=True)
          .sort_values(["year", "team", "Name"])
          .reset_index(drop=True)
    )
    df_all.to_json(ALL_JSON, orient="records", force_ascii=False)
    print(f"✔ wrote {ALL_JSON} ({ALL_JSON.stat().st_size/1_048_576:.1f} MB)")
    
    write_timestamp()
    


if __name__ == "__main__":
    main()
