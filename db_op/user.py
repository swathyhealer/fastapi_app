

from sqlalchemy.orm import Session
from helpers.hash import HashFunctions
import uuid
from typing import Union


from models import user as user_model
from schemas import user as user_schema
from schemas import common as common_schema


def create_user(db: Session, user: user_schema.UserIn, admin_id: str):

    hashed_password = HashFunctions.bcrypt_hasher(password=user.password)
    user_id = str(uuid.uuid4())
    temp_dict = user.dict()
    temp_dict.pop("password")
    db_user = user_model.User(**temp_dict, user_id=user_id,
                              hashed_password=hashed_password, created_by=admin_id)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # NOTE: fastapi will ignore other keys (keys which are not in response)
    return db_user


def get_user(db: Session, tokendata: common_schema.TokenData) -> Union[user_model.User, None]:
    user: Union[user_model.User, None] = db.query(user_model.User).filter(
        user_model.User.email == tokendata.username).first()

    if user:
        return user
    else:
        return None


def get_user_using_email(db: Session, email: str):
    user: Union[user_model.User, None] = db.query(user_model.User).filter(
        user_model.User.email == email).first()

    if user:
        return user
    else:
        return None
