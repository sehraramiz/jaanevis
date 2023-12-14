from jaanevis.repository.base import Repository
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.responses.response import (
    ResponseFailure,
    ResponseObject,
    ResponseSuccess,
)
from jaanevis.serializers import note_geojson_serializer as geo_serializer


class NoteListUseCase:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: NoteListRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)
        try:
            notes = self.repo.list(
                filters=request.filters, limit=request.limit, skip=request.skip
            )
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
        request_obj = NoteListRequest(
            filters=request.filters, limit=request.limit, skip=request.skip
        )
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
