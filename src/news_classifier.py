from __future__ import annotations
from typing import Dict, List
from src.news_fetcher import NewsItem


def _simple_summary(item: NewsItem) -> str:
    base = (item.summary or item.title).replace("<b>", "").replace("</b>", "")
    return base[:160] + ("..." if len(base) > 160 else "")


def _invest_comment(item: NewsItem) -> str:
    text = f"{item.title} {item.summary}".lower()
    if "금리" in text or "boj" in text or "한국은행" in text:
        return "정책 변화 가능성으로 변동성 확대에 주의가 필요합니다."
    if "강세" in text:
        return "통화 강세 구간은 해외자산 환산 수익률에 영향을 줄 수 있습니다."
    if "약세" in text:
        return "통화 약세 구간은 환헤지 여부 점검이 필요합니다."
    return "확실하지 않음: 추가 데이터 확인이 필요합니다."


def build_brief(news: Dict[str, List[NewsItem]]) -> Dict:
    idx = news.get("index", [])
    fx = news.get("fx", [])
    all_news = idx + fx

    if not all_news:
        return {
            "market_weather": "오늘 수집된 관련 뉴스가 없습니다",
            "headline_points": ["오늘 수집된 관련 뉴스가 없습니다"],
            "caution": "확실하지 않음",
            "counter_view": "데이터 부족으로 반대 관점 판단이 어렵습니다.",
            "action": "관찰",
            "index_news": [],
            "fx_news": [],
            "interpretation": ["오늘은 뉴스 공백일 가능성이 있어 관찰 중심으로 대응합니다."],
        }

    points = [n.title for n in all_news[:3]]
    return {
        "market_weather": "중립~주의",
        "headline_points": points,
        "caution": "헤드라인 중심 해석은 오류 가능성이 있어 원문 확인이 필요합니다.",
        "counter_view": "단기 변동 뉴스가 장기 추세와 다를 수 있습니다.",
        "action": "관찰",
        "index_news": [
            {"title": n.title, "source": n.source, "published": n.published_text, "link": n.link, "summary_ko": _simple_summary(n), "comment": _invest_comment(n)}
            for n in idx[:15]
        ],
        "fx_news": [
            {"title": n.title, "source": n.source, "published": n.published_text, "link": n.link, "summary_ko": _simple_summary(n), "comment": _invest_comment(n)}
            for n in fx[:15]
        ],
        "interpretation": [
            "나스닥100/QQQ: 단기 뉴스보다 장기 적립 규칙 준수 여부를 점검합니다.",
            "S&P500: 분산 축으로서 유지 여부를 확인하고 과열 신호는 경계합니다.",
            "일본 지수/2641: 엔화 방향성과 기업 실적 사이 괴리를 함께 점검합니다.",
            "원화/엔화 변동: 환산 수익률과 변동성 리스크를 동시에 관리합니다.",
        ],
    }


def maybe_enhance_with_openai(brief: Dict, api_key: str, model: str) -> Dict:
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = (
            "다음 JSON 브리핑을 한국어로 더 자연스럽게 다듬어라. "
            "원문에 없는 사실 추가 금지, 불확실하면 '확실하지 않음' 표기. JSON만 출력.\n"
            f"{brief}"
        )
        resp = client.responses.create(
            model=model,
            input=prompt,
            temperature=0.2,
        )
        text = resp.output_text
        import json
        return json.loads(text)
    except Exception:
        return brief
