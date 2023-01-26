from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject
from jaanevis.responses import response as res


class AuthenticateRequest(ValidRequestObject):
    """request object for authenticating user"""

    def __init__(self, session: str) -> None:
        self.session = session

    @classmethod
    def build(cls, session: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not session:
            invalid_req.error_code = res.StatusCode.invalid_session
            invalid_req.add_error(
                "session",
                "Invalid session",
                code=res.StatusCode.invalid_session,
            )
            return invalid_req

        return cls(session=session)
