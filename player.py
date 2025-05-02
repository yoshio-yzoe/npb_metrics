from __future__ import annotations
from typing import Optional, Dict, List
import pandas as pd

from .base import ScraperBase
from .constants import TEAM_TO_LEAGUE, VALID_LEAGUES
from .utils import league_summary_soup, league_team_links, fetch_soup, scraping_table


class PlayerScraper(ScraperBase):
    def __init__(
        self,
        years: List[int],
        league: Optional[str] = None,
        team: Optional[str] = None,
    ):
        if team and team not in TEAM_TO_LEAGUE:
            raise ValueError(f"team must be one of {list(TEAM_TO_LEAGUE)}")
        super().__init__(years, league or TEAM_TO_LEAGUE.get(team))
        self.team = team

    # --- public ------------------------------------------------------------
    def dataframe(self) -> pd.DataFrame:
        dfs = [self._scrape_year(year) for year in self.years]
        df = pd.concat(dfs, ignore_index=True)
        return df.set_index(["team", "year", "Name"])

    # --- private -----------------------------------------------------------
    def _scrape_year(self, year: int) -> pd.DataFrame:
        leagues = [self.league] if self.league else VALID_LEAGUES
        frames: List[pd.DataFrame] = []

        for lg in leagues:
            summary = league_summary_soup(lg)
            team_links = league_team_links(summary)[year]

            targets = (
                {self.team: team_links[self.team]} if self.team else team_links
            )

            for team, link in targets.items():
                team_soup = fetch_soup(link)
                table = self._extract_table(team_soup)
                df = scraping_table(table)
                df["team"] = team
                df["year"] = year
                frames.append(df)

        return pd.concat(frames, ignore_index=True)

    @staticmethod
    def _extract_table(team_soup):  # noqa: D401
        """override 在 Pitcher/Batter"""
        raise NotImplementedError
