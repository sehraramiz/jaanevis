from typing import Any


class StatusCode:
    success = 0
    failure = 1
    invalid_username_or_password = 2
    invalid_activation_token = 3
    invalid_session = 4
    expired_session = 5
    inactive_user = 6
    invalid_email = 7
    invalid_password = 8
    user_exists = 9
    invalid_username = 10


class ResponseSuccess:
    """Response class for output of usecases"""

    SUCCESS = "Success"

    def __init__(
        self, value: Any = None, code: StatusCode = StatusCode.success
    ) -> None:
        self.type = self.SUCCESS
        self.code = code
        self.value = value

    def __bool__(self) -> bool:
        return True


class ResponseFailure:
    """Response class for failed output of usecases"""

    RESOURCE_ERROR = "ResourceError"
    PARAMETERS_ERROR = "ParametersError"
    SYSTEM_ERROR = "SystemError"

    def __init__(
        self, type_: str, message: str, code: StatusCode = StatusCode.failure
    ) -> None:
        self.type = type_
        self.code = code
        self.message = self._format_message(message)

    def _format_message(self, msg: str | Exception) -> str:
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, msg)
        return msg

    @property
    def value(self) -> dict[str, str]:
        return {"type": self.type, "code": self.code, "message": self.message}

    def __bool__(self) -> bool:
        return False

    @classmethod
    def build_from_invalid_request_object(
        cls, invalid_request_obj: "InvalidRequestObject"
    ) -> "ResponseFailure":
        message = "\n".join(
            "{}: {}".format(err["parameter"], err["message"])
            for err in invalid_request_obj.errors
        )
        return cls(
            cls.PARAMETERS_ERROR, message, code=invalid_request_obj.error_code
        )

    @classmethod
    def build_resource_error(
        cls, message: str, code: StatusCode = StatusCode.failure
    ) -> "ResponseFailure":
        return cls(cls.RESOURCE_ERROR, message=message, code=code)

    @classmethod
    def build_system_error(
        cls, message: str, code: StatusCode = StatusCode.failure
    ) -> "ResponseFailure":
        return cls(cls.SYSTEM_ERROR, message=message, code=code)

    @classmethod
    def build_parameters_error(
        cls, message: str, code: StatusCode = StatusCode.failure
    ) -> "ResponseFailure":
        return cls(cls.PARAMETERS_ERROR, message=message, code=code)


ResponseObject = ResponseSuccess | ResponseFailure
