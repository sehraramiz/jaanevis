from jaanevis.requests import auth_request as req
from jaanevis.requests import login_request as login_req
from jaanevis.requests import logout_request as logout_req
from jaanevis.responses import response as res


def test_auth_request_build_from_empty_session() -> None:
    request = req.AuthenticateRequest.build(session="")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "session"
    assert request.errors[0]["code"] == res.StatusCode.invalid_session
    assert request.error_code == res.StatusCode.invalid_session


def test_auth_request_build_from_invalid_session() -> None:
    request = req.AuthenticateRequest.build(session=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "session"
    assert request.errors[0]["code"] == res.StatusCode.invalid_session
    assert request.error_code == res.StatusCode.invalid_session


def test_auth_request_build_from_auth_header() -> None:
    session = "validsession"
    request = req.AuthenticateRequest.build(session=session)

    assert bool(request) is True
    assert request.session == "validsession"


def test_login_request_build() -> None:
    request = login_req.LoginRequest.build(
        username="username", password="password"
    )

    assert bool(request) is True
    assert request.username == "username"
    assert request.password == "password"


def test_logout_request_build() -> None:
    request = logout_req.LogoutRequest.build(session="session")

    assert bool(request) is True
    assert request.session == "session"
