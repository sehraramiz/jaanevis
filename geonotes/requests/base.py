from typing import Any, Union


class InvalidRequestObject:
    """Class for request objects with errors"""

    def __init__(self) -> None:
        self.errors: list[dict[str, str]] = []

    def add_error(self, parameter: str, message: str) -> None:
        self.errors.append({"parameter": parameter, "message": message})

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
