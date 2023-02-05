from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class ActivateUserRequest(ValidRequestObject):
    """request object for user activation request"""

    def __init__(self, username: str, token: str) -> None:
        self.username = username
        self.token = token

    @classmethod
    def build(cls, username: str, token: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not username:
            invalid_req.add_error("username", _("Username can not be empty"))
            return invalid_req
        if not token:
            invalid_req.add_error("token", _("Token can not be empty"))
            return invalid_req

        return cls(username=username, token=token)
