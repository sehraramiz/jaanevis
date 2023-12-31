from jaanevis.repository.base import Repository
from jaanevis.requests.add_note_request import AddNoteRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess
from jaanevis.utils import event


class AddNoteUseCase:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: AddNoteRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)
        try:
            request.note.creator_id = request.user.email
            request.note.creator = request.user.username
            self.repo.add(request.note)
            event.post_event("note_added", request.note)
            return ResponseSuccess(request.note)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
