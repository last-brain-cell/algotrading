from pydantic import BaseModel, Field, EmailStr
from beanie import Document


class User(Document):
    team_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
