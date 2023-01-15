import uuid
from datetime import datetime, timedelta

from jaanevis.repository.base import Repository
from jaanevis.requests.login_request import LoginRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess


class LoginUseCase:
    """Use case for user to login and get session"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: LoginRequest) -> ResponseObject:
        user = self.repo.get_user_by_username(username=request.username)
        if not user:
            if not user:
                return ResponseFailure.build_parameters_error(
                    "Wrong username or password"
                )

        if user.password != request.password:
            return ResponseFailure.build_parameters_error(
                "Wrong username or password"
            )

        new_session_id = str(uuid.uuid4())
        tomorrow = datetime.now() + timedelta(days=1)
        print(datetime)
        expire_tomorrow = tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.repo.create_or_update_session(
            username=user.username,
            session_id=new_session_id,
            expire_time=tomorrow.timestamp(),
        )
        return ResponseSuccess(
            {"session": new_session_id, "expires": expire_tomorrow}
        )
