from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db_op import common as db_common_op
from helpers import depends
from schemas import common as common_schema

router = APIRouter()


@router.post("/login", response_model=common_schema.AccessToken)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(depends.get_db),
):
    # to catch the email validation error
    try:
        log_cred = common_schema.Logincred(
            id=form_data.username, password=str(form_data.password)
        )
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail={"email validation": str(e)},
        )
    accesstoken = db_common_op.authenticate(db=db, log_cred=log_cred)
    return accesstoken
