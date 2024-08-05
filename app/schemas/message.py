from pydantic import BaseModel
from datetime import datetime
from .user import User

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    timestamp: datetime
    sender_id: int
    chat_id: int
    sender: User

    class Config:
        from_attributes = True
