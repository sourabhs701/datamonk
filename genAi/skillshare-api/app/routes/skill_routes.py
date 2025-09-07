from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from ..database import get_session
from ..models import Skill
from ..schemas import SkillCreate, SkillUpdate, SkillOut
from ..auth import get_current_user_id
from .. import crud

skill_router = APIRouter(tags=["skills"])


@skill_router.post("/", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(data: SkillCreate, db: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    return crud.create_skill(db, user_id, data)


@skill_router.get("/", response_model=List[SkillOut])
def list_skills(db: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    return crud.get_skills_by_user(db, user_id)


@skill_router.get("/{skill_id}", response_model=SkillOut)
def get_skill(skill_id: int, db: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    return crud.get_skill(db, user_id, skill_id)


@skill_router.put("/{skill_id}", response_model=SkillOut)
def update_skill(skill_id: int, data: SkillUpdate, db: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    return crud.update_skill(db, user_id, skill_id, data)


@skill_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int, db: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    return crud.delete_skill(db, user_id, skill_id)