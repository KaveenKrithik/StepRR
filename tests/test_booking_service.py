import pytest
from unittest.mock import MagicMock, patch
import httpx
from services.booking_service import BookingService
from repository.booking import BookingRepository
from exceptions.exception import ArtistNotFoundException, ConcertNotFoundException

@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=BookingRepository)
    repo.is_artist_blocked.return_value = False
    repo.save.side_effect = lambda b: {**b, "bookingId": 999}
    return repo

@patch("httpx.Client.get")
def test_allocate_successful_balanced(mock_get, mock_repo):
    # Setup mock HTTP responses
    mock_concert_resp = MagicMock()
    mock_concert_resp.status_code = 200
    mock_concert_resp.json.return_value = {
        "concertId": 1,
        "concertTitle": "Corporate Night Chennai",
        "concertDate": "2026-08-01",
        "concertCity": "Chennai",
        "concertState": "Tamil Nadu",
        "strategyType": "BALANCED",
        "artistRole": "Singer-Male",
        "budgetAllocated": 15000
    }
    
    mock_artist_resp = MagicMock()
    mock_artist_resp.status_code = 200
    mock_artist_resp.json.return_value = {
        "artistId": 1,
        "artistName": "Arjun",
        "artistRole": "Singer-Male",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "performanceCost": 12000,
        "available": True
    }
    
    # Side effects for httpx client get: first call is concert, second is artist
    mock_get.side_effect = [mock_concert_resp, mock_artist_resp]
    
    service = BookingService(mock_repo)
    result = service.allocate(artist_id=1, concert_id=1, allocated_by="manager")
    
    assert result["bookingStatus"] == "Confirmed"
    assert result["bookingId"] == 999
    assert result["artistName"] == "Arjun"
    assert result["concertTitle"] == "Corporate Night Chennai"
    assert result["budgetRemaining"] == 3000.0

@patch("httpx.Client.get")
def test_allocate_rejected_blocked_artist(mock_get, mock_repo):
    # Setup mock responses
    mock_concert_resp = MagicMock()
    mock_concert_resp.status_code = 200
    mock_concert_resp.json.return_value = {
        "concertId": 1,
        "concertTitle": "Corporate Night Chennai",
        "concertDate": "2026-08-01",
        "concertCity": "Chennai",
        "concertState": "Tamil Nadu",
        "strategyType": "BALANCED",
        "artistRole": "Singer-Male",
        "budgetAllocated": 15000
    }
    
    mock_artist_resp = MagicMock()
    mock_artist_resp.status_code = 200
    mock_artist_resp.json.return_value = {
        "artistId": 3,
        "artistName": "Priya",
        "artistRole": "Singer-Male",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "performanceCost": 10000,
        "available": True
    }
    mock_get.side_effect = [mock_concert_resp, mock_artist_resp]
    
    # Block the artist
    mock_repo.is_artist_blocked.return_value = True
    
    service = BookingService(mock_repo)
    result = service.allocate(artist_id=3, concert_id=1, allocated_by="manager")
    
    assert result["bookingStatus"] == "Rejected"
    assert result["reason"] == "Artist is blocked"

@patch("httpx.Client.get")
def test_allocate_concert_not_found(mock_get, mock_repo):
    mock_concert_resp = MagicMock()
    mock_concert_resp.status_code = 404
    mock_get.return_value = mock_concert_resp
    
    service = BookingService(mock_repo)
    with pytest.raises(ConcertNotFoundException):
        service.allocate(artist_id=1, concert_id=999, allocated_by="manager")

@patch("httpx.Client.get")
def test_allocate_artist_not_found(mock_get, mock_repo):
    mock_concert_resp = MagicMock()
    mock_concert_resp.status_code = 200
    mock_concert_resp.json.return_value = {
        "concertId": 1,
        "concertTitle": "Corporate Night Chennai",
        "concertDate": "2026-08-01",
        "concertCity": "Chennai",
        "concertState": "Tamil Nadu",
        "strategyType": "BALANCED",
        "artistRole": "Singer-Male",
        "budgetAllocated": 15000
    }
    mock_artist_resp = MagicMock()
    mock_artist_resp.status_code = 404
    mock_get.side_effect = [mock_concert_resp, mock_artist_resp]
    
    service = BookingService(mock_repo)
    with pytest.raises(ArtistNotFoundException):
        service.allocate(artist_id=999, concert_id=1, allocated_by="manager")
