from typing import Optional
from pydantic import BaseModel,  constr


class UserBase(BaseModel):
    name: str
    username: str
    roll: str
    password: constr(min_length=4)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserCurrent(UserBase):
    id: int
    status: bool
    user_status:bool
