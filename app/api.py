from fastapi import FastAPI

from .routers import programs, muscles
from .database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def on_startup():
    return "Hello there!"


app.include_router(programs.router)
app.include_router(muscles.router)
