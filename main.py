from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import json
import requests
from blog_bot_friendly import run_auto_blog

app = FastAPI()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
REDIRECT_URI = "https://auto-blog-gpt-gtvy.onrender.com/callback"

@app.get("/")
def read_root():
    return {"message": "Hello, this is your auto blog bot!"}

@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        return JSONResponse({"error": "code parameter missing"}, status_code=400)

    # NAVER 토큰 요청
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

    return JSONResponse({"message": "OAuth callback received and token stored."})

@app.get("/run")
def run_posting():
    status, response = run_auto_blog()
    return {"status": status, "response": response}
