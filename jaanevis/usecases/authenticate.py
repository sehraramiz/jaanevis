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
            username = request.token.split(":")[0]
            user = self.repo.get_user_by_username(username=username)
            print(username, user)
            if not user:
                return ResponseFailure.build_resource_error("User not found")
            return ResponseSuccess(user)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
