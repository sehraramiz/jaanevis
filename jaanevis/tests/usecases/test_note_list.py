import uuid
from datetime import datetime
from unittest import mock

import pytest
from pytz import timezone

from jaanevis.domain import geojson as geo
from jaanevis.domain import note as n
from jaanevis.requests import note_list_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import note_list as uc

DEFAULT_CREATOR = "default"
LAT, LONG = 30.0, 50.0
COUNTRY = "IR"
CREATED = datetime.now(timezone("Asia/Tehran"))

notes = [
    n.Note(
        created=CREATED,
        code=str(uuid.uuid4()),
        creator=DEFAULT_CREATOR,
        url="https://example.com/1",
        text="some text",
        lat=LAT,
        long=LONG,
    ),
    n.Note(
        created=CREATED,
        code=str(uuid.uuid4()),
        creator=DEFAULT_CREATOR,
        url="https://example.com/2",
        text="some text",
        lat=LAT + 1,
        long=LONG + 1,
    ),
    n.Note(
        created=CREATED,
        code=str(uuid.uuid4()),
        creator=DEFAULT_CREATOR,
        url="https://example.com/3",
        text="some text",
        lat=LAT + 2,
        long=LONG + 2,
    ),
    n.Note(
        created=CREATED,
        code=str(uuid.uuid4()),
        creator=DEFAULT_CREATOR,
        url="https://example.com/4",
        text="some text",
        lat=LAT + 3,
        long=LONG + 3,
    ),
]


@pytest.fixture
def domain_notes() -> list[n.Note]:
    return notes


@pytest.fixture
def domain_notes_geojson() -> list[n.NoteGeoJsonFeature]:
    geojson_notes = []
    for note in notes:
        properties = n.NoteGeoJsonProperties(
            url=note.url,
            creator=note.creator,
            code=note.code,
            country=COUNTRY,
            text=note.text,
        )
        geometry = geo.GeoJsonPoint(coordinates=[note.long, note.lat])
        geojson_notes.append(
            n.NoteGeoJsonFeature(geometry=geometry, properties=properties)
        )
    return geojson_notes


def test_note_list_without_parameters(domain_notes) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes

    note_list_usecase = uc.NoteListUseCase(repo)
    request = req.NoteListRequest()

    response = note_list_usecase.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None, limit=None, skip=0)
    assert response.value == domain_notes


def test_note_list_without_parameters_with_limit(domain_notes) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes[:2]

    note_list_usecase = uc.NoteListUseCase(repo)
    request = req.NoteListRequest.from_dict({"limit": 2, "skip": 0})

    response = note_list_usecase.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None, limit=2, skip=0)
    assert response.value == domain_notes[:2]


def test_note_list_without_parameters_with_skip(domain_notes) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes[1:]

    note_list_usecase = uc.NoteListUseCase(repo)
    request = req.NoteListRequest.from_dict({"limit": 100, "skip": 1})

    response = note_list_usecase.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None, limit=100, skip=1)
    assert response.value == domain_notes[1:]


def test_note_list_with_filters(domain_notes) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes

    note_list_usecase = uc.NoteListUseCase(repo)
    qry_filters = {"code__eq": 5}
    request_obj = req.NoteListRequest.from_dict({"filters": qry_filters})

    response_obj = note_list_usecase.execute(request_obj)

    assert bool(response_obj) is True
    repo.list.assert_called_with(filters=qry_filters, limit=None, skip=0)
    assert response_obj.value == domain_notes


def test_note_list_handles_generic_error() -> None:
    repo = mock.Mock()
    repo.list.side_effect = Exception("An error message")

    note_list_usecase = uc.NoteListUseCase(repo)
    request_obj = req.NoteListRequest.from_dict({})

    response_obj = note_list_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }


def test_note_list_handles_bad_request() -> None:
    repo = mock.Mock()

    note_list_usecase = uc.NoteListUseCase(repo)
    request_obj = req.NoteListRequest.from_dict({"filters": 5})

    response_obj = note_list_usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "filters: Invalid filters type",
    }


def test_geojson_note_list(domain_notes, domain_notes_geojson) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes

    geojson_note_list_usecase = uc.GeoJsonNoteListUseCase(repo)
    request = req.NoteListRequest()

    response = geojson_note_list_usecase.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None, limit=None, skip=0)
    assert response.value == domain_notes_geojson


def test_geojson_note_list_with_limit_skip(
    domain_notes, domain_notes_geojson
) -> None:
    repo = mock.Mock()
    repo.list.return_value = domain_notes[1:3]

    geojson_note_list_usecase = uc.GeoJsonNoteListUseCase(repo)
    request = req.NoteListRequest.from_dict({"limit": 2, "skip": 1})

    response = geojson_note_list_usecase.execute(request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None, limit=2, skip=1)
    assert response.value == domain_notes_geojson[1:3]
