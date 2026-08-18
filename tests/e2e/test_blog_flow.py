import allure
import pytest

from src.api.services.comment_service import CommentService
from src.api.services.post_service import PostService
from src.assertions.common_assertions import assert_equal, assert_in
from src.models.responses.comment import CommentResponse
from src.models.responses.post import PostResponse
from src.models.responses.user import UserResponse


@allure.epic("GoRest API")
@allure.feature("Сквозные сценарии")
@allure.story("Блог")
@pytest.mark.e2e
class TestBlogFlow:
    """Полный сценарий: пользователь, пост и комментарий к нему."""

    @allure.title("Успешный сценарий создания поста с комментарием")
    def test_blog_flow(
        self,
        post_service: PostService,
        comment_service: CommentService,
        created_user: UserResponse,
        created_post: PostResponse,
        created_comment: CommentResponse,
    ):
        """Пользователь создаёт пост с комментарием, всё видно через API."""
        post_comments = comment_service.get_post_comments(created_post.id)
        assert_in(
            created_comment.id,
            {c.id for c in post_comments},
            "комментарий присутствует среди комментариев поста",
        )

        user_posts = post_service.get_user_posts(created_user.id)
        assert_in(created_post.id, {p.id for p in user_posts}, "пост присутствует в постах пользователя")

        assert_equal(created_comment.post_id, created_post.id, "post_id комментария совпадает с постом")
