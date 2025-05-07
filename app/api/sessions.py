from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select, Session as DBSession
from app.models.session import Session
from app.core.database import get_session

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Session)
def create_session(session: Session, db: DBSession = Depends(get_session)):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.get("/", response_model=list[Session])
def read_sessions(db: DBSession = Depends(get_session)):
    return db.exec(select(Session)).all()

@router.get("/{session_id}", response_model=Session)
def get_session_by_id(session_id: int, db: DBSession = Depends(get_session)):
    session = db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}", response_model=Session)
def update_session(session_id: int, new_data: Session, db: DBSession = Depends(get_session)):
    session = db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.title = new_data.title
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: DBSession = Depends(get_session)):
    session = db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
