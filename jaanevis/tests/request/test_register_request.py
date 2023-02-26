from jaanevis.requests import register_request as register_req
from jaanevis.responses import response as res


def test_register_request_build() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", username="username", password="password"
    )

    assert bool(request) is True
    assert request.email == "a@a.com"
    assert request.username == "username"
    assert request.password == "password"


def test_register_request_build_from_invalid_email() -> None:
    request = register_req.RegisterRequest.build(
        email="a", username="username", password="password"
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "email"
    assert request.error_code == res.StatusCode.invalid_email


def test_register_request_build_from_empty_username() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", username="", password="password"
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "username"
    assert request.error_code == res.StatusCode.invalid_username


def test_register_request_build_from_username_with_invalid_chracters() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", username="@username", password="password"
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "username"
    assert request.error_code == res.StatusCode.invalid_username


def test_register_request_build_from_invalid_password() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", username="username", password=None
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "password"
    assert request.error_code == res.StatusCode.invalid_password


def test_register_request_build_from_less_than_8_character_password() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", username="username", password="123456"
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "password"
    assert request.error_code == res.StatusCode.invalid_password
