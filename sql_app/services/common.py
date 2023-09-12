from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCES_TOKEN_EXPIRE_MINUTES = os.getenv("ACCES_TOKEN_EXPIRE_MINUTES")

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
        # 有効期限を設定
        expire = datetime.utcnow() + expires_delta
        # jwt.encode(データ, 秘密鍵, アルゴリズム)
        return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
