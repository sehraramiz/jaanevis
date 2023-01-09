import binascii
from base64 import b64decode

from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class AuthenticateRequest(ValidRequestObject):
    """request object for user authenticating user"""

    def __init__(self, token: str) -> None:
        self.token = token

    @classmethod
    def build(cls, token: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not token:
            invalid_req.add_error("header", "Invalid auth header")
            return invalid_req

        try:
            access_token = token.replace("Basic ", "")
            token = b64decode(access_token).decode("utf8")
        except binascii.Error:
            invalid_req.add_error("header", "Invalid auth header")
            return invalid_req

        return cls(token=token)
