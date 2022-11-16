from fastapi import FastAPI

import setup
from database import Base, engine
from routers import admin
from routers import common as common_router
from routers import user

Base.metadata.create_all(bind=engine)
setup.create_admins()
app = FastAPI()

# client = TestClient(app)
app.include_router(common_router.router)
app.include_router(admin.router)

app.include_router(user.router)
