from fastapi import FastAPI
from mangum import Mangum

from .routers import programs, muscles, exercises, users
from .database import create_db_and_tables

app = FastAPI()
handler = Mangum(app)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return "Hello there!"


app.include_router(programs.router)
app.include_router(muscles.router)
app.include_router(exercises.router)
app.include_router(users.router)
