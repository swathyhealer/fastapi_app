from fastapi import FastAPI

import setup
from database import Base, engine
from routers import admin, book
from routers import login as common_router

Base.metadata.create_all(bind=engine)
setup.create_admins()
app = FastAPI()


app.include_router(common_router.router)
app.include_router(admin.router)

app.include_router(book.router)
