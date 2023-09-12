from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append("~/sql_app")
from databases.database import Access_DB
from cruds import crud
from schemas import schemas

from services.common import Hash

router = APIRouter(
    prefix="/user", 
    tags=["user"],
    )

# ユーザー一覧を取得するAPI
@router.get("/", response_model=List[schemas.User])
async def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(Access_DB.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# ユーザーを作成するAPI
@router.post("/", response_model=schemas.User) # response_modelを指定することで、レスポンスのスキーマを指定できる
async def create_user(user: schemas.UserCreate, db: Session = Depends(Access_DB.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # パスワードをハッシュ化する
    user.password = Hash.encodeHashPassword(user.password)

    return crud.create_user(db=db, user=user)

# ユーザー情報を変更するAPI
@router.put("/")
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(Access_DB.get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ユーザーを削除するAPI
@router.delete("/")
async def delete_user(user_id: int, db: Session = Depends(Access_DB.get_db)):
    if crud.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    

# ユーザーIDを指定してユーザー情報を取得するAPI
@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(Access_DB.get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user