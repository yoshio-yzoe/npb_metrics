"""
Scrape NPB data via npb_metrics and export to docs/data/players.json
Run locally or from GitHub Actions.
"""

from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd
import argparse
import numpy as np

from npb_metrics import Pitcher, Batter  # ← 必要に応じて追加

OUT_DIR = Path("docs/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main(year_from: int, year_to: int):
    years = list(range(year_from, year_to + 1))   # ← 2005–2024 など
    print(f"▶ scraping {years}")

    df = Pitcher(years=years).dataframe().reset_index()   # ここを必要に応じて Batter も併用

    out_json = OUT_DIR / "players.json"
    df.to_json(out_json, orient="records", force_ascii=False, indent=None)
    print(f"✔ {out_json}  {out_json.stat().st_size/1_048_576:.1f} MB")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="year_from", type=int, default=2005)
    ap.add_argument("--to",   dest="year_to",   type=int, default=2024)
    args = ap.parse_args()
    main(args.year_from, args.year_to)
