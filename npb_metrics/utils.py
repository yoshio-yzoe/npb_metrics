"""
HTML 取得 & 解析ユーティリティ

- 最低 2 秒のレートリミットを挿入（_respect_rate_limit）
- 429, 5xx が出た場合は自動リトライ (urllib3 Retry)
"""

from __future__ import annotations

import time
import pandas as pd
from typing import Dict, List

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .client import session
from .constants import ROOT_URL

# ────────────────────────────────────────────────────────────
# Retry ポリシー: 429 や一時的 5xx を最大 5 回リトライ
# ────────────────────────────────────────────────────────────
retries = Retry(
    total=5,
    backoff_factor=1.5,            # 0 → 1.5 → 3 → 4.5 → ...
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
session.mount("https://", HTTPAdapter(max_retries=retries))

# ────────────────────────────────────────────────────────────
# シンプルなレートリミッタ（2 秒間隔）
# ────────────────────────────────────────────────────────────
_MIN_INTERVAL = 2.0  # sec
_last_call = 0.0


def _respect_rate_limit() -> None:
    global _last_call
    wait = _MIN_INTERVAL - (time.time() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.time()


def fetch_soup(path_or_url: str) -> BeautifulSoup:
    """
    URL もしくはルートからのパスを受け取り、BeautifulSoup を返す
    """
    _respect_rate_limit()

    url = (
        path_or_url
        if path_or_url.startswith("http")
        else f"{ROOT_URL}{path_or_url}"
    )
    resp = session.get(url, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "lxml")


# 既存の league_summary_soup, league_team_links, scraping_table など
# 以降の関数はそのまま動作します。



def league_summary_soup(league: str) -> BeautifulSoup:
    return fetch_soup(f"/register/league.cgi?code={league}&class=Fgn")


def league_team_links(soup: BeautifulSoup) -> Dict[int, Dict[str, str]]:
    """
    {2024: {"Hanshin Tigers": "/teams/...html", ...}, 2023: {...}}
    """
    table = soup.select_one("table")
    result: Dict[int, Dict[str, str]] = {}
    for row in table.select("tbody > tr"):
        year = int(row.th.text.strip())
        links = {
            a.text.strip(): a["href"] for a in row.select("td a[href]")
        }
        result[year] = links
    return result


def scraping_table(table_tag) -> pd.DataFrame:
    header = [th.text for th in table_tag.select_one("tr").find_all("th")][1:]
    rows = [
        [td.text.strip() for td in tr.select("td")]
        for tr in table_tag.select("tbody > tr")
    ]
    df = pd.DataFrame(rows, columns=header)
    # dominant hand 補正
    df["Hand"] = "Right"
    df.loc[df["Name"].str.endswith("*"), "Hand"] = "Left"
    df.loc[df["Name"].str.endswith("#"), "Hand"] = "Double"
    df["Name"] = df["Name"].str.rstrip("*# ").str.strip()
    return df
