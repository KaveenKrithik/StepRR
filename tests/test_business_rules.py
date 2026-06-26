import pytest
from services.allocation_service import BalancedStrategy

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

strategy = BalancedStrategy()

# ---- Role Validation Rule ----
def test_role_mismatch_gives_rejected():
    artist = make_artist(role="Guitarist")
    concert = make_concert(role="Singer-Male")
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Rejected"
    assert "role" in result["reason"].lower()

def test_role_match_passes():
    artist = make_artist(role="Singer-Male")
    concert = make_concert(role="Singer-Male")
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"

# ---- Availability Validation Rule ----
def test_unavailable_artist_gives_rejected():
    artist = make_artist(available=False)
    concert = make_concert()
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Rejected"
    assert "available" in result["reason"].lower()

def test_available_artist_passes():
    artist = make_artist(available=True)
    concert = make_concert()
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"

# ---- Location Validation Rule ----
def test_different_city_and_state_gives_rejected():
    artist = make_artist(city="Mumbai", state="Maharashtra")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Rejected"
    assert "city" in result["reason"].lower() or "state" in result["reason"].lower()

def test_same_city_passes():
    artist = make_artist(city="Chennai", state="Tamil Nadu")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"

def test_different_city_same_state_passes():
    artist = make_artist(city="Coimbatore", state="Tamil Nadu")
    concert = make_concert(city="Chennai", state="Tamil Nadu")
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"

# ---- Budget Validation Rule ----
def test_cost_exceeds_budget_gives_rejected():
    artist = make_artist(cost=20000)
    concert = make_concert(budget=15000)
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Rejected"
    assert "budget" in result["reason"].lower()

def test_cost_within_budget_passes():
    artist = make_artist(cost=12000)
    concert = make_concert(budget=15000)
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"

def test_cost_equal_to_budget_passes():
    artist = make_artist(cost=15000)
    concert = make_concert(budget=15000)
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"

# ---- All validations pass ----
def test_all_pass_gives_confirmed():
    artist = make_artist()
    concert = make_concert()
    result = strategy.allocate(artist, concert)
    assert result["status"] == "Confirmed"
    assert result["reason"] == "All validations passed"
