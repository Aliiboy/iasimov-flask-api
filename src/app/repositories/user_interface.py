from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.user.user_entity import UserEntity


class UserRepositoryInterface(ABC):
    # write
    @abstractmethod
    def sign_up_user(self, schema: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: UUID) -> None:
        pass

    # read
    @abstractmethod
    def login_user(self, schema: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_all_users_with_limit(self, limit: int) -> list[UserEntity]:
        pass
