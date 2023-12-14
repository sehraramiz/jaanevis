from jaanevis.requests import activate_user_request as req


def test_user_activate_request_build() -> None:
    username = "username"
    token = "token"
    request = req.ActivateUserRequest.build(username=username, token=token)

    assert bool(request) is True
    assert request.username == username
    assert request.token == token


def test_user_activate_request_build_from_invalid_username() -> None:
    request = req.ActivateUserRequest.build(username=None, token="token")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "username"


def test_user_activate_request_build_from_invalid_token() -> None:
    request = req.ActivateUserRequest.build(username="username", token=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "token"
