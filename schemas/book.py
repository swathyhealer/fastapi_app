from pydantic import BaseModel


class BookIn(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BookOut(BookIn):
    id: str
    status: str


class BookDetails(BaseModel):
    id: str
    name: str
