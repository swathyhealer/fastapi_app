from sqlalchemy.orm import Session
import database_operations
from fastapi import HTTPException


class Customvalidator:
    @staticmethod
    def email_already_exists(db: Session, email: str):
        user = database_operations.get_user_using_email(db=db, email=email)
        if user is not None:

            raise HTTPException(
                status_code=400,
                detail="email already exists"

            )
