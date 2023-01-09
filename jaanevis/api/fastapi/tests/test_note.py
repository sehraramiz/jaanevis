import uuid
from base64 import b64encode
from unittest import mock

from fastapi.testclient import TestClient

from jaanevis.api.fastapi.main import app
from jaanevis.domain.note import Note, NoteCreateApi, NoteUpdateApi
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


@mock.patch("jaanevis.usecases.delete_note.DeleteNoteUseCase")
def test_delete_note(mock_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_complete)

    response = client.delete(f"/note/{note_complete.code}")

    assert response.status_code == 200
    assert response.json() == note_complete.to_dict()
    mock_usecase().execute.assert_called()


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.add_note.AddNoteUseCase")
def test_create_note(mock_usecase, auth_usecase) -> None:
    new_note = note.dict()
    new_note["creator"] = "username"
    new_note.pop("code", None)
    mock_usecase().execute.return_value = res.ResponseSuccess(new_note)
    token = b64encode("username:password".encode("utf-8")).decode("ascii")

    response = client.post(
        "/note", json=new_note, headers={"Authorization": f"Basic {token}"}
    )
    result = response.json()
    result.pop("code", None)

    assert result == new_note
    assert response.status_code == 200
    mock_usecase().execute.assert_called()
    auth_usecase().execute.assert_called()


@mock.patch("jaanevis.usecases.update_note.UpdateNoteUseCase")
def test_update_note(mock_usecase) -> None:
    new_note = note_complete.to_dict()
    note_update = NoteUpdateApi(
        url="https://newurl.com",
        lat=note_complete.lat,
        long=note_complete.long,
    )
    mock_usecase().execute.return_value = res.ResponseSuccess(note_complete)

    response = client.put(
        f"/note/{note_complete.code}", json=note_update.dict()
    )
    result = response.json()

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


def test_create_note_respose_unauthorized_with_no_header() -> None:
    response = client.post("/note", json={})

    assert response.status_code == 401
