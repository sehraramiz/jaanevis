import uuid

from jaanevis.requests import delete_note_request as req


def test_build_note_delete_from_empty_code() -> None:
    request = req.DeleteNoteRequest.build(code="")

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "code"


def test_build_note_delete_request() -> None:
    code = str(uuid.uuid4())
    request = req.DeleteNoteRequest.build(code=code)

    assert bool(request) is True
    assert request.code == code
