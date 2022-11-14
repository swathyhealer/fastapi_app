

import database_operations


from fastapi import Depends
from sqlalchemy.orm import Session


import models
import schemas

from helpers.depends import DependencyFunc


from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"],

)


@router.post("/book/add", response_model=schemas.BookOut)
async def add_book(*, user: models.User = Depends(DependencyFunc.get_current_user), db: Session = Depends(DependencyFunc.get_db), book: schemas.BookIn):

    book_db = database_operations.add_book(book=book, user=user, db=db)
    book_out = schemas.BookOut(
        name=book_db.name, id=book_db.id, status="added")
    return book_out


@router.get("/book/list", response_model=list)
async def list_book(*, user: models.User = Depends(DependencyFunc.get_current_user), db: Session = Depends(DependencyFunc.get_db)):

    book_db_list = database_operations.get_books(db=db, user=user).all()

    return book_db_list


@router.delete("/book/{book_id}", response_model=dict)
async def delete_book(*, user: models.User = Depends(DependencyFunc.get_owner), db: Session = Depends(DependencyFunc.get_db), book_id: str):

    database_operations.delete_book(db=db, user=user, book_id=book_id)

    return {"data": "deleted book having id "+book_id}


@router.put("/book/{book_id}", response_model=dict)
async def update_book(*, user: models.User = Depends(DependencyFunc.get_owner), db: Session = Depends(DependencyFunc.get_db), book_id: str, new_name: str):

    book = database_operations.update_book_name(
        db=db, user=user, book_id=book_id, new_name=new_name)

    return {"data": "updated book having id "+book.id}
