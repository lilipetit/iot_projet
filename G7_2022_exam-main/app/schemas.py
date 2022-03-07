from typing import Optional

from pydantic import BaseModel


class Error(BaseModel):
    message: str


class Role(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_active: bool
    is_cheater: bool
    role_id: int

    class Config:
        orm_mode = True


class User(BaseUser):
    image: str

    class Config:
        orm_mode = True


class JWT(BaseModel):
    access_token: str
