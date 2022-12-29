import uuid
from unittest import mock

import pytest

from geonotes.domain import note as n
from geonotes.requests import note_list_request as req
from geonotes.responses import response as res
from geonotes.usecases import note_list as uc

DEFAULT_CREATOR = "default"


@pytest.fixture
def domain_notes() -> list[n.Note]:
    note_1 = n.Note(
        code=uuid.uuid4(),
        creator=DEFAULT_CREATOR,
        url="https://example.com/1",
        lat=1,
        long=1,
    )
    note_2 = n.Note(
        code=uuid.uuid4(),
        creator=DEFAULT_CREATOR,
        url="https://example.com/2",
        lat=2,
        long=2,
    )
    note_3 = n.Note(
        code=uuid.uuid4(),
        creator=DEFAULT_CREATOR,
        url="https://example.com/3",
        lat=1,
        long=1,
    )
    note_4 = n.Note(
        code=uuid.uuid4(),
        creator=DEFAULT_CREATOR,
        url="https://example.com/4",
        lat=4,
        long=4,
    )

    return [note_1, note_2, note_3, note_4]


def test_note_list_without_parameters(domain_notes) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes

    note_list_usecase = uc.NoteListUseCase(repo)
    request = req.NoteListRequest()

    response = note_list_usecase.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None)
    assert response.value == domain_notes


def test_note_list_with_filters(domain_notes) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes

    note_list_usecase = uc.NoteListUseCase(repo)
    qry_filters = {"code__eq": 5}
    request_obj = req.NoteListRequest.from_dict({"filters": qry_filters})

    response_obj = note_list_usecase.execute(request_obj)

    assert bool(response_obj) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response_obj.value == domain_notes


def test_note_list_handles_generic_error() -> None:
    repo = mock.Mock()
    repo.list.side_effect = Exception("An error message")

    note_list_usecase = uc.NoteListUseCase(repo)
    request_obj = req.NoteListRequest.from_dict({})

    response_obj = note_list_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "message": "Exception: An error message",
    }


def test_note_list_handles_bad_request() -> None:
    repo = mock.Mock()

    note_list_usecase = uc.NoteListUseCase(repo)
    request_obj = req.NoteListRequest.from_dict({"filters": 5})

    response_obj = note_list_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "filters: Is not iterable",
    }
