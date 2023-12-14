from jaanevis.domain.user import User, UserUpdateApi
from jaanevis.requests import (
    InvalidRequestObject,
    RequestObject,
    ValidRequestObject,
)


class UpdateOwnUserRequest(ValidRequestObject):
    """request object to update a user"""

    def __init__(self, update_user: UserUpdateApi, user: User) -> None:
        self.update_user = update_user
        self.user = user

    @classmethod
    def build(cls, update_user: UserUpdateApi, user: User) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not isinstance(update_user, UserUpdateApi):
            invalid_req.add_error("body", _("Invalid user type"))
            return invalid_req
        if not user:
            invalid_req.add_error("user", _("Invalid user"))
            return invalid_req
        return cls(update_user=update_user, user=user)
