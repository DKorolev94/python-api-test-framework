from pydantic import BaseModel, EmailStr


class CreateCommentRequest(BaseModel):
    post_id: int
    name: str
    email: EmailStr
    body: str
