from http import HTTPStatus

import allure
import pytest
from hamcrest import assert_that, equal_to, has_item, instance_of, not_, empty

from api.comments import CommentsAPI
from factories.comment import create_comment_payload, create_comment_payload_dict
from models.responses.comment import CommentResponse
from models.responses.post import PostResponse
from services.comment_service import CommentService
from utils.decorators import WorkItem, linked, step


@allure.feature("Comments")
@pytest.mark.contract
class TestCommentsPermissions:

    @linked(WorkItem(id=0, name="Comments: create without token returns 401"))
    def test_create_comment_no_token(self, comments_api_no_auth: CommentsAPI, created_post: PostResponse):
        with step("POST /comments without token"):
            response = comments_api_no_auth.create_comment(
                create_comment_payload_dict(post_id=created_post.id)
            )
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))


@allure.feature("Comments")
@pytest.mark.contract
class TestCommentsSchema:

    @linked(WorkItem(id=0, name="Comments: list returns 200 with valid schema"))
    def test_get_comments_schema(self, comments_api_no_auth: CommentsAPI):
        with step("GET /comments"):
            response = comments_api_no_auth.get_comments()
        with step("Response: 200, items match CommentResponse schema"):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))
            comments = [CommentResponse.model_validate(c) for c in response.json()]
            assert_that(comments, not_(empty()))

    @linked(WorkItem(id=0, name="Comments: get non-existent returns 404"))
    def test_get_comment_not_found(self, comments_api_no_auth: CommentsAPI):
        with step("GET /comments/0"):
            response = comments_api_no_auth.get_comment(0)
        with step("Response: 404 Not Found"):
            assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))

    @linked(WorkItem(id=0, name="Comments: create with invalid email returns 422"))
    def test_create_comment_invalid_email(self, comments_api: CommentsAPI, created_post: PostResponse):
        with step("POST /comments with invalid email"):
            response = comments_api.create_comment(
                create_comment_payload_dict(post_id=created_post.id, email="bad-email")
            )
        with step("Response: 422 Unprocessable Entity"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))


@allure.feature("Comments")
@pytest.mark.integration
class TestCommentsCreate:

    @linked(WorkItem(id=0, name="Comments: create returns valid comment"))
    def test_create_comment_success(
        self, comment_service: CommentService, created_post: PostResponse
    ):
        payload = create_comment_payload(post_id=created_post.id)
        with step("POST /comments"):
            comment = comment_service.create_comment(payload)
        with step("Comment created with correct post_id"):
            assert_that(comment.id, instance_of(int))
            assert_that(comment.post_id, equal_to(created_post.id))
        with step("Cleanup"):
            comment_service.delete_comment(comment.id)

    @linked(WorkItem(id=0, name="Comments: created comment appears in post comments"))
    def test_comment_in_post_comments(
        self, comment_service: CommentService, created_post: PostResponse
    ):
        payload = create_comment_payload(post_id=created_post.id)
        comment = comment_service.create_comment(payload)
        try:
            with step("GET /posts/{id}/comments"):
                post_comments = comment_service.get_post_comments(created_post.id)
            with step("Comment id present in post comments"):
                comment_ids = {c.id for c in post_comments}
                assert_that(comment_ids, has_item(comment.id))
        finally:
            comment_service.delete_comment(comment.id)
