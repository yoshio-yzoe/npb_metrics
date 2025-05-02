"""
Scrape NPB data via npb_metrics and export to docs/data/players.json
Run locally or from GitHub Actions.
"""

from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd

from npb_metrics import Pitcher, Batter  # ← 必要に応じて追加

OUT_DIR = Path("docs/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main() -> None:
    # --- scrape -----------------------------------------------------------
    years = [2023, 2024]              # 必要な年を追加
    df = Pitcher(years=years).dataframe().reset_index()

    # --- export -----------------------------------------------------------
    out_json = OUT_DIR / "players.json"
    df.to_json(out_json, orient="records", force_ascii=False)

    # 最終更新日時を書き出し（任意）
    ts = pd.Timestamp.now(tz=ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")
    Path("docs/last_update.txt").write_text(f"last_update: {ts}\n", encoding="utf-8")

    print(f"✔ exported {len(df):,} records -> {out_json}")


if __name__ == "__main__":
    main()
