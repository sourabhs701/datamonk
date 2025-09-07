from models import User
from auth import get_current_user_id
from fastapi import APIRouter, HTTPException, Depends, status
from schemas import UserCreate, TokenSchema, UserLogin, UserOut   
from sqlmodel import Session
from database import get_session
import crud

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register",response_model=TokenSchema)
def register_user(user: UserCreate, session: Session = Depends(get_session) ):
    token = crud.create_user(session, user)
    return {"token": token}

@auth_router.post('/login' ,response_model=TokenSchema)
def login(request: UserLogin, db: Session = Depends(get_session)):
    token = crud.user_login(db, request.email, request.password)
    return {"token": token}


@auth_router.get("/me",response_model=UserOut)
def get_current_user( db: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    return crud.user_info(db, user_id)