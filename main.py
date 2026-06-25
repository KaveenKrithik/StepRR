from fastapi import FastAPI
from routers import artist, concert

app = FastAPI()

app.include_router(artist.router)
app.include_router(concert.router)


@app.get("/")
def home():
    return {"message": "Welcome to The Project"}

def main():
    return

if __name__ == "__main__":
    main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
