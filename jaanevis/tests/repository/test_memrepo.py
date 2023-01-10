import json
import uuid
from typing import Any
from unittest import mock

import pytest

from jaanevis.domain import note as n
from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.repository import memrepo
from jaanevis.serializers import note_json_serializer as ser

uuid_session = "554f8c37-b3a1-4846-a1b6-02cc4d158646"


@pytest.fixture
def note_dicts() -> dict[str, list[Any]]:
    return {
        "notes": [
            {
                "code": str(uuid.uuid4()),
                "creator": "default",
                "url": "http://example.com/1",
                "lat": 1,
                "long": 1,
            },
            {
                "code": str(uuid.uuid4()),
                "creator": "default",
                "url": "http://example.com/2",
                "lat": 2,
                "long": 2,
            },
        ],
        "users": [{"username": "test@test.com"}],
        "sessions": [
            {"session_id": uuid_session, "username": "test@test.com"}
        ],
    }


def test_repository_list_without_parameters(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]

    assert repo.list() == notes


def test_repository_list_with_code_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(
        filters={"code__eq": note_dicts["notes"][0]["code"]}
    )

    assert len(repo_notes) == 1
    assert str(repo_notes[0].code) == note_dicts["notes"][0]["code"]


def test_repository_list_with_url_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"url__eq": "http://example.com/1"})

    assert len(repo_notes) == 1
    assert repo_notes[0].url == "http://example.com/1"


def test_repository_list_with_lat_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"lat__eq": 2})

    assert len(repo_notes) == 1
    assert repo_notes[0].lat == 2


def test_repository_list_with_long_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"long__eq": 2})

    assert len(repo_notes) == 1
    assert repo_notes[0].long == 2


def test_repository_adds_new_note() -> None:
    mock_open = mock.mock_open(read_data=json.dumps({"notes": []}))

    with mock.patch(
        "jaanevis.repository.memrepo.open", mock_open, create=True
    ):
        repo = memrepo.MemRepo()
        new_note = n.Note(
            creator="default", url="https://example.com", lat=1, long=1
        )
        repo.add(new_note)

        repo_notes = repo.list()

        assert len(repo_notes) == 1


def test_repository_get_note_by_code(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]

    assert repo.get_by_code(code=str(notes[0].code)) == notes[0]


def test_repository_get_note_by_code_handle_nonexistent_code(
    note_dicts,
) -> None:
    repo = memrepo.MemRepo(note_dicts)

    assert repo.get_by_code(code="nocode") is None


def test_repository_delete_by_code(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)
    repo._write_data_to_file = mock.Mock()

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]

    assert repo.delete_by_code(code=str(notes[0].code)) == notes[0]
    assert not any(n["code"] == notes[0].code for n in repo.data["notes"])


def test_repository_update(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)
    repo._write_data_to_file = mock.Mock()

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    newurl = "https://newurl.com"
    update_data = {
        "url": newurl,
        "lat": notes[0].lat,
        "long": notes[0].long,
    }
    new_note = n.Note(
        code=notes[0].code, creator=notes[0].creator, **update_data
    )

    updated_note = repo.update(obj=notes[0], data=update_data)
    note_in_db = None
    for note in repo.data["notes"]:
        if note["code"] == str(notes[0].code):
            note_in_db = n.Note.from_dict(note)

    assert updated_note == new_note
    assert note_in_db == new_note


@mock.patch("pathlib.Path")
def test_read_notes_from_file_with_no_init_data(path, note_dicts) -> None:
    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    read_data = json.dumps(notes, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch(
        "jaanevis.repository.memrepo.open", mock_open, create=True
    ):
        repo = memrepo.MemRepo()

    mock_open.assert_called_with("db.json", "r")
    assert repo.data == json.loads(read_data)


@mock.patch("pathlib.Path")
def test_write_new_created_note_to_file_db(path, note_dicts) -> None:
    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    data = {"notes": notes, "users": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        new_note = n.Note(
            creator="default", url="https://example.com", lat=1, long=1
        )
        repo.add(new_note)

    mock_open.assert_called_with("db.json", "w")


@mock.patch("pathlib.Path")
def test_remove_deleted_note_from_file_db(path, note_dicts) -> None:
    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    data = {"notes": notes, "users": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.delete_by_code(code=str(notes[0].code))

    mock_open.assert_called_with("db.json", "w")


@mock.patch("pathlib.Path")
def test_write_db_to_file_after_note_update(path, note_dicts) -> None:
    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    data = {"notes": notes, "users": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)
    update_data = {
        "url": "https://newurl.com",
        "lat": notes[0].lat,
        "long": notes[0].long,
    }

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.update(obj=notes[0], data=update_data)

    mock_open.assert_called_with("db.json", "w")


def test_get_user_by_username(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    users = [u.User.from_dict(data) for data in note_dicts["users"]]

    assert repo.get_user_by_username(username=users[0].username) == users[0]


def test_get_session_by_session_id(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    sessions = [s.Session.from_dict(data) for data in note_dicts["sessions"]]

    assert (
        repo.get_session_by_session_id(session_id=str(sessions[0].session_id))
        == sessions[0]
    )
