from unittest import mock

import pytest

from jaanevis.domain import note as n
from jaanevis.domain import user as u
from jaanevis.requests import update_note_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import update_note as uc


@pytest.fixture
def note() -> n.Note:
    return n.Note(creator="username", url="http://example.com", lat=1, long=1)


def test_update_note(note: n.Note) -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = note
    user = u.User(username="username", password="password")

    newurl = "https://newurl.com"
    note_update = n.NoteUpdateApi(url=newurl)
    updated_note = note
    updated_note.url = newurl
    repo.update.return_value = updated_note

    update_note_usecase = uc.UpdateNoteUseCase(repo)
    update_note_request = req.UpdateNoteRequest.build(
        code=str(note.code), note=note_update, user=user
    )

    response = update_note_usecase.execute(update_note_request)

    assert bool(response) is True
    repo.update.assert_called_with(obj=note, data={"url": newurl})
    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.value == updated_note


def test_note_update_handles_invalid_code(note: n.Note) -> None:
    repo = mock.Mock()
    user = u.User(username="username", password="password")
    newurl = "https://newurl.com"
    note_update = n.NoteUpdateApi(url=newurl)

    update_note_usecase = uc.UpdateNoteUseCase(repo)
    update_note_request = req.UpdateNoteRequest.build(
        code="", note=note_update, user=user
    )

    response = update_note_usecase.execute(update_note_request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "code: Invalid code",
    }


def test_note_update_handles_invalid_note(note: n.Note) -> None:
    repo = mock.Mock()
    user = u.User(username="username", password="password")

    update_note_usecase = uc.UpdateNoteUseCase(repo)
    update_note_request = req.UpdateNoteRequest.build(
        code="code", note=None, user=user
    )

    response = update_note_usecase.execute(update_note_request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "body: Invalid note type",
    }


def test_note_update_handles_nonexistent_note(note: n.Note) -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = None
    user = u.User(username="username", password="password")
    newurl = "https://newurl.com"
    note_update = n.NoteUpdateApi(url=newurl)

    update_note_usecase = uc.UpdateNoteUseCase(repo)
    update_note_request = req.UpdateNoteRequest.build(
        code="nocode", note=note_update, user=user
    )

    response = update_note_usecase.execute(update_note_request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "message": "note with code 'nocode' not found",
    }


def test_note_update_handles_wrong_user(note: n.Note) -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = note
    wrong_user = u.User(username="wrong_user", password="password")

    newurl = "https://newurl.com"
    note_update = n.NoteUpdateApi(url=newurl)
    updated_note = note
    updated_note.url = newurl
    repo.update.return_value = updated_note

    update_note_usecase = uc.UpdateNoteUseCase(repo)
    update_note_request = req.UpdateNoteRequest.build(
        code=str(note.code), note=note_update, user=wrong_user
    )

    response = update_note_usecase.execute(update_note_request)

    assert bool(response) is False
    repo.update.assert_not_called()
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "permission denied",
    }
