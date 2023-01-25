import uuid
from unittest import mock

from fastapi.testclient import TestClient

from jaanevis.api.fastapi.main import app
from jaanevis.domain.note import Note, NoteCreateApi, NoteUpdateApi
from jaanevis.responses import response as res

LAT, LONG = 30.0, 50.0
COUNTRY = "IR"
client = TestClient(app)
note = NoteCreateApi(
    url="http://example.com",
    text="some text",
    lat=LAT,
    long=LONG,
)

note_complete = Note(
    code=str(uuid.uuid4()),
    creator="default",
    text="some text",
    url="http://example.com",
    lat=LAT,
    long=LONG,
)
note_list = [note_complete]


@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes(mock_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)

    response = client.get("/note")

    mock_usecase().execute.assert_called()
    assert response.status_code == 200
    assert response.json() == [note_complete.to_dict()]


@mock.patch("jaanevis.requests.note_list_request.NoteListRequest")
@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_with_creator_filter(mock_usecase, mock_request) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)
    creator = "default"

    response = client.get(f"/note?creator={creator}")

    mock_request.from_dict.assert_called_with(
        data={
            "filters": {
                "creator__eq": creator,
                "country__eq": None,
                "tag__eq": None,
            }
        }
    )
    mock_usecase().execute.assert_called()
    assert response.status_code == 200
    assert response.json() == [note_complete.to_dict()]


@mock.patch("jaanevis.requests.note_list_request.NoteListRequest")
@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_with_country_filter(mock_usecase, mock_request) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)
    country = "IR"

    response = client.get(f"/note?country={country}")

    mock_request.from_dict.assert_called_with(
        data={
            "filters": {
                "country__eq": country,
                "creator__eq": None,
                "tag__eq": None,
            }
        }
    )
    mock_usecase().execute.assert_called()
    assert response.status_code == 200
    assert response.json() == [note_complete.to_dict()]


@mock.patch("jaanevis.requests.note_list_request.NoteListRequest")
@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_with_tag_filter(mock_usecase, mock_request) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)
    tag = "text"

    response = client.get(f"/note?tag={tag}")

    mock_request.from_dict.assert_called_with(
        data={
            "filters": {
                "tag__eq": tag,
                "country__eq": None,
                "creator__eq": None,
            }
        }
    )
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


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.delete_note.DeleteNoteUseCase")
def test_delete_note(mock_usecase, auth_usecase) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_complete)
    session = uuid.uuid4()

    response = client.delete(
        f"/note/{note_complete.code}", headers={"cookie": f"session={session}"}
    )

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
    session = uuid.uuid4()

    response = client.post(
        "/note", json=new_note, headers={"cookie": f"session={session}"}
    )
    result = response.json()
    result.pop("code", None)

    assert result == {**new_note, "country": "", "tags": None}
    assert response.status_code == 200
    mock_usecase().execute.assert_called()
    auth_usecase().execute.assert_called()


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.update_note.UpdateNoteUseCase")
def test_update_note(mock_usecase, auth_usecase) -> None:
    new_note = note_complete.to_dict()
    note_update = NoteUpdateApi(
        url="https://newurl.com",
        text="some text",
        lat=note_complete.lat,
        long=note_complete.long,
    )
    mock_usecase().execute.return_value = res.ResponseSuccess(note_complete)
    session = uuid.uuid4()

    response = client.put(
        f"/note/{note_complete.code}",
        json=note_update.dict(),
        headers={"cookie": f"session={session}"},
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


@mock.patch("jaanevis.requests.note_list_request.NoteListRequest")
@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_geojson_data_with_creator_filter(
    mock_usecase, mock_request
) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)
    creator = "default"

    response = client.get(f"/note/geojson?creator={creator}")
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
    mock_request.from_dict.assert_called_with(
        data={
            "filters": {
                "creator__eq": creator,
                "country__eq": None,
                "tag__eq": None,
            }
        }
    )


@mock.patch("jaanevis.requests.note_list_request.NoteListRequest")
@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_geojson_data_with_country_filter(
    mock_usecase, mock_request
) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)

    response = client.get(f"/note/geojson?country={COUNTRY}")
    result = response.json()

    assert response.status_code == 200
    assert result[0]["type"] == "Feature"
    assert result[0]["geometry"] == {
        "type": "Point",
        "coordinates": [note.long, note.lat],
    }
    assert result[0]["properties"]["url"] == note.url
    assert result[0]["properties"]["country"] == COUNTRY
    assert len(result[0]["properties"]["code"])
    mock_usecase().execute.assert_called()
    mock_request.from_dict.assert_called_with(
        data={
            "filters": {
                "country__eq": COUNTRY,
                "creator__eq": None,
                "tag__eq": None,
            }
        }
    )


@mock.patch("jaanevis.requests.note_list_request.NoteListRequest")
@mock.patch("jaanevis.usecases.note_list.NoteListUseCase")
def test_read_notes_geojson_data_with_tag_filter(
    mock_usecase, mock_request
) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess(note_list)

    response = client.get("/note/geojson?tag=text")
    result = response.json()

    assert response.status_code == 200
    assert result[0]["type"] == "Feature"
    assert result[0]["geometry"] == {
        "type": "Point",
        "coordinates": [note.long, note.lat],
    }
    assert result[0]["properties"]["url"] == note.url
    assert result[0]["properties"]["country"] == COUNTRY
    assert len(result[0]["properties"]["code"])
    mock_usecase().execute.assert_called()
    mock_request.from_dict.assert_called_with(
        data={
            "filters": {
                "tag__eq": "text",
                "country__eq": None,
                "creator__eq": None,
            }
        }
    )


def test_create_note_respose_unauthorized_with_no_cookie() -> None:
    response = client.post("/note", json=note.dict())

    assert response.status_code == 401


def test_update_note_respose_unauthorized_with_no_cookie() -> None:
    response = client.put("/note/somenotecode", json=note.dict())

    assert response.status_code == 401


def test_delete_note_respose_unauthorized_with_no_cookie() -> None:
    response = client.delete("/note/somenotecode")

    assert response.status_code == 401


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.delete_note.DeleteNoteUseCase")
def test_delete_note_from_wrong_user(mock_usecase, auth_usecase) -> None:
    mock_usecase().execute.return_value = (
        res.ResponseFailure.build_parameters_error("forbidden")
    )
    session = uuid.uuid4()

    response = client.delete(
        f"/note/{note_complete.code}", headers={"cookie": f"session={session}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "forbidden"}


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.update_note.UpdateNoteUseCase")
def test_update_note_from_wrong_user(mock_usecase, auth_usecase) -> None:
    note_update = NoteUpdateApi(
        url="https://newurl.com",
        lat=note_complete.lat,
        long=note_complete.long,
    )
    mock_usecase().execute.return_value = (
        res.ResponseFailure.build_parameters_error("forbidden")
    )
    session = uuid.uuid4()

    response = client.put(
        f"/note/{note_complete.code}",
        json=note_update.dict(),
        headers={"cookie": f"session={session}"},
    )
    result = response.json()

    assert response.status_code == 403
    assert result == {"detail": "forbidden"}
