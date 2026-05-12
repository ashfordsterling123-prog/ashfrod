from datetime import datetime, timezone
from src.news_fetcher import NewsItem
from src.news_classifier import build_brief, MAX_NEWS_ITEMS_DEFAULT
from src.config import get_news_limit


def _item(i, title):
    return NewsItem(title, f"https://x/{i}", "src", datetime.now(timezone.utc).isoformat(), datetime.now(timezone.utc), f"summary {i}")


def test_default_news_limit_is_5(monkeypatch):
    monkeypatch.delenv("NEWS_LIMIT", raising=False)
    assert MAX_NEWS_ITEMS_DEFAULT == 5
    assert get_news_limit() == 5


def test_news_limit_env_3(monkeypatch):
    monkeypatch.setenv("NEWS_LIMIT", "3")
    assert get_news_limit() == 3


def test_render_only_5_when_more_available():
    items = [_item(i, f"QQQ 뉴스 {i}") for i in range(10)]
    brief = build_brief({"index": items, "fx": []}, limit=5)
    assert len(brief["top_news"]) == 5
