
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated
from dotenv import load_dotenv
from datetime import timedelta
from services.common import Hash, Access_token, ACCES_TOKEN_EXPIRE_MINUTES
import os
import sys
sys.path.append("~/sql_app")
from databases.database import Access_DB
from cruds import crud
from schemas import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/login", 
    tags=["login"]
    )

def authorize_user(db: Session , username: str, password: str):
    """
    ユーザー認証を行う関数
    Parameters
    ----------
    db : Session
        SQLAlchemyのセッション
    username : str
        ユーザー名
    password : str
        パスワード
    Returns
    -------
    user : models.Users
        ユーザー情報
    """
    user = crud.get_current_user_by_email(db, email=username)
    if user is None:
        return False
    if not Hash.checkHashPassword(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user

def get_active_user(
    authorize_user: Annotated[schemas.Login_user, Depends(authorize_user)]
    ):
    """
    ユーザーがアクティブかどうかを確認する関数
    Parameters
    ----------
    authorize_user : models.Users
        ユーザー情報
    Returns
    -------
    authorize_user : models.Users
        ユーザー情報
    """
    if authorize_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return authorize_user

@router.get("/")
async def confirm_oauth2(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@router.get("/user/")
def read_user(current_user: schemas.User):
    active_user = get_active_user(current_user)
    return active_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(Access_DB.get_db)
    ):
    # ユーザー認証を行う
    user = authorize_user(db, username=form.username, password=form.password)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    # アクセストークンを作成する
    token = Access_token.create_access_token(
        {"sub": user.email},
        expires_delta=timedelta(minutes=float(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES"))),
        secret_key=os.getenv("SECRET_KEY")
    )
    return schemas.Token(access_token=token, token_type="bearer")