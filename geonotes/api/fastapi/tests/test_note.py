from unittest import mock

from fastapi.testclient import TestClient

from geonotes.api.fastapi.main import app
from geonotes.domain.note import Note
from geonotes.responses import response as res

client = TestClient(app)
note = Note(
    creator="default",
    url="http://example.com",
    lat=1,
    long=1,
)
note_list = [note]


@mock.patch("geonotes.usecases.note_list.NoteListUseCase")
def test_read_notes(mock_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)

    response = client.get("/note")

    mock_usecase().execute.assert_called()
    assert response.status_code == 200
    assert response.json() == [note.to_dict()]


@mock.patch("geonotes.usecases.add_note.AddNoteUseCase")
def test_create_note(mock_usecase) -> None:
    new_note = note.to_dict()
    new_note.pop("code", None)
    mock_usecase().execute.return_value = res.ResponseSuccess(new_note)

    response = client.post("/note", json=new_note)
    result = response.json()
    result.pop("code", None)

    assert result == new_note
    assert response.status_code == 200
    mock_usecase().execute.assert_called()
