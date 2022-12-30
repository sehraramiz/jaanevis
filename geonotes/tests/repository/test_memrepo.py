import uuid

import pytest

from geonotes.domain import note as n
from geonotes.repository import memrepo


@pytest.fixture
def note_dicts() -> list[dict]:
    return [
        {
            "code": uuid.uuid4(),
            "creator": "default",
            "url": "http://example.com/1",
            "lat": 1,
            "long": 1,
        },
        {
            "code": uuid.uuid4(),
            "creator": "default",
            "url": "http://example.com/2",
            "lat": 2,
            "long": 2,
        },
    ]


def test_repository_list_without_parameters(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    notes = [n.Note.from_dict(data) for data in note_dicts]

    assert repo.list() == notes


def test_repository_list_with_code_equal_filter(note_dicts) -> None:
    repo = memrepo.MemRepo(note_dicts)

    repo_notes = repo.list(filters={"code__eq": note_dicts[0]["code"]})

    assert len(repo_notes) == 1
    assert repo_notes[0].code == note_dicts[0]["code"]


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
