from sqlalchemy.orm import Session
from db_op import user as db_user_op
from fastapi import HTTPException


class Customvalidator:
    @staticmethod
    def email_already_exists(db: Session, email: str):
        user = db_user_op.get_user_using_email(db=db, email=email)
        if user is not None:

            raise HTTPException(
                status_code=400,
                detail="email already exists"

            )
