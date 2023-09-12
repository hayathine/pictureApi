from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from databases.database import Access_DB
import sys
sys.path.append("~/sql_app")
from cruds import crud
from schemas import schemas

router = APIRouter(
    prefix="/picture", 
    tags=["picture"]
    )

# ユーザーIDに紐づいたすべての画像を取得するAPI
@router.get("/{user_id}", response_model=List[schemas.Picture])
def get_pictures(user_id: int,skip=0, limit=100, db: Session = Depends(Access_DB.get_db)):
    # ユーザーIDが存在するか確認する
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_pictures = crud.get_pictures(db=db, owner_id=user_id, skip=skip, limit=limit)
    return db_pictures

# 画像情報を作成するAPI
@router.post("/", response_model=schemas.Picture)
async def create_picture(picture: schemas.PictureCreate, db: Session = Depends(Access_DB.get_db)):
    # ユーザーIDが存在するか確認する
    db_user = crud.get_user_by_id(db, picture.owner_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_picture(db=db, picture=picture)
    

@router.get("/{user_id}/{picture_id}", response_model=schemas.Picture)
async def get_picture_by_id(user_id:int, picture_id: int, db: Session = Depends(Access_DB.get_db)):
    # ユーザーIDが存在するか確認する
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_picture = crud.get_picture_by_user_id_and_picture_id(db, user_id, picture_id)
    if db_picture is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    return db_picture