from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserOut(SQLModel):
    id: int
    username: str
    email: str



class TokenSchema(SQLModel):
    token: str


class SkillBase(SQLModel):
    name: str
    level: str
    description: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SQLModel):
    name: Optional[str] = None
    level: Optional[str] = None
    description: Optional[str] = None


class SkillOut(SkillBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime