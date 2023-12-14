import uuid

from jaanevis.requests import read_note_request as req


def test_build_note_read_from_empty_code() -> None:
    request = req.ReadNoteRequest.build(code="")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "code"


def test_build_note_read_request() -> None:
    code = str(uuid.uuid4())
    request = req.ReadNoteRequest.build(code=code)

    assert bool(request) is True
    assert request.code == code
