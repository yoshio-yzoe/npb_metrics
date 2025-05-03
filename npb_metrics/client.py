

"""
共通 HTTP クライアント

- requests-cache でレスポンスをローカル SQLite キャッシュ
- User-Agent を統一
"""

from typing import Final
import requests_cache

# ────────────────────────────────────────────────────────────
# CachedSession の作成
#   * cache_name="npb_cache" → ./npb_cache.sqlite が生成
#   * expire_after=7 日
# ────────────────────────────────────────────────────────────
session: Final = requests_cache.CachedSession(
    cache_name="npb_cache",
    backend="sqlite",
    expire_after=60 * 60 * 24 * 7,
)

session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (compatible; NPB-Metrics/1.0; "
            "+https://github.com/yoshio-yzoe/npb_metrics)"
        )
    }
)
