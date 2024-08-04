from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    participant_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="owned_chats", foreign_keys=[owner_id])
    participant = relationship("User", back_populates="participated_chats", foreign_keys=[participant_id])
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
