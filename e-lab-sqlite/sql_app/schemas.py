from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class Temperature(BaseModel)    :
    id: int
    value: dict = None
    time: datetime = None 
    # value: Optional[Union[str, int]] = None

    class Config:
        # arbitrary_types_allowed = True
        orm_mode = True 