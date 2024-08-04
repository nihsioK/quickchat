from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..schemas.chat import ChatCreate, Chat
from ..crud.chat import create_chat, get_chat, get_chats, create_or_get_chat, get_chats_for_user
from ..db.session import get_db
from ..models.user import User
from ..dependencies import get_current_user
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger("chat_api")

@router.post("/chats/", response_model=Chat)
def create_new_chat(chat: ChatCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_chat(db=db, chat=chat, owner_id=current_user.id)

@router.get("/chats/", response_model=List[Chat])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_chats(db, skip=skip, limit=limit)

@router.get("/chats/mine", response_model=List[Chat])
def read_my_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_chats_for_user(db, user_id=current_user.id)

@router.get("/chats/{chat_id}", response_model=Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@router.post("/chats/{participant_id}", response_model=Chat)
def create_or_get_chat_with_participant(participant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_or_get_chat(db, owner_id=current_user.id, participant_id=participant_id)