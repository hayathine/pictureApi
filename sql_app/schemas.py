# pydanticのためのスキーマを定義するファイル

from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class PictureBase(BaseModel):
    file_name: str
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True