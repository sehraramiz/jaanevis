import pytest

from jaanevis.requests import note_list_request as req


def test_build_note_list_request_without_parameters() -> None:
    request = req.NoteListRequest()

    assert request.filters is None
    assert bool(request) is True


def test_build_note_list_request_from_empty_dict() -> None:
    request = req.NoteListRequest.from_dict({})

    assert request.filters is None
    assert bool(request) is True


def test_build_note_list_request_with_empty_filters() -> None:
    request = req.NoteListRequest(filters={})

    assert request.filters == {}
    assert bool(request) is True


def test_build_note_list_request_from_dict_with_empty_filters() -> None:
    request = req.NoteListRequest.from_dict({"filters": {}})

    assert request.filters == {}
    assert bool(request) is True


def test_build_note_list_request_from_dict_with_wrong_filters() -> None:
    request = req.NoteListRequest.from_dict({"filters": {"a": 1}})

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


def test_build_note_list_request_from_dict_with_invalid_filters() -> None:
    request = req.NoteListRequest.from_dict({"filters": 5})

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


@pytest.mark.parametrize(
    "key", ["code__eq", "url__eq", "lat__eq", "long__eq", "creator__eq"]
)
def test_build_note_list_request_accepted_filters(key: str) -> None:
    filters = {key: 1}

    request = req.NoteListRequest.from_dict({"filters": filters})

    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ["code__lte", "code__gte"])
def test_build_note_list_request_rejected_filters(key) -> None:
    filters = {key: 1}

    request = req.NoteListRequest.from_dict({"filters": filters})

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False
