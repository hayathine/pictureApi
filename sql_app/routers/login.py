
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import timedelta
from common import Hash, Access_token, ACCES_TOKEN_EXPIRE_MINUTES
import sys
sys.path.append("~/sql_app")
import crud, models, schemas, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/login", 
    tags=["login"]
    )

def get_db():
    db = database.sessionLocal()
    try:
        yield db
    finally:
        db.close()

def authorize_user(db: Session, username: str, password: str):
    """
    ユーザー認証を行う関数
    """
    user = crud.get_current_user_by_email(db, email=username)
    if user is None:
        return False
    if not Hash.checkHashPassword(plain_password=password, hashed_password=user.hashed_password):
        return False
    return user

@router.get("/")
async def confirm_oauth2(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# @router.get("/user/")
# async def read_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
#     return current_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
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
        expires_delta=timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    )
    return schemas.Token(access_token=token, token_type="bearer")