# backend/app/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import os
import sys

# Add path to import SalesDB
from app.database.db import SalesDB

router = APIRouter()

# Constants for JWT
SECRET_KEY = "your-secret-key"  # Replace with a strong secret key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic model
class LoginRequest(BaseModel):
    phone: str
    password: str
    role: str

# ✅ Authenticate using database
def verify_user_db(phone: str, password: str, role: str):
    with SalesDB() as db:
        users = db.get_records("users", [("phone", "=", phone)])
        if not users:
            return False
        user = users[0]
        return (
            user["password"] == password
            and user["role"].lower() == role.lower()
        )

# JWT creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login endpoint
@router.post("/login")
async def login(login_req: LoginRequest):
    phone = login_req.phone
    password = login_req.password
    role = login_req.role

    if not verify_user_db(phone, password, role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone, password or role",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": phone, "role": role})
    return {"access_token": access_token, "token_type": "bearer"}

# Get user from JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str = payload.get("sub")
        role: str = payload.get("role")
        if phone is None or role is None:
            raise credentials_exception
        return {"phone": phone, "role": role}
    except JWTError:
        raise credentials_exception
