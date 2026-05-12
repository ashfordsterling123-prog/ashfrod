# Ashford Sterling Daily Brief

매일 **한국 시간(KST) 오전 6:40**에 투자/환율 뉴스를 RSS로 수집해 HTML 이메일로 보내는 자동 뉴스레터입니다.

## 핵심 원칙
- 기본값은 **무료 RSS + 규칙 기반 요약**입니다.
- `OPENAI_API_KEY`가 **없으면 OpenAI API를 절대 호출하지 않습니다.**
- 민감정보(SMTP 비밀번호/API 키)는 코드에 넣지 않고 GitHub Secrets로만 읽습니다.

## 뉴스 출력 개수 제한
- 기본 이메일 표시 뉴스 수는 **최대 5개**입니다.
- 내부적으로 여러 RSS를 수집하더라도 최종 이메일에는 우선순위 기반으로 최대 5개만 표시됩니다.
- 기본값은 `MAX_NEWS_ITEMS_DEFAULT = 5`이며 `src/news_classifier.py`에서 쉽게 변경 가능합니다.
- 환경변수 `NEWS_LIMIT`가 있으면 해당 값(예: 3)을 우선 사용합니다.
- GitHub Actions에서는 `vars.NEWS_LIMIT`(Repository Variables) 또는 로컬 환경변수로 설정할 수 있습니다.

## 파일 구조
- `main.py`
- `src/news_fetcher.py`
- `src/news_classifier.py`
- `src/email_renderer.py`
- `src/email_sender.py`
- `src/japanese_phrases.py`
- `data/japanese_phrases.json`
- `.github/workflows/daily-brief.yml`

## GitHub Secrets 설정
필수:
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `MAIL_TO`
- `MAIL_FROM`

선택:
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

추가 변수(선택):
- `NEWS_LIMIT` (Repository Variables 권장, 기본값 5)

> 추가 비용을 피하려면 `OPENAI_API_KEY`를 넣지 마세요.

## Gmail SMTP 팁
- Gmail 일반 비밀번호 사용 금지
- **앱 비밀번호** 또는 조직 정책에 맞는 인증 방식 사용

## 실행 방법 (로컬)
1. Python 3.11 설치
2. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
3. 환경변수 설정 후 실행
   ```bash
   export SMTP_HOST=smtp.gmail.com
   export SMTP_PORT=587
   export SMTP_USER=example@gmail.com
   export SMTP_PASSWORD=app_password
   export MAIL_TO=recipient@example.com
   export MAIL_FROM=example@gmail.com
   export NEWS_LIMIT=5
   # 선택
   # export OPENAI_API_KEY=...
   # export OPENAI_MODEL=gpt-4o-mini

   python main.py
   ```

## GitHub Actions 설정
- 워크플로우 파일: `.github/workflows/daily-brief.yml`
- 스케줄: `40 21 * * *` (UTC) = **KST 다음날 06:40**
- 수동 실행: Actions 탭 → `Ashford Sterling Daily Brief` → `Run workflow`

## 품질/안전
- 일부 RSS 실패 시 전체 중단 대신 가능한 소스 계속 수집
- 발행시간이 없으면 `발행시간 확인 불가` 표시
- 뉴스가 0개면 안내 문구 메일 발송
- 이 메일은 투자 조언이 아니라 참고 브리핑입니다
