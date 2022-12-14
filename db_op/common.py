from datetime import timedelta
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from helpers.common import CommonFunction
from helpers.hash import HashFunctions
from models import admin as admin_model
from models import user as user_model
from schemas import common as common_schema


def authenticate(db: Session, log_cred: common_schema.Logincred):
    admin: Union[admin_model.Admin, None] = (
        db.query(admin_model.Admin)
        .filter(admin_model.Admin.email == log_cred.id)
        .first()
    )
    user: Union[user_model.User, None] = (
        db.query(user_model.User).filter(user_model.User.email == log_cred.id).first()
    )

    authentication_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if admin:
        hashed_password = admin.hashed_password
        id = admin.email

    elif user:
        hashed_password = user.hashed_password
        id = user.email
    if admin == None and user == None:
        raise authentication_error
    else:
        # password verification
        if not HashFunctions.bcrypt_hash_checker(
            password=log_cred.password, hashed_password=hashed_password
        ):
            raise authentication_error
        jwt_token_config = CommonFunction.get_jwt_config()
        access_token_expires = timedelta(
            minutes=jwt_token_config.access_token_expire_minutes
        )
        access_token = CommonFunction.create_access_token(
            data={"sub": id},
            expires_delta=access_token_expires,
            secret_key=jwt_token_config.secret_key,
            algorithm=jwt_token_config.algorithm,
        )
        return common_schema.AccessToken(access_token=access_token, token_type="bearer")


# def get_general_user(db: Session, tokendata: schemas.TokenData) -> Union[schemas.GeneralUser, None]:
#     admin: Union[models.Admin, None] = db.query(models.Admin).filter(
#         models.Admin.admin_id == tokendata.username).first()
#     if admin:
#         return schemas.GeneralUser(is_admin=True, admin=admin)
#     user: Union[models.User, None] = db.query(models.User).filter(
#         models.User.user_id == tokendata.username).first()

#     if user:
#         return schemas.GeneralUser(user=user)
#     else:
#         return None
