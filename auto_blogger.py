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
    당신은 전문 블로거입니다. IT, 테크, 또는 생활 경제 분야에서 대중이 흥미로워할 만한 주제를 하나 선정해 주세요.
    애드센스 수익형 블로그에 적합하도록 정보가 알차고 가독성 좋게 마크다운 형식으로 작성해 주세요.
    
    반드시 아래 형식으로 출력해 주세요:
    [제목]: (여기에 매력적인 블로그 제목 작성)
    [태그]: (쉼표로 구분된 태그 5개 작성)
    [본문]:
    (여기에 본문 내용 작성)
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
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("텔레그램으로 글 전송 성공!")
    else:
        print(f"전송 실패: {response.text}")

if __name__ == "__main__":
    print("AI가 블로그 글을 작성 중입니다...")
    blog_post = generate_blog_content()
    send_to_telegram(blog_post)
