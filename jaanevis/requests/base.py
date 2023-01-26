from typing import Any, Union

from jaanevis.responses import StatusCode


class InvalidRequestObject:
    """Class for request objects with errors"""

    def __init__(self, error_code: StatusCode = StatusCode.failure) -> None:
        self.errors: list[dict[str, str]] = []
        self.error_code = error_code

    def add_error(
        self,
        parameter: str,
        message: str,
        code: StatusCode = StatusCode.failure,
    ) -> None:
        self.errors.append(
            {"parameter": parameter, "message": message, "code": code}
        )

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self) -> bool:
        return False


class ValidRequestObject:
    """Class for request objects with valid data"""

    @classmethod
    def from_dict(
        cls, data: dict[str, Any]
    ) -> Union["ValidRequestObject", InvalidRequestObject]:
        raise NotImplementedError

    def __bool__(self) -> bool:
        return True


RequestObject = ValidRequestObject | InvalidRequestObject
