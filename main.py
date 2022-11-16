


from fastapi import FastAPI

import setup


from database import engine

from routers import admin, user
from routers import common as common_router

from database import Base
Base.metadata.create_all(bind=engine)
setup.create_admins()
app = FastAPI()

# client = TestClient(app)
app.include_router(common_router.router)
app.include_router(admin.router)

app.include_router(user.router)
