from unittest import mock

import pytest

from jaanevis.domain import note as n
from jaanevis.requests import update_note_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import update_note as uc

DEFAULT_CREATOR = "default"


@pytest.fixture
def note() -> n.Note:
    return n.Note(creator="default", url="http://example.com", lat=1, long=1)


def test_update_note(note: n.Note) -> None:
    repo = mock.Mock()
    repo.get_by_code.return_value = note

    newurl = "https://newurl.com"
    note_update = n.NoteUpdateApi(url=newurl)
    updated_note = note
    updated_note.url = newurl
    repo.update.return_value = updated_note

    update_note_usecase = uc.UpdateNoteUseCase(repo)
    update_note_request = req.UpdateNoteRequest(
        code=str(note.code), note=note_update
    )

    response = update_note_usecase.execute(update_note_request)

    assert bool(response) is True
    repo.update.assert_called_with(obj=note, data={"url": newurl})
    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.value == updated_note
