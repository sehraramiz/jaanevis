from jaanevis.requests import auth_request as req


def test_auth_request_build_from_empty_session() -> None:
    request = req.AuthenticateRequest.build(session="")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "session"


def test_auth_request_build_from_invalid_session() -> None:
    request = req.AuthenticateRequest.build(session=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "session"


def test_auth_request_build_from_auth_header() -> None:
    session = "validsession"
    request = req.AuthenticateRequest.build(session=session)

    assert bool(request) is True
    assert request.session == "validsession"
