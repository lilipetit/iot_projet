from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from json import JSONEncoder

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, server_default="true", nullable=False)
    is_cheater = Column(Boolean, default=False, server_default="false", nullable=False)

    image = Column(String, nullable=True)

    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("User", back_populates="role")
