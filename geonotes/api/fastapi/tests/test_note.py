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
    t = res.ResponseSuccess(note_list)

    response = client.get("/note")

    mock_usecase().execute.assert_called()
    assert response.status_code == 200
    assert response.json() == [note.to_dict()]
