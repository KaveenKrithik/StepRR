from fastapi import FastAPI, HTTPException

app = FastAPI(title="Raga Roads Artist Service", version="1.0.0")

# Stubbed artist database
ARTISTS = {
    1: {
        "artistId": 1,
        "artistName": "Arjun",
        "artistRole": "Singer-Male",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "performanceCost": 12000,
        "available": True
    },
    2: {
        "artistId": 2,
        "artistName": "Rahul",
        "artistRole": "Singer-Male",
        "city": "Bangalore",
        "state": "Karnataka",
        "performanceCost": 15000,
        "available": True
    },
    3: {
        "artistId": 3,
        "artistName": "Priya",
        "artistRole": "Singer-Female",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "performanceCost": 10000,
        "available": True
    },
    4: {
        "artistId": 4,
        "artistName": "Megha",
        "artistRole": "Singer-Female",
        "city": "Hyderabad",
        "state": "Telangana",
        "performanceCost": 12000,
        "available": False
    },
    5: {
        "artistId": 5,
        "artistName": "Karthik",
        "artistRole": "Guitarist",
        "city": "Bangalore",
        "state": "Karnataka",
        "performanceCost": 9000,
        "available": True
    },
    6: {
        "artistId": 6,
        "artistName": "Vikram",
        "artistRole": "Guitarist",
        "city": "Mumbai",
        "state": "Maharashtra",
        "performanceCost": 11000,
        "available": True
    },
    7: {
        "artistId": 7,
        "artistName": "Rohit",
        "artistRole": "Drummer",
        "city": "Delhi",
        "state": "Delhi",
        "performanceCost": 8500,
        "available": True
    },
    8: {
        "artistId": 8,
        "artistName": "Amit",
        "artistRole": "Drummer",
        "city": "Pune",
        "state": "Maharashtra",
        "performanceCost": 9500,
        "available": False
    },
    9: {
        "artistId": 9,
        "artistName": "Manoj",
        "artistRole": "Keyboardist",
        "city": "Hyderabad",
        "state": "Telangana",
        "performanceCost": 10000,
        "available": True
    },
    10: {
        "artistId": 10,
        "artistName": "Suresh",
        "artistRole": "Keyboardist",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "performanceCost": 11000,
        "available": True
    },
    11: {
        "artistId": 11,
        "artistName": "Naveen",
        "artistRole": "Flutist",
        "city": "Mysore",
        "state": "Karnataka",
        "performanceCost": 12000,
        "available": True
    },
    12: {
        "artistId": 12,
        "artistName": "Kiran",
        "artistRole": "Flutist",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "performanceCost": 13000,
        "available": True
    },
    13: {
        "artistId": 13,
        "artistName": "Ramesh",
        "artistRole": "Tablist",
        "city": "Mumbai",
        "state": "Maharashtra",
        "performanceCost": 7000,
        "available": True
    },
    14: {
        "artistId": 14,
        "artistName": "Sanjay",
        "artistRole": "Tablist",
        "city": "Jaipur",
        "state": "Rajasthan",
        "performanceCost": 8000,
        "available": True
    }
}

@app.get("/")
def home():
    return {"service": "Artist Service", "status": "Running"}

@app.get("/artists")
def get_artists():
    return list(ARTISTS.values())

@app.get("/artists/{artist_id}")
def get_artist(artist_id: int) -> dict:
    artist = ARTISTS.get(artist_id)
    if not artist:
        raise HTTPException(
            status_code=404,
            detail="Artist Not Found"
        )
    return artist
