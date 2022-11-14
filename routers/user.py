

from db_op import book as db_book_op


from fastapi import Depends
from sqlalchemy.orm import Session


from helpers.depends import DependencyFunc
from models import user as user_model

from fastapi import APIRouter
from schemas import book as book_schema

router = APIRouter(
    prefix="/user",
    tags=["user"],

)


@router.post("/book/add", response_model=book_schema.BookOut)
async def add_book(*, user: user_model.User = Depends(DependencyFunc.get_current_user), db: Session = Depends(DependencyFunc.get_db), book: book_schema.BookIn):

    book_db = db_book_op.add_book(book=book, user=user, db=db)
    book_out = book_schema.BookOut(
        name=book_db.name, id=book_db.id, status="added")
    return book_out


@router.get("/book/list", response_model=list)
async def list_book(*, user: user_model.User = Depends(DependencyFunc.get_current_user), db: Session = Depends(DependencyFunc.get_db)):

    book_db_list = db_book_op.get_books(db=db, user=user).all()

    return book_db_list


@router.delete("/book/{book_id}", response_model=dict)
async def delete_book(*, user: user_model.User = Depends(DependencyFunc.get_owner), db: Session = Depends(DependencyFunc.get_db), book_id: str):

    db_book_op.delete_book(db=db, user=user, book_id=book_id)

    return {"data": "deleted book having id "+book_id}


@router.put("/book/{book_id}", response_model=dict)
async def update_book(*, user: user_model.User = Depends(DependencyFunc.get_owner), db: Session = Depends(DependencyFunc.get_db), book_id: str, new_name: str):

    book = db_book_op.update_book_name(
        db=db, user=user, book_id=book_id, new_name=new_name)

    return {"data": "updated book having id "+book.id}
