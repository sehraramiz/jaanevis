from jaanevis.domain import session as s


def test_session_model_init() -> None:
    session = s.Session(username="username")

    assert str(session.session_id)
    assert session.username == "username"


def test_session_model_from_dict() -> None:
    session = s.Session.from_dict({"username": "username"})

    assert str(session.session_id)
    assert session.username == "username"


def test_session_model_to_dict() -> None:
    session = s.Session(username="username")

    assert session.to_dict() == {
        "session_id": str(session.session_id),
        "username": "username",
    }
