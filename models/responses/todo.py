from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    due_on: str | None = None
    status: str
