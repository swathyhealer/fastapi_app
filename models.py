from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


from database import Base


class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String)
    hashed_password = Column(String)
    users = relationship("User", back_populates="responsibility")


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String)
    hashed_password = Column(String)
    created_by = Column(String, ForeignKey("admins.admin_id"))

    responsibility = relationship("Admin", back_populates="users")

    owned = relationship("Book", back_populates="responsibility")


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String)
    owned_by = Column(String, ForeignKey("users.user_id"))
    responsibility = relationship("User", back_populates="owned")
