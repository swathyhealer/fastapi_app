
from sqlalchemy.orm import Session

import uuid
from typing import Union


from models import user as user_model
from models import book as book_model
from schemas import book as book_schema


def add_book(db: Session, book: book_schema.BookIn, user: user_model.User):

    book_db = book_model.Book(id=str(uuid.uuid4()),
                              name=book.name, owned_by=user.user_id)
    db.add(book_db)
    db.commit()
    db.refresh(book_db)
    return book_db


def get_books(db: Session, user: user_model.User):
    book_list = db.query(book_model.Book).filter(
        book_model.Book.owned_by == user.user_id)
    return book_list


def get_book(db: Session, book_id: str) -> Union[None, book_model.Book]:
    book = db.query(book_model.Book).filter(
        book_model.Book.id == book_id).first()
    return book


def delete_book(db: Session, user: user_model.User, book_id: str):
    db.query(book_model.Book).filter(book_model.Book.id == book_id).delete()
    # db.delete(book)
    db.commit()


def update_book_name(db: Session, user: user_model.User, book_id: str, new_name: str):
    book: book_model.Book = db.query(book_model.Book).filter(
        book_model.Book.id == book_id).first()
    book.name = new_name
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
