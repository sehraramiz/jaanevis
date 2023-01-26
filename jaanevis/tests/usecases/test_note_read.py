import uuid
from unittest import mock

from jaanevis.domain import note as n
from jaanevis.requests import read_note_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import read_note as uc

notes = [
    n.Note(
        code=str(uuid.uuid4()),
        creator="default",
        url="https://example.com/1",
        lat=1,
        long=1,
    ),
    n.Note(
        code=str(uuid.uuid4()),
        creator="default",
        url="https://example.com/2",
        lat=2,
        long=2,
    ),
]


def test_note_read_handles_bad_request() -> None:
    repo = mock.Mock()

    read_note_usecase = uc.ReadNoteUseCase(repo)
    request_obj = req.ReadNoteRequest.build(code=None)

    response_obj = read_note_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "code: Invalid code value",
    }


def test_read_note_by_code() -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = notes[0]

    note_read_usecase = uc.ReadNoteUseCase(repo)
    request = req.ReadNoteRequest.build(code=notes[0].code)

    response = note_read_usecase.execute(request)

    assert bool(response) is True
    repo.get_by_code.assert_called_with(code=notes[0].code)
    assert response.value == notes[0]


def test_read_note_by_code_handles_nonexistent_code() -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = None

    note_read_usecase = uc.ReadNoteUseCase(repo)
    request = req.ReadNoteRequest.build(code="nocode")

    response = note_read_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "code": res.StatusCode.failure,
        "message": "note with code 'nocode' not found",
    }
