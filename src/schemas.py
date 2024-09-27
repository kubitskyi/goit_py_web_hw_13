from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class ContactSchema(BaseModel):
    # id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[date]
    additional_info: Optional[str]

    class Config:
        from_attributes = True


class ContactBirthday(BaseModel):
    id: int
    first_name: str
    last_name: str
    birthday: date
    

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr
