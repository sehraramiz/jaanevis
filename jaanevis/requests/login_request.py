from jaanevis.requests import RequestObject, ValidRequestObject


class LoginRequest(ValidRequestObject):
    """request object for user login"""

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    @classmethod
    def build(cls, username: str, password: str) -> RequestObject:
        return cls(username=username, password=password)
