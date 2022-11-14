from pydantic import BaseModel, EmailStr
import models
from typing import Union


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


class Logincred(BaseModel):
    id: EmailStr
    password: str

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: EmailStr


class BookIn(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BookOut(BookIn):
    id: str
    status: str


class BookDetails(BaseModel):
    id: str
    name: str


class JwtConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class GeneralUser(BaseModel):
    is_admin: bool = False
    user: Union[None, models.User] = None
    admin: Union[None, models.Admin] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
