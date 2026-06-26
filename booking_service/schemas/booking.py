from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    authenticated: bool
    userId: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None
    token: Optional[str] = None
    message: Optional[str] = None

class BookingRequest(BaseModel):
    concertId: int
    artistId: int

class BookingResponse(BaseModel):
    bookingId: int
    concertId: int
    concertTitle: str
    concertDate: str
    concertCity: str
    artistId: int
    artistName: str
    artistRole: str
    bookingStatus: str
    reason: str
    strategyApplied: str
    budgetAllocated: float
    artistCost: float
    budgetRemaining: float
    allocatedBy: str
