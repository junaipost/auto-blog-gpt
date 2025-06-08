from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Auto Blog GPT is running!"}

@app.get("/callback", response_class=HTMLResponse)
def callback(request: Request):
    return "<h3>네이버 OAuth 인증이 완료되었습니다. 서버가 code를 수신했습니다.</h3>"