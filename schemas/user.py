from typing import Union

from pydantic import BaseModel, EmailStr

from models import admin as admin_model
from models import user as user_model


class UserBase(BaseModel):

    email: EmailStr


class UserIn(UserBase):
    password: str


class UserDB(UserBase):
    user_id: str
    hashed_password: str
    created_by: str

    class Config:
        orm_mode = True


class UserOut(UserBase):
    user_id: str
    created_by: str

    class Config:
        orm_mode = True
