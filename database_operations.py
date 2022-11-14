import models
import schemas
from sqlalchemy.orm import Session
from helpers.hash import HashFunctions
import uuid
from typing import Union
from fastapi import HTTPException, status
from helpers.common import CommonFunction
from datetime import timedelta
from helpers.common import CommonFunction
from schemas import AccessToken


def create_user(db: Session, user: schemas.UserIn, admin_id: str):

    hashed_password = HashFunctions.bcrypt_hasher(password=user.password)
    user_id = str(uuid.uuid4())
    temp_dict = user.dict()
    temp_dict.pop("password")
    db_user = models.User(**temp_dict, user_id=user_id,
                          hashed_password=hashed_password, created_by=admin_id)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # NOTE: fastapi will ignore other keys (keys which are not in response)
    return db_user


def authenticate(db: Session, log_cred: schemas.Logincred):
    admin: Union[models.Admin, None] = db.query(models.Admin).filter(
        models.Admin.email == log_cred.id).first()
    user: Union[models.User, None] = db.query(models.User).filter(
        models.User.email == log_cred.id).first()
    active_person: Union[models.Admin, models.User, None] = None
    if admin:
        active_person = admin
        id = admin.email
    elif user:
        active_person = user
        id = user.email
    if active_person == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    else:

        jwt_token_config = CommonFunction.get_jwt_config()
        access_token_expires = timedelta(
            minutes=jwt_token_config.access_token_expire_minutes)
        access_token = CommonFunction.create_access_token(
            data={"sub": id}, expires_delta=access_token_expires, secret_key=jwt_token_config.secret_key, algorithm=jwt_token_config.algorithm)
        return AccessToken(access_token=access_token, token_type="bearer")


def get_general_user(db: Session, tokendata: schemas.TokenData) -> Union[schemas.GeneralUser, None]:
    admin: Union[models.Admin, None] = db.query(models.Admin).filter(
        models.Admin.admin_id == tokendata.username).first()
    if admin:
        return schemas.GeneralUser(is_admin=True, admin=admin)
    user: Union[models.User, None] = db.query(models.User).filter(
        models.User.user_id == tokendata.username).first()

    if user:
        return schemas.GeneralUser(user=user)
    else:
        return None


def get_user(db: Session, tokendata: schemas.TokenData) -> Union[models.User, None]:
    user: Union[models.User, None] = db.query(models.User).filter(
        models.User.email == tokendata.username).first()

    if user:
        return user
    else:
        return None


def get_user_using_email(db: Session, email: str):
    user: Union[models.User, None] = db.query(models.User).filter(
        models.User.email == email).first()

    if user:
        return user
    else:
        return None


def get_admin(db: Session, tokendata: schemas.TokenData) -> Union[models.Admin, None]:
    admin: Union[models.Admin, None] = db.query(models.Admin).filter(
        models.Admin.email == tokendata.username).first()

    if admin:
        return admin
    else:
        return None


def add_book(db: Session, book: schemas.BookIn, user: models.User):

    book_db = models.Book(id=str(uuid.uuid4()),
                          name=book.name, owned_by=user.user_id)
    db.add(book_db)
    db.commit()
    db.refresh(book_db)
    return book_db


def get_books(db: Session, user: models.User):
    book_list = db.query(models.Book).filter(
        models.Book.owned_by == user.user_id)
    return book_list


def get_book(db: Session, book_id: str) -> Union[None, models.Book]:
    book = db.query(models.Book).filter(
        models.Book.id == book_id).first()
    return book


def delete_book(db: Session, user: models.User, book_id: str):
    db.query(models.Book).filter(models.Book.id == book_id).delete()
    # db.delete(book)
    db.commit()


def update_book_name(db: Session, user: models.User, book_id: str, new_name: str):
    book: models.Book = db.query(models.Book).filter(
        models.Book.id == book_id).first()
    book.name = new_name
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
