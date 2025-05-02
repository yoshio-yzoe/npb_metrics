from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, List, Optional
import pandas as pd

from .constants import VALID_LEAGUES


class ScraperBase(ABC):
    def __init__(
        self,
        years: Iterable[int],
        league: Optional[str] = None,
    ) -> None:
        years = list(years)
        if not years:
            raise ValueError("years must contain at least one year")
        if league and league not in VALID_LEAGUES:
            raise ValueError(f"league must be in {VALID_LEAGUES}")
        self.years: List[int] = years
        self.league: Optional[str] = league

    @abstractmethod
    def dataframe(self) -> pd.DataFrame: ...
