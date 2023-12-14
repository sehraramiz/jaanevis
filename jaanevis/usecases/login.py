import uuid
from datetime import datetime, timedelta

from jaanevis.repository.base import Repository
from jaanevis.requests.login_request import LoginRequest
from jaanevis.responses import (
    ResponseFailure,
    ResponseObject,
    ResponseSuccess,
    StatusCode,
)
from jaanevis.utils import security


class LoginUseCase:
    """Use case for user to login and get session"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: LoginRequest) -> ResponseObject:
        try:
            user = self.repo.get_user_by_username(username=request.username)
            if not user:
                if not user:
                    return ResponseFailure.build_parameters_error(
                        _("Wrong username or password"),
                        code=StatusCode.invalid_username_or_password,
                    )
            if not user.is_active:
                return ResponseFailure.build_parameters_error(
                    _("User is not active"), code=StatusCode.inactive_user
                )

            password_valid = security.verify_password(
                hashed_password=user.password, password=request.password
            )
            if not password_valid:
                return ResponseFailure.build_parameters_error(
                    _("Wrong username or password"),
                    code=StatusCode.invalid_username_or_password,
                )

            new_session_id = str(uuid.uuid4())
            tomorrow = datetime.now() + timedelta(days=1)
            expire_tomorrow = tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT")
            self.repo.create_or_update_session(
                email=user.email,
                username=user.username,
                session_id=new_session_id,
                expire_time=tomorrow.timestamp(),
            )
            return ResponseSuccess(
                {"session": new_session_id, "expires": expire_tomorrow}
            )
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
