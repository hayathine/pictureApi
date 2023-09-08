from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base

# DB情報
user_name = "ryo"
password = "password"
host = "localhost"
database_name = "picture_db"

SQLALCHEMY_DATABASE_URL = "mysql://%s:%s@%s/%s?charset=utf8" % (
    user_name,
    password,
    host,
    database_name,
)

# DB接続
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # encoding="utf-8",
    echo=True
    )

# セッション作成
sessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
# DBが存在しない場合は作成する
if  not database_exists(engine.url):
    create_database(engine.url)
# テーブル作成
Base.metadata.create_all(bind=engine)

# DB接続用のセッションクラス、インスタンスが作成されるとDBに接続される
Base.query = sessionLocal.query_property()
