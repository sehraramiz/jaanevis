import re

from jaanevis.requests import InvalidRequestObject, RequestObject
from jaanevis.responses import response as res


class RegisterRequest:
    """request object for user registeration"""

    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self.password = password

    @classmethod
    def build(cls, email: str, username: str, password: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        email_re = "^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$"
        if not re.search(email_re, email):
            invalid_req.error_code = res.StatusCode.invalid_email
            invalid_req.add_error("email", _("Invalid email"))
            return invalid_req

        username_re = "^(?!.*\\.\\.)(?!.*\\.$)[^\\W][\\w.]{0,29}$"
        if not re.search(username_re, username):
            invalid_req.error_code = res.StatusCode.invalid_username
            invalid_username_error = _(
                "Invalid username, only use letters, numbers, underscores and periods."
            )
            invalid_req.add_error(
                "username",
                invalid_username_error,
            )
            return invalid_req

        if not password:
            invalid_req.error_code = res.StatusCode.invalid_password
            invalid_req.add_error("password", _("Password can not be empty"))
            return invalid_req
        if len(password) < 8:
            invalid_req.error_code = res.StatusCode.invalid_password
            invalid_req.add_error(
                "password", _("minimum password length must be 8 characters")
            )
            return invalid_req

        return cls(email=email, username=username, password=password)
