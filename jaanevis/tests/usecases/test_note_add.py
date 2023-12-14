from datetime import datetime
from unittest import mock

import pytest

from jaanevis.domain import note as n
from jaanevis.domain import user as u
from jaanevis.requests import add_note_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import add_note as uc

CREATED = datetime.strptime("2023-01-01 00:00:01", "%Y-%m-%d %H:%M:%S")


@pytest.fixture
def new_note() -> n.Note:
    return n.Note(
        created=CREATED,
        url="http://example.com",
        text="some text",
        lat=1,
        long=1,
    )


def test_add_note(new_note: n.Note) -> None:
    repo = mock.Mock()
    user = u.User(email="a@a.com", username="username", password="password")

    add_note_usecase = uc.AddNoteUseCase(repo)
    add_note_request = req.AddNoteRequest(note=new_note, user=user)

    response = add_note_usecase.execute(add_note_request)
    expected_note = n.Note(
        created=CREATED,
        code=new_note.code,
        url=new_note.url,
        lat=new_note.lat,
        long=new_note.long,
        creator_id="a@a.com",
        creator="username",
        text="some text",
    )

    assert bool(response) is True
    repo.add.assert_called_with(expected_note)
    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.value == expected_note


@mock.patch("jaanevis.utils.event.post_event")
def test_add_note_send_note_add_event(event_mock, new_note: n.Note) -> None:
    repo = mock.Mock()
    user = u.User(email="a@a.com", username="username", password="password")
    expected_note = n.Note(
        created=CREATED,
        code=new_note.code,
        url=new_note.url,
        lat=new_note.lat,
        long=new_note.long,
        creator_id="a@a.com",
        creator="username",
        text="some text",
    )

    add_note_usecase = uc.AddNoteUseCase(repo)
    add_note_request = req.AddNoteRequest(note=new_note, user=user)

    response = add_note_usecase.execute(add_note_request)

    assert bool(response) is True
    event_mock.assert_called_with("note_added", expected_note)


def test_add_note_handles_non_existant_user(new_note: n.Note) -> None:
    repo = mock.Mock()
    user = None

    add_note_usecase = uc.AddNoteUseCase(repo)
    add_note_request = req.AddNoteRequest.build(note=new_note, user=user)

    response = add_note_usecase.execute(add_note_request)

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR


def test_add_note_handles_generic_error(new_note: n.Note) -> None:
    repo = mock.Mock()
    repo.add.side_effect = Exception("An error message")
    user = u.User(email="a@a.com", username="username", password="password")

    add_note_usecase = uc.AddNoteUseCase(repo)
    request_obj = req.AddNoteRequest(note=new_note, user=user)

    response_obj = add_note_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }


def test_add_note_handles_bad_request() -> None:
    repo = mock.Mock()

    add_note_usecase = uc.AddNoteUseCase(repo)
    request_obj = req.AddNoteRequest.build(note=None, user=None)

    response_obj = add_note_usecase.execute(request_obj)

    assert bool(request_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "body: Invalid note type",
    }
