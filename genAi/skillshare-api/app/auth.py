
from passlib.context import CryptContext
from .utils.jwt_handler import decode_token
from fastapi import HTTPException, Header

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_current_user_id(authorization: str = Header(...)) -> int:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization Header")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid Token")
    try:
        return int(payload["sub"])
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Token Subject")
        
