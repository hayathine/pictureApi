from sqlalchemy.orm import Session

from . import models
from . import schemas
from . import crud_log

#　ロガーの設定
logger = crud_log.get_logger(__name__)

# 全ユーザーを取得する関数
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    """
    メールアドレスからユーザーを取得する関数
    Parameters
    ----------
    db : Session
        SQLAlchemyのセッション
    email : str
        メールアドレス
    Returns
    -------
    db_user : models.Users
        ユーザー情報
    """
    return db.query(models.Users).filter(models.Users.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """
    IDからユーザーを取得する関数
    Parameters
    ----------
    db : Session
        SQLAlchemyのセッション
    user_id : int
        ユーザーID
    Returns
    -------
    db_user : models.Users
        ユーザー情報
    """
    return db.query(models.Users).filter(models.Users.user_id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    ユーザーを作成する関数
    Parameters
    ----------
    db : Session
        SQLAlchemyのセッション
    user : schemas.UserCreate
        ユーザー情報
    Returns
    -------
    db_user : models.Users
        作成したユーザー情報
    """ 
    db_user = models.Users(name=user.name, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



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

def get_pictures(db: Session, owner_id:int, skip: int = 0, limit: int = 100):
    """
    ユーザーIDに紐づいている画像を取得する関数
    Parameters
    ----------
    db : Session
        SQLAlchemyのセッション
    owner_id : int
        ユーザーID
    skip : int, optional
        取得する画像の開始位置, by default 0
    limit : int, optional
        取得する画像の数, by default 100
    Returns
    -------
    db_pictures : List[models.Pictures]
        画像情報のリスト
    """
    return db.query(models.Pictures).filter(models.Pictures.owner_id == owner_id).offset(skip).limit(limit).all()

def create_picture(db: Session, picture: schemas.PictureCreate):
    """
    画像情報を作成する関数
    Parameters
    ----------
    db : Session
        SQLAlchemyのセッション
    picture : schemas.PictureCreate
        画像情報
    Returns
    -------
    db_picture : models.Pictures
        作成した画像情報
    """
    # logger.info("create_picture")   
    db_picture = models.Pictures(file_name=picture.file_name, title=picture.title, description=picture.description, owner_id=picture.owner_id)
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture