from datetime import datetime

from jaanevis.i18n import gettext as _
from jaanevis.repository.base import Repository
from jaanevis.requests.auth_request import AuthenticateRequest
from jaanevis.responses import (
    ResponseFailure,
    ResponseObject,
    ResponseSuccess,
    StatusCode,
)


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
                    _("Session not found"), code=StatusCode.invalid_session
                )

            user = self.repo.get_user_by_email(email=session.email)
            if not user:
                return ResponseFailure.build_resource_error("User not found")

            if not user.is_active:
                return ResponseFailure.build_parameters_error(
                    _("User is not active"), code=StatusCode.inactive_user
                )

            if session.expire_time < datetime.now().timestamp():
                self.repo.delete_session_by_session_id(
                    session_id=str(session.session_id)
                )
                return ResponseFailure.build_parameters_error(
                    _("Session expired"), code=StatusCode.expired_session
                )
            return ResponseSuccess(user)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
