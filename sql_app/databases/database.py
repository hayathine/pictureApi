from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os
from models.models import Base


# DB情報
load_dotenv('.env')
user_name = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database_name = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8" % (
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

class Access_DB:
    @staticmethod
    def get_db():
        db = sessionLocal()
        try:
            yield db
        finally:
            db.close()