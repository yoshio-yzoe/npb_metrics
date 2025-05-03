"""
DataFrame → JSON を生成するビルドスクリプト

使い方例:
    poetry run python gen_site.py --from 2005 --to 2024
    poetry run python gen_site.py --from 2010 --to 2014 --append
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from npb_metrics import Pitcher, Batter  # 必要なら Batter も

OUT_DIR = Path("docs/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = OUT_DIR / "players.json"


def scrape_dataframe(year_from: int, year_to: int) -> pd.DataFrame:
    years = list(range(year_from, year_to + 1))
    print(f"▶ scraping {years}")

    df = Pitcher(years=years).dataframe().reset_index()
    # 例: 打者データも結合したい場合
    # df_bat = Batter(years=years).dataframe().reset_index()
    # df = pd.concat([df, df_bat], ignore_index=True)

    return df


def write_json(df: pd.DataFrame, append: bool) -> None:
    if append and OUT_JSON.exists():
        print("append mode: merging with existing JSON …")
        existing = pd.read_json(OUT_JSON)
        df = pd.concat([existing, df]).drop_duplicates(
            subset=["team", "year", "Name"]
        )

    df.to_json(OUT_JSON, orient="records", force_ascii=False)
    print(f"✔ wrote {OUT_JSON}  ({OUT_JSON.stat().st_size/1_048_576:.1f} MB)")


def write_timestamp() -> None:
    ts = pd.Timestamp.now(tz=ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")
    Path("docs/last_update.txt").write_text(f"last_update: {ts}\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="year_from", type=int, default=2020)
    ap.add_argument("--to", dest="year_to", type=int, default=2024)
    ap.add_argument("--append", action="store_true", help="既存 JSON に追記")
    args = ap.parse_args()

    df = scrape_dataframe(args.year_from, args.year_to)
    write_json(df, append=args.append)
    write_timestamp()


if __name__ == "__main__":
    main()
