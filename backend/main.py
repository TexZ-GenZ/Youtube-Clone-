from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.base import Base
from routes import auth
from db.db import engine
app = FastAPI()

origins = ["http://localhost:3000", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")


@app.get("/")
def root():
    return {"message": "Hello Stupid Docke"}


Base.metadata.create_all(bind=engine)