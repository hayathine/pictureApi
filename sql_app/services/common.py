from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from mysqlx import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from schemas import schemas
import os
import bcrypt
from sql_app.cruds import crud

from sql_app.cruds.crud import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCES_TOKEN_EXPIRE_MINUTES = os.getenv("ACCES_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# 
class Hash():
    # create hash password
    @staticmethod
    def encodeHashPassword(plain_password):
        return pwd_context.hash(plain_password)
    
    # check hash password
    @staticmethod
    def checkHashPassword(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

class Access_token():
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM):
        to_encode = data.copy()
        # 有効期限を設定
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        # jwt.encode(データ, 秘密鍵, アルゴリズム)
        encode_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_current_user(db: Session,token: Annotated[str, Depends(oauth2_scheme)]):
        credtials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credtials_exception
            token_data = schemas.Token(email=email)
        except JWTError:
            raise credtials_exception
        user = get_user_by_email(db, email=token_data.email)
        if user is None:
            raise credtials_exception
        return user

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
            HTTPException(status_code=400, detail="Incorrect username or password")
        if not Hash.checkHashPassword(plain_password=password, hashed_password=user.hashed_password):
            HTTPException(status_code=400, detail="Incorrect username or password")
        return user

    @staticmethod
    def get_active_user(
        authorize_user: Annotated[schemas.Login_user, Depends(get_current_user)]
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