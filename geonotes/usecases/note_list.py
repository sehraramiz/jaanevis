from typing import Protocol

from geonotes.requests.note_list_request import NoteListRequest
from geonotes.responses.response import ResponseFailure, ResponseObject, ResponseSuccess


class Repository(Protocol):
    def list(self) -> list:
        pass


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
