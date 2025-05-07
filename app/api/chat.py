from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession, select
from app.core.database import get_session
from app.models.message import Message
from app.services.ollama import generate
from typing import Optional

router = APIRouter(prefix="/chat", tags=["chat"])

# app/api/chat.py修改
@router.post("/")
async def chat_endpoint(
    payload: dict,
    db: DBSession = Depends(get_session)
):
    session_id = payload.get("session_id")
    messages = payload["messages"]
    stream = payload.get("stream", True)
    model = payload["model"]

    # 驗證session_id是否存在
    if session_id is not None:
        session = db.get(Session, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        old_msgs = db.exec(
            select(Message).where(Message.session_id == session_id).order_by(Message.id)
        ).all()
        old_msgs_dicts = [{"role": m.role, "content": m.content} for m in old_msgs]
        messages = old_msgs_dicts + messages

    try:
        # 呼叫Ollama API
        result = await generate(model=model, messages=messages, stream=stream)
        
        # 如果啟用了流處理，返回StreamingResponse
        if stream:
            from fastapi.responses import StreamingResponse
            return StreamingResponse(
                result,
                media_type="application/x-ndjson"
            )
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=400, detail="Model not found or not loaded")
        raise HTTPException(status_code=500, detail="Error calling Ollama API")