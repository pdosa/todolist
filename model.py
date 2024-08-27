# Models
from datetime import datetime
from typing import List

from fastapi import Form
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str
    todos: List[dict] = []

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: str | None = None

class Task(BaseModel):
    id:int
    title:str=Form(...)
    description:str=Form(...)
    start:str=Form(...)
    end:str=Form(...)
    priority:str=Form(...)

