from jaanevis.requests import register_request as register_req


def test_register_request_build() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", password="password"
    )

    assert bool(request) is True
    assert request.email == "a@a.com"
    assert request.password == "password"


def test_register_request_build_from_invalid_email() -> None:
    request = register_req.RegisterRequest.build(
        email="a", password="password"
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "email"


def test_register_request_build_from_invalid_password() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", password=None
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "password"


def test_register_request_build_from_less_than_8_character_password() -> None:
    request = register_req.RegisterRequest.build(
        email="a@a.com", password="123456"
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "password"
