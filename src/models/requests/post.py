from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    user_id: int
    title: str
    body: str


class UpdatePostRequest(BaseModel):
    title: str | None = None
    body: str | None = None
