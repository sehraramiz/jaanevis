from jaanevis.requests import auth_request as req


def test_auth_request_build_from_empty_auth_header() -> None:
    request = req.AuthenticateRequest.build(token="")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "header"


def test_auth_request_build_from_invalid_auth_header() -> None:
    request = req.AuthenticateRequest.build(token="invalid auth")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "header"


def test_auth_request_build_from_auth_header() -> None:
    auth_header = "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
    request = req.AuthenticateRequest.build(token=auth_header)

    assert bool(request) is True
    assert request.token == "username:password"
