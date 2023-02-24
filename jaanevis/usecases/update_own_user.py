from jaanevis.domain import user as u
from jaanevis.repository.base import Repository
from jaanevis.requests.update_own_user_request import UpdateOwnUserRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess


class UpdateOwnUserUseCase:
    """update own user"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: UpdateOwnUserRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)

        try:
            user_exists = self.repo.get_user_by_username(
                username=request.update_user.username
            )
            if user_exists:
                return ResponseFailure.build_resource_error(
                    f"user with username '{request.update_user.username}' already exists"
                )

            data = request.update_user.dict(exclude_unset=True)
            updated_user = self.repo.update_user(obj=request.user, data=data)
            user_read = u.UserRead(
                username=updated_user.username,
                is_active=updated_user.is_active,
            )
            return ResponseSuccess(user_read)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
