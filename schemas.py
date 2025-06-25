from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Users(BaseModel):
    user_id: int
    username: str
    email: str


class ReadUsers(BaseModel):
    user_id: int
    username: str
    email: str
    class Config:
        from_attributes = True


class UserRoles(BaseModel):
    user_id: int
    role_id: int
    assigned_at: datetime.time


class ReadUserRoles(BaseModel):
    user_id: int
    role_id: int
    assigned_at: datetime.time
    class Config:
        from_attributes = True


class Roles(BaseModel):
    role_id: int
    role_name: str


class ReadRoles(BaseModel):
    role_id: int
    role_name: str
    class Config:
        from_attributes = True




class PostUserRoles(BaseModel):
    user_id: int = Field(...)
    role_id: int = Field(...)
    assigned_at: Any = Field(...)

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    user_id: int = Field(...)
    username: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



class PostRoles(BaseModel):
    role_id: int = Field(...)
    role_name: str = Field(..., max_length=100)

    class Config:
        from_attributes = True

