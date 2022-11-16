from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String)
    owned_by = Column(String, ForeignKey("users.user_id"))
    responsibility = relationship("User", back_populates="owned")
