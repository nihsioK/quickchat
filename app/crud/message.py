from sqlalchemy.orm import Session
from ..models.message import Message
from ..schemas.message import MessageCreate
from datetime import datetime

def create_message(db: Session, message: MessageCreate, sender_id: int, chat_id: int):
    db_message = Message(
        **message.dict(),
        sender_id=sender_id,
        chat_id=chat_id,
        timestamp=datetime.utcnow()  # Ensure timestamp is set to current time
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages(db: Session, chat_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.chat_id == chat_id).offset(skip).limit(limit).all()
