import uuid
from unittest import mock

from jaanevis.domain import note as n
from jaanevis.domain import user as u
from jaanevis.requests import delete_note_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import delete_note as uc

notes = [
    n.Note(
        code=str(uuid.uuid4()),
        creator="username",
        url="https://example.com/1",
        lat=1,
        long=1,
    ),
]
user = u.User(username="username", password="password")


def test_note_delete_handles_invalid_code() -> None:
    repo = mock.Mock()

    delete_note_usecase = uc.DeleteNoteUseCase(repo)
    request_obj = req.DeleteNoteRequest.build(code=None, user=user)

    response_obj = delete_note_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "code: Invalid code value",
    }


def test_note_delete_handles_invalid_user() -> None:
    repo = mock.Mock()
    code = str(uuid.uuid4())

    delete_note_usecase = uc.DeleteNoteUseCase(repo)
    request_obj = req.DeleteNoteRequest.build(code=code, user=None)

    response_obj = delete_note_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "user: Invalid user",
    }


def test_delete_note_by_code() -> None:
    repo = mock.Mock()
    repo.delete_by_code.return_value = notes[0]
    repo.get_by_code.return_value = notes[0]

    note_delete_usecase = uc.DeleteNoteUseCase(repo)
    request = req.DeleteNoteRequest.build(code=notes[0].code, user=user)

    response = note_delete_usecase.execute(request)

    assert bool(response) is True
    repo.delete_by_code.assert_called_with(code=notes[0].code)
    assert response.value == notes[0]


def test_delete_note_by_code_wrong_user() -> None:
    repo = mock.Mock()
    wrong_user = u.User(username="wrong_user", password="password")
    repo.get_by_code.return_value = notes[0]

    note_delete_usecase = uc.DeleteNoteUseCase(repo)
    request = req.DeleteNoteRequest.build(code=notes[0].code, user=wrong_user)

    response = note_delete_usecase.execute(request)

    assert bool(response) is False
    repo.delete_by_code.assert_not_called()
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "permission denied",
    }


def test_delete_note_by_code_handles_nonexistent_code() -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = None

    note_delete_usecase = uc.DeleteNoteUseCase(repo)
    request = req.DeleteNoteRequest.build(code="nocode", user=user)

    response = note_delete_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "code": res.StatusCode.failure,
        "message": "note with code 'nocode' not found",
    }


def test_delete_note_by_code_handles_generic_error() -> None:
    repo = mock.Mock()
    repo.get_by_code.side_effect = Exception("An error message")

    note_delete_usecase = uc.DeleteNoteUseCase(repo)
    request = req.DeleteNoteRequest.build(code=notes[0].code, user=user)

    response = note_delete_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }
