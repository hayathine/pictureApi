from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from routers import users, pictures
import sys
sys.path.append("~/sql_app")
import crud, models, schemas, database

import uvicorn

app = FastAPI()

app.include_router(users.router)
app.include_router(pictures.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def confirm_oauth2(token: str = Depends(oauth2_scheme)):
    return {"token": token}

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8080)