from http import HTTPStatus

import allure
import pytest
from hamcrest import assert_that, equal_to, has_item, instance_of, not_, empty

from api.posts import PostsAPI
from factories.post import create_post_payload, create_post_payload_dict, update_post_payload
from helpers.post_checks import all_posts_belong_to_user, post_ids
from models.responses.post import PostResponse
from models.responses.user import UserResponse
from services.post_service import PostService
from utils.decorators import WorkItem, linked, step


@allure.feature("Posts")
@pytest.mark.contract
class TestPostsPermissions:

    @linked(WorkItem(id=0, name="Posts: create without token returns 401"))
    def test_create_post_no_token(self, posts_api_no_auth: PostsAPI, created_user: UserResponse):
        with step("POST /posts without token"):
            response = posts_api_no_auth.create_post(create_post_payload_dict(user_id=created_user.id))
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))

    @linked(WorkItem(id=0, name="Posts: delete without token returns 401"))
    def test_delete_post_no_token(self, posts_api_no_auth: PostsAPI, created_post: PostResponse):
        with step("DELETE /posts/{id} without token"):
            response = posts_api_no_auth.delete_post(created_post.id)
        with step("Response: 401 Unauthorized"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))


@allure.feature("Posts")
@pytest.mark.contract
class TestPostsSchema:

    @linked(WorkItem(id=0, name="Posts: list returns 200 with valid schema"))
    def test_get_posts_schema(self, posts_api_no_auth: PostsAPI):
        with step("GET /posts"):
            response = posts_api_no_auth.get_posts()
        with step("Response: 200, items match PostResponse schema"):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))
            posts = [PostResponse.model_validate(p) for p in response.json()]
            assert_that(posts, not_(empty()))

    @linked(WorkItem(id=0, name="Posts: get non-existent returns 404"))
    def test_get_post_not_found(self, posts_api_no_auth: PostsAPI):
        with step("GET /posts/0"):
            response = posts_api_no_auth.get_post(0)
        with step("Response: 404 Not Found"):
            assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))

    @linked(WorkItem(id=0, name="Posts: create with missing title returns 422"))
    def test_create_post_missing_title(self, posts_api: PostsAPI, created_user: UserResponse):
        payload = create_post_payload_dict(user_id=created_user.id)
        payload.pop("title")
        with step("POST /posts without title"):
            response = posts_api.create_post(payload)
        with step("Response: 422 Unprocessable Entity"):
            assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))


@allure.feature("Posts")
@pytest.mark.integration
class TestPostsCreate:

    @linked(WorkItem(id=0, name="Posts: create returns valid post"))
    def test_create_post_success(self, created_post: PostResponse, created_user: UserResponse):
        with step("Post created via fixture"):
            assert_that(created_post.id, instance_of(int))
            assert_that(created_post.user_id, equal_to(created_user.id))
            assert_that(created_post.title, instance_of(str))

    @linked(WorkItem(id=0, name="Posts: created post readable by id"))
    def test_created_post_readable(self, post_service: PostService, created_post: PostResponse):
        with step("GET /posts/{id}"):
            fetched = post_service.get_post(created_post.id)
        with step("Fetched post matches created"):
            assert_that(fetched.id, equal_to(created_post.id))
            assert_that(fetched.title, equal_to(created_post.title))


@allure.feature("Posts")
@pytest.mark.integration
class TestPostsUpdate:

    @linked(WorkItem(id=0, name="Posts: update title"))
    def test_update_post_title(self, post_service: PostService, created_post: PostResponse):
        new_title = "Updated Post Title"
        with step(f"PATCH /posts/{created_post.id}"):
            updated = post_service.update_post(created_post.id, update_post_payload(title=new_title))
        with step("Title updated, id unchanged"):
            assert_that(updated.title, equal_to(new_title))
            assert_that(updated.id, equal_to(created_post.id))


@allure.feature("Posts")
@pytest.mark.integration
class TestPostsByUser:

    @linked(WorkItem(id=0, name="Posts: user posts all belong to user"))
    def test_user_posts_belong_to_user(
        self, post_service: PostService, created_user: UserResponse, created_post: PostResponse
    ):
        with step("GET /users/{id}/posts"):
            posts = post_service.get_user_posts(created_user.id)
        with step("All posts have correct user_id"):
            assert_that(all_posts_belong_to_user(posts, created_user.id), equal_to(True))
            assert_that(post_ids(posts), has_item(created_post.id))
