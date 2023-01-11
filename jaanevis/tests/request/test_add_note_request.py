from jaanevis.domain import note as n
from jaanevis.domain import user as u
from jaanevis.requests import add_note_request as req


def test_build_note_add_request() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)
    user = u.User(username="username", password="password")
    request = req.AddNoteRequest(note=note, user=user)

    assert request.note == note
    assert request.user == user
    assert bool(request) is True


def test_build_note_add_from_wrong_type_note() -> None:
    request = req.AddNoteRequest.build(note=None, user=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "body"


def test_build_note_add_from_non_existant_user() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)
    request = req.AddNoteRequest.build(note=note, user=None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "user"
