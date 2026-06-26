from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
from config.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

USERS = {
    "admin":   {"userId": 1, "username": "admin",   "password": "admin123",   "role": "Administrator"},
    "manager": {"userId": 2, "username": "manager", "password": "manager123", "role": "Band Manager"},
    "artist1": {"userId": 3, "username": "artist1", "password": "artist123",  "role": "Artist"},
    "artist2": {"userId": 4, "username": "artist2", "password": "artist123",  "role": "Artist"},
    "artist3": {"userId": 5, "username": "artist3", "password": "artist123",  "role": "Artist"},
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    user = USERS.get(request.username)
    if not user:
        return {"authenticated": False, "message": "Invalid Username"}
    if request.password != user["password"]:
        return {"authenticated": False, "message": "Invalid Password"}
    
    token_data = {
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "authenticated": True,
        "userId": user["userId"],
        "username": user["username"],
        "role": user["role"],
        "token": token,
    }

@router.post("/validate")
def validate_token(authorization: str = Header(...)):
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        role = payload.get("role")
        return {"valid": True, "username": username, "role": role}
    except Exception:
        return {"valid": False, "message": "Invalid Token"}
