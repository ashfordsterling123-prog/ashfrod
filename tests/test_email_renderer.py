from src.email_renderer import render_html_email


def test_render_html_email():
    brief = {
        "market_weather": "중립",
        "headline_points": ["a", "b", "c"],
        "caution": "주의",
        "counter_view": "반대",
        "action": "관찰",
        "index_news": [],
        "fx_news": [],
        "interpretation": ["x"],
    }
    html = render_html_email(brief, [{"jp":"a","furigana":"b","ko":"c","scene":"d","example":"e"}], "2026-01-01")
    assert "Ashford Sterling Daily Brief" in html
    assert "오늘의 일본어 여행 문장 3개" in html
