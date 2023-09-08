from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .database import sessionLocal, engine
from . import crud, models, schemas


app = FastAPI()

# origins = [
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# ユーザー一覧を取得するAPI
@app.get("/user/", response_model=List[schemas.User])
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# ユーザーを作成するAPI
@app.post("/user", response_model=schemas.User) # response_modelを指定することで、レスポンスのスキーマを指定できる
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)

# ユーザー情報を変更するAPI
@app.put("/user")
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    # if db_user is None:
        # raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ユーザーを削除するAPI
@app.delete("/user")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # if crud.get_user_by_id(db, user_id) is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    

@app.get("/user/{user_id}")
async def get_user_by_id(user_id: int):
    pass

@app.get("/picture/")
async def get_picture():
    pass

@app.post("/picture/")
async def create_picture():
    pass

@app.get("/picture/{picture_id}")
async def get_picture_by_id(picture_id: int):
    pass

