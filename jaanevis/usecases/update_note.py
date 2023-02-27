from jaanevis.repository.base import Repository
from jaanevis.requests.update_note_request import UpdateNoteRequest
from jaanevis.responses import ResponseFailure, ResponseObject, ResponseSuccess


class UpdateNoteUseCase:
    """update a note"""

    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def execute(self, request: UpdateNoteRequest) -> ResponseObject:
        if not request:
            return ResponseFailure.build_from_invalid_request_object(request)

        try:
            note = self.repo.get_by_code(code=request.code)
            if not note:
                return ResponseFailure.build_resource_error(
                    f"note with code '{request.code}' not found"
                )
            if note.creator_id != request.user.email:
                return ResponseFailure.build_parameters_error(
                    _("permission denied")
                )

            data = request.note.dict(exclude_unset=True)
            data["url"] = str(data["url"])
            updated_note = self.repo.update(obj=note, data=data)
            return ResponseSuccess(updated_note)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )
