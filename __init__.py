"""
NPB_Metrics の公開 API。
使用例:

    from npb_metrics import Pitcher, Batter

    df = Pitcher(years=[2024], team="Hanshin Tigers").dataframe()
"""

from __future__ import annotations

from .pitcher import PitcherScraper as Pitcher
from .batter import BatterScraper as Batter

# チーム単位スクレイパを後で実装する場合に備えて try-import
try:
    from .team import TeamScraper as Team  # noqa: F401
except ImportError:  # pragma: no cover
    Team = None  # type: ignore[assignment]

__all__ = ["Pitcher", "Batter", "Team"]
