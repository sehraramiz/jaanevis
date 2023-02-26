from datetime import datetime, timedelta

import pytest

from jaanevis.domain import session as s


@pytest.fixture
def expire_time() -> float:
    return (datetime.now() - timedelta(hours=1)).timestamp()


def test_session_model_init(expire_time) -> None:
    session = s.Session(email="a@a.com", expire_time=expire_time)

    assert str(session.session_id)
    assert session.email == "a@a.com"
    assert session.expire_time == expire_time


def test_session_model_from_dict(expire_time) -> None:
    session = s.Session.from_dict(
        {"email": "a@a.com", "expire_time": expire_time}
    )

    assert str(session.session_id)
    assert session.email == "a@a.com"
    assert session.expire_time == expire_time


def test_session_model_to_dict(expire_time) -> None:
    session = s.Session(email="a@a.com", expire_time=expire_time)

    assert session.to_dict() == {
        "session_id": str(session.session_id),
        "email": "a@a.com",
        "expire_time": expire_time,
    }
