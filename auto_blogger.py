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
  
  [Part 1. HTML 태그 구조 지침]
  - 티스토리 HTML 에디터에 바로 붙여넣을 수 있도록, 반드시 **HTML 태그(`<h3>`, `<h4>`, `<p>`, `<ul>`, `<li>`, `<strong>` 등)**를 사용하여 가독성 있게 작성하세요.
  - 글의 대제목(단락 제목)은 반드시 `<h3>` 태그를 사용하되, 학술적/보고서용 단어('개요', '메커니즘' 등)는 절대 쓰지 말고 5060 독자가 친근하게 느낄 수 있는 질문형이나 설명형으로 작성하세요.
  - 세부 소제목이나 항목 제목은 반드시 `<h4>` 태그를 사용하세요.

  글의 흐름은 반드시 아래 7가지 구조를 따르세요:
  1. [도입부]: 독자의 공감을 이끌어내는 질문과 경각심을 유발하는 배경 설명.
  2. [핵심 원인 및 발생 이유]: 원인이나 작용 원리를 이해하기 쉽게 3가지로 설명.
  3. [핵심 리스팅 (음식/증상/운동 등)]: 각 항목당 효능/원인과 상세 설명을 2~3줄 이상 작성.
  4. [도움이 되는 생활 습관 및 주의사항]: 실천 팁, 피해야 할 행동, 부작용 안내.
  5. [병원 방문/검진 기준]: 전문의 진료가 필요한 위험 신호 제시.
  6. [자주 묻는 질문 (FAQ 3가지)]: 독자들이 가장 궁금해할 만한 질문 3가지를 Q&A 형태로 구성.
  7. [마치며]: 전체 내용 요약 및 따뜻한 격려와 응원의 메시지.
  
  [Part 2. 쿠팡 파트너스 및 추천제품 지침]
  - **[중요]** 본문 맨 상단(제목 바로 아래, 도입부 시작 전)에 아래 공정고시 문구를 HTML로 반드시 배치해 주세요.
  <p style="font-size: 13px; color: #555; margin-bottom: 20px;"><em>"이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."</em></p>
  - [태그] 윗부분에 **[쿠팡 추천제품]** 항목을 만들어, 이번 포스팅 주제와 가장 어울리는 쿠팡 판매 상품명을 1개 추천해 주세요.

  [Part 3. Tone & Writing Style]
  - 어조: 5060세대가 읽기 편한 친절하고 따뜻한 구어체 (~입니다, ~습니다).
  - 의학적 안전성: "무조건 치료된다"는 단정 대신 "도움이 될 수 있습니다", "전문의 상담이 필요합니다" 표현 사용.

  [Output Format (출력 양식)]
  반드시 아래 양식에 맞춰 출력해 주세요:
  [제목]: (매력적인 블로그 제목 작성)

  [HTML 본문]:
  (상단 공정고시 문구가 포함되고, <h3>와 <h4> 태그가 적용된 전체 HTML 본문 작성)

  [쿠팡 추천제품]:
  - 추천 상품명: (예: 관절 영양제 / 무릎 온열 보호대 등)
  
  [태그]:
  #주요키워드 #연관키워드1 #연관키워드2 ... (10~15개의 해시태그)

  [썸네일 문구 및 프롬프트]:
  - 메인 타이틀: (핵심 키워드 중심의 직관적인 텍스트)
  - 서브 타이틀: (경고 또는 유용한 정보 알림 문구)
  - 이미지 생성 프롬프트: (밝고 깨끗한 헬스케어 이미지 배경에 중앙/하단에 선명한 한국어 텍스트 레이아웃이 적용된 고품질 썸네일 생성을 위한 영문 프롬프트)
  """
  
  response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
  )
  return response.text

def send_to_telegram(message):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
  }
  
  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print("텔레그램으로 글 전송 성공!")
  else:
    # 이 부분이 실패했을 때 정확한 텔레그램 서버의 에러 메시지를 출력해 줍니다.
    pritn(f"전송 실패! 에러 코드: {response.status_code}")
    print(f"에러 내용: {response.text}")

if __name__ == "__main__":
  print("AI가 오늘의 건강 이슈를 검색하고 글을 작성 중입니다...")
  blog_post = generate_blog_content()
  send_to_telegram(blog_post)
