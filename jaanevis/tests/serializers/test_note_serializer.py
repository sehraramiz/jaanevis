import json
import uuid

from jaanevis.domain import geojson as geo
from jaanevis.domain import note as n
from jaanevis.serializers import note_geojson_serializer as geo_serializer
from jaanevis.serializers import note_json_serializer as ser


def test_serialize_domain_note() -> None:
    code = uuid.uuid4()

    note = n.Note(
        code=code,
        creator="default",
        url="http://example.com",
        lat=1,
        long=1,
    )

    expected_json = """
        {{
            "code": "{}",
            "creator": "default",
            "url": "http://example.com",
            "lat": 1,
            "long": 1
        }}
    """.format(
        code
    )

    json_note = json.dumps(note, cls=ser.NoteJsonEncoder)

    assert json.loads(json_note) == json.loads(expected_json)


def test_serialize_domain_note_to_geojson() -> None:
    code = uuid.uuid4()

    note = n.Note(
        code=code,
        creator="default",
        url="http://example.com",
        lat=1,
        long=2,
    )

    expected_json = """
        {{
            "type": "Feature",
            "coordinates": [2, 1],
            "properties": {{
                "url": "http://example.com",
                "creator": "default",
                "code": "{}"
            }}
        }}
    """.format(
        code
    )

    json_note = json.dumps(note, cls=ser.NoteGeoJsonEncoder)

    assert json.loads(json_note) == json.loads(expected_json)


def test_serialize_notes_to_geojson() -> None:
    code_1 = uuid.uuid4()
    code_2 = uuid.uuid4()

    notes = [
        n.Note(
            code=code_1,
            creator="default",
            url="http://example.com/1",
            lat=1,
            long=2,
        ),
        n.Note(
            code=code_2,
            creator="default",
            url="http://example.com/2",
            lat=3,
            long=4,
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
                "code": code_2,
            },
        },
    ]


def test_serialize_notes_to_geojson_features() -> None:
    code_1 = uuid.uuid4()

    notes = [
        n.Note(
            code=code_1,
            creator="default",
            url="http://example.com/1",
            lat=1,
            long=2,
        ),
    ]

    geojson_notes = geo_serializer.notes_to_geojson_features(notes)

    assert geojson_notes == [
        n.NoteGeoJsonFeature(
            geometry=geo.GeoJsonPoint(
                coordinates=[notes[0].long, notes[0].lat]
            ),
            properties=n.NoteGeoJsonProperties(
                code=code_1, creator="default", url=notes[0].url
            ),
        )
    ]
