from fastapi import FastAPI
from app.core.database import init_db
from app.api import sessions, messages, chat

app = FastAPI(
    title="AI Web Chatbot",
    version="1.0.0",
    description="Baseline API for chat, session, and message management"
)

# 初始化資料庫
init_db()

# 掛上三組路由
app.include_router(sessions.router)
app.include_router(messages.router)
app.include_router(chat.router)
