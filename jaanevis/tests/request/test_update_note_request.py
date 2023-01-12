from jaanevis.domain import note as n
from jaanevis.domain import user as u
from jaanevis.requests import update_note_request as req

user = u.User(username="username", password="password")


def test_build_note_update_request() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)
    note_update = n.NoteUpdateApi(**note.to_dict())
    request = req.UpdateNoteRequest.build(
        code=str(note.code), note=note_update, user=user
    )

    assert request.note == note_update
    assert bool(request) is True


def test_build_note_update_from_wrong_type_note() -> None:
    request = req.UpdateNoteRequest.build(code="code", note=None, user=user)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "body"


def test_build_note_update_from_empty_code() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)
    note_update = n.NoteUpdateApi(**note.to_dict())
    request = req.UpdateNoteRequest.build(code="", note=note_update, user=user)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "code"


def test_build_note_update_from_invalid_user() -> None:
    note = n.Note(creator="username", url="http://example.com", lat=1, long=1)
    note_update = n.NoteUpdateApi(**note.to_dict())
    request = req.UpdateNoteRequest.build(
        code="code", note=note_update, user=None
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "user"
