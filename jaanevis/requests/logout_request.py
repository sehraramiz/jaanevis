from jaanevis.requests import RequestObject, ValidRequestObject


class LogoutRequest(ValidRequestObject):
    """request object for logging out a user"""

    def __init__(self, session: str) -> None:
        self.session = session

    @classmethod
    def build(cls, session: str) -> RequestObject:
        return cls(session=session)
