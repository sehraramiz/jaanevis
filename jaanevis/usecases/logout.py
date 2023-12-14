from jaanevis.repository.base import Repository
from jaanevis.requests.logout_request import LogoutRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess


class LogoutUseCase:
    """usecase for logging a user out"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: LogoutRequest) -> ResponseObject:
        try:
            session = self.repo.get_session_by_session_id(
                session_id=request.session
            )
            if not session:
                return ResponseSuccess(True)
            self.repo.delete_session_by_session_id(session_id=request.session)
            return ResponseSuccess(True)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
