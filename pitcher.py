from __future__ import annotations
from bs4 import BeautifulSoup, Comment
from .player import PlayerScraper

class PitcherScraper(PlayerScraper):
    """
    投手成績テーブルは `<table>` が HTML コメント内に埋まっているので
    コメントを展開して取り出す。
    """

    @staticmethod
    def _extract_table(team_soup: BeautifulSoup):
        # コメントノードをすべて走査し、最初に見つかった table を返す
        for comment in team_soup.find_all(string=lambda t: isinstance(t, Comment)):
            comment_soup = BeautifulSoup(comment, "lxml")
            table = comment_soup.select_one("table")
            if table is not None:
                return table
        # 構造が変わって table が取得できなかった場合
        raise RuntimeError("Pitching table not found – page format may have changed.")
