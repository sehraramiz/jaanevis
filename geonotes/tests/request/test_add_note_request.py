from geonotes.domain import note as n
from geonotes.requests import add_note_request as req


def test_build_note_add_request() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)
    request = req.AddNoteRequest(note)

    assert request.note == note
    assert bool(request) is True


def test_build_note_add_from_wrong_type_note() -> None:
    request = req.AddNoteRequest.build(None)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "body"
