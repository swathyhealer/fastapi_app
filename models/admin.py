from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base


class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(String, primary_key=True, index=True, unique=True)
    email = Column(String)
    hashed_password = Column(String)
    users = relationship("User", back_populates="responsibility")
