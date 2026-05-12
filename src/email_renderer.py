from typing import Dict, List


def _news_cards(items: List[Dict]) -> str:
    if not items:
        return "<p>오늘 수집된 관련 뉴스가 없습니다.</p>"
    html = []
    for n in items:
        html.append(f"""
        <div class='card'>
          <h4>{n['title']}</h4>
          <p><b>출처:</b> {n['source']} | <b>발행:</b> {n['published']}</p>
          <p>{n['summary_ko']}</p>
          <p>💡 {n['comment']}</p>
          <a href='{n['link']}'>원문 링크</a>
        </div>
        """)
    return "\n".join(html)


def render_html_email(brief: Dict, phrases: List[Dict], report_date: str) -> str:
    phrases_html = "".join([
        f"<div class='card'><h4>{p['jp']} ({p['furigana']})</h4><p>{p['ko']}</p><p>{p['scene']}</p><p>예문: {p['example']}</p></div>"
        for p in phrases
    ])
    points = "".join([f"<li>{p}</li>" for p in brief["headline_points"]])
    return f"""
<html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#1f2937}}
.container{{max-width:780px;margin:auto;padding:16px}}
.hero{{background:#1e293b;color:white;padding:14px;border-radius:12px}}
.card{{background:white;padding:12px;border-radius:10px;margin:10px 0;border:1px solid #e5e7eb}}
.section{{margin-top:20px}}
</style></head><body><div class='container'>
<div class='hero'><h2>📰 Ashford Sterling Daily Brief ({report_date})</h2><p>오늘의 시장 날씨: {brief['market_weather']}</p><p>행동 구분: <b>{brief['action']}</b></p></div>
<div class='section'><h3>섹션 A. 오늘의 핵심 요약 ⚠️</h3><ul>{points}</ul><p><b>주의:</b> {brief['caution']}</p><p><b>반대 관점:</b> {brief['counter_view']}</p></div>
<div class='section'><h3>섹션 B. 지수 뉴스 📈</h3>{_news_cards(brief['index_news'])}</div>
<div class='section'><h3>섹션 C. 환율 뉴스 💱</h3>{_news_cards(brief['fx_news'])}</div>
<div class='section'><h3>섹션 D. Ashford Sterling 투자 해석</h3><ul>{''.join([f'<li>{i}</li>' for i in brief['interpretation']])}</ul></div>
<div class='section'><h3>섹션 E. 오늘의 일본어 여행 문장 3개 🇯🇵</h3>{phrases_html}</div>
</div></body></html>
"""


def render_text_email(brief: Dict, phrases: List[Dict], report_date: str) -> str:
    lines = [f"[Ashford Sterling] Daily Brief - {report_date}", f"시장 날씨: {brief['market_weather']}", f"행동 구분: {brief['action']}"]
    lines.append("\n[핵심 요약]")
    lines.extend([f"- {p}" for p in brief["headline_points"]])
    lines.append("\n[지수 뉴스]")
    for n in brief["index_news"]:
        lines.append(f"- {n['title']} ({n['source']}) {n['published']} {n['link']}")
    lines.append("\n[환율 뉴스]")
    for n in brief["fx_news"]:
        lines.append(f"- {n['title']} ({n['source']}) {n['published']} {n['link']}")
    lines.append("\n[일본어 문장]")
    for p in phrases:
        lines.append(f"- {p['jp']} / {p['furigana']} / {p['ko']}")
    return "\n".join(lines)
