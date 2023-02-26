from jaanevis.requests import activate_user_request as req


def test_user_activate_request_build() -> None:
    email = "a@a.com"
    token = "token"
    request = req.ActivateUserRequest.build(email=email, token=token)

    assert bool(request) is True
    assert request.email == email
    assert request.token == token


def test_user_activate_request_build_from_invalid_email() -> None:
    request = req.ActivateUserRequest.build(email=None, token="token")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "email"


def test_user_activate_request_build_from_invalid_token() -> None:
    request = req.ActivateUserRequest.build(email="a@a.com", token=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "token"
