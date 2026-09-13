import os
import requests
from google import genai

# 환경 변수에서 키 불러오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def generate_blog_content():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = """
    당신은 5060 중장년층을 타깃으로 하는 전문 건강 블로그 라이터이자, SEO 콘텐츠 디자이너입니다.
    오늘 날짜 기준으로 최근 대중에게 화제가 되었거나 이슈가 된 건강 정보/질환/이슈를 하나 선정하고, 아래 지침에 맞춰 블로그 포스팅을 작성해 주세요.

    [Part 1. Article Structure & Formatting Guidelines (모바일 에디터 최적화 지침)]
    - 티스토리 모바일 앱에서 그대로 복사·붙여넣기 할 것이므로, **HTML 태그(`<h2>` 등)는 절대 사용하지 마세요.**
    - 대신 가독성이 좋도록 이모지(📌, 💡, ⚠️ 등)와 줄바꿈을 적극 활용해 주세요.
    - 대제목이나 소제목은 눈에 띄게 굵은 글씨 느낌이나 구분선 기호(`---`)를 활용해 주세요.
    
    글의 흐름은 반드시 아래 7가지 구조를 따르세요:
    1. [도입부]: 독자의 공감을 이끌어내는 질문과 경각심을 유발하는 배경 설명.
    2. [핵심 원인 및 발생 이유]: 원인이나 작용 원리를 이해하기 쉽게 3~5가지로 설명.
    3. [핵심 리스팅 (음식/증상/운동 등)]: 각 항목당 효능/원인과 상세 설명을 2~3줄 이상 작성.
    4. [도움이 되는 생활 습관 및 주의사항]: 실천 팁, 피해야 할 행동, 부작용 안내.
    5. [병원 방문/검진 기준]: 전문의 진료가 필요한 위험 신호 제시.
    6. [자주 묻는 질문 (FAQ 3가지)]: 독자들이 가장 궁금해할 만한 질문 3가지를 Q&A 형태로 구성.
    7. [마치며]: 전체 내용 요약 및 따뜻한 격려와 응원의 메시지.

    [Part 2. 쿠팡 파트너스 및 추천제품 지침]
    - **[중요]** 본문 맨 상단(제목 바로 아래, 도입부 시작 전)에 아래 공정고시 문구를 반드시 배치해 주세요.
      "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
    - [태그] 윗부분에 **[쿠팡 추천제품]** 항목을 만들어, 이번 포스팅 주제와 가장 어울리는 쿠팡 판매 상품명을 1~2개 추천해 주세요.

    [Part 3. Tone & Writing Style]
    - 어조: 5060세대가 읽기 편한 친절하고 따뜻한 구어체 (~입니다, ~습니다).
    - 의학적 안전성: "무조건 치료된다"는 단정 대신 "도움이 될 수 있습니다", "전문의 상담이 필요합니다" 표현 사용.

    [Output Format (출력 양식)]
    반드시 아래 양식에 맞춰 출력해 주세요:

    [제목]: (매력적인 블로그 제목 작성)

    [본문]:
    (맨 위에 쿠팡 공정고시 문구가 들어가고, 이모지와 줄바꿈이 적용된 깔끔한 전체 본문 작성)

    [쿠팡 추천제품]: 
    - 추천 상품명: (예: 관절 영양제 / 무릎 온열 보호대 등)

    [태그]: 
    #주요키워드 #연관키워드1 #연관키워드2 ... (10~15개의 해시태그)

    [썸네일 문구]:
    - 메인 타이틀: (굵고 짧은 제목)
    - 서브 타이틀: (경고 또는 유용한 알림 문구)
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # 모바일 텍스트 가독성을 위해 마크다운 파싱 모드 사용
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("텔레그램으로 글 전송 성공!")
    else:
        print(f"전송 실패: {response.text}")

if __name__ == "__main__":
    print("AI가 오늘의 건강 이슈를 검색하고 글을 작성 중입니다...")
    blog_post = generate_blog_content()
    send_to_telegram(blog_post)
