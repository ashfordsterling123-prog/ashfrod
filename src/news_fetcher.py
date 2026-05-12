from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import List, Dict
from urllib.parse import quote_plus


@dataclass
class NewsItem:
    title: str
    link: str
    source: str
    published_text: str
    published_at: datetime | None
    summary: str


INDEX_KEYWORDS = ["나스닥100", "NASDAQ 100", "QQQ", "QQQM", "S&P 500", "SPY", "VOO", "2641", "일본 지수", "일본 ETF", "Nikkei 225", "TOPIX"]
FX_KEYWORDS = ["원달러 환율", "달러 원 환율", "USD KRW", "엔화 환율", "원엔 환율", "JPY KRW", "USD JPY", "미국 달러", "일본 엔화", "한국 원화", "미국 금리", "일본은행", "BOJ", "한국은행", "환율 영향", "원화 약세", "원화 강세", "엔화 약세", "엔화 강세"]


def _rss_url(query: str) -> str:
    return f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=ko&gl=KR&ceid=KR:ko"


def _parse_entry(entry) -> NewsItem:
    published_at = None
    published_text = "발행시간 확인 불가"
    if getattr(entry, "published", None):
        try:
            published_at = parsedate_to_datetime(entry.published)
            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)
            published_text = published_at.isoformat()
        except Exception:
            published_text = "발행시간 확인 불가"
    source = getattr(getattr(entry, "source", None), "title", "출처 확인 불가")
    return NewsItem(title=getattr(entry, "title", "제목 없음"), link=getattr(entry, "link", ""), source=source, published_text=published_text, published_at=published_at, summary=getattr(entry, "summary", ""))


def _fetch_for_keywords(keywords: List[str], per_keyword_limit: int = 4) -> List[NewsItem]:
    items: List[NewsItem] = []
    try:
        import feedparser
    except Exception:
        return items
    for kw in keywords:
        try:
            feed = feedparser.parse(_rss_url(kw))
            for e in feed.entries[:per_keyword_limit]:
                items.append(_parse_entry(e))
        except Exception:
            continue
    return items


def deduplicate(items: List[NewsItem]) -> List[NewsItem]:
    seen = set(); out = []
    for item in items:
        key = (item.title.strip().lower(), item.link.strip())
        if key in seen:
            continue
        seen.add(key); out.append(item)
    return out


def filter_recent_24h(items: List[NewsItem], now_utc: datetime | None = None) -> List[NewsItem]:
    now_utc = now_utc or datetime.now(timezone.utc)
    lower = now_utc - timedelta(hours=24)
    out = []
    for item in items:
        if item.published_at is None:
            continue
        dt = item.published_at.astimezone(timezone.utc)
        if lower <= dt <= now_utc:
            out.append(item)
    return out


def fetch_all_news() -> Dict[str, List[NewsItem]]:
    index_news = filter_recent_24h(deduplicate(_fetch_for_keywords(INDEX_KEYWORDS)))
    fx_news = filter_recent_24h(deduplicate(_fetch_for_keywords(FX_KEYWORDS)))
    return {"index": index_news, "fx": fx_news}
