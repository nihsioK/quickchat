from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    owned_chats = relationship("Chat", foreign_keys="[Chat.owner_id]", back_populates="owner")
    participated_chats = relationship("Chat", foreign_keys="[Chat.participant_id]", back_populates="participant")
