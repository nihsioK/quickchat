from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..models.chat import Chat
from ..schemas.chat import ChatCreate

def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).offset(skip).limit(limit).all()

def get_chats_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Chat).filter(Chat.owner_id == user_id).offset(skip).limit(limit).all()

def create_chat(db: Session, chat: ChatCreate, owner_id: int, participant_id: int):
    db_chat = Chat(name=chat.name, owner_id=owner_id, participant_id=participant_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_or_get_chat(db: Session, owner_id: int, participant_id: int):
    chat = db.query(Chat).filter(Chat.owner_id == owner_id, Chat.participant_id == participant_id).first()
    if chat:
        return chat
    chat = db.query(Chat).filter(Chat.owner_id == participant_id, Chat.participant_id == owner_id).first()
    if chat:
        return chat
    return create_chat(db, ChatCreate(name="Private chat"), owner_id=owner_id, participant_id=participant_id)



