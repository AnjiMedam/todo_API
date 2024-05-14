
from pydantic import BaseModel 
from typing import Union,List
from datetime import date

class TaskBase(BaseModel):
    title: str
    description:str
    due_date:date
    status: str

class Task(TaskBase):
    id:int 
    class Config():
        from_attributes = True


class UserBase(BaseModel):
    email:str
    
class User(BaseModel):
    username:str 
    password:str
    email:str


class Userwithoutpass(BaseModel):
    id:int
    username:str
    email:str

class ShowUser(BaseModel):
    username:str
    email:str
    tasks : List[Task] =[]

    class Config():
        from_attributes = True


class ShowUserWithId(ShowUser):
    id:int
    class Config():
        from_attributes = True
        
class ShowUserwithDeleteFlag(ShowUserWithId):
    role:str
    is_delete:bool
    class Config():
        from_attributes = True

class ShowtaskUser(BaseModel):
    username:str
    email:str

class ShowTask(BaseModel):
    title: str
    description:str
    due_date:date
    status: str
    creator: ShowtaskUser

    class Config():
        from_attributes = True

class Login(BaseModel):
    username:str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
