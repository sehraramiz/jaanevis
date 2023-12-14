import uuid

from jaanevis.domain import user as u
from jaanevis.requests import delete_note_request as req


def test_build_note_delete_from_empty_code() -> None:
    user = u.User(email="a@a.com", username="username", password="password")
    request = req.DeleteNoteRequest.build(code="", user=user)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "code"


def test_build_note_delete_request() -> None:
    code = str(uuid.uuid4())
    user = u.User(email="a@a.com", username="username", password="password")
    request = req.DeleteNoteRequest.build(code=code, user=user)

    assert bool(request) is True
    assert request.code == code
    assert request.user == user


def test_build_note_delete_from_invalid_user() -> None:
    code = str(uuid.uuid4())
    request = req.DeleteNoteRequest.build(code=code, user=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "user"
