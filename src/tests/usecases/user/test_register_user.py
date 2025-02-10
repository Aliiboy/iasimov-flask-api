import unittest
from typing import cast
from unittest.mock import MagicMock

from app.repositories.user_interface import UserRepositoryInterface
from app.usecases.user.register_user import RegisterUserUseCase
from domain.entities.user.user_entity import User
from infra.services.bcrypt_password_hasher import BcryptPasswordHasher


class RegisterUserUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: UserRepositoryInterface = MagicMock(
            spec=UserRepositoryInterface
        )
        self.mock_password_hasher = BcryptPasswordHasher()
        self.use_case = RegisterUserUseCase(
            repository=self.mock_user_repository,
        )

    def test_create_user_success(self) -> None:
        email: str = "test@example.com"
        password: str = "Password_1234!"
        cast(MagicMock, self.mock_user_repository.get_user_by_email).return_value = None

        new_user: User = self.use_case.execute(email=email, password=password)

        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.email, email)
        cast(MagicMock, self.mock_user_repository.add_user).assert_called_once_with(
            new_user
        )
