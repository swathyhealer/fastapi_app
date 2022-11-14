
from typing import List, Union
import database_operations
from fastapi.testclient import TestClient

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter


import schemas

from fastapi.security import OAuth2PasswordRequestForm
from helpers.depends import DependencyFunc


router = APIRouter()


@router.post("/login", response_model=schemas.AccessToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(DependencyFunc.get_db)):
    # to catch the email validation error
    try:
        log_cred = schemas.Logincred(
            id=form_data.username, password=str(form_data.password))
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail={"email validation": str(e)},

        )
    accesstoken = database_operations.authenticate(db=db, log_cred=log_cred)
    return accesstoken
