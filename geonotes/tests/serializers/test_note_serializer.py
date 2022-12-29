import json
import uuid

from geonotes.domain import note as n
from geonotes.serializers import note_json_serializer as ser


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
