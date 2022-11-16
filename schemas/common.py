from typing import Union

from pydantic import BaseModel, EmailStr

from models import admin as admin_model
from models import user as user_model


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


class JwtConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class GeneralUser(BaseModel):
    is_admin: bool = False
    user: Union[None, user_model.User] = None
    admin: Union[None, admin_model.Admin] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
