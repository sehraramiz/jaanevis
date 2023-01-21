import uuid
from datetime import datetime, timedelta
from typing import Protocol

from jaanevis.domain import user as u
from jaanevis.repository.base import Repository
from jaanevis.requests.register_request import RegisterRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess
from jaanevis.utils import security


class EmailHandler(Protocol):
    def send_email(email_to: str, text: str, subject: str) -> None:
        ...


class RegisterUseCase:
    """usecase for user registration"""

    def __init__(self, repo: Repository, email_handler: EmailHandler) -> None:
        self.repo = repo
        self.email_handler = email_handler

    def execute(self, request: RegisterRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)
        user = self.repo.get_user_by_username(username=request.email)
        if user:
            return ResponseFailure.build_resource_error(
                "User with this email already exists"
            )
        hashed_password = security.hash_password(request.password)
        created_user = self.repo.create_user(
            username=request.email, password=hashed_password
        )

        hashed_session = security.hash_password(uuid.uuid4().hex)
        expire_time = (datetime.now() + timedelta(days=2)).timestamp()
        self.repo.create_session(
            session_id=hashed_session,
            username=request.email,
            expire_time=expire_time,
        )

        self.email_handler.send_email()
        new_user = u.UserRead(
            username=created_user.username, is_active=created_user.is_active
        )

        return ResponseSuccess(new_user)
