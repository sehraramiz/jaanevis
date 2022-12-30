from typing import Any

from geonotes.requests import InvalidRequestObject


class ResponseSuccess:
    """Response class for output of usecases"""

    SUCCESS = "Success"

    def __init__(self, value: Any = None) -> None:
        self.type = self.SUCCESS
        self.value = value

    def __bool__(self) -> bool:
        return True


class ResponseFailure:
    """Response class for failed output of usecases"""

    RESOURCE_ERROR = "ResourceError"
    PARAMETERS_ERROR = "ParametersError"
    SYSTEM_ERROR = "SystemError"

    def __init__(self, type_: str, message: str) -> None:
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg: str | Exception) -> str:
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, msg)
        return msg

    @property
    def value(self) -> dict[str, str]:
        return {"type": self.type, "message": self.message}

    def __bool__(self) -> bool:
        return False

    @classmethod
    def build_from_invalid_request_object(
        cls, invalid_request_obj: InvalidRequestObject
    ) -> "ResponseFailure":
        message = "\n".join(
            "{}: {}".format(err["parameter"], err["message"])
            for err in invalid_request_obj.errors
        )
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_resource_error(cls, message: str) -> "ResponseFailure":
        return cls(cls.RESOURCE_ERROR, message=message)

    @classmethod
    def build_system_error(cls, message: str) -> "ResponseFailure":
        return cls(cls.SYSTEM_ERROR, message=message)

    @classmethod
    def build_parameters_error(cls, message: str) -> "ResponseFailure":
        return cls(cls.PARAMETERS_ERROR, message=message)


ResponseObject = ResponseSuccess | ResponseFailure
