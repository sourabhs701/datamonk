"""
JWT Utility Module

Includes:
- Create (encode) JWT token
- Decode JWT token
- Extract user info from token

This file keeps auth logic separate and reusable across your app.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Union, Any
import jwt
try:
    from jwt.exceptions import InvalidTokenError
except ImportError:
    InvalidTokenError = Exception

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "devsecret"
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))


def create_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token with the given subject and expiry.
    """
    expire_time = datetime.utcnow() + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    
    payload = {
        "exp": expire_time,
        "sub": str(subject),
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token and returns the payload.
    Returns None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        return None
