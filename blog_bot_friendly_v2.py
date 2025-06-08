import os
import requests
import openai
import json
from datetime import datetime

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ 최신 openai API 클라이언트 사용
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Step 1: 트렌드 키워드 가져오기 (모의)
def get_trending_keywords():
    return ["오늘의 인기 키워드", "트렌디한 이야기"]

# ✅ Step 2: GPT로 친근한 말투 블로그 글 생성
def generate_blog_content(keyword):
    prompt = (
        f"'{keyword}'라는 주제로 부드럽고 친근한 말투로 블로그 스타일의 글을 써줘. "
        "‘~했어요’, ‘~하답니다’, ‘~해볼까요?’ 같은 말투로, "
        "서론-본론-결론 구성, 500자 정도 분량으로."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.8
    )
    return response.choices[0].message.content

# ✅ Step 3: DALL·E 이미지 생성 및 저장
def generate_image(prompt, filename="image.png"):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    img_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(img_data)
    return filename

# ✅ Step 4: 네이버 이미지 업로드
def upload_image_to_naver(image_path):
    with open("token_store.json", "r", encoding="utf-8") as f:
        token_data = json.load(f)
    access_token = token_data.get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    files = {
        'image': open(image_path, 'rb')
    }
    res = requests.post("https://openapi.naver.com/blog/uploadImage.json", headers=headers, files=files)
    return res.json().get("result", {}).get("url")

# ✅ Step 5: 포스트 업로드
def post_to_blog(title, content, image_url=None):
    with open("token_store.json", "r", encoding="utf-8") as f:
        token_data = json.load(f)
    access_token = token_data.get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    if image_url:
        content += f"<br><br><img src='{image_url}' />"

    params = {
        "title": title,
        "contents": content
    }
    res = requests.post("https://openapi.naver.com/blog/writePost.json", headers=headers, params=params)
    return res.status_code, res.text

# ✅ 전체 실행 함수
def run_auto_blog():
    keywords = get_trending_keywords()
    keyword = keywords[0]
    content = generate_blog_content(keyword)
    image_file = generate_image(keyword)
    image_url = upload_image_to_naver(image_file)
    status, response = post_to_blog(f"[트렌드] {keyword}", content, image_url)
    return status, response