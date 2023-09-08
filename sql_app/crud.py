from sqlalchemy.orm import Session

from . import models
from . import schemas

# 全ユーザーを取得する関数
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

# 特定のユーザーを取得する関数
def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

# 新規ユーザーを作成する関数
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(name=user.name, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 全写真を取得する関数
def get_pictures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pictures).offset(skip).limit(limit).all()

# 特定のユーザーの写真を取得する関数
def get_pictures_by_user_id(db: Session, user_id: int):
    return db.query(models.Pictures).filter(models.Pictures.owner_id == user_id).all()

# 特定のユーザーの特定の写真を取得する関数
def get_picture_by_user_id_and_picture_id(db: Session, user_id: int, picture_id: int):
    return db.query(models.Pictures).filter(models.Pictures.owner_id == user_id).filter(models.Pictures.picure_id == picture_id).first()

# ユーザー情報を変更する関数
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    db_user.name = user.name
    db_user.email = user.email
    db_user.hashed_password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザーを削除する関数
def delete_user(db: Session,user_id: int):
    delete_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    delete_user.is_active = 0
    db.commit()