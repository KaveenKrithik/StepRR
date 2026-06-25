import base64
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
router = APIRouter(prefix="/auth", tags=["Auth"])
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
    token = base64.b64encode(
        f"{user['username']}:{user['role']}".encode()
    ).decode()
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
        decoded = base64.b64decode(authorization).decode()
        username, role = decoded.split(":", 1)
        return {"valid": True, "username": username, "role": role}
    except Exception:
        return {"valid": False, "message": "Invalid Token"}