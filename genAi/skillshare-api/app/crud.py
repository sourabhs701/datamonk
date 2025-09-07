from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from .models import User, Skill
from .schemas import UserCreate, SkillCreate, SkillUpdate
from .auth import get_password_hash, verify_password
from .utils.jwt_handler import create_token


def create_user(session: Session, data: UserCreate) -> str:
    """Create a new user and return a JWT token."""
    existing_user: Optional[User] = (
        session.query(User)
        .filter((User.email == data.email) | (User.username == data.username))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = get_password_hash(data.password)
    user = User(username=data.username, email=data.email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_token(user.id)
    return token


def create_skill(session: Session, user_id: int, data: SkillCreate) -> Skill:
    """Create a new skill for the given user."""
    existing_skill = (
        session.query(Skill)
        .filter(Skill.name == data.name, Skill.user_id == user_id)
        .first()
    )
    if existing_skill:
        raise HTTPException(status_code=400, detail="Skill Already Exist")

    skill = Skill(
        name=data.name,
        level=data.level,
        description=data.description,
        user_id=user_id,
    )
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


def get_skills_by_user(session: Session, user_id: int) -> List[Skill]:
    """Return all skills for the given user."""
    skills = session.query(Skill).filter(Skill.user_id == user_id).all()
    return skills


def delete_skill(session: Session, user_id: int, skill_id: int) -> None:
    """Delete a user's skill by id."""
    skill = (
        session.query(Skill)
        .filter(Skill.id == skill_id, Skill.user_id == user_id)
        .first()
    )
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found")
    session.delete(skill)
    session.commit()
    return None


def get_skill(session: Session, user_id: int, skill_id: int) -> Skill:
    """Get a single skill for the user by id."""
    skill = (
        session.query(Skill)
        .filter(Skill.id == skill_id, Skill.user_id == user_id)
        .first()
    )
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found")
    return skill


def update_skill(session: Session, user_id: int, skill_id: int, data: SkillUpdate) -> Skill:
    """Update an existing skill for the user."""
    skill = (
        session.query(Skill)
        .filter(Skill.id == skill_id, Skill.user_id == user_id)
        .first()
    )
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found")
    if data.name is not None:
        skill.name = data.name
    if data.level is not None:
        skill.level = data.level
    if data.description is not None:
        skill.description = data.description
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


def user_login(session: Session, email: str, password: str) -> str:
    """Authenticate a user and return a JWT token."""
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    token = create_token(user.id)
    return token


def user_info(session: Session, user_id: int) -> dict:
    """Return public info for the current user."""
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}


