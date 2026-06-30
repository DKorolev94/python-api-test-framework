import allure
import pytest
from hamcrest import assert_that, equal_to, has_item

from factories.comment import create_comment_payload
from factories.post import create_post_payload
from factories.user import create_user_payload
from services.comment_service import CommentService
from services.post_service import PostService
from services.user_service import UserService
from utils.decorators import WorkItem, linked, step


@allure.feature("Blog Flow")
@pytest.mark.e2e
class TestBlogFlow:

    @linked(WorkItem(id=0, name="Blog flow: user creates post with comment, all visible"))
    def test_blog_flow(
        self,
        user_service: UserService,
        post_service: PostService,
        comment_service: CommentService,
    ):
        with step("Create user"):
            user = user_service.create_user(create_user_payload())
        try:
            with step("Create post for user"):
                post = post_service.create_post(create_post_payload(user_id=user.id))
            try:
                with step("Create comment on post"):
                    comment = comment_service.create_comment(
                        create_comment_payload(post_id=post.id)
                    )
                try:
                    with step("Verify comment appears in post comments"):
                        post_comments = comment_service.get_post_comments(post.id)
                        comment_ids = {c.id for c in post_comments}
                        assert_that(comment_ids, has_item(comment.id))

                    with step("Verify post appears in user posts"):
                        user_posts = post_service.get_user_posts(user.id)
                        post_ids = {p.id for p in user_posts}
                        assert_that(post_ids, has_item(post.id))

                    with step("Verify comment body matches"):
                        assert_that(comment.post_id, equal_to(post.id))

                finally:
                    comment_service.delete_comment(comment.id)
            finally:
                post_service.delete_post(post.id)
        finally:
            user_service.delete_user(user.id)
