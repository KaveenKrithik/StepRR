from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from config.config import settings
from schemas.booking import BookingRequest
from services.booking_service import BookingService
from repository.booking import BookingRepository
from repository.db_connection import get_db
from jose import jwt, JWTError

router = APIRouter(prefix="/bookings", tags=["Bookings"])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Please provide authorization token")
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        role = payload.get("role")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/allocate")
def allocate_artist(
    request: BookingRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization)
    if user["role"] != "Band Manager":
        raise HTTPException(status_code=401, detail="Only band manager can allocate artists")

    repo = BookingRepository(db)
    booking_service = BookingService(repo)
    try:
        result = booking_service.allocate(request.artistId, request.concertId, user["username"])
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/")
def get_all_bookings(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    get_current_user(authorization)
    repo = BookingRepository(db)
    booking_service = BookingService(repo)
    return booking_service.get_all()

@router.post("/block/{artist_id}")
def block_artist(
    artist_id: int,
    reason: str = "Blocked by Admin or Manager",
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization)
    if user["role"] not in ["Band Manager", "Administrator"]:
        raise HTTPException(status_code=401, detail="Unauthorized role")
    repo = BookingRepository(db)
    return repo.add_blocked_artist(artist_id, reason)
