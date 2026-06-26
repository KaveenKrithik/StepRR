import httpx
from config.config import settings
from services.allocation_service import StrategyFactory
from repository.booking import BookingRepository
from exceptions.exception import ArtistNotFoundException, ConcertNotFoundException

class BookingService:
    def __init__(self, repository: BookingRepository):
        self.repository = repository

    def allocate(self, artist_id: int, concert_id: int, allocated_by: str) -> dict:
        # Fetch concert details from Concert Service over HTTP
        concert_url = f"{settings.CONCERT_SERVICE_URL}/concerts/{concert_id}"
        try:
            with httpx.Client() as client:
                response = client.get(concert_url)
                if response.status_code == 404:
                    raise ConcertNotFoundException(concert_id)
                response.raise_for_status()
                concert = response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to communicate with Concert Service: {str(e)}")

        # Fetch artist details from Artist Service over HTTP
        artist_url = f"{settings.ARTIST_SERVICE_URL}/artists/{artist_id}"
        try:
            with httpx.Client() as client:
                response = client.get(artist_url)
                if response.status_code == 404:
                    raise ArtistNotFoundException(artist_id)
                response.raise_for_status()
                artist = response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to communicate with Artist Service: {str(e)}")

        # Check if the artist is blocked in the DB
        if self.repository.is_artist_blocked(artist_id):
            result = {"status": "Rejected", "reason": "Artist is blocked"}
        else:
            # Execute the strategy
            strategy = StrategyFactory.get_strategy(concert["strategyType"])
            result = strategy.allocate(artist, concert)

        booking = {
            "concertId": concert["concertId"],
            "concertTitle": concert["concertTitle"],
            "concertDate": concert["concertDate"],
            "concertCity": concert["concertCity"],
            "artistId": artist["artistId"],
            "artistName": artist["artistName"],
            "artistRole": artist["artistRole"],
            "bookingStatus": result["status"],
            "reason": result["reason"],
            "strategyApplied": concert["strategyType"],
            "budgetAllocated": float(concert["budgetAllocated"]),
            "artistCost": float(artist["performanceCost"]),
            "budgetRemaining": float(concert["budgetAllocated"] - artist["performanceCost"]),
            "allocatedBy": allocated_by
        }

        return self.repository.save(booking)

    def get_all(self):
        return self.repository.get_all()
