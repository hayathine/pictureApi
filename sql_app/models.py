from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name  = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    pictures = relationship("Pictures", back_populates="owner")

class Pictures(Base):
    __tablename__ = "pictures"
    picture_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String(255))
    title = Column(String(255), index=True)
    description = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("Users", back_populates="pictures")
