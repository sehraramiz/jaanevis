from jaanevis.domain import user as u
from jaanevis.repository.base import Repository
from jaanevis.requests.activate_user_request import ActivateUserRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess


class ActivateUserUseCase:
    """usecase for user activation"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: ActivateUserRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)

        session = self.repo.get_session_by_session_id_and_username(
            session_id=request.token, username=request.username
        )
        if not session:
            return ResponseFailure.build_parameters_error(
                "Invalid activation token"
            )

        user = self.repo.get_user_by_username(username=request.username)
        if not user:
            return ResponseFailure.build_resource_error("User not found")
        if user.is_active:
            return ResponseFailure.build_parameters_error(
                "User is already activated"
            )
        updated_user = self.repo.update_user(
            obj=user, data={"is_active": True}
        )
        self.repo.delete_session_by_session_id(session_id=request.token)
        updated_user_res = u.UserRead(
            username=updated_user.username, is_active=updated_user.is_active
        )

        return ResponseSuccess(updated_user_res)
