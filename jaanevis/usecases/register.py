import secrets
from datetime import datetime, timedelta

from jaanevis.domain import user as u
from jaanevis.repository.base import Repository
from jaanevis.requests.register_request import RegisterRequest
from jaanevis.responses import (
    ResponseFailure,
    ResponseObject,
    ResponseSuccess,
    StatusCode,
)
from jaanevis.utils import event, security


class RegisterUseCase:
    """usecase for user registration"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: RegisterRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)

        try:
            user = self.repo.get_user_by_username(username=request.username)
            if user:
                return ResponseFailure.build_resource_error(
                    _("User with this username already exists"),
                    code=StatusCode.user_exists,
                )
            user = self.repo.get_user_by_email(email=request.email)
            if user:
                return ResponseFailure.build_resource_error(
                    _("User with this email already exists"),
                    code=StatusCode.user_exists,
                )
            hashed_password = security.hash_password(request.password)
            created_user = self.repo.create_user(
                email=request.email,
                username=request.username,
                password=hashed_password,
            )

            activation_token = secrets.token_urlsafe(40)
            expire_time = (datetime.now() + timedelta(days=2)).timestamp()
            self.repo.create_session(
                session_id=activation_token,
                email=request.email,
                username=request.username,
                expire_time=expire_time,
            )

            event.post_event(
                "user_registered",
                {
                    "email": request.email,
                    "username": request.username,
                    "activation_token": activation_token,
                },
            )
            new_user = u.UserRead(
                username=created_user.username,
                is_active=created_user.is_active,
            )

            return ResponseSuccess(new_user)
        except Exception as exc:
            self.repo.delete_user(username=request.email)
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
