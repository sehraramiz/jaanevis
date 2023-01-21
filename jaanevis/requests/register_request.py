import re

from jaanevis.requests import InvalidRequestObject, RequestObject


class RegisterRequest:
    """request object for user registeration"""

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    @classmethod
    def build(cls, email: str, password: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        email_re = "^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$"
        if not re.search(email_re, email):
            invalid_req.add_error("email", "Invalid email")
            return invalid_req
        if not password:
            invalid_req.add_error("password", "Password can not be empty")
            return invalid_req
        if len(password) < 8:
            invalid_req.add_error(
                "password", "minimum password length must be 8 characters"
            )
            return invalid_req

        return cls(email=email, password=password)
