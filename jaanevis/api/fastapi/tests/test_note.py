import uuid
from unittest import mock

from fastapi.testclient import TestClient

from jaanevis.api.fastapi.main import app
from jaanevis.domain.note import Note, NoteCreateApi
from jaanevis.responses import response as res

client = TestClient(app)
note = NoteCreateApi(
    url="http://example.com",
    lat=1,
    long=2,
)

note_complete = Note(
    code=uuid.uuid4(),
    creator="default",
    url="http://example.com",
    lat=1,
    long=2,
)
note_list = [note_complete]


@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes(mock_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)

    response = client.get("/note")

    mock_usecase().execute.assert_called()
    assert response.status_code == 200
    assert response.json() == [note_complete.to_dict()]


@mock.patch("jaanevis.usecases.read_note.ReadNoteUseCase")
def test_read_note_by_code(mock_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_complete)

    response = client.get(f"/note/{note_complete.code}")

    assert response.status_code == 200
    assert response.json() == note_complete.to_dict()
    mock_usecase().execute.assert_called()


@mock.patch("jaanevis.usecases.add_note.AddNoteUseCase")
def test_create_note(mock_usecase) -> None:
    new_note = note.dict()
    new_note["creator"] = "default"
    new_note.pop("code", None)
    mock_usecase().execute.return_value = res.ResponseSuccess(new_note)

    response = client.post("/note", json=new_note)
    result = response.json()
    result.pop("code", None)

    assert result == new_note
    assert response.status_code == 200
    mock_usecase().execute.assert_called()


@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_geojson_data(mock_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)

    response = client.get("/note/geojson")
    result = response.json()

    assert response.status_code == 200
    assert result[0]["type"] == "Feature"
    assert result[0]["geometry"] == {
        "type": "Point",
        "coordinates": [note.long, note.lat],
    }
    assert result[0]["properties"]["url"] == note.url
    assert result[0]["properties"]["creator"] == "default"
    assert len(result[0]["properties"]["code"])
    mock_usecase().execute.assert_called()