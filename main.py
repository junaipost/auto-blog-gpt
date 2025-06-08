from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests
import json
import os

app = FastAPI()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
REDIRECT_URI = "https://auto-blog-gpt-gtvy.onrender.com/callback"

@app.get("/")
def home():
    return {"message": "Auto Blog GPT is running!"}

@app.get("/callback", response_class=HTMLResponse)
def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        return HTMLResponse("<h3>code가 없습니다. 인증 실패</h3>")

    # 토큰 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": code,
        "state": state
    }
    res = requests.post(token_url, params=params)
    token_data = res.json()

    # access_token 저장
    with open("token_store.json", "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2, ensure_ascii=False)

    return HTMLResponse(f"<h3>✅ access_token 발급 성공!<br>결과: {token_data}</h3>")