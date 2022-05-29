from datetime import date, datetime
from secrets import token_bytes
from typing import Optional, Literal
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr
# from pydantic.types import conint

# user
class UserBase(BaseModel):
    user_name : str
    email : EmailStr
    password : str

class CreateUser(UserBase):
    pass

class UserResponse(BaseModel):
    user_id : int
    user_name : str
    email : EmailStr
    created_at = datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    user_name : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# response todo
class TodoBase(BaseModel):
    todo_text : str
    todo_description : str
    todo_complete_by : date

class CreateTodo(TodoBase):
    completed : bool

class TodoResponse(TodoBase):
    todo_id : int
    user_id : int
    todo_text : str
    todo_description : str
    todo_complete_by : date
    completed : bool
    is_active : bool
    created_at : datetime

    class Config:
        orm_mode = True

