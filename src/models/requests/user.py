from typing import Literal

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    gender: Literal["male", "female"]
    status: Literal["active", "inactive"] = "active"


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    gender: Literal["male", "female"] | None = None
    status: Literal["active", "inactive"] | None = None
