from fastapi import FastAPI
from blog_bot_friendly import run_auto_blog

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is your auto blog bot!"}

@app.get("/callback")
def callback():
    return {"message": "OAuth callback received and token stored."}

@app.get("/run")
def run_posting():
    status, response = run_auto_blog()
    return {"status": status, "response": response}
