from typing import Final
import requests

__all__ = ["session"]

session: Final[requests.Session] = requests.Session()
session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (compatible; NPB-Metrics/1.0; "
            "+https://github.com/yoshio-yzoe/npb_metrics)"
        )
    }
)
