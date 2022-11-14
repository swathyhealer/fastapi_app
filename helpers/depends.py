from database import SessionLocal
from fastapi import HTTPException, Depends, status

from helpers.common import CommonFunction
from jose import JWTError
import schemas
from sqlalchemy.orm import Session
from database_operations import get_user
from authentication_scheme import auth2_scheme
import database_operations


class DependencyFunc:

    async def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def get_current_user(token: str = Depends(auth2_scheme), db: Session = Depends(get_db)):

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
            token_data = schemas.TokenData(username=username)
        except JWTError:
            raise credentials_exception
        general_user = get_user(db=db, tokendata=token_data)
        if general_user is None:
            raise credentials_exception
        else:
            return general_user
            # if general_user.is_admin==True:
            #     return general_user.admin
            # else:
            #     return general_user.user

    async def get_owner(book_id: str, user: schemas.models.User = Depends(get_current_user), db: Session = Depends(get_db)):
        book: schemas.models.Book = database_operations.get_book(
            db=db, book_id=book_id)
        if book == None:
            raise HTTPException(status_code=400, detail="invalid book id")
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
            token_data = schemas.TokenData(username=username)
        except JWTError:
            raise credentials_exception
        admin = database_operations.get_admin(db=db, tokendata=token_data)
        if admin is None:
            raise credentials_exception
        else:
            return admin
