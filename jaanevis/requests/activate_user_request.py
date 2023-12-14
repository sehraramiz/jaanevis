from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class ActivateUserRequest(ValidRequestObject):
    """request object for user activation request"""

    def __init__(self, email: str, token: str) -> None:
        self.email = email
        self.token = token

    @classmethod
    def build(cls, email: str, token: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not email:
            invalid_req.add_error("email", _("Email can not be empty"))
            return invalid_req
        if not token:
            invalid_req.add_error("token", _("Token can not be empty"))
            return invalid_req

        return cls(email=email, token=token)
