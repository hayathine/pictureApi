
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated
from dotenv import load_dotenv
from datetime import timedelta
from services.common import Hash, Access_token
import os
import sys
sys.path.append("~/sql_app")
from databases.database import Access_DB
from cruds import crud
from schemas import schemas
from schemas.schemas import Login_user, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

router = APIRouter(
    prefix="/login", 
    tags=["login"]
    )

@router.get("/")
async def confirm_oauth2(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@router.get("/user/", response_model=User)
def read_user(
#TODO ここでエラーが出る　本当はアノテーション機能を使いたい
    current_user: schemas.Login_user
    ):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(Access_DB.get_db)
    ):
    # ユーザー認証を行う
    user_dict= Access_token.authorize_user(db, username=form.username, password=form.password)

    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    # user = Login_user(**user_dict)
    access_token_expires = timedelta(minutes=float(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES")))
    # アクセストークンを作成する
    access_token = Access_token.create_access_token(
    #     # TODO ここでエラーが出る
        data = {"sub": user_dict.email},
        expires_delta=access_token_expires,
    )

    return {"access_token":access_token, "token_type":"bearer"}   