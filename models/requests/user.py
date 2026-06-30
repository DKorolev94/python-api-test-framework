from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str  # "male" | "female"
    status: str = "active"  # "active" | "inactive"


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    gender: str | None = None
    status: str | None = None
