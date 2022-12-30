from unittest import mock

import pytest

from geonotes.domain import note as n
from geonotes.requests import add_note_request as req
from geonotes.responses import response as res
from geonotes.usecases import add_note as uc

DEFAULT_CREATOR = "default"


@pytest.fixture
def new_note() -> n.Note:
    return n.Note(creator="default", url="", lat=1, long=1)


def test_add_note(new_note: n.Note) -> None:
    repo = mock.Mock()

    add_note_usecase = uc.AddNoteUseCase(repo)
    add_note_request = req.AddNoteRequest(new_note)

    response = add_note_usecase.execute(add_note_request)

    assert bool(response) is True
    repo.add.assert_called_with(new_note)
    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.value == new_note


def test_add_note_handles_generic_error(new_note: n.Note) -> None:
    repo = mock.Mock()
    repo.add.side_effect = Exception("An error message")

    add_note_usecase = uc.AddNoteUseCase(repo)
    request_obj = req.AddNoteRequest(new_note)

    response_obj = add_note_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "message": "Exception: An error message",
    }


def test_add_note_handles_bad_request() -> None:
    repo = mock.Mock()

    add_note_usecase = uc.AddNoteUseCase(repo)
    request_obj = req.AddNoteRequest.build(None)

    response_obj = add_note_usecase.execute(request_obj)

    assert bool(request_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "body: Invalid note type",
    }
