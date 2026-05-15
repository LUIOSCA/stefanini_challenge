from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: RoleEnum = RoleEnum.user
    active: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "luis hernando osorio castañeda",
                    "email": "luisosoriocastaeda@gmail.com",
                    "first_name": "Luis",
                    "last_name": "Osorio",
                    "role": "admin",
                    "active": True,
                }
            ]
        }
    )

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[RoleEnum] = None
    active: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    detail: str