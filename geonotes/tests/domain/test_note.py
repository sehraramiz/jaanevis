import uuid

from geonotes.domain import note as n


def test_note_model_init() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)

    assert str(note.code)
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.lat == 1
    assert note.long == 1


def test_note_model_from_dict() -> None:
    note = n.Note.from_dict(
        {
            "creator": "default",
            "url": "http://example.com",
            "lat": 1,
            "long": 1,
        }
    )

    assert str(note.code)
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.lat == 1
    assert note.long == 1


def test_note_model_to_dict() -> None:
    note = n.Note(creator="default", url="http://example.com", lat=1, long=1)

    assert note.to_dict() == {
        "code": note.code,
        "creator": "default",
        "url": "http://example.com",
        "lat": 1,
        "long": 1,
    }
