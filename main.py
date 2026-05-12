from src.news_fetcher import fetch_all_news
from src.news_classifier import build_brief, maybe_enhance_with_openai, MAX_NEWS_ITEMS_DEFAULT
from src.japanese_phrases import load_phrases, pick_three_phrases
from src.email_renderer import render_html_email, render_text_email
from src.email_sender import send_email
from src.config import get_news_limit
from datetime import datetime
import pytz
import os


def main() -> None:
    kst = pytz.timezone("Asia/Seoul")
    today = datetime.now(kst).date()

    news_items = fetch_all_news()
    brief = build_brief(news_items, limit=get_news_limit())

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    if api_key:
        brief = maybe_enhance_with_openai(brief, api_key=api_key, model=model)

    phrases = pick_three_phrases(load_phrases("data/japanese_phrases.json"), today.isoformat())

    subject = f"[Ashford Sterling] Daily Brief - {today.isoformat()}"
    html = render_html_email(brief=brief, phrases=phrases, report_date=today.isoformat())
    text = render_text_email(brief=brief, phrases=phrases, report_date=today.isoformat())
    send_email(subject=subject, html_body=html, text_body=text)


if __name__ == "__main__":
    main()
