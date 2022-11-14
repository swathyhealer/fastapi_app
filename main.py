
from fastapi.testclient import TestClient

from fastapi import FastAPI

import setup
import models

from database import engine

from routers import admin, user
from routers import common as common_router


models.Base.metadata.create_all(bind=engine)
setup.create_admins()
app = FastAPI()

client = TestClient(app)
app.include_router(common_router.router)
app.include_router(admin.router)

app.include_router(user.router)
