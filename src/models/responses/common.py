from pydantic import BaseModel


class PaginationMeta(BaseModel):
    total: int
    pages: int
    page: int
    limit: int


class GoRestError(BaseModel):
    message: str


class ValidationErrorItem(BaseModel):
    field: str
    message: str
