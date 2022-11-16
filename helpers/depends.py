from typing import Union

from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from authentication_scheme import auth2_scheme
from database import SessionLocal
from db_op import admin as db_admin_op
from db_op import book as db_book_op
from db_op import user as db_user_op
from helpers.common import CommonFunction
from models import book as book_model
from models import user as user_model
from schemas import common as common_schema


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(auth2_scheme), db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = CommonFunction.decode_token(token=token)
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = common_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    general_user = db_user_op.get_user(db=db, tokendata=token_data)
    if general_user is None:
        raise credentials_exception
    else:
        return general_user
        # if general_user.is_admin==True:
        #     return general_user.admin
        # else:
        #     return general_user.user


async def get_owner(
    book_id: str,
    user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    book = db_book_op.get_book(db=db, book_id=book_id)
    if book == None:
        raise HTTPException(status_code=400, detail="invalid book id")
    else:

        if book.owned_by != user.user_id:
            raise HTTPException(status_code=401, detail="permission denied")
        return user


async def get_admin(token: str = Depends(auth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = CommonFunction.decode_token(token=token)
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = common_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    admin = db_admin_op.get_admin(db=db, tokendata=token_data)
    if admin is None:
        raise credentials_exception
    else:
        return admin
