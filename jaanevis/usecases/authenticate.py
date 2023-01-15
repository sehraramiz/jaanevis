from datetime import datetime

from jaanevis.repository.base import Repository
from jaanevis.requests.auth_request import AuthenticateRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess


class AuthenticateUseCase:
    """authenticate a user from auth session"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: AuthenticateRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)

        try:
            session = self.repo.get_session_by_session_id(
                session_id=request.session
            )
            if not session:
                return ResponseFailure.build_resource_error(
                    "Session not found"
                )

            user = self.repo.get_user_by_username(username=session.username)
            if not user:
                return ResponseFailure.build_resource_error("User not found")

            if session.expire_time < datetime.now().timestamp():
                self.repo.delete_session_by_session_id(
                    session_id=str(session.session_id)
                )
                return ResponseFailure.build_parameters_error(
                    "Session expired"
                )

            return ResponseSuccess(user)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
