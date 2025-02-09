from collections.abc import Callable
from http import HTTPStatus
from typing import cast

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.user.get_all_users import GetAllUsersUsecase
from app.usecases.user.login_user import LoginUserUseCase
from app.usecases.user.register_user import RegisterUserUseCase
from domain.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    UserInvalidPasswordException,
    UserNotFoundException,
)
from infra.web.container import AppContainer
from infra.web.decorators.role_required import role_required
from infra.web.dtos.book_dtos import GetAllBooksQueryParams
from infra.web.dtos.generic import ClientErrorResponse, SuccessResponse
from infra.web.dtos.user_dtos import (
    GetAllUsersResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)

tag = Tag(name="Authentication", description="S'enregistrer et se connecter à l'API")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/auth",
    __name__,
    url_prefix="/auth",
    abp_tags=[tag],
    doc_ui=True,
)


@router.post(
    "/register",
    description="Permet de s'enregistrer dans la base de données de l'API",
    responses={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.CONFLICT: ClientErrorResponse,
    },
)
@inject
def register(
    body: RegisterRequest,
    use_case: RegisterUserUseCase = Provide[AppContainer.register_user_usecase],
) -> Response:
    try:
        use_case.execute(email=body.email, password=body.password)
        return SuccessResponse(
            code=HTTPStatus.CREATED, message="Utilisateur créé avec succès"
        ).to_response()

    except UserAlreadyExistsException as e:
        return ClientErrorResponse(
            code=HTTPStatus.CONFLICT, message=str(e)
        ).to_response()


@router.post(
    "/login",
    description="Permet de se connecter et de récuperer le token pour l'inserer dans votre agent GPT",
    responses={
        HTTPStatus.OK: LoginResponse,
        HTTPStatus.NOT_FOUND: ClientErrorResponse,
        HTTPStatus.UNAUTHORIZED: ClientErrorResponse,
    },
)
@inject
def login(
    body: LoginRequest,
    use_case: LoginUserUseCase = Provide[AppContainer.login_user_usecase],
) -> Response:
    try:
        token = use_case.execute(email=body.email, password=body.password)
        return LoginResponse(access_token=token).to_response()

    except UserNotFoundException as e:
        return ClientErrorResponse(
            code=HTTPStatus.NOT_FOUND, message=str(e)
        ).to_response()

    except UserInvalidPasswordException as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNAUTHORIZED, message=str(e)
        ).to_response()


@router.get(
    "get_all_users",
    description="Récupère la liste de tous les utilisateurs",
    security=security,
    responses={
        HTTPStatus.OK: GetAllUsersResponse,
        HTTPStatus.FORBIDDEN: ClientErrorResponse,
    },
)
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required("admin"))
@inject
def get_all_users(
    query: GetAllBooksQueryParams,
    use_case: GetAllUsersUsecase = Provide[AppContainer.get_all_users_usecase],
) -> Response:
    # TODO : try except
    users = use_case.execute(limit=query.limit)

    users_to = [UserResponse.model_validate(user.model_dump()) for user in users]

    response = GetAllUsersResponse(users=users_to)
    return response.to_response()
