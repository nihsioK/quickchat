from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.message import MessageCreate, Message
from ..crud.message import create_message, get_message, get_messages
from ..db.session import get_db
from ..schemas.user import User
from ..dependencies import get_current_user
from typing import List
from ..crud.chat import get_chat

router = APIRouter()

@router.post("/chats/{chat_id}/messages/", response_model=Message)
def create_new_message(chat_id: int, message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = get_chat(db, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.owner_id != current_user.id and chat.participant_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to send messages to this chat")
    return create_message(db=db, message=message, sender_id=current_user.id, chat_id=chat_id)

@router.get("/chats/{chat_id}/messages/", response_model=List[Message])
def read_messages(chat_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = get_chat(db, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.owner_id != current_user.id and chat.participant_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to read messages from this chat")
    return get_messages(db, chat_id=chat_id, skip=skip, limit=limit)
