from jaanevis.repository.base import Repository
from jaanevis.requests.read_note_request import ReadNoteRequest
from jaanevis.responses.response import (
    ResponseFailure,
    ResponseObject,
    ResponseSuccess,
)


class ReadNoteUseCase:
    """Use case to get a note by it's code"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: ReadNoteRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)
        try:
            note = self.repo.get_by_code(code=request.code)
            if not note:
                return ResponseFailure.build_resource_error(
                    f"note with code '{request.code}' not found"
                )
            return ResponseSuccess(note)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
