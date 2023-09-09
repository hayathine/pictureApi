# pydanticのためのスキーマを定義するファイル

from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str

class PictureBase(BaseModel):
    file_name: str
    title: str
    owner_id: int

class PictureCreate(PictureBase):
    description: Optional[str] = None

class Picture(PictureBase):
    picture_id: int

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True