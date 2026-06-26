from fastapi import FastAPI, HTTPException

app = FastAPI(title="Raga Roads Concert Service", version="1.0.0")

# Stubbed concert database
CONCERTS = {
    1: {
        "concertId": 1,
        "concertTitle": "Corporate Night Chennai",
        "concertDate": "2026-08-01",
        "concertTime": "18:00",
        "concertCity": "Chennai",
        "concertState": "Tamil Nadu",
        "strategyType": "BALANCED",
        "artistRole": "Singer-Male",
        "budgetAllocated": 15000
    },
    2: {
        "concertId": 2,
        "concertTitle": "Wedding Reception Chennai",
        "concertDate": "2026-08-05",
        "concertTime": "19:00",
        "concertCity": "Chennai",
        "concertState": "Tamil Nadu",
        "strategyType": "AVAILABILITY",
        "artistRole": "Singer-Female",
        "budgetAllocated": 12000
    },
    3: {
        "concertId": 3,
        "concertTitle": "Infosys Annual Day",
        "concertDate": "2026-08-08",
        "concertTime": "18:30",
        "concertCity": "Bangalore",
        "concertState": "Karnataka",
        "strategyType": "BALANCED",
        "artistRole": "Guitarist",
        "budgetAllocated": 10000
    },
    4: {
        "concertId": 4,
        "concertTitle": "Tech Summit",
        "concertDate": "2026-08-10",
        "concertTime": "17:00",
        "concertCity": "Bangalore",
        "concertState": "Karnataka",
        "strategyType": "AVAILABILITY",
        "artistRole": "Drummer",
        "budgetAllocated": 9000
    },
    5: {
        "concertId": 5,
        "concertTitle": "Music Fest Hyderabad",
        "concertDate": "2026-08-12",
        "concertTime": "18:00",
        "concertCity": "Hyderabad",
        "concertState": "Telangana",
        "strategyType": "BALANCED",
        "artistRole": "Keyboardist",
        "budgetAllocated": 11000
    },
    6: {
        "concertId": 6,
        "concertTitle": "Cultural Event Pune",
        "concertDate": "2026-08-15",
        "concertTime": "18:30",
        "concertCity": "Pune",
        "concertState": "Maharashtra",
        "strategyType": "AVAILABILITY",
        "artistRole": "Flutist",
        "budgetAllocated": 13000
    },
    7: {
        "concertId": 7,
        "concertTitle": "Startup Meetup Mumbai",
        "concertDate": "2026-08-18",
        "concertTime": "19:00",
        "concertCity": "Mumbai",
        "concertState": "Maharashtra",
        "strategyType": "BALANCED",
        "artistRole": "Tablist",
        "budgetAllocated": 8000
    },
    8: {
        "concertId": 8,
        "concertTitle": "Corporate Event Delhi",
        "concertDate": "2026-08-20",
        "concertTime": "18:00",
        "concertCity": "Delhi",
        "concertState": "Delhi",
        "strategyType": "AVAILABILITY",
        "artistRole": "Singer-Male",
        "budgetAllocated": 16000
    },
    9: {
        "concertId": 9,
        "concertTitle": "Leadership Summit Kochi",
        "concertDate": "2026-08-22",
        "concertTime": "18:00",
        "concertCity": "Kochi",
        "concertState": "Kerala",
        "strategyType": "BALANCED",
        "artistRole": "Singer-Female",
        "budgetAllocated": 12000
    },
    10: {
        "concertId": 10,
        "concertTitle": "Festival Mysore",
        "concertDate": "2026-08-25",
        "concertTime": "19:00",
        "concertCity": "Mysore",
        "concertState": "Karnataka",
        "strategyType": "AVAILABILITY",
        "artistRole": "Guitarist",
        "budgetAllocated": 10000
    },
    11: {
        "concertId": 11,
        "concertTitle": "Concert Coimbatore",
        "concertDate": "2026-08-28",
        "concertTime": "18:00",
        "concertCity": "Coimbatore",
        "concertState": "Tamil Nadu",
        "strategyType": "BALANCED",
        "artistRole": "Drummer",
        "budgetAllocated": 9000
    },
    12: {
        "concertId": 12,
        "concertTitle": "Corporate Vizag",
        "concertDate": "2026-09-01",
        "concertTime": "18:00",
        "concertCity": "Visakhapatnam",
        "concertState": "Andhra Pradesh",
        "strategyType": "AVAILABILITY",
        "artistRole": "Keyboardist",
        "budgetAllocated": 10000
    },
    13: {
        "concertId": 13,
        "concertTitle": "Wedding Jaipur",
        "concertDate": "2026-09-05",
        "concertTime": "19:00",
        "concertCity": "Jaipur",
        "concertState": "Rajasthan",
        "strategyType": "BALANCED",
        "artistRole": "Flutist",
        "budgetAllocated": 14000
    },
    14: {
        "concertId": 14,
        "concertTitle": "Festival Lucknow",
        "concertDate": "2026-09-08",
        "concertTime": "18:00",
        "concertCity": "Lucknow",
        "concertState": "Uttar Pradesh",
        "strategyType": "AVAILABILITY",
        "artistRole": "Tablist",
        "budgetAllocated": 8000
    },
    15: {
        "concertId": 15,
        "concertTitle": "Corporate Chandigarh",
        "concertDate": "2026-09-10",
        "concertTime": "18:30",
        "concertCity": "Chandigarh",
        "concertState": "Punjab",
        "strategyType": "BALANCED",
        "artistRole": "Singer-Male",
        "budgetAllocated": 15000
    },
    16: {
        "concertId": 16,
        "concertTitle": "Tech Event Indore",
        "concertDate": "2026-09-12",
        "concertTime": "18:00",
        "concertCity": "Indore",
        "concertState": "Madhya Pradesh",
        "strategyType": "AVAILABILITY",
        "artistRole": "Singer-Female",
        "budgetAllocated": 12000
    },
    17: {
        "concertId": 17,
        "concertTitle": "Public Concert Goa",
        "concertDate": "2026-09-15",
        "concertTime": "19:00",
        "concertCity": "Panaji",
        "concertState": "Goa",
        "strategyType": "BALANCED",
        "artistRole": "Guitarist",
        "budgetAllocated": 12000
    },
    18: {
        "concertId": 18,
        "concertTitle": "Music Night Surat",
        "concertDate": "2026-09-18",
        "concertTime": "18:00",
        "concertCity": "Surat",
        "concertState": "Gujarat",
        "strategyType": "AVAILABILITY",
        "artistRole": "Drummer",
        "budgetAllocated": 9000
    },
    19: {
        "concertId": 19,
        "concertTitle": "Business Meet Nagpur",
        "concertDate": "2026-09-20",
        "concertTime": "18:00",
        "concertCity": "Nagpur",
        "concertState": "Maharashtra",
        "strategyType": "BALANCED",
        "artistRole": "Keyboardist",
        "budgetAllocated": 10000
    },
    20: {
        "concertId": 20,
        "concertTitle": "Annual Function Patna",
        "concertDate": "2026-09-25",
        "concertTime": "18:00",
        "concertCity": "Patna",
        "concertState": "Bihar",
        "strategyType": "AVAILABILITY",
        "artistRole": "Flutist",
        "budgetAllocated": 13000
    }
}

@app.get("/")
def home():
    return {"service": "Concert Service", "status": "Running"}

@app.get("/concerts")
def get_concerts():
    return list(CONCERTS.values())

@app.get("/concerts/{concert_id}")
def get_concert(concert_id: int) -> dict:
    concert = CONCERTS.get(concert_id)
    if not concert:
        raise HTTPException(
            status_code=404,
            detail="Concert Not Found"
        )
    return concert
