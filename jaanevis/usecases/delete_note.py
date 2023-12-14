from jaanevis.repository.base import Repository
from jaanevis.requests.delete_note_request import DeleteNoteRequest
from jaanevis.responses.response import (
    ResponseFailure,
    ResponseObject,
    ResponseSuccess,
)


class DeleteNoteUseCase:
    """Use case to delete a note by it's code"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: DeleteNoteRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)
        try:
            note = self.repo.get_by_code(code=request.code)
            if not note:
                return ResponseFailure.build_resource_error(
                    f"note with code '{request.code}' not found"
                )
            if note.creator != request.user.username:
                return ResponseFailure.build_parameters_error(
                    _("permission denied")
                )
            self.repo.delete_by_code(code=request.code)
            return ResponseSuccess(note)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
