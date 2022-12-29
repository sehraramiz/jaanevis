import uuid

from geonotes.domain import note as n


def test_note_model_init() -> None:
    code = uuid.uuid4()
    note = n.Note(
        code, creator="default", url="http://example.com", lat=1, long=1
    )

    assert note.code == code
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.lat == 1
    assert note.long == 1


def test_note_model_from_dict() -> None:
    code = uuid.uuid4()
    note = n.Note.from_dict(
        {
            "code": code,
            "creator": "default",
            "url": "http://example.com",
            "lat": 1,
            "long": 1,
        }
    )

    assert note.code == code
    assert note.lat == 1
    assert note.long == 1


def test_note_model_to_dict() -> None:
    note_dict = {
        "code": uuid.uuid4(),
        "creator": "default",
        "url": "http://example.com",
        "lat": 1,
        "long": 1,
    }

    note = n.Note.from_dict(note_dict)

    assert note.to_dict() == note_dict
