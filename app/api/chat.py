from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession, select
from app.core.database import get_session
from app.models.message import Message
from app.services.ollama import generate
from typing import Optional

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_endpoint(
    payload: dict,
    db: DBSession = Depends(get_session)
):
    session_id: Optional[int] = payload.get("session_id")
    messages: list[dict] = payload["messages"]
    stream: bool = payload.get("stream", False)
    model: str = payload["model"]

    # 若 session_id 存在，把舊對話加入 messages 最前面
    if session_id is not None:
        old_msgs = db.exec(
            select(Message).where(Message.session_id == session_id).order_by(Message.id)
        ).all()
        old_msgs_dicts = [{"role": m.role, "content": m.content} for m in old_msgs]
        messages = old_msgs_dicts + messages

    # 呼叫 Ollama API
    result = await generate(model=model, messages=messages, stream=stream)
    return result
