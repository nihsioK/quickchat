from pydantic import BaseModel
from typing import List, Optional
from .message import Message
from .user import User

class ChatBase(BaseModel):
    name: str

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    owner_id: int
    participant_id: int
    messages: List['Message'] = []

    class Config:
        from_attributes = True
