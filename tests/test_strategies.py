import pytest
from unittest.mock import patch
from services.allocation_service import (
    BalancedStrategy, AvailabilityStrategy, StrategyFactory
)

# ---- helpers ----
def make_artist(role="Singer-Male", available=True, city="Chennai", state="Tamil Nadu", cost=12000):
    return {
        "artistRole": role,
        "available": available,
        "city": city,
        "state": state,
        "performanceCost": cost
    }

def make_concert(role="Singer-Male", city="Chennai", state="Tamil Nadu", budget=15000):
    return {
        "artistRole": role,
        "concertCity": city,
        "concertState": state,
        "budgetAllocated": budget
    }

# ---- Balanced Strategy ----
def test_balanced_confirms_same_city():
    artist = make_artist(city="Chennai", state="Tamil Nadu")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = BalancedStrategy().allocate(artist, concert)
    assert result["status"] == "Confirmed"

def test_balanced_confirms_same_state_diff_city():
    artist = make_artist(city="Coimbatore", state="Tamil Nadu")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = BalancedStrategy().allocate(artist, concert)
    assert result["status"] == "Confirmed"

def test_balanced_rejects_wrong_location():
    artist = make_artist(city="Mumbai", state="Maharashtra")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = BalancedStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

def test_balanced_rejects_role_mismatch():
    artist = make_artist(role="Drummer")
    concert = make_concert(role="Singer-Male")
    result = BalancedStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

def test_balanced_rejects_unavailable_artist():
    artist = make_artist(available=False)
    concert = make_concert()
    result = BalancedStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

def test_balanced_rejects_over_budget():
    artist = make_artist(cost=20000)
    concert = make_concert(budget=15000)
    result = BalancedStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

# ---- Availability Strategy ----
def test_availability_ignores_location():
    artist = make_artist(city="Mumbai", state="Maharashtra")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = AvailabilityStrategy().allocate(artist, concert)
    assert result["status"] == "Confirmed"

def test_availability_rejects_role_mismatch():
    artist = make_artist(role="Flutist")
    concert = make_concert(role="Singer-Male")
    result = AvailabilityStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

def test_availability_rejects_unavailable():
    artist = make_artist(available=False)
    concert = make_concert()
    result = AvailabilityStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

def test_availability_rejects_over_budget():
    artist = make_artist(cost=20000)
    concert = make_concert(budget=15000)
    result = AvailabilityStrategy().allocate(artist, concert)
    assert result["status"] == "Rejected"

def test_availability_confirms_all_pass():
    artist = make_artist()
    concert = make_concert()
    result = AvailabilityStrategy().allocate(artist, concert)
    assert result["status"] == "Confirmed"

# ---- Strategy Factory ----
def test_factory_returns_balanced():
    strategy = StrategyFactory.get_strategy("BALANCED")
    assert isinstance(strategy, BalancedStrategy)

def test_factory_returns_availability():
    strategy = StrategyFactory.get_strategy("AVAILABILITY")
    assert isinstance(strategy, AvailabilityStrategy)

def test_factory_handles_lowercase():
    strategy = StrategyFactory.get_strategy("balanced")
    assert isinstance(strategy, BalancedStrategy)

def test_factory_raises_on_invalid():
    with pytest.raises(ValueError):
        StrategyFactory.get_strategy("INVALID_STRATEGY")