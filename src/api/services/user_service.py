from src.api.clients.users import UsersAPI
from src.models.requests.user import CreateUserRequest, UpdateUserRequest
from src.models.responses.common import PaginationMeta
from src.models.responses.user import UserResponse


class UserService:
    """Разбирает ответы user API в модели UserResponse."""

    def __init__(self, users_api: UsersAPI):
        self.users_api = users_api

    def get_users(self, page: int | None = None, per_page: int | None = None) -> list[UserResponse]:
        """Возвращает список пользователей постранично и валидирует их в модели UserResponse."""
        response = self.users_api.get_users(page=page, per_page=per_page)
        response.raise_for_status()
        return [UserResponse.model_validate(u) for u in response.json()]

    def get_page(
        self, page: int | None = None, per_page: int | None = None
    ) -> tuple[list[UserResponse], PaginationMeta]:
        """Возвращает страницу пользователей вместе с метаданными пагинации из заголовков ответа."""
        response = self.users_api.get_users(page=page, per_page=per_page)
        response.raise_for_status()
        users = [UserResponse.model_validate(u) for u in response.json()]
        meta = PaginationMeta(
            total=int(response.headers.get("X-Pagination-Total", 0)),
            pages=int(response.headers.get("X-Pagination-Pages", 1)),
            page=int(response.headers.get("X-Pagination-Page", 1)),
            limit=int(response.headers.get("X-Pagination-Limit", 10)),
        )
        return users, meta

    def get_user(self, user_id: int) -> UserResponse:
        """Возвращает пользователя по id и валидирует его в модель UserResponse."""
        response = self.users_api.get_user(user_id)
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    def create_user(self, payload: CreateUserRequest) -> UserResponse:
        """Создаёт пользователя и валидирует ответ в модель UserResponse."""
        response = self.users_api.create_user(payload.model_dump(mode="json"))
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    def update_user(self, user_id: int, payload: UpdateUserRequest) -> UserResponse:
        """Обновляет пользователя и валидирует ответ в модель UserResponse."""
        response = self.users_api.update_user(user_id, payload.model_dump(exclude_none=True, mode="json"))
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    def delete_user(self, user_id: int) -> None:
        """Удаляет пользователя по id."""
        response = self.users_api.delete_user(user_id)
        response.raise_for_status()
