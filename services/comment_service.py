from api.comments import CommentsAPI
from models.requests.comment import CreateCommentRequest
from models.responses.comment import CommentResponse


class CommentService:
    def __init__(self, comments_api: CommentsAPI):
        self.comments_api = comments_api

    def get_comments(self, page: int | None = None, per_page: int | None = None) -> list[CommentResponse]:
        response = self.comments_api.get_comments(page=page, per_page=per_page)
        response.raise_for_status()
        return [CommentResponse.model_validate(c) for c in response.json()]

    def get_post_comments(self, post_id: int) -> list[CommentResponse]:
        response = self.comments_api.get_post_comments(post_id)
        response.raise_for_status()
        return [CommentResponse.model_validate(c) for c in response.json()]

    def get_comment(self, comment_id: int) -> CommentResponse:
        response = self.comments_api.get_comment(comment_id)
        response.raise_for_status()
        return CommentResponse.model_validate(response.json())

    def create_comment(self, payload: CreateCommentRequest) -> CommentResponse:
        response = self.comments_api.create_comment(payload.model_dump(mode="json"))
        response.raise_for_status()
        return CommentResponse.model_validate(response.json())

    def delete_comment(self, comment_id: int) -> None:
        response = self.comments_api.delete_comment(comment_id)
        response.raise_for_status()
