import uuid
from datetime import datetime

from jaanevis.domain import note as n

LAT, LONG = 30.0, 50.0
COUNTRY = "IR"


def test_note_model_init() -> None:
    note = n.Note(
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="some text",
        lat=LAT,
        long=LONG,
    )

    assert str(note.code)
    assert note.creator_id == "a@a.com"
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.text == "some text"
    assert note.lat == LAT
    assert note.long == LONG


def test_note_model_init_with_tags() -> None:
    note = n.Note(
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="some #text #for_test",
        lat=LAT,
        long=LONG,
    )

    assert note.tags == ["text", "for_test"]


def test_note_model_init_with_farsi_tags() -> None:
    note = n.Note(
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="some #text #تگ_فارسی",
        lat=LAT,
        long=LONG,
    )

    assert note.tags == ["text", "تگ_فارسی"]


def test_note_model_from_dict() -> None:
    note = n.Note.from_dict(
        {
            "creator_id": "a@a.com",
            "creator": "default",
            "url": "http://example.com",
            "text": "some text",
            "lat": LAT,
            "long": LONG,
        }
    )

    assert str(note.code)
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.text == "some text"
    assert note.lat == LAT
    assert note.long == LONG
    assert note.country == COUNTRY


def test_note_model_to_dict() -> None:
    created = datetime.now()
    note = n.Note(
        created=created,
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="some text",
        lat=LAT,
        long=LONG,
    )

    assert note.to_dict() == {
        "created": created.isoformat(),
        "code": str(note.code),
        "creator_id": "a@a.com",
        "creator": "default",
        "url": "http://example.com",
        "text": "some text",
        "tags": [],
        "lat": LAT,
        "long": LONG,
        "country": COUNTRY,
    }


def test_note_model_to_dict_with_tags() -> None:
    created = datetime.now()
    note = n.Note(
        created=created,
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="some #text",
        lat=LAT,
        long=LONG,
    )

    assert note.to_dict() == {
        "created": created.isoformat(),
        "code": str(note.code),
        "creator_id": "a@a.com",
        "creator": "default",
        "url": "http://example.com",
        "text": "some #text",
        "tags": ["text"],
        "lat": LAT,
        "long": LONG,
        "country": COUNTRY,
    }


def test_note_geojson_properties_init() -> None:
    code = uuid.uuid4()
    note_properties = n.NoteGeoJsonProperties(
        code=code,
        creator="default",
        url="http://exp.com",
        country=COUNTRY,
        text="some text",
    )

    assert note_properties.code == code
    assert note_properties.creator == "default"
    assert note_properties.url == "http://exp.com"
    assert note_properties.country == COUNTRY
    assert note_properties.text == "some text"


def test_note_model_init_with_created() -> None:
    created = datetime.now()
    note = n.Note(
        created=created,
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="",
        lat=LAT,
        long=LONG,
    )

    assert str(note.code)
    assert note.created == created
    assert note.creator_id == "a@a.com"
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.text == ""
    assert note.lat == LAT
    assert note.long == LONG
