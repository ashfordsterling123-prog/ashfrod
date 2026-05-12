from datetime import datetime, timezone, timedelta
from src.news_fetcher import NewsItem, deduplicate, filter_recent_24h


def test_deduplicate():
    now = datetime.now(timezone.utc)
    a = NewsItem("t1", "u1", "s", "p", now, "")
    b = NewsItem("t1", "u1", "s", "p", now, "")
    assert len(deduplicate([a, b])) == 1


def test_filter_recent_24h():
    now = datetime(2026, 1, 2, tzinfo=timezone.utc)
    inside = NewsItem("a", "u", "s", "p", now - timedelta(hours=2), "")
    outside = NewsItem("b", "u2", "s", "p", now - timedelta(hours=30), "")
    assert filter_recent_24h([inside, outside], now_utc=now) == [inside]
