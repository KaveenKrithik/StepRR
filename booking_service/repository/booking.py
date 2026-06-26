from sqlalchemy.orm import Session
from models import Booking, BlockedArtist

class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, booking_dict: dict) -> dict:
        booking = Booking(
            concert_id=booking_dict["concertId"],
            concert_title=booking_dict["concertTitle"],
            concert_date=booking_dict["concertDate"],
            concert_city=booking_dict["concertCity"],
            artist_id=booking_dict["artistId"],
            artist_name=booking_dict["artistName"],
            artist_role=booking_dict["artistRole"],
            booking_status=booking_dict["bookingStatus"],
            reason=booking_dict.get("reason"),
            strategy_applied=booking_dict["strategyApplied"],
            budget_allocated=booking_dict["budgetAllocated"],
            artist_cost=booking_dict["artistCost"],
            budget_remaining=booking_dict["budgetRemaining"],
            allocated_by=booking_dict["allocatedBy"]
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        
        booking_dict["bookingId"] = booking.booking_id
        return booking_dict

    def get_all(self):
        bookings = self.db.query(Booking).all()
        result = []
        for b in bookings:
            result.append({
                "bookingId": b.booking_id,
                "concertId": b.concert_id,
                "concertTitle": b.concert_title,
                "concertDate": b.concert_date,
                "concertCity": b.concert_city,
                "artistId": b.artist_id,
                "artistName": b.artist_name,
                "artistRole": b.artist_role,
                "bookingStatus": b.booking_status,
                "reason": b.reason,
                "strategyApplied": b.strategy_applied,
                "budgetAllocated": b.budget_allocated,
                "artistCost": b.artist_cost,
                "budgetRemaining": b.budget_remaining,
                "allocatedBy": b.allocated_by
            })
        return result

    def is_artist_blocked(self, artist_id: int) -> bool:
        blocked = self.db.query(BlockedArtist).filter(BlockedArtist.artist_id == artist_id).first()
        return blocked is not None

    def add_blocked_artist(self, artist_id: int, reason: str = "Unspecified"):
        # Check if already blocked
        if not self.is_artist_blocked(artist_id):
            blocked = BlockedArtist(artist_id=artist_id, reason=reason)
            self.db.add(blocked)
            self.db.commit()
            self.db.refresh(blocked)
        return {"artistId": artist_id, "blocked": True}
