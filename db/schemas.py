from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemUpdate(ItemBase):
    title: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

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

class UpdateUserSchema(UserBase):
    email: Optional[str] = ""
    is_active: Optional[bool] = False
    
    
class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True