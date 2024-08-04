import logging

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI
from .api import user, auth, chat, message
from .db.session import SessionLocal, get_db
from .db.base import Base
from fastapi import Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .schemas.user import UserCreate, User
from .crud.user import get_user_by_username, create_user as crud_create_user
from .crud.chat import create_chat as crud_create_chat, get_chat as crud_get_chat, get_chats as crud_get_chats
from .crud.message import create_message as crud_create_message, get_messages
from .dependencies import get_current_user
from .core.security import create_access_token
from .api.auth import authenticate_user
from fastapi.staticfiles import StaticFiles
import os
import json
from typing import List
from .schemas.chat import Chat, ChatCreate
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=SessionLocal().bind)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(chat.router, prefix="/api/v1", tags=["chats"])
app.include_router(message.router, prefix="/api/v1", tags=["messages"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/chat/{chat_id}", response_class=HTMLResponse)
async def chat(request: Request, chat_id: int):
    return templates.TemplateResponse("chat.html", {"request": request, "chat_id": chat_id})

@app.get("/chats", response_class=HTMLResponse)
async def chats(request: Request):
    return templates.TemplateResponse("chats.html", {"request": request})
