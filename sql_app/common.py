
from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    # create hash password
    @staticmethod
    def encodeHashPassword(plain_password):
        return pwd_context.hash(plain_password)
    
    # check hash password
    @staticmethod
    def checkHashPassword(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)