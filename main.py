from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat_model import ChatRequest
from service import ask_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "API running"}


@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_video(
        request.video_id,
        request.question
    )

    return {
        "answer": answer
    }