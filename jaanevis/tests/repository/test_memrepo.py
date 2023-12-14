import json
import uuid
from datetime import datetime, timedelta
from typing import Any
from unittest import mock

import pytest
from pytz import timezone

from jaanevis.config import settings
from jaanevis.domain import note as n
from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.repository import memrepo
from jaanevis.serializers import note_json_serializer as ser

uuid_session = "554f8c37-b3a1-4846-a1b6-02cc4d158646"
LAT, LONG = 30.0, 50.0
COUNTRY = "IR"
DB_PATH = settings.DATA_BASE_DIR / "data/db.json"
CREATED = datetime.now(timezone("Asia/Tehran"))


@pytest.fixture
def note_dicts() -> dict[str, list[Any]]:
    return {
        "notes": [
            {
                "created": str(CREATED),
                "code": str(uuid.uuid4()),
                "creator": "default",
                "url": "http://example.com/1",
                "text": "some #text",
                "tags": ["text"],
                "lat": LAT,
                "long": LONG,
            },
            {
                "created": str(CREATED + timedelta(days=1)),
                "code": str(uuid.uuid4()),
                "creator": "default2",
                "url": "http://example.com/2",
                "text": "#some text",
                "tags": ["some"],
                "lat": LAT + 1,
                "long": LONG + 1,
            },
        ],
        "users": [
            {
                "email": "test@test.com",
                "username": "username",
                "password": "password",
                "is_active": False,
            }
        ],
        "sessions": [
            {
                "session_id": uuid_session,
                "email": "test@test.com",
                "username": "username",
                "expire_time": (
                    datetime.now() + timedelta(days=1)
                ).timestamp(),
            }
        ],
    }


def test_repository_list_without_parameters(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    sorted_notes = sorted(notes, key=lambda n: n.created)[::-1]

    assert repo.list() == sorted_notes


def test_repository_list_with_limit_skip(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    sorted_notes = sorted(notes, key=lambda n: n.created)[::-1]
    result = repo.list(limit=1, skip=1)

    assert result == sorted_notes[1:2]


def test_repository_list_default_sort_by_created(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    sorted_notes = sorted(notes, key=lambda n: n.created)[::-1]

    result = repo.list()

    assert result == sorted_notes


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

    repo_notes = repo.list(filters={"lat__eq": LAT})

    assert len(repo_notes) == 1
    assert repo_notes[0].lat == LAT


def test_repository_list_with_long_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"long__eq": LONG})

    assert len(repo_notes) == 1
    assert repo_notes[0].long == LONG


def test_repository_list_with_creator_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"creator__eq": "default"})

    assert len(repo_notes) == 1
    assert repo_notes[0].creator == "default"


def test_repository_list_with_country_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"country__eq": COUNTRY})

    assert len(repo_notes) == 2
    assert repo_notes[0].country == COUNTRY


def test_repository_list_with_tag_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"tag__eq": "text"})

    assert len(repo_notes) == 1
    assert "text" in repo_notes[0].tags


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
        "text": notes[0].text,
        "lat": notes[0].lat,
        "long": notes[0].long,
    }
    new_note = n.Note(
        created=CREATED,
        code=notes[0].code,
        creator=notes[0].creator,
        **update_data
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

    mock_open.assert_called_with(DB_PATH, "r")
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

    mock_open.assert_called_with(DB_PATH, "w")


@mock.patch("pathlib.Path")
def test_remove_deleted_note_from_file_db(path, note_dicts) -> None:
    notes = [n.Note.from_dict(data) for data in note_dicts["notes"]]
    data = {"notes": notes, "users": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.delete_by_code(code=str(notes[0].code))

    mock_open.assert_called_with(DB_PATH, "w")


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

    mock_open.assert_called_with(DB_PATH, "w")


def test_get_user_by_username(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    users = [u.User.from_dict(data) for data in note_dicts["users"]]

    assert repo.get_user_by_email(email=users[0].email) == users[0]


def test_get_user_by_email(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    users = [u.User.from_dict(data) for data in note_dicts["users"]]

    assert repo.get_user_by_email(email=users[0].email) == users[0]


def test_create_user(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)
    repo._write_data_to_file = mock.Mock()
    with mock.patch("jaanevis.repository.memrepo.open"):
        username, email, password = "username", "a@a.com", "22334455"
        user = u.User(
            email=email, username=username, password=password, is_active=False
        )

        assert (
            repo.create_user(email=email, username=username, password=password)
            == user
        )
        assert len(repo.data["users"]) == 2
        assert any(u == user.to_dict() for u in repo.data["users"])


def test_get_session_by_session_id(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    sessions = [s.Session.from_dict(data) for data in note_dicts["sessions"]]

    assert (
        repo.get_session_by_session_id(session_id=str(sessions[0].session_id))
        == sessions[0]
    )


def test_get_session_by_session_id_and_email(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    sessions = [s.Session.from_dict(data) for data in note_dicts["sessions"]]

    assert (
        repo.get_session_by_session_id_and_email(
            session_id=str(sessions[0].session_id),
            email=sessions[0].email,
        )
        == sessions[0]
    )


def test_get_session_by_session_id_and_username(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    sessions = [s.Session.from_dict(data) for data in note_dicts["sessions"]]

    assert (
        repo.get_session_by_session_id_and_username(
            session_id=str(sessions[0].session_id),
            username=sessions[0].username,
        )
        == sessions[0]
    )


@mock.patch("jaanevis.repository.memrepo.open")
def test_delete_session_by_session_id(mock_open, note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    sessions = [s.Session.from_dict(data) for data in note_dicts["sessions"]]
    session_id = str(sessions[0].session_id)

    repo.delete_session_by_session_id(session_id=session_id)

    assert not any(
        s["session_id"] == session_id for s in repo.data["sessions"]
    )


@mock.patch("jaanevis.repository.memrepo.open")
def test_create_or_update_creates_new_session(mock_open, note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)
    new_session_id = str(uuid.uuid4())
    expire_time = 0.0
    new_session = s.Session(
        email="b@b.com",
        username="user1",
        session_id=new_session_id,
        expire_time=expire_time,
    )

    assert (
        repo.create_or_update_session(
            email="b@b.com",
            username="user1",
            session_id=str(new_session_id),
            expire_time=expire_time,
        )
        == new_session
    )


@mock.patch("jaanevis.repository.memrepo.open")
def test_create_new_session(mock_open, note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)
    new_session_id = str(uuid.uuid4())
    expire_time = 0.0
    new_session = s.Session(
        email="b@b.com",
        username="user1",
        session_id=new_session_id,
        expire_time=expire_time,
    )

    assert (
        repo.create_session(
            email="b@b.com",
            username="user1",
            session_id=str(new_session_id),
            expire_time=expire_time,
        )
        == new_session
    )


@mock.patch("jaanevis.repository.memrepo.open")
def test_create_or_update_updates_existing_session(
    mock_open, note_dicts
) -> None:
    repo = memrepo.MemRepo(note_dicts)

    sessions = [s.Session.from_dict(data) for data in note_dicts["sessions"]]

    assert (
        repo.create_or_update_session(
            email=sessions[0].email,
            username=sessions[0].username,
            session_id=str(sessions[0].session_id),
            expire_time=sessions[0].expire_time,
        )
        == sessions[0]
    )


@mock.patch("pathlib.Path")
def test_write_db_to_file_after_session_create(path, note_dicts) -> None:
    session_id = str(uuid.uuid4())
    data = {"notes": [], "users": [], "sessions": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.create_or_update_session(
            email="a@a.com",
            username="user1",
            session_id=session_id,
            expire_time=0,
        )
        repo.create_session(
            email="a@a.com",
            username="user1",
            session_id=session_id,
            expire_time=0,
        )

    mock_open.assert_called_with(DB_PATH, "w")
    assert mock_open.call_count == 3


@mock.patch("pathlib.Path")
def test_write_db_to_file_after_session_update(path, note_dicts) -> None:
    session_id = str(uuid.uuid4())
    data = {"notes": [], "users": [], "sessions": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.create_or_update_session(
            email="a@a.com",
            username="user1",
            session_id=session_id,
            expire_time=0,
        )

    mock_open.assert_called_with(DB_PATH, "w")


@mock.patch("pathlib.Path")
def test_write_db_to_file_after_session_delete(path, note_dicts) -> None:
    session_id = str(uuid.uuid4())
    data = {"notes": [], "users": [], "sessions": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.delete_session_by_session_id(session_id=session_id)

    mock_open.assert_called_with(DB_PATH, "w")


@mock.patch("pathlib.Path")
def test_write_db_to_file_after_user_create(path, note_dicts) -> None:
    data = {"notes": [], "users": [], "sessions": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.create_user(
            email="a@a.com", username="username", password="22334455"
        )

    mock_open.assert_called_with(DB_PATH, "w")


@mock.patch("jaanevis.repository.memrepo.open")
def test_update_user_change_active_status(mock_open, note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)
    users = [u.User.from_dict(data) for data in note_dicts["users"]]
    updated_user = u.User(
        email=users[0].email,
        username=users[0].username,
        password=users[0].password,
        is_active=True,
    )

    result = repo.update_user(obj=users[0], data={"is_active": True})

    assert repo.data["users"][0]["is_active"] is True
    assert result == updated_user


@mock.patch("jaanevis.repository.memrepo.open")
def test_delete_user(mock_open, note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    users = [u.User.from_dict(data) for data in note_dicts["users"]]
    username = str(users[0].username)

    repo.delete_user(username=username)

    assert not any(u["username"] == username for u in repo.data["users"])


@mock.patch("pathlib.Path")
def test_write_db_to_file_after_user_delete(path, note_dicts) -> None:
    username = "a@a.com"
    data = {"notes": [], "users": [], "sessions": []}
    read_data = json.dumps(data, cls=ser.NoteJsonEncoder)
    mock_open = mock.mock_open(read_data=read_data)

    with mock.patch("jaanevis.repository.memrepo.open", mock_open):
        repo = memrepo.MemRepo()
        repo.delete_user(username=username)

    mock_open.assert_called_with(DB_PATH, "w")
