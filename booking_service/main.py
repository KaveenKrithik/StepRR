from fastapi import FastAPI
from routers import auth, booking
from models import Base, BlockedArtist
from repository.db_connection import engine, SessionLocal

app = FastAPI(
    title="Raga Roads Booking Service",
    description="Artist allocation booking platform microservice",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(booking.router)

@app.on_event("startup")
def on_startup():
    # Automatically create tables in PostgreSQL on startup
    Base.metadata.create_all(bind=engine)
    
    # Seed default blocked artist (Artist ID 3) if not already seeded
    db = SessionLocal()
    try:
        if not db.query(BlockedArtist).filter(BlockedArtist.artist_id == 3).first():
            db.add(BlockedArtist(artist_id=3, reason="Blocked due to past contract breach"))
            db.commit()
    except Exception as e:
        print(f"Skipping database seeding: {str(e)}")
    finally:
        db.close()

@app.get("/")
def home():
    return {"service": "Booking Service", "status": "Running"}
