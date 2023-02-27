import json
import uuid

from jaanevis.domain import geojson as geo
from jaanevis.domain import note as n
from jaanevis.serializers import note_geojson_serializer as geo_serializer
from jaanevis.serializers import note_json_serializer as ser

LAT, LONG = 30.0, 50.0
COUNTRY = "IR"


def test_serialize_domain_note() -> None:
    code = uuid.uuid4()

    note = n.Note(
        code=code,
        creator_id="a@a.com",
        creator="default",
        url="http://example.com",
        text="some text",
        lat=LAT,
        long=LONG,
    )

    expected_json = """
        {{
            "code": "{}",
            "creator": "default",
            "country": "{}",
            "text": "some text",
            "url": "http://example.com",
            "lat": {},
            "long": {}
        }}
    """.format(
        code, COUNTRY, LAT, LONG
    )

    json_note = json.dumps(note, cls=ser.NoteJsonEncoder)

    assert json.loads(json_note) == json.loads(expected_json)


def test_serialize_domain_note_to_geojson() -> None:
    code = uuid.uuid4()

    note = n.Note(
        code=code,
        creator_id="a@a.com",
        creator="default",
        text="some text",
        country=COUNTRY,
        url="http://example.com",
        lat=LAT,
        long=LONG,
    )

    expected_json = """
        {{
            "type": "Feature",
            "coordinates": [{long}, {lat}],
            "properties": {{
                "url": "http://example.com",
                "creator": "default",
                "text": "some text",
                "country": "{country}",
                "code": "{code}"
            }}
        }}
    """.format(
        lat=LAT,
        long=LONG,
        country=COUNTRY,
        code=code,
    )

    json_note = json.dumps(note, cls=ser.NoteGeoJsonEncoder)

    assert json.loads(json_note) == json.loads(expected_json)


def test_serialize_notes_to_geojson() -> None:
    code_1 = uuid.uuid4()
    code_2 = uuid.uuid4()

    notes = [
        n.Note(
            code=code_1,
            creator_id="a@a.com",
            creator="default",
            text="some text",
            url="http://example.com/1",
            lat=LAT,
            long=LONG,
        ),
        n.Note(
            code=code_2,
            creator_id="a@a.com",
            creator="default",
            text="some text",
            url="http://example.com/2",
            lat=LAT + 1,
            long=LONG + 1,
        ),
    ]

    geojson_notes = geo_serializer.notes_to_geojson(notes)

    assert geojson_notes == [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [notes[0].long, notes[0].lat],
            },
            "properties": {
                "url": notes[0].url,
                "creator": "default",
                "text": "some text",
                "country": COUNTRY,
                "code": code_1,
            },
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [notes[1].long, notes[1].lat],
            },
            "properties": {
                "url": notes[1].url,
                "creator": "default",
                "text": "some text",
                "country": COUNTRY,
                "code": code_2,
            },
        },
    ]


def test_serialize_notes_to_geojson_features() -> None:
    code_1 = uuid.uuid4()

    notes = [
        n.Note(
            code=code_1,
            creator_id="a@a.com",
            creator="default",
            text="some text",
            url="http://example.com/1",
            lat=LAT,
            long=LONG,
        ),
    ]

    geojson_notes = geo_serializer.notes_to_geojson_features(notes)

    assert geojson_notes == [
        n.NoteGeoJsonFeature(
            geometry=geo.GeoJsonPoint(
                coordinates=[notes[0].long, notes[0].lat]
            ),
            properties=n.NoteGeoJsonProperties(
                code=code_1,
                creator="default",
                text="some text",
                country=COUNTRY,
                url=notes[0].url,
            ),
        )
    ]
