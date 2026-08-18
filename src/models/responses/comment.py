from pydantic import BaseModel


class CommentResponse(BaseModel):
    id: int
    post_id: int
    name: str
    email: str
    body: str
