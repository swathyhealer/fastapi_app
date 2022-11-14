

from fastapi import Depends
from sqlalchemy.orm import Session


from helpers.depends import DependencyFunc
from db_op import user as db_user_op

from helpers.db_based_user_input_validator import Customvalidator
from fastapi import APIRouter
from models import admin as admin_model
from schemas import user as user_schema
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={400: {"description": "email already exists"}},
)


@router.post("/user/create", response_model=user_schema.UserOut)
async def create_user(*, admin: admin_model.Admin = Depends(DependencyFunc.get_admin), user: user_schema.UserIn, db: Session = Depends(DependencyFunc.get_db)):
    Customvalidator.email_already_exists(db=db, email=user.email)
    return db_user_op.create_user(db=db, user=user, admin_id=admin.admin_id)
