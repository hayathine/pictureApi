# pydanticのためのスキーマを定義するファイル

from typing import List, Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str

class PictureBase(BaseModel):
    file_name:str = Field( max_length=100)
    title:str = Field( max_length=100)
    owner_id:int = Field(gt=0)

class PictureCreate(PictureBase):
    description:str = Field(max_length=100)

class Picture(PictureBase):
    picture_id: int = Field(gt=0)
    # from_attributes = Trueを指定することで、モデルの属性をそのままスキーマにすることができる
    class ConfigDict:
        from_attributes = True

class UserCreate(UserBase):
    email: str
    password: str

class UserUpdate(UserBase):
    email: str
    password: str

class User(UserBase):
    user_id: int
    is_active: bool
    pictures: List[PictureBase] = []

    class ConfigDict:
        from_attributes = True