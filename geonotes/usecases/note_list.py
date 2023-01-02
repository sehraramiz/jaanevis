from typing import Optional, Protocol

from geonotes.domain import note as n
from geonotes.requests.note_list_request import NoteListRequest
from geonotes.responses.response import ResponseFailure, ResponseObject, ResponseSuccess
from geonotes.serializers import note_geojson_serializer as geo_serializer


class Repository(Protocol):
    def list(self, filters: Optional[dict] = None) -> list[n.Note]:
        ...


class NoteListUseCase:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: NoteListRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)
        try:
            notes = self.repo.list(filters=request.filters)
            return ResponseSuccess(notes)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )


class GeoJsonNoteListUseCase:
    """list notes with geojson feature format"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: NoteListRequest) -> ResponseObject:
        note_list_usecase = NoteListUseCase(self.repo)
        request_obj = NoteListRequest(filters=request.filters)
        response = note_list_usecase.execute(request_obj)

        if not response:
            return response

        try:
            geojson_notes = geo_serializer.notes_to_geojson_features(
                response.value
            )
            return ResponseSuccess(geojson_notes)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
