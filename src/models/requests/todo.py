from typing import Literal

from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    user_id: int
    title: str
    due_on: str  # ISO 8601 datetime
    status: Literal["pending", "completed"] = "pending"


class UpdateTodoRequest(BaseModel):
    title: str | None = None
    due_on: str | None = None
    status: Literal["pending", "completed"] | None = None
