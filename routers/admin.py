import database_operations


from fastapi import Depends
from sqlalchemy.orm import Session


import models
import schemas


from helpers.depends import DependencyFunc


from helpers.db_based_user_input_validator import Customvalidator
from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={400: {"description": "email already exists"}},
)


@router.post("/user/create", response_model=schemas.UserOut)
async def create_user(*, admin: models.Admin = Depends(DependencyFunc.get_admin), user: schemas.UserIn, db: Session = Depends(DependencyFunc.get_db)):
    Customvalidator.email_already_exists(db=db, email=user.email)
    return database_operations.create_user(db=db, user=user, admin_id=admin.admin_id)
