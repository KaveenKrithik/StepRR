from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    
    booking_id = Column(Integer, primary_key=True, index=True)
    concert_id = Column(Integer, nullable=False)
    concert_title = Column(String, nullable=False)
    concert_date = Column(String, nullable=False)
    concert_city = Column(String, nullable=False)
    artist_id = Column(Integer, nullable=False)
    artist_name = Column(String, nullable=False)
    artist_role = Column(String, nullable=False)
    booking_status = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    strategy_applied = Column(String, nullable=False)
    budget_allocated = Column(Float, nullable=False)
    artist_cost = Column(Float, nullable=False)
    budget_remaining = Column(Float, nullable=False)
    allocated_by = Column(String, nullable=False)

class BlockedArtist(Base):
    __tablename__ = "blocked_artists"
    
    artist_id = Column(Integer, primary_key=True, index=True)
    reason = Column(String, nullable=True)
