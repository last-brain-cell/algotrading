from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from beanie import Document


class Role(Enum):
    participant = "participant"
    admin = "admin"


class User(Document):
    team_name: str
    email: EmailStr
    password: str
    role: Role

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Team Algotrading",
                "email": "johndoe@example.com",
                "password": "password",
                "role": "participant",
            }
        }


class UserSignup(BaseModel):
    team_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    confirm_password: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "team_name": "Team Awesome",
                "email": "johndoe@example.com",
                "password": "password",
                "confirm_password": "password",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"email": "johndoe@example.com", "password": "password"}
        }
