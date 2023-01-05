import uuid
from unittest import mock

from jaanevis.domain import note as n
from jaanevis.requests import delete_note_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import delete_note as uc

notes = [
    n.Note(
        code=uuid.uuid4(),
        creator="default",
        url="https://example.com/1",
        lat=1,
        long=1,
    ),
]


def test_note_delete_handles_bad_request() -> None:
    repo = mock.Mock()

    delete_note_usecase = uc.DeleteNoteUseCase(repo)
    request_obj = req.DeleteNoteRequest.build(code=None)

    response_obj = delete_note_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "code: Invalid code value",
    }


def test_delete_note_by_code() -> None:
    repo = mock.Mock()
    repo.delete_by_code.return_value = notes[0]

    note_delete_usecase = uc.DeleteNoteUseCase(repo)
    request = req.DeleteNoteRequest.build(code=notes[0].code)

    response = note_delete_usecase.execute(request)

    assert bool(response) is True
    repo.delete_by_code.assert_called_with(code=notes[0].code)
    assert response.value == notes[0]


def test_delete_note_by_code_handles_nonexistent_code() -> None:
    repo = mock.Mock()
    repo.delete_by_code.return_value = None

    note_delete_usecase = uc.DeleteNoteUseCase(repo)
    request = req.DeleteNoteRequest.build(code="nocode")

    response = note_delete_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "message": "note with code 'nocode' not found",
    }
