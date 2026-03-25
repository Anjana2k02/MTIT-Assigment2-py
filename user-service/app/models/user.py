from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phoneNo = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=False)

    role = relationship("Role", back_populates="users")
