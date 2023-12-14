import pytest

from jaanevis.requests import note_list_request as req
from jaanevis.responses import response as res


@pytest.fixture
def response_value() -> dict:
    return {"key": ["value1", "value2"]}


@pytest.fixture
def response_type() -> str:
    return "ResponseError"


@pytest.fixture
def response_message() -> str:
    return "This is a response error"


def test_response_success_is_true() -> None:
    assert bool(res.ResponseSuccess(response_value)) is True


def test_response_success_has_type_value_status_code(response_value) -> None:
    response = res.ResponseSuccess(response_value)

    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.code == res.StatusCode.success
    assert response.value == response_value


def test_response_failure_is_false(response_type, response_message) -> None:
    response = res.ResponseFailure(response_type, response_message)

    assert bool(response) is False


def test_response_failure_has_type_message_status_code(
    response_type, response_message
) -> None:
    response = res.ResponseFailure(response_type, response_message)

    assert response.type == response_type
    assert response.code == res.StatusCode.failure
    assert response.message == response_message


def test_response_failure_contains_value(
    response_type, response_message
) -> None:
    response = res.ResponseFailure(response_type, response_message)

    assert response.value == {
        "type": response_type,
        "code": res.StatusCode.failure,
        "message": response_message,
    }


def test_response_failure_initialisation_with_exception(response_type) -> None:
    response = res.ResponseFailure(
        response_type, Exception("An error message")
    )

    assert bool(response) is False
    assert response.type == response_type
    assert response.type == response_type
    assert response.message == "Exception: An error message"


def test_response_failure_from_empty_invalid_request_object() -> None:
    response = res.ResponseFailure.build_from_invalid_request_object(
        req.InvalidRequestObject()
    )

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.code == res.StatusCode.failure


def test_response_failure_from_invalid_request_object_with_errors() -> None:
    request_obj = req.InvalidRequestObject()
    request_obj.add_error("url", "Is mandatory")
    request_obj.add_error("url", "Can't be blank")

    response = res.ResponseFailure.build_from_invalid_request_object(
        request_obj
    )

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.code == res.StatusCode.failure
    assert response.message == "url: Is mandatory\nurl: Can't be blank"


def test_response_failure_build_resource_error() -> None:
    response = res.ResponseFailure.build_resource_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.RESOURCE_ERROR
    assert response.code == res.StatusCode.failure
    assert response.message == "test message"


def test_response_failure_build_parameters_error() -> None:
    response = res.ResponseFailure.build_parameters_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.code == res.StatusCode.failure
    assert response.message == "test message"


def test_response_failure_build_system_error() -> None:
    response = res.ResponseFailure.build_system_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.SYSTEM_ERROR
    assert response.message == "test message"


def test_response_failure_build_resource_error_with_code() -> None:
    response = res.ResponseFailure.build_resource_error(
        "test message", code=res.StatusCode.invalid_username_or_password
    )

    assert bool(response) is False
    assert response.type == res.ResponseFailure.RESOURCE_ERROR
    assert response.code == res.StatusCode.invalid_username_or_password
    assert response.message == "test message"


def test_response_failure_build_parameters_error_with_code() -> None:
    response = res.ResponseFailure.build_parameters_error(
        "test message", code=res.StatusCode.invalid_username_or_password
    )

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.code == res.StatusCode.invalid_username_or_password
    assert response.message == "test message"


def test_response_failure_build_system_error_with_code() -> None:
    response = res.ResponseFailure.build_system_error(
        "test message", code=res.StatusCode.invalid_username_or_password
    )

    assert bool(response) is False
    assert response.type == res.ResponseFailure.SYSTEM_ERROR
    assert response.code == res.StatusCode.invalid_username_or_password
    assert response.message == "test message"
