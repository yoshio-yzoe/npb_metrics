from __future__ import annotations
from bs4 import BeautifulSoup, Comment
from typing import Dict, List
import pandas as pd

from .constants import ROOT_URL
from .client import session


def fetch_soup(path_or_url: str) -> BeautifulSoup:
    url = path_or_url if path_or_url.startswith("http") else f"{ROOT_URL}{path_or_url}"
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "lxml")


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
