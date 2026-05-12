import os
from src.news_classifier import MAX_NEWS_ITEMS_DEFAULT


def get_news_limit() -> int:
    raw = os.getenv("NEWS_LIMIT", "").strip()
    if not raw:
        return MAX_NEWS_ITEMS_DEFAULT
    try:
        n = int(raw)
        return n if n > 0 else MAX_NEWS_ITEMS_DEFAULT
    except ValueError:
        return MAX_NEWS_ITEMS_DEFAULT
