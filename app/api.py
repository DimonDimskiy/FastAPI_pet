from fastapi import FastAPI

from .routers import programs, muscles, exercises
from .database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return "Hello there!"


app.include_router(programs.router)
app.include_router(muscles.router)
app.include_router(exercises.router)
