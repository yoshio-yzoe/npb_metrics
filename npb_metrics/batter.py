from __future__ import annotations
from bs4 import BeautifulSoup
from .player import PlayerScraper


class BatterScraper(PlayerScraper):
    """打者成績テーブルを取得するスクレイパ。"""

    @staticmethod
    def _extract_table(team_soup: BeautifulSoup):
        table = team_soup.select_one("table#team_batting")
        if table is None:
            raise RuntimeError("Batting table not found – page format may have changed.")
        return table
