import uuid

from jaanevis.domain import note as n

LAT, LONG = 30.0, 50.0
COUNTRY = "IR"


def test_note_model_init() -> None:
    note = n.Note(
        creator="default",
        url="http://example.com",
        text="some text",
        lat=LAT,
        long=LONG,
    )

    assert str(note.code)
    assert note.creator == "default"
    assert note.url == "http://example.com"
    assert note.text == "some text"
    assert note.lat == LAT
    assert note.long == LONG


def test_note_model_from_dict() -> None:
    note = n.Note.from_dict(
        {
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
    note = n.Note(
        creator="default",
        url="http://example.com",
        text="some text",
        lat=LAT,
        long=LONG,
    )

    assert note.to_dict() == {
        "code": str(note.code),
        "creator": "default",
        "url": "http://example.com",
        "text": "some text",
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
