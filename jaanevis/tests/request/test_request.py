from jaanevis.requests.base import InvalidRequestObject, ValidRequestObject
from jaanevis.responses import response as res


def test_build_valid_request() -> None:
    request = ValidRequestObject()

    assert bool(request) is True


def test_build_invalid_request_with_no_error_code() -> None:
    request = InvalidRequestObject()
    request.add_error("param", "some error")

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "param"
    assert request.errors[0]["code"] == res.StatusCode.failure
    assert bool(request) is False


def test_build_invalid_request_with_error_code() -> None:
    request = InvalidRequestObject()
    request.add_error(
        parameter="param",
        message="some error",
        code=res.StatusCode.invalid_session,
    )

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "param"
    assert request.errors[0]["code"] == res.StatusCode.invalid_session
    assert bool(request) is False


def test_build_invalid_request_with_request_error_code() -> None:
    request = InvalidRequestObject(error_code=res.StatusCode.invalid_session)

    assert bool(request) is False
    assert request.error_code == res.StatusCode.invalid_session
